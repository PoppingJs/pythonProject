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

#高级接口测试  --测试用例的代码写的都一样

# 调用 read_excel_dict 文件读取Excel 当中的测试数据

log.info("正在读取测试数据")

items = read_excel_dict(Config.CASE_FILE, 'order_flow')
# 表示这个测试类需要用到数据驱动
@ddt
class TestOrderFlow(unittest.TestCase, APICase):

    # @classmethod
    # def setUpClass(cls) :
    #     pass
    #
    # def tearDown(self) -> None:
    #     pass

    @list_data(items)
    def test_order_flow(self, item):
        """
        1， 访问获取验证码的接口
        2， 通过数据库读取验证码
        3， 访问校验验证码接口，得到 flag
        4, 访问注册信息接口
        """
        data = item['json']
        data = self.replace_data(data)

        headers = {}
        if item['headers']:
            headers = item['headers']     #完整的请求头已经放在excel表格
            headers = self.replace_data(headers)
            headers = json.loads(headers)  #将json转化为字典
        data = json.loads(data)

        response = requests.request(method=item["method"],
                                    url=item["url"],
                                    json=data,
                                    headers=headers
                                    )

        # 数据提取
        extract_data = item['extract_data']

        if extract_data:     #可能是没有extract_data的
            #excel里的一般是json格式的---json.loads转化成字典
            extract_data2 = json.loads(extract_data)
            self.extract(response, extract_data2)

        print(response.text)
        try:
            self.assertTrue(item["expected_data"] in response.text)
        except AssertionError as e:
            self.logger.error(f"断言失败：{e}")
            # 一定不要忘记，记录好日志之后，要手工再把异常抛出来。
            # 这样用例才能触发异常，实现用例不通过
            raise e

