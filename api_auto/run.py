# -----------------------------------------------
# Author: yuz
# Copyright: 湖南零檬信息技术有限公司
# Email: wagyu2016@163.com
# Phone&Wechat: 18173179913
# Site: http://www.lemonban.com
# Forum: http://testingpai.com
# -----------------------------------------------
import unittest
from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover('test_1')

runner = TestRunner(suite, filename="接口自动化测试报告.html",
                    report_dir='./report',
                    tester='young',
                    desc="接口自动化测试报告",
                    templates=2)
runner.run()