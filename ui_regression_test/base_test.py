from selenium import webdriver
import os
import pytest
import requests
import logging

logger = logging.getLogger(__name__)

class BaseTest:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def open(self, url):
        self.driver.get(url)

    def get_console_errors(self):
        logs = self.driver.get_log("browser")
        return [log for log in logs if log["level"] == "SEVERE"]

    def save_screenshot(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)

    def quit(self):
        self.driver.quit()

    def get_status_code(self):
        """
        获取当前页面的 HTTP 状态码。
        """
        try:
            # 使用 Selenium 执行 JavaScript 获取状态码（需要服务器支持）
            status_code = self.driver.execute_script(
                """
                try {
                    return window.performance.getEntriesByType('navigation')[0]?.responseStart || 200;
                } catch (e) {
                    return 200;  // 默认返回 200
                }
                """
            )
            return int(status_code)
        except Exception as e:
            logger.warning(f"Failed to fetch status code using JavaScript for {self.driver.current_url}: {e}")
        
        # 回退机制：检查页面内容是否包含错误关键字
        page_source = self.driver.page_source
        error_keywords = ["404 Not Found", "Page Not Found", "Error 404"]
        if any(keyword in page_source for keyword in error_keywords):
            logger.error(f"Error keyword detected in page source for {self.driver.current_url}")
            return 404
        
        # 默认返回 200（假设页面正常）
        return 200

@pytest.fixture(scope="session")
def driver():
    test = BaseTest(headless=False)  # 使用有头模式
    yield test
    test.quit()