import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options as AndroidOptions
from utils.config_reader import Config
import logging
import allure
from datetime import datetime
import os
import sys
from pathlib import Path

# 获取项目根目录路径
root_dir = Path(__file__).resolve().parent.parent  # 根据文件位置调整层级
sys.path.append(str(root_dir))

class BaseTest:
    driver = None
    config = None
    logger = None

    @classmethod
    def setup_class(cls):
        """在测试类开始前执行，设置Appium配置"""
        cls.config = Config()
        cls.logger = logging.getLogger(__name__)
        cls.driver = None

    def setup_method(self, method):
        """在每个测试方法开始前执行，启动Appium会话"""
        caps = self.config.get_android_capabilities()
        print(f"Capabilities配置: {caps}")
        print(f"Appium服务器URL: {self.config.get_appium_server_url()}")
        
        # 使用新的初始化方式
        options = AndroidOptions().load_capabilities(caps)
        
        self.driver = webdriver.Remote(
            command_executor=self.config.get_appium_server_url(),
            options=options
        )
        print("WebDriver初始化成功")
        self.driver.implicitly_wait(self.config.get_implicit_wait())
        self.logger.info(f"Starting test: {method.__name__}")

    def teardown_method(self, method):
        """在每个测试方法结束后执行，关闭Appium会话"""
        if self.driver:
            try:
                # 失败截图由conftest.py统一处理
                pass
            finally:
                self.driver.quit()
                self.logger.info(f"Finished test: {method.__name__}")

    @classmethod
    def teardown_class(cls):
        """测试类结束后清理"""
        if cls.driver:
            cls.driver.quit()
            cls.driver = None

    def _take_screenshot(self, test_name):
        """测试失败时截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_{timestamp}.png"
        screenshot_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "reports",
            "screenshots"
        )
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)
        
        try:
            self.driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
