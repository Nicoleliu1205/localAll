from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def input_username(self, username):
        """输入用户名"""
        try:
            username_input = WebDriverWait(self.driver, 20).until(
                lambda d: d.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.EditText").instance(0)'
                )
            )
            username_input.click()
            username_input.clear()
            username_input.send_keys(username)
        except TimeoutException:
            self.driver.save_screenshot("debug_login_page.png")
            raise AssertionError("未找到用户名输入框，请检查页面结构和xpath")

    def input_password(self, password):
        """输入密码"""
        try:
            password_input = WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.EditText").instance(1)'
                )
            )
            password_input.click()
            password_input.clear()
            password_input.send_keys(password)
        except TimeoutException:
            self.driver.save_screenshot("debug_input_password.png")
            raise AssertionError("未找到密码输入框，请检查定位表达式和页面结构")

    def click_login(self):
        """点击登录按钮"""
        # 等待按钮可用（enabled）
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="登录"]').is_enabled()
        )
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="登录"]').click()

    def login(self, username, password):
        """执行登录操作"""
        self.input_username(username)
        self.input_password(password)
        self.click_login()

    def get_error_message(self):
        """获取登录弹窗的错误信息"""
        try:
            error_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "用户名或密码错误，请重新输入")) )
            return error_element.is_displayed()
        except TimeoutException:
            self.driver.save_screenshot("debug_get_error_message.png")
            return False

    def is_home_button_present(self):
        """判断首页按钮是否出现"""
        try:
            home_btn = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "首页\n第 1 个标签，共 2 个")) )
            return home_btn.is_displayed()
        except TimeoutException:
            self.driver.save_screenshot("debug_home_button.png")
            return False
