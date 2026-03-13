import pymssql
# from .Cookies.emaill import Alarm


# 封装类
class SQLserver():
    conn = None  # 这里的None相当于其它语言的NULL
    serr_num = 1

    def __init__(self):  # 构造函数
        try:
            self.conn = pymssql.connect('The database connection address of sqlserver')
        except Exception as erorr:
            self.serr_num = 5
            # a = '数据库链接错误' + str(erorr)
            # alarm = Alarm()
            # alarm.send_mail(a)
            # print(a)
            return

            # 调用语句 执行语句

    def m_update(self, sql):
        try:
            cursor = self.conn.cursor()

            cursor.execute(sql)
            self.conn.commit()

        except Exception as erorr:
            self.serr_num = self.serr_num + 1
            a = '数据库更新错误' + str(erorr)
            # alarm = Alarm()
            # alarm.send_mail(a)
            # print(a)
            self.conn.rollback()

    # 插入语句
    def m_insert(self, sql, param):
        try:
            cursor = self.conn.cursor()

            cursor.executemany(sql, param)
            self.conn.commit()



        except Exception as erorr:
            self.serr_num = self.serr_num + 1
            a = '数据库插入错误' + str(erorr)
            # alarm = Alarm()
            # alarm.send_mail(a)
            # print(a)
            # self.conn.rollback()

    # 查询 接收全部的返回结果行
    def select_fetchall(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            self.conn.commit()

            return result
        except Exception as erorr:
            self.serr_num = self.serr_num + 1
            # a = '数据库查询错误' + str(erorr)
            # alarm = Alarm()
            # alarm.send_mail(a)
            # print(a)
            self.conn.rollback()

    # 查询 接收单个的返回结果行
    def select_fetchone(self, sql):
        try:
            cursor = self.conn.cursor(as_dict=True)
            cursor.execute(sql)
            result = cursor.fetchone()
            self.conn.commit()

            return result
        except Exception as erorr:
            self.serr_num = self.serr_num + 1
            # a = '数据库查询错误' + str(erorr)
            # alarm = Alarm()
            # alarm.send_mail(a)
            # print(a)

    # 关闭连接

    def __del__(self):  # 析构函数
        self.conn.close()  # 关闭数据库连接
