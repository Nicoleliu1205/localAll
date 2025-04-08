import pytest
import yaml
import os
from typing import Dict, Any
from utils.http_client import HttpClient
from utils.logger import Logger

# 初始化日志记录器
logger = Logger()

# 加载测试数据
def load_test_data() -> Dict[str, Any]:
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'test_data.yaml')
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 测试数据
test_data = load_test_data()

class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试用例前置操作"""
        self.client = HttpClient()
        self.logger = logger
        self.test_data = test_data
        yield
        # 测试用例后置操作（如果需要）

    def test_create_user(self):
        """测试创建用户"""
        test_case = self.test_data['api_test_data']['create_user']
        self.logger.info("开始测试创建用户")
        
        response = self.client.post(
            test_case['endpoint'],
            json=test_case['request_body']
        )
        
        assert response.status_code == test_case['expected_status']
        assert response.json()['message'] == test_case['expected_response']['message']
        self.logger.info("创建用户测试通过")

    def test_get_user(self):
        """测试获取用户信息"""
        test_case = self.test_data['api_test_data']['get_user']
        self.logger.info("开始测试获取用户信息")
        
        # 假设我们已经有一个测试用户ID
        user_id = "test_user_id"
        endpoint = test_case['endpoint'].format(user_id=user_id)
        
        response = self.client.get(endpoint)
        
        assert response.status_code == test_case['expected_status']
        response_data = response.json()
        assert response_data['username'] == test_case['expected_response']['username']
        assert response_data['email'] == test_case['expected_response']['email']
        self.logger.info("获取用户信息测试通过")

    def test_update_user(self):
        """测试更新用户信息"""
        test_case = self.test_data['api_test_data']['update_user']
        self.logger.info("开始测试更新用户信息")
        
        # 假设我们已经有一个测试用户ID
        user_id = "test_user_id"
        endpoint = test_case['endpoint'].format(user_id=user_id)
        
        response = self.client.put(
            endpoint,
            json=test_case['request_body']
        )
        
        assert response.status_code == test_case['expected_status']
        assert response.json()['message'] == test_case['expected_response']['message']
        self.logger.info("更新用户信息测试通过")

    def test_delete_user(self):
        """测试删除用户"""
        test_case = self.test_data['api_test_data']['delete_user']
        self.logger.info("开始测试删除用户")
        
        # 假设我们已经有一个测试用户ID
        user_id = "test_user_id"
        endpoint = test_case['endpoint'].format(user_id=user_id)
        
        response = self.client.delete(endpoint)
        
        assert response.status_code == test_case['expected_status']
        self.logger.info("删除用户测试通过") 