import unittest
from ddt import ddt,data
from api_auto.common.excel import DoExcel
from api_auto.api.apis import APICase
from api_auto.config.config import Config
test_datas= DoExcel(Config.CASE_FILE,'Login').read_excel_dict()
@ddt
class login(unittest.TestCase, APICase):
    def setUp(self):
        self.doexcel= DoExcel(self.config.CASE_FILE,'Login')
    @data(*test_datas)
    def test_case1(self,test_data):
        method = test_data["method"]
        url = self.config.HOST+test_data["url"]
        data = eval(test_data["json"])
        headers = eval(test_data["headers"])
        expected = test_data["expected"]
        #json=data，data传参必须是字典格式，res.json()返回的也是字典格式
        res = self.api(method, url,data=data, headers=headers)
        if res.status_code == 200:
            actual_res = res.json()
        else:      #存在异常情况，返回response不是json格式---respons.json()报错
            actual_res = res.text
        try:
            self.assertTrue(expected in actual_res)
            test_res = 'PASS'
        except AssertionError:
            test_res = 'Fail'
            raise AssertionError('账号密码不正确')
        finally:
            #默认excel行和列都是从1开始，除去标题,写入准确位置数据，行=id+1
            self.doexcel.write_res(test_data['id']+1,8,str(actual_res))
            self.doexcel.write_res(test_data['id']+1,9,str(test_res))





