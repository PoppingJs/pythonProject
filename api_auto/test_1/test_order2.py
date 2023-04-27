
import json
import unittest

import requests
from faker import Faker
from unittestreport import ddt, list_data

from api_auto.api.apis import send_sms, check_sms, APICase
from api_auto.common.db import MySQLHandler
from api_auto.config.config import Config
from api_auto.common.excel import read_excel_dict
from api_auto.common.logger import log

# 调用 read_excel_dict 文件读取Excel 当中的测试数据

log.info("正在读取测试数据")

items = read_excel_dict(Config.CASE_FILE, 'register')


# 表示这个测试类需要用到数据驱动
@ddt
class TestOrder(unittest.TestCase, APICase):

    def setUp(self):
        token = self.user_login()
        self.get_product(token)
        order_number = self.confirm_order(token)
        self.orderId = order_number
        self.token = token


    def tearDown(self) -> None:
        self.callback(self.token, self.orderId)


    @list_data(items)
    def test_admin_login(self, item):
        """
        """
        data = {"payType": 3, "orderNumbers": self.orderId}

        headers = {"Authorization": f"bearer{self.token}"}
        response = requests.request(
            'post',
            # url=Config.urls.adminLogin,
            url="http://mall.lemonban.com:8107/p/order/pay",
            json=data,
            headers=headers
        )

        print(response.text)
        self.logger.error("hello")

        # headers = {"Authorization": f"Bearer{self.token}"}
        # data = json.loads(data)
        #
        # response = requests.request(method=item["method"],
        #                             url=item["url"] ,
        #                             json=data,
        #                             )
        # print(response.text)