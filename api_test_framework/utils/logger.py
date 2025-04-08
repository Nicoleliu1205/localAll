import logging
import os
import yaml
from logging.handlers import RotatingFileHandler
from typing import Optional

class Logger:
    _instance: Optional['Logger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # 加载配置文件
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 获取日志配置
        log_config = self.config['logging']
        
        # 创建日志目录
        log_dir = os.path.dirname(log_config['file'])
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置日志记录器
        self.logger = logging.getLogger('api_test')
        self.logger.setLevel(getattr(logging, log_config['level']))
        
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            log_config['file'],
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_config['level']))
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_config['level']))
        
        # 设置日志格式
        formatter = logging.Formatter(log_config['format'])
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def critical(self, message: str):
        self.logger.critical(message) 