import pytest
import logging
import os
from datetime import datetime

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """配置日志"""
    log_dir = os.path.join(os.path.dirname(__file__), "reports", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def pytest_configure(config):
    """添加自定义标记"""
    config.addinivalue_line("markers", "smoke: 冒烟测试用例")
    config.addinivalue_line("markers", "regression: 回归测试用例")

@pytest.fixture(scope="function")
def screenshot_on_failure(request):
    """测试失败时自动截图的fixture"""
    yield
    
    # 如果测试失败，自动截图
    if request.node.rep_call.failed:
        driver = request.node.instance.driver
        screenshot_dir = os.path.join(
            os.path.dirname(__file__),
            "reports",
            "screenshots"
        )
        os.makedirs(screenshot_dir, exist_ok=True)
        
        screenshot_name = f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)
        driver.get_screenshot_as_file(screenshot_path)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用于在测试失败时获取错误信息的钩子"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
