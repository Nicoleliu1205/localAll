import pytest
import os
import yaml
from typing import Dict, Any

def pytest_configure(config):
    """配置 pytest"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试"
    )
    config.addinivalue_line(
        "markers", "api: API 测试"
    )

@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """加载测试配置"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def test_data() -> Dict[str, Any]:
    """加载测试数据"""
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'test_data.yaml')
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def pytest_html_report_title(report):
    """自定义 HTML 报告标题"""
    report.title = "API 自动化测试报告"

def pytest_html_results_table_header(cells):
    """自定义 HTML 报告表头"""
    cells.insert(2, "测试描述")
    cells.pop()

def pytest_html_results_table_row(report, cells):
    """自定义 HTML 报告表格行"""
    cells.insert(2, report.description)
    cells.pop() 