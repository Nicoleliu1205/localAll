import logging
import time
import os
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests

class WebRegressionTest:
    def __init__(self, base_url: str, output_dir: str = "test_results"):
        """初始化网页回归测试框架
        
        Args:
            base_url: 要测试的网站主页URL
            output_dir: 测试结果输出目录
        """
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls: Set[str] = set()
        self.error_pages: List[Dict] = []
        self.output_dir = output_dir
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 设置日志
        self._setup_logging()
        
        # 初始化WebDriver
        self.driver = self._setup_webdriver()
        
    def _setup_logging(self):
        """配置日志系统"""
        log_file = os.path.join(self.output_dir, f"regression_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _setup_webdriver(self) -> webdriver.Chrome:
        """配置Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # 启用浏览器日志
        chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def _is_valid_url(self, url: str) -> bool:
        """检查URL是否有效且属于同一域名"""
        if not url:
            return False
        
        parsed_url = urlparse(url)
        return (
            parsed_url.netloc == self.domain and
            not url.startswith(('javascript:', 'mailto:', 'tel:')) and
            not url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar'))
        )
    
    def _get_page_links(self, url: str) -> Set[str]:
        """获取页面中的所有链接"""
        links = set()
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                if self._is_valid_url(absolute_url):
                    links.add(absolute_url)
        except Exception as e:
            self.logger.error(f"获取页面链接时出错 {url}: {str(e)}")
        return links
    
    def _check_page_errors(self, url: str) -> Optional[Dict]:
        """检查页面是否存在错误"""
        try:
            # 等待页面加载完成
            time.sleep(2)  # 给予页面充足的加载时间
            
            # 检查控制台错误
            try:
                console_logs = self.driver.get_log('browser')
                js_errors = [
                    log for log in console_logs 
                    if log['level'] in ['SEVERE', 'ERROR'] and 
                    not any(ignored in log['message'] for ignored in [
                        '404', # 忽略资源404错误
                        'favicon.ico',
                        'net::ERR_FAILED',
                        'net::ERR_CONNECTION_REFUSED'
                    ])
                ]
            except Exception as e:
                self.logger.warning(f"获取控制台日志失败: {str(e)}")
                js_errors = []
            
            # 检查页面可见错误信息
            error_elements = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'error') or contains(text(), 'Error') or contains(text(), '错误') or contains(text(), '异常') or contains(text(), '失败')]")
            visible_errors = [elem.text for elem in error_elements if elem.is_displayed()]
            
            # 检查HTTP状态码
            try:
                navigation_entries = self.driver.execute_script("""
                    return window.performance.getEntries().filter(function(e) {
                        return e.entryType === 'resource';
                    }).map(function(e) {
                        return {
                            url: e.name,
                            type: e.entryType,
                            duration: e.duration
                        };
                    });
                """)
                
                # 使用requests检查当前页面的状态码
                response = requests.head(url, allow_redirects=True, timeout=10)
                status_code = response.status_code
                
            except Exception as e:
                self.logger.warning(f"获取性能数据失败: {str(e)}")
                navigation_entries = []
                status_code = None
            
            if js_errors or visible_errors or (status_code and status_code >= 400):
                error_info = {
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                    'js_errors': js_errors,
                    'visible_errors': visible_errors,
                    'status_code': status_code,
                    'performance_data': navigation_entries
                }
                
                # 如果配置了截图，保存错误页面截图
                try:
                    screenshot_path = os.path.join(
                        self.output_dir, 
                        f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    self.driver.save_screenshot(screenshot_path)
                    error_info['screenshot'] = screenshot_path
                except Exception as e:
                    self.logger.warning(f"保存截图失败: {str(e)}")
                
                return error_info
                
        except Exception as e:
            self.logger.error(f"检查页面错误时出错 {url}: {str(e)}")
        return None
    
    def _save_results(self):
        """保存测试结果"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存错误报告为JSON
        json_file = os.path.join(self.output_dir, f'error_report_{timestamp}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.error_pages, f, ensure_ascii=False, indent=2)
        
        # 创建Excel报告
        if self.error_pages:
            df = pd.DataFrame(self.error_pages)
            excel_file = os.path.join(self.output_dir, f'error_report_{timestamp}.xlsx')
            df.to_excel(excel_file, index=False)
        
        self.logger.info(f"测试结果已保存到 {self.output_dir}")
    
    def crawl_and_test(self, max_pages: int = None):
        """开始爬取和测试网页
        
        Args:
            max_pages: 最大测试页面数，None表示无限制
        """
        try:
            pages_tested = 0
            urls_to_visit = {self.base_url}
            
            while urls_to_visit and (max_pages is None or pages_tested < max_pages):
                current_url = urls_to_visit.pop()
                if current_url in self.visited_urls:
                    continue
                
                self.logger.info(f"测试页面: {current_url}")
                
                try:
                    self.driver.get(current_url)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # 检查页面错误
                    error_info = self._check_page_errors(current_url)
                    if error_info:
                        self.error_pages.append(error_info)
                        self.logger.warning(f"在页面 {current_url} 发现错误")
                    
                    # 获取新链接
                    new_links = self._get_page_links(current_url)
                    urls_to_visit.update(new_links - self.visited_urls)
                    
                    self.visited_urls.add(current_url)
                    pages_tested += 1
                    
                except TimeoutException:
                    self.logger.error(f"页面加载超时: {current_url}")
                    self.error_pages.append({
                        'url': current_url,
                        'timestamp': datetime.now().isoformat(),
                        'error': 'Page load timeout'
                    })
                except Exception as e:
                    self.logger.error(f"处理页面时出错 {current_url}: {str(e)}")
                    self.error_pages.append({
                        'url': current_url,
                        'timestamp': datetime.now().isoformat(),
                        'error': str(e)
                    })
                
                time.sleep(1)  # 避免请求过于频繁
                
        except Exception as e:
            self.logger.error(f"测试过程中出现错误: {str(e)}")
        finally:
            self._save_results()
            self.driver.quit()
            
        self.logger.info(f"测试完成! 共测试 {len(self.visited_urls)} 个页面，发现 {len(self.error_pages)} 个问题页面。")

if __name__ == "__main__":
    # 使用示例
    test = WebRegressionTest("https://newpay.la/en")
    test.crawl_and_test(max_pages=100) 