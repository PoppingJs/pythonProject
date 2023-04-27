
import unittest

import requests
from unittestreport import ddt, list_data
from api_auto.config.config import Config
from api_auto.api.funcs import login
from api_auto.common.excel import read_excel_dict
from api_auto.common.logger import log

# 调用 read_excel_dict 文件读取Excel 当中的测试数据
log.info("正在读取测试数据")

items = read_excel_dict(Config.CASE_FILE, 'adminLogin')


# 表示这个测试类需要用到数据驱动
@ddt
class TestAdminLogin(unittest.TestCase):

    @list_data(items)
    def test_admin_login(self, item):
        print(item)
        """测试函数当中不能随便加参数的。
        """

        log.info("正在生成测试用例")
        url = item["url"]
        data = item['json']
        data = eval(data)
        method = item['method']
        expected = item['expected']

        # 访问接口
        response = requests.request(method=method,
                                    url=url,
                                    json=data)

        # content = response.json()
        content = response.text
        print(content)

        # 断言  预期结果   实际结果
        print(expected)

        # 判断响应结果和预期是否完全相等
        # 判断响应结果和预期是否部分相等（包含了某个字段，是不是存在 token 字段）
        # 判断相应结果中是否包含了预期结果
        self.assertTrue(expected in content)


class TestAdminLogin2(unittest.TestCase):

    def test_admin_login_1(self):
        """测试函数当中不能随便加参数的。
        """

        log.info("正在生成测试用例")
        url = "http://mall.lemonban.com:8108/adminLogin"

        data = {
            "principal": "student",
            "credentials": "123456a",
            "imageCode": "lemon"
        }
        method = "post"
        expected = {"token_type": "Bearer"}

        # 访问接口
        response = requests.request(method=method,
                                    url=url,
                                    json=data)
        content = response.json()
        self.assertEqual(content['token_type'], expected['token_type'])

    def test_admin_login_2(self):
        """测试函数当中不能随便加参数的。
        """

        log.info("正在生成测试用例")
        url = "http://mall.lemonban.com:8108/adminLogin"

        data = {
            "principal": "stud",
            "credentials": "123456a",
            "imageCode": "lemon"
        }
        method = "post"
        expected = "Incorrect account or password"

        # 访问接口
        response = requests.request(method=method,
                                    url=url,
                                    json=data)
        content = response.text
        self.assertEqual(content, expected)
