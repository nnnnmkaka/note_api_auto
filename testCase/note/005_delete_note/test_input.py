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
class TestDeleteNote_Input(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']
    userid2 = envConfig['userId2']
    wps_sid2 = envConfig['sid2']
    dataConfig = YamlRead().data_config()
    url = host + dataConfig['interface']['DeleteNote']['path']
    optionKeys = dataConfig['interface']['DeleteNote']['optionKeys']
    base = dataConfig['interface']['DeleteNote']['base']
    assertBase = {"responseTime": int}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """noteIds缺失"""
        step('PRE-STEP:创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        body = copy.deepcopy(self.base)
        body.pop('noteId')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        # 断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['‘1=1', '“ or ”1=1'])
    def testCase02(self, v):
        """noteIds入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')
        # 断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None])
    def testCase03(self, v):
        """noteIds入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase04(self):
        """noteId入参校验:特殊字符"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = '@&#……￥'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb', 'abcdefg112233'])
    def testCase05(self, v):
        """身份校验：wps_id过期、非法"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = c_notes[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=v)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2010, "errorMsg": ""}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase06(self):
        """身份校验：wps_id缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = c_notes[0]
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userid)
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2009, "errorMsg": ""}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase07(self):
        """身份校验：userid非法"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = c_notes[0]
        res = self.re.post(url=self.url, body=body, userId='aaa112233', sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase08(self):
        """身份校验：userid缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = c_notes[0]
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.wps_sid}'
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        # 断言
        CheckMethod().output_check(expect, res.json())
