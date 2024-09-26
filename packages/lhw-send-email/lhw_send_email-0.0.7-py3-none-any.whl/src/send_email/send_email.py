'''
encoding:   -*- coding: utf-8 -*-
@Time           :  2024/9/24 13:32
@Project_Name   :  All_Learning
@Author         :  lhw
@File_Name      :  send_email.py

功能描述

实现步骤

'''

import smtplib
from email.mime.text import MIMEText



class SendEmail:
    def __init__(self, fromEmailAddress: str, password: str, destination: list[str], content: str, subject: str,
                 api=None):
        """
        fromEmailAddress: 格式 "Name <example@qq.com>"  <>中是邮件服务器(地址)
        password: 邮箱授权码
        destination: 格式 "example@qq.com"  邮箱地址,不一定为qq邮箱
        content: 内容
        subject: 邮件标题
        api: 邮件服务器地址(默认为ses.tencentcloudapi.com)
        """

        self.fromEmailAddress = fromEmailAddress
        self.password = password
        self.destination = destination
        self.content = content
        self.subject = subject
        self.api = 'smtp.qq.com'

        if api is None:
            self.api = "smtp.qq.com"
        else:
            self.api = api

        self.msg = MIMEText(content, 'plain', 'utf-8')  # 纯文本

        self.msg['From'] = fromEmailAddress  # 发送者邮件地址
        self.msg['To'] = destination[0]  # 接收者邮件地址
        self.msg['Subject'] = self.subject  # 邮件标题

    def send(self):
        try:
            # 初始化,建立SMTP,SSL的链接,链接发送方的服务器
            smtp = smtplib.SMTP_SSL(self.api, 465)
            # smtp.starttls()

            # 登录发送方的邮箱
            smtp.login(self.fromEmailAddress, self.password)

            # 发送
            smtp.sendmail(self.fromEmailAddress, self.destination, self.msg.as_string())

            smtp.quit()
        except Exception as e:
            return f'发送失败:\n{e}'






