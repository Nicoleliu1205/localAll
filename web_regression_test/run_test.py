from web_crawler import WebRegressionTest
import argparse
import yaml

def load_config(config_file: str = 'config.yaml'):
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='网页回归测试工具')
    parser.add_argument('url', help='要测试的网站URL')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    parser.add_argument('--max-pages', type=int, help='最大测试页面数')
    parser.add_argument('--output-dir', help='测试结果输出目录')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 更新配置
    if args.max_pages is not None:
        config['crawler']['max_pages'] = args.max_pages
    if args.output_dir:
        config['reporting']['output_dir'] = args.output_dir
    
    # 创建测试实例并运行
    test = WebRegressionTest(
        base_url=args.url,
        output_dir=config['reporting']['output_dir']
    )
    
    test.crawl_and_test(max_pages=config['crawler']['max_pages'])

if __name__ == "__main__":
    main() 