import base64
import json
import re
import time
import uuid

import jsonpath
import requests
from faker import Faker

from api_auto.common.db import MySQLHandler
from api_auto.common.logger import log
from api_auto.config.config import Config



def get_img():
    """获取验证码"""
    url = Config.HOST + '/captcha.jpg'
    uid = str(uuid.uuid4())
    resp = requests.get(url, params={"uuid": uid})
    return resp.content, uid


def base64_api(uname, pwd, img, typeid):
    """上传图片"""
    base64_data = base64.b64encode(img)
    b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


def adminLogin(username, password, code="lemon"):
    """管理员登录.
    访问登录接口封装成函数
    """
    user = {
        "principal": username,
        "credentials": password,
        "imageCode": code
    }
    response = requests.request(
        'POST',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8108/adminLogin",
        json=user
    )
    try:
        content = response.json()
        return content['access_token']
    except Exception as e:
        log.error(f"登录失败:{e}")
        raise e


def upload_image(file, token):
    """图片上传"""
    f = open(file, 'rb')
    headers = {"Authorization": f"Bearer{token}"}
    response = requests.request(
        'POST',
        url="http://mall.lemonban.com:8108/admin/file/upload/img",
        files={"file": f},
        headers=headers
    )
    f.close()
    # 2022/06/c46e4c6e808949528628ca5ecad04661.jpg
    return response.text


def send_sms(mobile):
    """发送验证码"""
    data = {"mobile": mobile}
    response = requests.request(
        'PUT',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/user/sendRegisterSms",
        json=data
    )
    content = response.text
    return content


def check_sms(mobile, validCode):
    """校验验证码"""
    data = {"mobile": mobile, "validCode": validCode}
    response = requests.request(
        'PUT',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/user/checkRegisterSms",
        json=data
    )
    content = response.text
    print(content)
    if content == 'The verification code is wrong or expired':
        raise ValueError("验证码错误或者超时")
    return content  # flag


def generate_mobile():
    """生成手机号码"""
    fk = Faker(locale=['zh-CN'])
    mobile = fk.phone_number()
    return mobile


def user_login():
    """用户登录"""
    data = {"principal": "yuze", "credentials": "1234", "appType": 3, "loginType": 0}
    response = requests.request(
        'post',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/login",
        json=data
    )
    return response.json()['access_token']


def get_product(token):
    """用户登录"""
    mydb = MySQLHandler(host='47.113.180.81',
                        port=3306,
                        user='lemon',
                        password='lemon123',
                        database='yami_shops')
    result = mydb.query_one('SELECT prod_id FROM tz_prod where status=1 and total_stocks > 10 and sold_num < 9')
    product_id = result[0]

    sku = mydb.query_one(f'SELECT sku_id FROM tz_sku WHERE prod_id = {product_id} AND is_delete=0 AND stocks > 1')
    sku_id = sku[0]
    # hey
    data = {"addrId": 0,
            "orderItem": {"prodId": product_id, "skuId": sku_id, "prodCount": 1, "shopId": 1},
            "couponIds": [],
            "isScorePay": 0,
            "userChangeCoupon": 0,
            "userUseScore": 0,
            # "uuid":"2ef80031-eb8d-4b3c-8ed8-e33720c4388a"
            }

    headers = {"Authorization": f"bearer{token}"}
    response = requests.request(
        'post',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/p/order/confirm",
        json=data,
        headers=headers
    )
    return response.text


def submit_order(token):
    """用户登录"""

    data = {"orderShopParam": [{"remarks": "", "shopId": 1}]}

    headers = {"Authorization": f"bearer{token}"}
    response = requests.request(method=
        'post',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/p/order/submit",
        json=data,
        headers=headers
    )
    return response.json()['orderNumbers']


def pay_order(token, orderNum):  #用户再次确认产品信息是否正确
    """下单"""
    # /p/order/getOrderPayInfoByOrderNumber?orderNumbers=1539147910774788096
    params = {"orderNumbers": orderNum}

    headers = {"Authorization": f"bearer{token}"}
    response = requests.request(
        'get',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/p/order/getOrderPayInfoByOrderNumber",
        params=params,
        headers=headers
    )
    return response.text


def pay(token, orderId):
    """发起支付"""
    # http://mall.lemonban.com:8107/p/order/pay
    data = {"payType": 3, "orderNumbers": orderId}

    headers = {"Authorization": f"bearer{token}"}
    response = requests.request(
        'post',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/p/order/pay",
        json=data,
        headers=headers
    )
    return response.text


def callback(token, orderId):
    """发起支付"""
    # http://mall.lemonban.com:8107/notice/pay/3
    data = {"payNo": orderId,
            "bizPayNo": str(int(time.time() * 1000)),
            "isPaySuccess": True, }

    headers = {"Authorization": f"bearer{token}"}
    response = requests.request(
        'post',
        # url=Config.urls.adminLogin,
        url="http://mall.lemonban.com:8107/notice/pay/3",
        json=data,
        headers=headers
    )
    return response.text


class APICase:      #接口操作放在APICase下面便于继承
    # 需要用到的类或者模块保存成类属性
    logger = log
    config = Config
    # db = MySQLHandler(host='47.113.180.81',
    #                     port=3306,
    #                     user='lemon',
    #                     password='lemon123',
    #                     database='yami_shops')
    #
    # # 方法1
    # db_config = Config.db
    # db = MySQLHandler(host=db_config['host'],
    #                   port=db_config['port'],
    #                   user=db_config['user'],
    #                   password=db_config['password'],
    #                   database=db_config['database'])
    # 方法2：字典解包   -解成A=B形式
    db = MySQLHandler(**Config.db)    #数据库初始化放在APICase类
    # db2 = MySQLHandler(**Config.db2)

    def api(self,method, url, params=None, data=None, headers=None):
        response = requests.request(method=method,
                               url=url,
                               params=params,
                               json=data,
                               headers=headers)
        return response

    # @classmethod
    def replace_data(self, my_string):
        """替换 #。。# 标记"""
        result = re.finditer('#(.+?)#', my_string)
        for el in result:
            target = el.group()  # #smsflag#
            prop = el.group(1)
            value = getattr(self, prop)   #动态获取类属性
            my_string = my_string.replace(target, str(value))
        return my_string

    #放在APICase里面方便继承
    def user_login(self, username, password):
        """用户的登录"""
        data = {"principal":username,"credentials":password,"appType":3,"loginType":0}
        headers = {"Content-Type":"application/json"}
        response = requests.request(method='post',
                         headers= headers,
                         json=data,             #接收的data为字典类型 ，若是json格式，需要转换为字典
                         url=self.config.HOST + '/login')
        return response   #['access_token']   #.json()返回的是字典类型

    def get_product(self, product_id):
        """获取 product, 2131"""
        url =self.config.HOST +'/prod/prodInfo'   #原本：url= 'http://mall.Lemonban.com:8107/prod/prodInfo?prodId=2131'
        response = requests.request(method='get',
                                    url=url,
                                    params={'prodId': product_id})    #将动态prodId作为参数传进去
        content = response.json()
        return product_id, content['skuList'][0]['skuId']    #根据接口返回结果写ckuId


    def get_product_jsonpath(self, product_id):
        """jsonpath 版本"""
        url =self.config.HOST +  '/prod/prodInfo'
        response = requests.request(method='get',
                                    url=url,
                                    params={'prodId': product_id})
        content = response.json()
        sku_id = jsonpath.jsonpath(content, '$..skuId')[0]
        return product_id, sku_id


    def confirm_order(self, token, product_id, sku_id):
        """确认订单"""
        data = {"addrId": 0,
                "orderItem": {"prodId": product_id, "skuId": sku_id, "prodCount": 1, "shopId": 1},
                "couponIds": [],
                "isScorePay": 0,
                "userChangeCoupon": 0,
                "userUseScore": 0,
                # "uuid":"2ef80031-eb8d-4b3c-8ed8-e33720c4388a"
                }
        url = self.config.HOST + '/p/order/confirm'
        headers = {"Authorization": f"bearer{token}"}
        response = requests.request(
            method='post',
            url=url,
            json=data,
            headers=headers
        )
        return response.text

    def submit_order(self, token):
        """用户登录, 得到 orderNumber"""
        data = {"orderShopParam": [{"remarks": "", "shopId": 1}]}

        headers = {"Authorization": f"bearer{token}"}
        response = requests.request(
            'post',
            # url=Config.urls.adminLogin,
            url=self.config.HOST + "/p/order/submit",
            json=data,
            headers=headers
        )
        return response.json()['orderNumbers']

    def pay(self, token, orderId):
        """发起支付"""
        # http://mall.lemonban.com:8107/p/order/pay
        data = {"payType": 3, "orderNumbers": orderId}

        headers = {"Authorization": f"bearer{token}"}
        response = requests.request(
            'post',
            # url=Config.urls.adminLogin,
            url=self.config.HOST + "/p/order/pay",
            json=data,
            headers=headers
        )
        return response.text

    def callback(self, token, orderId):
        """回调-发起支付"""
        # http://mall.lemonban.com:8107/notice/pay/3
        data = {"payNo": orderId,
                "bizPayNo": str(int(time.time() * 1000)),
                "isPaySuccess": True }

        url = self.config.HOST + '/notice/pay/3'
        headers = {"Authorization": f"bearer{token}"}
        response = requests.request(
            'post',
            # url=Config.urls.adminLogin,
            url=url,
            json=data,
            headers=headers
        )
        return response.text

    @classmethod   # extract只能是类方法
    def extract(cls, response, extract_data):
        """数据提取
        extract_data: {"access_token":"$..access_token"}
        """

        try:
            content = response.json()
        except:
            raise ValueError("返回值不是json")
        else:
            for prop, jp in extract_data.items():
                # prop =  'access_token'  --动态属性
                # jp = '$..access_token'  --jsonpath表达式
                # value: 取出来的值
                value = jsonpath.jsonpath(content, jp)[0]
                setattr(cls, prop, value)   #动态设置属性


if __name__ == '__main__':

    data = APICase().user_login("15755808689", "123456")
    print(data)




