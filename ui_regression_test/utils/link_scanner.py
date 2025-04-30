import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LinkScanner:
    def __init__(self, base_url, driver, max_depth=2, delay=1):
        self.base_url = base_url
        self.driver = driver
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.links = set()

    def is_internal(self, url):
        base_domain = urlparse(self.base_url).netloc
        target_domain = urlparse(url).netloc
        return base_domain == target_domain or target_domain == ''

    def scan(self, url=None, depth=0):
        if depth > self.max_depth:
            return

        if not url:
            url = self.base_url

        if url in self.visited:
            return

        logger.info(f"Scanning URL: {url}")
        self.visited.add(url)

        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            logger.warning(f"Timeout while loading {url}")
            return

        self._extract_links()
        self._scan_iframes()

        for link in self.links.copy():
            if link not in self.visited:
                self.scan(link, depth + 1)

    def _extract_links(self):
        elements = self.driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            href = element.get_attribute("href")
            if href and href.startswith("http"):
                full_url = urljoin(self.base_url, href)
                if full_url not in self.links:
                    logger.info(f"Found link: {full_url}")
                    self.links.add(full_url)

    def _scan_iframes(self):
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                logger.info("Switched to iframe")
                self._extract_links()
                self.driver.switch_to.default_content()
            except Exception as e:
                logger.warning(f"Failed to scan iframe: {e}")
                self.driver.switch_to.default_content()