# 接口自动化测试框架

这是一个基于 Python 的接口自动化测试框架，使用 pytest 作为测试框架，requests 作为 HTTP 客户端。

## 项目结构

```
api_test_framework/
├── config/                 # 配置文件目录
│   ├── config.yaml        # 配置文件
│   └── .env              # 环境变量文件
├── data/                  # 测试数据目录
│   └── test_data.yaml    # 测试数据文件
├── testcases/            # 测试用例目录
│   └── api/             # API 测试用例
├── utils/                # 工具类目录
│   ├── http_client.py   # HTTP 客户端
│   └── logger.py        # 日志工具
└── conftest.py          # pytest 配置文件
```

## 环境要求

- Python 3.8+
- pip

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试用例
pytest testcases/api/test_example.py

# 生成 HTML 报告
pytest --html=report.html
```

## 配置说明

1. 在 `config/config.yaml` 中配置测试环境信息
2. 在 `config/.env` 中配置敏感信息（如 API keys）
3. 在 `data/test_data.yaml` 中添加测试数据

## 编写测试用例

参考 `testcases/api/test_example.py` 编写新的测试用例。 