# lhw-send-email

使用 pip install lhw-send-email 进行下载该库<br>
本库是作者第一个自主发布的三方库<br>

# 开发目的

为了完善自主开发的网站的验证码机制而做出的尝试

# 基本用法
1. 安装:
   ```pip install lhw-send-email```
2. 导入包
```
import lhw_send_email as lse

s = lse.SendEmail(fromEmailAddress, password, destination, content, subject, api=None)
```
3. 参数解释
```
fromEmailAddress: 格式 "Name <example@qq.com>"  <>中是邮件服务器(地址)-也可以是qq邮箱地址
password: 邮箱授权码
destination: 格式 "example@qq.com"  邮箱地址,不一定为qq邮箱
content: 内容
subject: 邮件标题
api: 邮件服务器地址(默认为ses.tencentcloudapi.com)
```
