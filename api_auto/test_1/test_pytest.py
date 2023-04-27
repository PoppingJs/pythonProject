import pytest
from api_auto.api.apis import APICase
import json
from api_auto.config.config import Config
from api_auto.common.excel import DoExcel
#单接口
test_datas = DoExcel(Config.CASE_FILE, 'adminLogin').read_excel_dict()

class Testlogin(APICase):
    def setup_method(self):
        self.doexcel= DoExcel(self.config.CASE_FILE,'Login')

    @pytest.mark.parametrize('dic', test_datas)
    def test_login(self,dic):
        method = dic["method"]
        url = self.config.HOST+dic["url"]
        data = json.loads(dic["json"])     #将json转换为字典用json.loads比eval()安全
        headers = json.loads(dic["headers"])
        expected = dic["expected"]
        res = self.api(method, url, data=data, headers=headers)
        if res.status_code == 200:
            actual_res = res.json()
        else:
            actual_res = res.text
        try:
            assert expected in actual_res
            if True:
                test_res = 'PASS'
            else:
                test_res = 'Fail'
        except Exception as e:
            test_res = 'Fail'
            print(e)
        finally:
            self.doexcel.write_res(dic['id'] + 1, 8, str(actual_res))
            self.doexcel.write_res(dic['id'] + 1, 9, str(test_res))

if __name__ == '__main__':
    pytest.main('-vs')




