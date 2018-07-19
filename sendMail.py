import smtplib
from email.mime.text import MIMEText
def sendmail(subject, content,maillist ='644128000@qq.com'):
    email_host = 'smtp.126.com'     # 发送者是163邮箱
    email_user = 'snow5hao@126.com'  # 发送者账号
    email_pwd = 'arrow98.local'       # 发送者密码
    # 三个参数：第一个为文本内容，第二个 html 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(content, 'html', 'utf-8')    # 邮件内容
    msg['Subject'] = subject    # 邮件主题
    msg['From'] = email_user    # 发送者账号
    msg['To'] = maillist    # 接收者账号列表

    smtp = smtplib.SMTP(email_host) # 如上变量定义的，是163邮箱
    #smtp = smtplib.SMTP_SSL(email_host, 465) 阿里云的服务器要把上面的改成这行
    smtp.login(email_user, email_pwd)   # 发送者的邮箱账号，密码
    smtp.sendmail(email_user, maillist, msg.as_string())    # 参数分别是发送者，接收者，第三个不知道
    smtp.quit() # 发送完毕后退出smtp
    # print ('email send success.')

#调用
# sendmail('python smtp', 'python mail test ***')    # 调用发送邮箱的函数
# sendmail('python smtp', 'python mail test','abc@126.com')    # 调用发送邮箱的函数