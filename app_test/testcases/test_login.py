import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from testcases.base_test import BaseTest
from pageobjects.login_page import LoginPage
from typing import Dict
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

@allure.feature("登录功能")
class TestLogin(BaseTest):

    @allure.story("异常登录")    
    @allure.title("使用无效凭据登录")
    def test_invalid_login(self):
        """测试使用无效的用户名和密码登录"""
        login_page = LoginPage(self.driver)
        
        with allure.step("输入无效的用户名和密码"):
            login_page.login("invalid_user", "invalid_password")
        
        with allure.step("验证错误信息显示"):
            assert login_page.get_error_message(), "错误提示内容不符合预期"
            print("登录失败:出现用户名或密码错误提示语")
    
    @allure.story("正常登录")
    @allure.title("使用有效凭据登录")
    @pytest.mark.smoke
    def test_valid_login(self):
        """测试使用有效的用户名和密码登录"""
        login_page = LoginPage(self.driver)
        
        with allure.step("输入有效的用户名和密码"):
            login_page.login("2072583546", "np123456")
        
        with allure.step("验证登录成功"):
            assert login_page.is_home_button_present(), "首页按钮未显示"
            print("登录成功：找到了 首页 元素")
                
