import smtplib
from email.mime.text import MIMEText  # 邮件正文
from email.utils import formataddr
from zhongBao_unit.sqlserver import SQLserver

my_sender = 'you sender'  # 发件人邮箱账号
my_pass = 'you pass'  # 发件人邮箱密码
my_user = 'you username'  # 收件人邮箱账号，我这边发送给自己


class Alarm():
    def send_mail(self, shuju, head='异常检测',):
        my_users = self.get_users()

        msg = MIMEText(f'{str(head)}:{str(shuju)}', 'plain', 'utf-8')
        msg['From'] = formataddr([f"{head}", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["管理员", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "大鱼程序报告"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_users, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接

    def get_users(self):

        server = SQLserver()
        sql = server.select_fetchall('select email from monitor where status=0')
        print(sql)
        return sql


if __name__ == '__main__':
    api = Alarm()
    # api.get_users()
    api.send_mail('shuju', '飞猪登录失效')
