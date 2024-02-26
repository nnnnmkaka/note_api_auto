import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.clearNote import ClearNote
from businessCommon.createNote import CreateNotes
from common.yamlRead import YamlRead
from common.caseLog import info, error, step, class_case_log
import copy
from businessCommon.re import Re
from parameterized import parameterized


@class_case_log
class TestGetHomeNotes_Input(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']

    assertBase = {"responseTime": int, "webNotes": [
        {"noteId": str, "createTime": int, "star": 0, "remindTime": 0,
         "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
         "title": str,
         "summary": str,
         "thumbnail": "null",
         "contentVersion": int, "contentUpdateTime": int}]}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """过期的wps_sid"""

        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)

        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid='V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb')
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2010, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase02(self):
        """非法的wps_sid"""

        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)

        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid='abcdefg112233')
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2010, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase03(self):
        """wps_id key缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, headers={})
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2009, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase04(self, v):
        """startindex入参校验"""

        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        startindex = v
        rows = 10
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为500')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase05(self, v):
        """rows入参校验"""

        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        startindex = 1
        rows = v
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase06(self, v):
        """userid入参校验"""

        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        userid = v
        startindex = 1
        rows = 10
        path = f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为500')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

