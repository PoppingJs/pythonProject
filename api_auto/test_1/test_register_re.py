import json
import unittest

import requests
from faker import Faker
from unittestreport import ddt, list_data

from api_auto.api.apis import send_sms, check_sms
from api_auto.common.db import MySQLHandler
from api_auto.config.config import Config
from api_auto.common.excel import read_excel_dict
from api_auto.common.logger import log
from api_auto.api.apis import APICase
# 调用 read_excel_dict 文件读取Excel 当中的测试数据

log.info("正在读取测试数据")

items = read_excel_dict(Config.CASE_FILE, 'register')

# 表示这个测试类需要用到数据驱动
@ddt
class TestRegister(unittest.TestCase,APICase):

    def setUp(self):
        # 发送验证码
        fk = Faker(locale=['zh-CN'])
        mobile = fk.phone_number()

        send_sms(mobile)

        # 查询数据库，得到验证码
        self.mydb = MySQLHandler(host='47.113.180.81',
                            port=3306,
                            user='lemon',
                            password='lemon123',
                            database='yami_shops')
        # 查询数据库，得到验证码
        sql = f"SELECT mobile_code FROM tz_sms_log WHERE user_phone = {mobile} ORDER BY rec_date DESC"
        code = self.mydb.query_one(sql)[0]

        # 校验验证码
        self.smsflag = check_sms(mobile, code)
        self.mobile = mobile
        self.username = mobile

    def tearDown(self) -> None:
        self.mydb.close()

    @list_data(items)
    def test_admin_login(self, item):
        """
        1， 访问获取验证码的接口
        2， 通过数据库读取验证码
        3， 访问校验验证码接口，得到 flag
        4, 访问注册信息接口
        """
        data = item['json']

        # TODO: 数据替换
        data = self.replace_data(data)

        # headers = {"Authorization": f"Bearer{self.token}"}
        data = json.loads(data)

        response = requests.request(method=item["method"],
                                    url=item["url"] ,
                                    json=data,
                                    )
        print(response.text)