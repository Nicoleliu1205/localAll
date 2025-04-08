import requests
import yaml
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

class HttpClient:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 加载配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 获取当前环境
        self.env = os.getenv('ENVIRONMENT', 'dev')
        self.base_url = self.config['environments'][self.env]['base_url']
        self.timeout = self.config['environments'][self.env]['timeout']
        
        # 设置默认请求头
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 设置认证信息
        api_key = os.getenv('API_KEY')
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """发送HTTP请求
        
        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE)
            endpoint: API端点
            **kwargs: 其他请求参数
            
        Returns:
            requests.Response: 响应对象
        """
        url = f"{self.base_url}{endpoint}"
        
        # 设置默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
            
        # 设置默认请求头
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
            
        response = requests.request(method, url, **kwargs)
        return response

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self._request('GET', endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """发送POST请求"""
        return self._request('POST', endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """发送PUT请求"""
        return self._request('PUT', endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        return self._request('DELETE', endpoint, **kwargs) 