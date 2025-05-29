from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config_reader import Config
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(
            self.driver, 
            self.config.get_explicit_wait()
        )

    def find_element(self, locator):
        """查找单个元素"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise

    def find_elements(self, locator):
        """查找多个元素"""
        try:
            elements = self.wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found with locator: {locator}")
            raise

    def click(self, locator):
        """点击元素"""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """获取元素文本"""
        element = self.find_element(locator)
        return element.text

    def is_element_visible(self, locator, timeout=None):
        """判断元素是否可见"""
        try:
            wait = WebDriverWait(
                self.driver, 
                timeout or self.config.get_explicit_wait()
            )
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """滑动操作"""
        action = self.driver.touch_action()
        action.press(x=start_x, y=start_y)\
              .wait(duration or 200)\
              .move_to(x=end_x, y=end_y)\
              .release()\
              .perform()

    def scroll_to_text(self, text):
        """滚动到指定文本"""
        self.driver.find_element_by_android_uiautomator(
            f'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            f'.scrollIntoView(new UiSelector().text("{text}").instance(0))'
        )
