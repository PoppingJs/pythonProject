
import json
import unittest

import requests
from unittestreport import ddt, list_data
from api_auto.config.config import Config
from api_auto.common.excel import read_excel_dict
from api_auto.common.logger import log

# 调用 read_excel_dict 文件读取Excel 当中的测试数据
from api_auto.api.apis import adminLogin, upload_image

log.info("正在读取测试数据")

items = read_excel_dict(Config.CASE_FILE, 'addProduct')





# 表示这个测试类需要用到数据驱动
@ddt
class TestAdminLogin(unittest.TestCase):

    def setUp(self):
        # 登录
        self.token = adminLogin("student", "123456a")
        # 上传一张图片
        file = r'C:\py50\day25_接口实战7_前置接口\上课笔记\code.png'
        self.img = upload_image(file, self.token)


    @list_data(items)
    def test_admin_login(self, item):
        """
        1，登录
        2， 上传文件
        3， 访问上传产品的接口
        :param item:
        :return:
        """
        projectInfo = item['json']
        headers = {"Authorization": f"Bearer{self.token}"}
        data = json.loads(projectInfo)
        data['pic'] = self.img
        data['imgs'] = self.img

        response = requests.request(method='post',
                                    url=item['url'] ,
                                    json=data,
                                    headers=headers)
        print(response.json())


        # url = item["url"]
        # data = item['json']
        # data = eval(data)
        # method = item['method']
        # expected = eval(item['expected'])

        # 把通用的验证码设置成 我们识别后的验证码
        # data['imageCode'] = self.code
        # data['sessionUUID'] = self.uid
        # # data['t'] = time.time()
        #
        # # 访问接口
        # response = requests.request(method=method,
        #                             url=url,
        #                             json=data)
        #
        # # content = response.json()
        # try:
        #     content = response.json()
        #     content["custom_msg"] = "success"
        # except:
        #     # 先把响应结果转化成 字典
        #     # Incorrect account or password
        #     # "msg":
        #     content = {"custom_msg": response.text}
        #
        # # 判断响应结果和预期是否完全相等
        # # 判断响应结果和预期是否部分相等（包含了某个字段，是不是存在 token 字段）
        # # 判断相应结果中是否包含了预期结果
        # self.assertEqual(content["custom_msg"], expected["custom_msg"])
