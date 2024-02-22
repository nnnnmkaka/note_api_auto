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
class TestCreateNoteContent_Input(unittest.TestCase):
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
    url = host + dataConfig['interface']['CreateNoteContent']['path']
    optionKeys = dataConfig['interface']['CreateNoteContent']['optionKeys']
    base = dataConfig['interface']['CreateNoteContent']['base']
    assertBase = {
        "responseTime": int,
        "contentVersion": int,
        "contentUpdateTime": int
    }

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """noteid缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body.pop('noteId')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase02(self):
        """title（必填）缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body.pop('title')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None])
    def testCase03(self, v):
        """title入参校验：为空"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['title'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase04(self):
        """title入参校验:@&#……￥"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['title'] = '@&#……￥'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['‘ or ‘1=1', '“ or ”1=1'])
    def testCase05(self, v):
        """title入参校验:sql注入"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['title'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase06(self):
        """title入参校验:长度校验：输入超过200个字符的title"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['title'] = 'sssssssssssssssssssssssssssssddddddddddddddddddddddddddddddddddddddddddddddddddddddddsssssssss' \
                        'swwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' \
                        'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvsssssddddddddddddddddddddddddddddsssssssssssss'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase07(self):
        """summary（必填）缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body.pop('summary')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None])
    def testCase08(self, v):
        """summary入参校验：为空"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['summary'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['@&#……￥', ' ‘ or ‘1=1', '“ or ”1=1'])
    def testCase9(self, v):
        """summary入参校验:特殊字符、sql注入"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['summary'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase10(self):
        """summary入参校验:长度校验：输入超过200个字符的title"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['summary'] = 'sssssssssssssssssssssssssssssddddddddddddddddddddddddddddddddddddddddddddddddddddddddsssssssss' \
                        'swwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' \
                        'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvsssssddddddddddddddddddddddddddddsssssssssssss'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase11(self):
        """body（必填）缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body.pop('body')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1012, "errorMsg": "Note body Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['', None])
    def testCase12(self, v):
        """body入参校验：为空"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['body'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1012, "errorMsg": "Note body Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase13(self):
        """body入参校验:特殊字符"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['body'] = '@&#……￥'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand([' ‘ or ‘1=1', '“ or ”1=1'])
    def testCase14(self, v):
        """body入参校验:特殊字符、sql注入"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['body'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase15(self):
        """body入参校验:长度校验：输入超过200个字符的body"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['body'] = 'sssssssssssssssssssssssssssssddddddddddddddddddddddddddddddddddddddddddddddddddddddddsssssssss' \
                        'swwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww' \
                        'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvsssssddddddddddddddddddddddddddddsssssssssssss'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase16(self):
        """localContentVersion（必填）缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body.pop('localContentVersion')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None, 1000])
    def testCase17(self, v):
        """localContentVersion入参校验"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = v
        body['noteId'] = c_noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['@&#……￥', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase18(self, v):
        """localContentVersion入参校验"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = v
        body['noteId'] = c_noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase19(self):
        """BodyType（必填）缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body.pop('bodyType')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None])
    def testCase20(self, v):
        """bodyType入参校验"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['bodyType'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['@&#……￥', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase21(self, v):
        """bodyType入参校验"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        body['bodyType'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb', 'abcdefg112233', '', None])
    def testCase21(self, v):
        """wps_id入参校验"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=v)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2010, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase22(self):
        """wps_id缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userid)
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2009, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase23(self):
        """非法的userid"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        res = self.re.post(url=self.url, body=body, userId='ddfdf233', sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode":-7,"errorMsg":"参数类型错误！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase24(self):
        """userid缺失"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.wps_sid}'
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())
