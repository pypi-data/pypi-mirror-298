import smtplib
import logging

from email.mime.text import MIMEText
from email.utils import formataddr


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def send_mail(subject, content, server_ip, server_port, sender, receiver, authorized_code):
    # 创建邮件消息对象
    message = MIMEText(content, 'plain', 'utf-8')
    # 设置邮件消息对象的发件人和收件人
    message['From'] = formataddr(('实验通知', sender))
    message['To'] = formataddr(('stevenazy', receiver))
    # 设置邮件消息对象的主题
    message['Subject'] = subject

    try:
        # 连接SMTP服务器
        # server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server = smtplib.SMTP_SSL(server_ip, server_port)
        # 登录邮箱账号
        server.login(sender, authorized_code)
        # 发送邮件
        server.sendmail(sender, [receiver], message.as_string())
        # 关闭SMTP连接
        server.quit()
        logging.info("邮件发送成功")
    except Exception as e:
        logging.info(f"邮件发送失败:{e}")



