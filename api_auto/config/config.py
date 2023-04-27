import pathlib

class Config:
    HOST ='http://mall.lemonban.com:8107'
    #账号：15755808681    密码：123456
    # # 获取当前(调用该方法的文件-test_login.py)目录的绝对路径 /test_1
    # FILE = pathlib.Path('.').absolute()
    # # /python_50目录的绝对路径
    # CONFIG_DIR = FILE.parent

    #获取config文件的绝对路径
    CONFIG_FILE = pathlib.Path(__file__).absolute()
    #config目录上级python50的路径
    CONFIG_DIR = CONFIG_FILE.parent.parent

    # 项目的根目录
    ROOT = CONFIG_DIR
    # 测试用例的路径
    CASE_FILE = ROOT / 'data' / 'cases2.xlsx'
    # 日志存储的路径
    LOG_FILE = ROOT / 'common' / 'TY.log'

    # 数据库配置
    db = dict(host='47.113.180.81',
                        port=3306,
                        user='lemon',
                        password='lemon123',
                        database='yami_shops')

    db2 = dict(host='47.113.180.81',
                        port=3307,
                        user='lemon',
                        password='lemon123',
                        database='yami_shops2')


