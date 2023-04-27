
import unittest

import requests
from unittestreport import ddt, list_data
from api_auto.config.config import Config
from api_auto.common.excel import read_excel_dict
from api_auto.common.logger import log
from api_auto.api import apis

# 调用 read_excel_dict 文件读取Excel 当中的测试数据
log.info("正在读取测试数据")


items = read_excel_dict(Config.CASE_FILE, 'adminLogin')


# 表示这个测试类需要用到数据驱动
@ddt
class TestAdminLogin(unittest.TestCase):

    def setUp(self):
        img, uid = apis.get_img()
        self.code = apis.base64_api('simple', 'yuan5311645', img, typeid=3)
        self.uid = uid

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
        expected = eval(item['expected'])

        # 把通用的验证码设置成 我们识别后的验证码
        data['imageCode'] = self.code
        data['sessionUUID'] = self.uid
        # data['t'] = time.time()

        # 访问接口
        response = requests.request(method=method,
                         url=url,
                         json=data)

        # content = response.json()
        try:
            content = response.json()
            content["custom_msg"] = "success"
        except:
            # 先把响应结果转化成 字典
            # Incorrect account or password
            # "msg":
            content = {"custom_msg":  response.text}

        # 判断响应结果和预期是否完全相等
        # 判断响应结果和预期是否部分相等（包含了某个字段，是不是存在 token 字段）
        # 判断相应结果中是否包含了预期结果
        self.assertEqual(content["custom_msg"], expected["custom_msg"])


