import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class LinkScanner:
    def __init__(self, base_url, driver, max_depth=5, delay=1):
        self.base_url = base_url
        self.driver = driver
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()  # 已访问的链接
        self.links = set()    # 收集到的所有链接

    def is_internal(self, url):
        """
        判断链接是否为站点内部链接
        """
        base_domain = urlparse(self.base_url).netloc
        target_domain = urlparse(url).netloc
        return base_domain == target_domain or target_domain == ''

    def _normalize_url(self, url):
        """
        标准化 URL，忽略查询参数和片段标识符。
        """
        parsed = urlparse(url)
        return urlunparse(parsed._replace(query="", fragment=""))

    def scan(self, url=None, depth=0):
        """
        扫描页面，提取链接并递归扫描子页面
        """
        if depth > self.max_depth:
            return

        if not url:
            url = self.base_url

        normalized_url = self._normalize_url(url)
        if normalized_url in self.visited:
            return

        logger.info(f"Scanning URL: {url}")
        self.visited.add(normalized_url)

        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self._scroll_page()  # 模拟滚动页面
            self._extract_links()  # 提取链接
            self._scan_iframes()  # 扫描 iframe
            self._click_interactive_elements()  # 点击交互元素
        except TimeoutException:
            logger.warning(f"Timeout while loading {url}")
            return

        for link in self.links.copy():
            if link not in self.visited:
                self.scan(link, depth + 1)

    def _extract_links(self):
        """
        提取当前页面中的所有链接（静态和动态）
        """
        # 优先使用 requests 提取静态链接
        try:
            response = requests.get(self.driver.current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(self.base_url, href)
                normalized_url = self._normalize_url(full_url)
                if normalized_url not in self.links:
                    logger.info(f"Found link: {full_url}")
                    self.links.add(normalized_url)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch links using requests: {e}")

        # 使用 Selenium 提取动态生成的链接
        elements = self.driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            href = element.get_attribute("href")
            if href and href.startswith("http"):
                full_url = urljoin(self.base_url, href)
                normalized_url = self._normalize_url(full_url)
                if normalized_url not in self.links:
                    logger.info(f"Found link: {full_url}")
                    self.links.add(normalized_url)

    def _scan_iframes(self):
        """
        扫描页面中的 iframe，并提取其中的链接
        """
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                logger.info("Switched to iframe")
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                self._extract_links()
                self.driver.switch_to.default_content()
            except Exception as e:
                logger.warning(f"Failed to scan iframe: {e}")
                self.driver.switch_to.default_content()

    def _click_interactive_elements(self):
        """
        尝试点击页面上的交互元素，触发新页面加载或动态内容
        """
        try:
            # 查找所有交互元素（按钮或带有 role="button" 的链接）
            buttons = self.driver.find_elements(By.XPATH, "//button | //a[@role='button']")
            for btn in buttons:
                try:
                    # 等待按钮可点击
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(btn))
                    
                    # 记录当前页面 URL
                    current_url = self.driver.current_url
                    
                    # 点击按钮
                    btn.click()
                    time.sleep(2)  # 等待页面加载或动态内容加载
                    
                    # 检查是否跳转到新页面
                    new_url = self.driver.current_url
                    if new_url != current_url and new_url not in self.visited:
                        logger.info(f"New URL detected after click: {new_url}")
                        self.links.add(new_url)
                    
                    # 如果未跳转，提取动态加载的内容
                    self._extract_links()
                except Exception as e:
                    logger.warning(f"Failed to click element: {e}")
        except Exception as e:
            logger.warning(f"Error during interactive element scanning: {e}")

    def _scroll_page(self):
        """
        模拟滚动页面，触发动态加载的内容
        """
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # 等待动态内容加载
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            logger.warning(f"Error during scrolling: {e}")