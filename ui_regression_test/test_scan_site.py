import os
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base_test import BaseTest
from utils.link_scanner import LinkScanner
from utils.image_diff import compare_images
from utils.logger import get_logger

BASE_URL = "https://newpay.la"
SCREENSHOT_BASE = "screenshots/baseline"
SCREENSHOT_CURRENT = "screenshots/current"

# 获取日志记录器
logger = get_logger(__name__)

@pytest.fixture(scope="session")
def driver():
    test = BaseTest(headless=True)
    yield test
    test.quit()

@pytest.fixture(scope="session")
def all_links(driver):
    """
    使用 LinkScanner 扫描 BASE_URL 下的所有链接，包括 iframe 和动态加载的链接。
    """
    logger.info(f"Scanning all links under {BASE_URL}")
    scanner = LinkScanner(BASE_URL, driver.driver, max_depth=10)  # 根据需要调整 max_depth
    scanner.scan()
    logger.info(f"Found {len(scanner.links)} links: {scanner.links}")
    return list(scanner.links)

def pytest_generate_tests(metafunc):
    """
    动态生成测试用例参数，避免重复扫描链接。
    """
    if "url" in metafunc.fixturenames:
        # 从 all_links fixture 获取链接
        links = metafunc.config.cache.get("all_links", None)
        if not links:
            scanner = LinkScanner(BASE_URL, max_depth=10)
            links = scanner.scan()
            metafunc.config.cache.set("all_links", links)
        metafunc.parametrize("url", links)

def generate_screenshot_path(url, base_dir):
    """
    根据 URL 生成截图路径。
    """
    filename = url.replace("://", "_").replace("/", "_").replace("?", "_") + ".png"
    return os.path.join(base_dir, filename)

def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver.driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def test_pages_ui_regression(driver, url):
    """
    动态生成测试用例，测试页面的 UI 回归。
    """
    logger.info(f"Testing URL: {url}")
    driver.open(url)

    # 等待页面加载完成
    try:
        WebDriverWait(driver.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except TimeoutException:
        logger.error(f"Page load timeout for {url}")
        pytest.fail(f"Page load timeout for {url}")

    baseline_path = os.path.join(SCREENSHOT_BASE, url.replace("://", "_").replace("/", "_") + ".png")
    current_path = os.path.join(SCREENSHOT_CURRENT, url.replace("://", "_").replace("/", "_") + ".png")

    driver.driver.save_screenshot(current_path)

    if not os.path.exists(baseline_path):
        logger.warning(f"Baseline screenshot not found for {url}. Creating new baseline.")
        os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
        driver.driver.save_screenshot(baseline_path)
        pytest.skip(f"No baseline screenshot for {url}, baseline created. Please review and rerun.")

    changed, detail = compare_images(baseline_path, current_path)
    if changed:
        logger.error(f"Visual regression detected on {url}: {detail}")
    assert not changed, f"Visual regression detected on {url}: {detail}"

def test_pages_js_errors(driver, url):
    driver.open(url)
    wait_for_page_load(driver, timeout=30)

    errors = driver.get_console_errors()
    ignored_errors = ["Failed to fetch", "Deprecated API usage"]
    critical_errors = [
        error for error in errors if not any(ignored in error["message"] for ignored in ignored_errors)
    ]

    if critical_errors:
        logger.error(f"Critical JS errors found on {url}: {critical_errors}")
    else:
        logger.info(f"No critical JS errors found on {url}")

def test_pages_http_status(driver, url):
    driver.open(url)
    wait_for_page_load(driver)

    status_code = driver.get_status_code()
    logger.info(f"Testing URL: {url}, Status Code: {status_code}")

    assert status_code is not None, f"Failed to retrieve status code for {url}"
    assert 200 <= status_code < 300, f"Non-success status code {status_code} for {url}"