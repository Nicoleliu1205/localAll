import logging
import os
import sys
from datetime import datetime

def setup_logger():
    """
    配置全局日志
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 可切换为INFO减少日志

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

setup_logger()

def get_logger(name, log_file="test_results.log"):
    # 确保日志目录存在
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 动态生成日志文件路径
    log_path = os.path.join(log_dir, log_file)

    # 配置日志
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 确保日志级别为 INFO 或更低

    # 文件日志处理器
    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)  # 确保文件处理器的日志级别为 INFO 或更低
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 确保控制台处理器的日志级别为 INFO 或更低
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 避免重复添加处理器
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger