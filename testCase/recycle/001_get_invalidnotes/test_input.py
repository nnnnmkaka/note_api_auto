import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.clearNote import ClearNote
from businessCommon.createNote import CreateNotes
import copy
import time
from common.yamlRead import YamlRead
from common.caseLog import info, error, step, class_case_log
from common.yamlRead import YamlRead
from businessCommon.re import Re
from parameterized import parameterized


@class_case_log
class TestGetInvaildNotes_Input(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']
    assertBase = {"responseTime": int, "webNotes": [
        {"noteId": str, "createTime": int, "star": 0, "remindTime": 0,
         "remindType": 0, "infoVersion": int, "infoUpdateTime": int, "groupId": None,
         "title": str,
         "summary": str,
         "thumbnail": "null",
         "contentVersion": int, "contentUpdateTime": int}]}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """userid字段缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(404, res.status_code, msg='状态码异常，期望的状态值为404')

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase02(self, v):
        """userid字段:入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{v}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为500')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase03(self, v):
        """startindex入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = v
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase03(self, v):
        """rows入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = 0
        rows = v
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb', 'abcdefg112233'])
    def testCase04(self, v):
        """身份校验：过期or非法的wps_sid"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=v)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2010, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase05(self):
        """身份校验：wps_sid缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, headers={})
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2009, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())
