
import pytest
import requests
from api_auto.common.excel import DoExcel
from api_auto.config.config import Config
#fixture格式
# @pytest.fixture(scope='session')
# def init_env():
#     """前置后置，加几句"""
#     print("前置")
#     yield
#     print("后置")

#保持登录会话请求，应用多个接口
@pytest.fixture(scope='session')
def init_env():
    # 在测试开始前，创建一个session对象
    session = requests.Session()
    # 在测试结束后，关闭session
    yield session
    session.close()

@pytest.fixture(scope='function')
def login(init_env):
    # 登录，获取access_token
    url = 'http://api.example.com/login'
    data = {
            "principal": "15755808681",
            "credentials": "123456",
            "appType": 3,
            "loginType": 0
            }
    headers = {"Content-Type": "application/json"}
    response = init_env.request("post", url, json=data,headers=headers)
    access_token = response.json()['access_token']
    # 设置访问头
    init_env.headers.update({'Authorization': 'Bearer ' + access_token})












