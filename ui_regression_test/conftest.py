import os
import pytest
from datetime import datetime

def pytest_configure(config):
    """
    动态生成日志文件名，并配置 pytest 的日志路径。
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 生成带时间标记的日志文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"test_results_{timestamp}.log")

    # 设置日志文件路径
    config.option.log_file = log_file