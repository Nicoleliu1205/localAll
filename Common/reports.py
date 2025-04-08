import unittest
from HTMLTestRunner import HTMLTestRunner

class TestRunner:
    def generate_report(self, test_suite, report_path):
        with open(report_path, 'wb') as f:
            runner = HTMLTestRunner(
                stream=f,
                title='商户端反扫功能测试报告',
                description='接口自动化测试结果'
            )
            runner.run(test_suite)

# 使用示例
suite = unittest.TestLoader().loadTestsFromTestCase(PaymentAPITest)
report = TestRunner()
report.generate_report(suite, "report.html")