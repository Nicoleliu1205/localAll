from selenium import webdriver
import os
import pytest

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

@pytest.fixture(scope="session")
def driver():
    test = BaseTest(headless=False)  # 使用有头模式
    yield test
    test.quit()