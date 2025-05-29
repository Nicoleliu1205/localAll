import schedule
import time
import pymysql
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import logging

# 数据库配置
DB_CONFIG = {
    'host': 'your_db_host',
    'user': 'your_username',
    'password': 'your_password',
    'db': 'newpay',
    'port': 3306
}

# 邮件配置
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'sender': 'your_email@example.com',
    'password': 'your_email_password',
    'receivers': ['recipient1@example.com', 'recipient2@example.com']
}

# 添加日志配置
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'settlement_check.log')),
        logging.StreamHandler()
    ]
)

def check_settlement_data():
    """检查今日结算数据"""
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 获取当前时间
        current_time = datetime.now()
        today = current_time.strftime('%Y-%m-%d')
        
        # 查询今日新增数据
        query = """
        SELECT COUNT(*) 
        FROM pay_console_settlement 
        WHERE DATE(create_time) = %s
        """
        
        cursor.execute(query, (today,))
        count = cursor.fetchone()[0]
        
        # 记录日志
        log_message = f"查询时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        log_message += f"表名: pay_console_settlement\n"
        log_message += f"新增数据条数: {count}\n"
        log_message += "-" * 50
        logging.info(log_message)
        
        # 如果没有新增数据，发送邮件通知
        if count == 0:
            send_alert_email(today)
            
        return count
            
    except Exception as e:
        error_msg = f"数据库查询错误: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        send_error_email(str(e))
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

def send_alert_email(date):
    """发送警告邮件"""
    subject = f'结算数据告警 - {date}'
    message = f'''
    警告：
    日期：{date}
    问题：未检测到新增结算数据
    请及时检查系统是否正常运行。
    '''
    
    send_email(subject, message)

def send_error_email(error_msg):
    """发送错误邮件"""
    subject = f'结算数据检查脚本错误'
    message = f'''
    错误信息：
    {error_msg}
    请检查脚本运行状态。
    '''
    
    send_email(subject, message)

def send_email(subject, message):
    """发送邮件的通用函数"""
    try:
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = ','.join(EMAIL_CONFIG['receivers'])

        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.sendmail(
                EMAIL_CONFIG['sender'],
                EMAIL_CONFIG['receivers'],
                msg.as_string()
            )
        print(f"邮件发送成功: {subject}")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")

def main():
    """主函数"""
    # 设置每天早上7点运行
    schedule.every().day.at("07:00").do(check_settlement_data)
    
    print("监控脚本已启动...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    main()