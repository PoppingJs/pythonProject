import pymysql


class MySQLHandler:

    def __init__(self, host=None,
                 port=3306,
                 user=None,
                 password=None,
                 database=None, **kwargs):
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=password,
                                    database=database, **kwargs)

    def query_all(self, sql):
        """查询所有的记录.
        游标对象最好不要用多次，用完关掉，下次再初始化。
        """
        cursor = self.conn.cursor()
        # 事务提交
        self.conn.commit()

        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        return records

    def query_one(self, sql):
        """查询一条记录"""
        cursor = self.conn.cursor()
        # 提交事务
        self.conn.commit()

        cursor.execute(sql)
        record = cursor.fetchone()
        cursor.close()
        return record

    def close(self):
        """关闭连接"""
        self.conn.close()


if __name__ == '__main__':
    mydb = MySQLHandler(host='47.113.180.81',
                        port=3306,
                        user='lemon',
                        password='lemon123',
                        database='yami_shops')
    sql = "SELECT mobile_code FROM tz_sms_log WHERE user_phone = '18711277355' LIMIT 5;"

    items = mydb.query_one(sql)
    print(items[0])
