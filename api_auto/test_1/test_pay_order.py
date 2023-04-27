
import json

import ddt
import unittest

import requests
from api_auto.api.apis import APICase
from api_auto.common.excel import read_excel_dict
from api_auto.config.config import Config

# 调用 read_excel_dict 文件读取Excel 当中的测试数据
items = read_excel_dict(Config.CASE_FILE, 'pay')

# 表示这个测试类需要用到数据驱动
@ddt.ddt
class TestPayOrder(unittest.TestCase, APICase):
    '''支付主要的是token和order_number,其他都是前置条件，只需要满足条件即可'''
    '''但也必须是测试通过的接口'''
    def setUp(self):
        """前置"""
        # 访问登录接口， 得到 token

        token = self.user_login('yuze', '1234')
        self.logger.info(f"正在登录，获取 token 值")
        # 获取某个商品的数据
        product_id, sku_id = self.get_product(2131)
        self.logger.info(f"正在获取商品 id {product_id}")
        # 创建订单
        self.confirm_order(token, product_id, sku_id)
        # 确认生成订单，得到一个 orderNumber
        order_number = self.submit_order(token)

        self.token = token
        self.order_number = order_number

    @ddt.data(*items)
    def test_admin_login(self, item):

        data = item['json']
        #数据替换
        data = data.replace('#orderId#', self.order_number)
        #字符串转成json格式
        data = json.loads(data)

        headers = {"Authorization": f"bearer{self.token}"}

        response = requests.request(method='post',
                                    url=self.config.HOST + item['url'],
                                    json=data,
                                    headers=headers)

        self.logger.info(f"请求数据：{data}")
        self.logger.info(f"响应结果：{response.text}")

        try:
            self.assertTrue(item['expected'] in response.text)
        except AssertionError as e:
            self.logger.error(f"断言失败：{e}")
            # 一定不要忘记，记录好日志之后，要手工再把异常抛出来。
            # 这样用例才能触发异常，实现用例不通过
            raise e


