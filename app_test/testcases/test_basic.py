import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options as AndroidOptions
from appium.webdriver.common.appiumby import AppiumBy
from base_test import BaseTest
from utils.config_reader import Config

class TestBasicAndroid(BaseTest):
    """基础Android测试类"""
    
    def setup_method(self, method):
        """每个测试方法开始前执行"""
        caps = Config.get_android_capabilities()
        options = AndroidOptions().load_capabilities(caps)
        
        self.driver = webdriver.Remote(
            command_executor=Config.get_appium_server_url(),
            options=options
        )
    
    def test_android_settings(self):
        """测试Android设置应用的基本功能"""
        try:
            # 等待页面加载
            self.driver.implicitly_wait(10)
            
            # 验证页面标题存在
            title = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView")
            assert title.is_displayed(), "页面标题未显示"
            
            print(f"页面标题: {title.text}")
            
        except Exception as e:
            pytest.fail(f"测试失败: {str(e)}")
            raise
