import pytest
from base_test import BaseTest
import os
from utils.image_diff import compare_images

BASE_URL = "https://newpay.la"  # 测试示例网址

@pytest.fixture(scope="module")
def driver():
    test = BaseTest(headless=True)
    yield test
    test.quit()

def test_homepage_ui(driver):
    url = BASE_URL
    driver.open(url)

    screenshot_path = "screenshots/current/homepage.png"
    baseline_path = "screenshots/baseline/homepage.png"

    driver.save_screenshot(screenshot_path)

    if not os.path.exists(baseline_path):
        pytest.skip("No baseline screenshot to compare.")

    changed, detail = compare_images(baseline_path, screenshot_path)
    assert not changed, f"Homepage UI regression detected: {detail}"

def test_login_page_js_errors(driver):
    url = BASE_URL + "/login"
    driver.open(url)
    errors = driver.get_console_errors()
    assert len(errors) == 0, f"JS error(s) found on login page: {errors}"