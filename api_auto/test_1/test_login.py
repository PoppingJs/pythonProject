import unittest
from unittestreport import ddt, list_data
from api_auto.common.excel import read_excel_dict
from api_auto.api.funcs import login
from api_auto.common.logger import log
from api_auto.config.config import Config

# 调用 read_excel_dict 文件读取Excel 当中的测试数据
log.info("正在读取测试数据")

items = read_excel_dict(Config.CASE_FILE, 'Sheet1')

# 表示这个测试类需要用到数据驱动
@ddt
class TestLogin(unittest.TestCase):

    @list_data(items)
    def test_login_all(self, item):
        """测试函数当中不能随便加参数的。
        """
        log.info("正在生成测试用例")
        username = item["username"]
        password = item["password"]
        expected = item['expected']
        actual = login(username, password)
        log.info("正在测试")
        self.assertEqual(eval(expected), actual)
        log.info("测试完成")
