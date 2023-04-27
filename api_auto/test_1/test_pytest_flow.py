import pytest
from api_auto.api.apis import APICase
import json
from api_auto.config.config import Config
from api_auto.common.excel import DoExcel
#Flow
test_datas = DoExcel(Config.CASE_FILE, 'order_ftest').read_excel_dict()

class Testflow(APICase):
    def setup_method(self):
        self.doexcel= DoExcel(self.config.CASE_FILE,'order_ftest')

    @pytest.mark.parametrize('dic', test_datas)
    def test_flow(self,dic):
        method = dic["method"]
        url = self.config.HOST+dic["url"]
        #数据替换
        data = self.replace_data(dic["json"])
        data = json.loads(data)            #将json转换为字典用json.loads比eval()安全
        headers = {}
        if dic['headers']:
            headers = dic['headers']     #完整的请求头已经放在excel表格
            headers = self.replace_data(headers)
            headers = json.loads(headers)  #将json转化为字典
        expected_data = dic["expected_data"]
        res = self.api(method, url, data=data, headers=headers)
        # 数据提取
        extract_data = dic["extract_data"]
        if extract_data:     #可能是没有extract_data的
            extract_data2 = json.loads(extract_data)
            self.extract(res, extract_data2)

        if 'application/json' in res.headers["Content-Type"]:
            actual_res = res.json()
        else:
            actual_res = res.text
        try:
            assert expected_data in actual_res
            if True:
                test_res = 'PASS'
            else:
                test_res = 'Fail'
        except Exception as e:
            test_res = 'Fail'
            print(e)
        finally:
            self.doexcel.write_res(dic['id'] + 1, 10, str(actual_res))
            self.doexcel.write_res(dic['id'] + 1, 13, str(test_res))

if __name__ == '__main__':
    pytest.main('-vs')