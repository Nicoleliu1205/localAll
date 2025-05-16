from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urljoin, urlparse, urlunparse
import time
import json
from bs4 import BeautifulSoup
import re

results = []
skipped_pages = {}  # 使用字典记录跳过的页面及其原因
successful_pages = set()
error_pages = []

def get_links_from_html(html_content):
    """
    使用 BeautifulSoup 从 HTML 内容中提取所有 <a> 标签链接
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return [a.get('href') for a in soup.find_all('a', href=True)]

def get_links_from_selenium(driver):
    """
    使用 Selenium 获取所有可点击元素的链接
    """
    links = set()

    # 1. 获取所有可点击元素
    clickable_selectors = [
        "span[onclick]",  # 带onclick的span
        "span[data-href]",  # 带data-href的span
        "div[onclick]",    # 带onclick的div
        "button[onclick]", # 带onclick的button
        "*[role='link']",  # 具有link角色的元素
        "*[class*='link']",# class包含link的元素
        "*[class*='btn']", # class包含btn的元素
        "a"               # 所有a标签
    ]

    for selector in clickable_selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for element in elements:
            # 检查各种可能包含链接的属性
            for attr in ['href', 'onclick', 'data-href']:
                value = element.get_attribute(attr)
                if value:
                    if attr == 'onclick':
                        # 从onclick中提取URL
                        urls = re.findall(r"window\.location\.href=[\'\"](.+?)[\'\"]", value)
                        urls.extend(re.findall(r"location\.href=[\'\"](.+?)[\'\"]", value))
                        for url_found in urls:
                            if url_found:
                                links.add(url_found)
                    else:
                        links.add(value)

    # 2. 获取动态生成的链接
    js_links = driver.execute_script("""
        var links = [];
        var elements = document.querySelectorAll('*');
        for(var i=0; i<elements.length; i++) {
            var el = elements[i];
            if(el.onclick || el.dataset.href || el.getAttribute('role') === 'link') {
                links.push(el.href || el.dataset.href);
            }
        }
        return links;
    """)
    links.update([link for link in js_links if link])

    return links

def handle_special_elements(driver, url):
    """
    处理特殊页面元素，记录新窗口和跳转页面
    """
    try:
        links = set()
        # 记录当前窗口句柄
        main_window = driver.current_window_handle
        
        # 定义特殊元素
        special_elements = [
            {
                'selector': 'span.label[data-v-e6714991]',
                'xpath': "//span[contains(@class, 'label') and contains(text(), 'API Document')]",
                'name': 'API Document'
            },
            {
                'selector': 'button.btn.btn1',
                'xpath': "//button[contains(@class, 'btn btn1')]",
                'name': 'Online merchant'
            },
            {
                'selector': 'button.btn.btn2',
                'xpath': "//button[contains(@class, 'btn btn2')]",
                'name': 'Traditional merchant'
            }
        ]
        
        for element_info in special_elements:
            try:
                # 获取点击前的窗口句柄
                old_handles = set(driver.window_handles)
                
                # 查找并点击元素
                elements = driver.find_elements(By.CSS_SELECTOR, element_info['selector'])
                if not elements:
                    elements = driver.find_elements(By.XPATH, element_info['xpath'])
                
                if elements:
                    print(f"\n尝试点击 {element_info['name']} 按钮...")
                    current_url = driver.current_url
                    
                    # 点击元素
                    try:
                        driver.execute_script("arguments[0].click();", elements[0])
                        time.sleep(2)  # 等待新窗口或页面加载
                        
                        # 检查新窗口
                        new_handles = set(driver.window_handles)
                        new_windows = new_handles - old_handles
                        
                        if new_windows:
                            # 处理新窗口
                            for new_window in new_windows:
                                try:
                                    driver.switch_to.window(new_window)
                                    new_url = driver.current_url
                                    print(f"发现新窗口页面: {new_url}")
                                    links.add(new_url)
                                    successful_pages.add(new_url)
                                    
                                    # 关闭新窗口
                                    driver.close()
                                except Exception as e:
                                    print(f"处理新窗口时出错: {e}")
                            
                            # 切回主窗口
                            driver.switch_to.window(main_window)
                        else:
                            # 检查页面跳转
                            new_url = driver.current_url
                            if new_url != current_url:
                                print(f"页面跳转到: {new_url}")
                                links.add(new_url)
                                successful_pages.add(new_url)
                                
                                # 返回上一页
                                driver.back()
                                time.sleep(1)
                    
                    except Exception as e:
                        print(f"点击元素时出错: {e}")
                
            except Exception as e:
                print(f"处理 {element_info['name']} 时出错: {e}")
                continue
        
        return links
    
    except Exception as e:
        print(f"处理特殊元素时发生错误: {e}")
        return set()

def try_click_methods(driver, element):
    """
    尝试多种点击方法，确保元素能被正确点击
    """
    methods = [
        # 方法1: 直接点击
        lambda: element.click(),
        # 方法2: JavaScript 点击
        lambda: driver.execute_script("arguments[0].click();", element),
        # 方法3: ActionChains 点击
        lambda: ActionChains(driver).move_to_element(element).click().perform(),
        # 方法4: JavaScript 触发事件
        lambda: driver.execute_script("""
            var evt = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(evt);
        """, element)
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            method()
            print(f"点击方法 {i} 成功")
            return True
        except Exception as e:
            print(f"点击方法 {i} 失败: {e}")
            continue
    
    return False

def get_all_links(driver, url):
    """
    获取页面所有链接，包括特殊元素点击后的新页面
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)

        links = set()
        
        # 处理特殊元素
        special_links = handle_special_elements(driver, url)
        links.update(special_links)
        
        # 获取常规链接
        elements = driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            href = element.get_attribute("href")
            if href:
                full_url = urljoin(url, href)
                links.add(full_url)
        
        return list(links), len(driver.page_source)
    except Exception as e:
        print(f"获取链接时出错: {e}")
        return [], 0

def normalize_url(url):
    """
    标准化 URL，保留必要的查询参数
    """
    if not url:
        return ""
    parsed = urlparse(url)
    # 只移除特定的查询参数（如时间戳、随机数等）
    query_params = {}
    if parsed.query:
        for param in parsed.query.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # 保留重要的查询参数
                if key not in ['t', 'timestamp', 'random', '_']:
                    query_params[key] = value
    
    new_query = '&'.join(f"{k}={v}" for k, v in query_params.items())
    return urlunparse(parsed._replace(query=new_query, fragment=""))

def is_excluded(target_url, excluded_domains):
    """
    判断链接是否属于需要排除的域名
    """
    target_domain = urlparse(target_url).netloc
    return any(excluded_domain in target_domain for excluded_domain in excluded_domains)

def scan(driver, url, visited, excluded_domains, depth=0, max_depth=20):
    """
    递归扫描页面，提取链接并检查跳转页面
    """
    if depth > max_depth:
        skipped_pages[url] = "Reached maximum depth"
        print(f"Skipping URL: {url} - Reason: Reached maximum depth ({max_depth})")
        return

    normalized_url = normalize_url(url)
    if normalized_url in visited:
        skipped_pages[url] = "Already visited"
        print(f"Skipping URL: {url} - Reason: Already visited")
        return

    if is_excluded(url, excluded_domains):
        skipped_pages[url] = "Excluded domain"
        print(f"Skipping URL: {url} - Reason: Excluded domain")
        return

    print(f"Scanning URL: {url} (Depth: {depth})")
    visited.add(normalized_url)

    # 获取所有链接
    links, page_size = get_all_links(driver, url)
    print(f"Found {len(links)} links, Page Size: {page_size} bytes")

    try:
        successful_pages.add(url)
        # 递归扫描子页面
        for link in links:
            if not link:  # 跳过空链接
                continue
                
            normalized_link = normalize_url(link)
            if normalized_link not in visited:
                if not is_excluded(link, excluded_domains):
                    scan(driver, link, visited, excluded_domains, depth + 1, max_depth)
                else:
                    skipped_pages[link] = "Excluded domain"
                    print(f"Skipping URL: {link} - Reason: Excluded domain")

    except Exception as e:
        error_pages.append({"url": url, "error": str(e)})
        print(f"Error scanning {url}: {e}")

if __name__ == "__main__":
    # 输入目标网站 URL
    target_url = "https://newpay.la"
    max_depth = 20  # 设置最大递归深度

    # 设置需要排除的域名
    excluded_domains = [
        "apple.com", "instagram.com", "digicert.com", "facebook.com", 
        "meta.com", "google.com", "telegram.org", "github.com",
        "ladt.co", "microsoft.com","x.com","twitter.com"
    ]

    print("正在递归扫描所有链接...")
    
    # 初始化 Selenium WebDriver
    driver = webdriver.Chrome()
    visited_links = set()

    try:
        scan(driver, target_url, visited_links, excluded_domains, max_depth=max_depth)
    finally:
        driver.quit()

    # 定期清理不再需要的数据
    if len(visited_links) > 1000:
        print("Warning: Large number of visited links, consider increasing excluded_domains")

    # 输出统计结果
    print("\n扫描完成！统计结果如下：")
    print(f"成功访问的页面数量：{len(successful_pages)}")
    
    if successful_pages:
        print("\n成功访问的页面列表：")
        for page in successful_pages:
            print(f"- {page}")

    print(f"\n跳过的页面数量：{len(skipped_pages)}")
    if skipped_pages:
        print("\n跳过的页面列表：")
        for page, reason in skipped_pages.items():
            print(f"- {page} - Reason: {reason}")

    print(f"\n访问报错的页面数量：{len(error_pages)}")
    if error_pages:
        print("\n访问报错的页面列表：")
        for error in error_pages:
            print(f"- URL: {error['url']} - Error: {error['error']}")

    # 保存结果到文件
    with open("./scan_results.json", "w", encoding='utf-8') as f:
        json.dump({
            "successful_pages": list(successful_pages),
            "skipped_pages": skipped_pages,
            "error_pages": error_pages
        }, f, indent=2, ensure_ascii=False)