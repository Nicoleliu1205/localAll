import logging
import yaml
import os
from typing import Dict

class Config:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._load_config()
        return cls._instance

    @classmethod
    def _load_config(cls):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            cls._config = yaml.safe_load(f)

    @classmethod
    def get_android_capabilities(cls) -> Dict:
        return cls._config['android']['capabilities']

    @classmethod
    def get_appium_server_url(cls) -> str:
        server = cls._config['appium']['server']
        return f"http://{server['host']}:{server['port']}"

    @classmethod
    def get_implicit_wait(cls) -> int:
        return cls._config['framework']['implicit_wait']

    @classmethod
    def get_explicit_wait(cls) -> int:
        return cls._config['framework']['explicit_wait']
