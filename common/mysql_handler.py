import pymysql
from pymysql.cursors import DictCursor


class MysqlHandler():
    def __init__(self,
                 host=None,
                 port=3306,
                 user=None,
                 password=None,
                 charset="UTF8",
                 database=None,
                 cursorclass=DictCursor):
        self.con = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   charset=charset,
                                   database=database,
                                   cursorclass=cursorclass)

        cur = self.con.cursor()
        self.cur = cur

    def query(self, sql, one=True):
        self.con.commit()
        self.cur.execute(sql)
        if one:
            return self.cur.fetchone()
        # self.close()
        return self.cur.fetchall()

    def update(self, sql):
        self.cur.execute(sql)
        self.con.commit()
        # self.close()

    def close(self):
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    qu = MysqlHandler(host="rm-wz930973056btd6j76o.mysql.rds.aliyuncs.com",
                      port=3306,
                      user="nideshop_test",
                      password="!Ji!Z4uQms25oFQs75#w",
                      charset="utf8",
                      database="tpms_toro",
                      cursorclass=DictCursor)


    print(qu.query("select * from tb_user;"))
    qu.close()
