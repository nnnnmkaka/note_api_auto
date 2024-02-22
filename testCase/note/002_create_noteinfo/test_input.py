import unittest
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
class TestCreateNoteInfo_Input(unittest.TestCase):
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
    url = host + dataConfig['interface']['CreateNoteInfo']['path']
    optionKeys = dataConfig['interface']['CreateNoteInfo']['optionKeys']
    base = dataConfig['interface']['CreateNoteInfo']['base']
    assertBase = {
        "responseTime": int,
        "infoVersion": int,
        "infoUpdateTime": int
    }
    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    @parameterized.expand(['abc哈哈', '@&#……￥', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase01(self, v):
        """star入参校验"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body['star'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase02(self):
        """star缺失"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body.pop('star')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['abc哈哈', '@&#……￥'])
    def testCase03(self, v):
        """noteId入参校验"""
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = v
        print(body['noteId'])
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase04(self):
        """noteId缺失"""
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body.pop('noteId')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['abc哈哈', '@&#……￥', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase05(self, v):
        """remindTime（选填）入参校验"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body['remindTime'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase06(self):
        """remindTime缺失"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body.pop('remindTime')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['abc哈哈', '@&#……￥', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase07(self, v):
        """remindType（选填）入参校验"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body['remindType'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase08(self):
        """remindType缺失"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body.pop('remindType')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['abc哈哈', '@&#……￥'])
    def testCase09(self, v):
        """groupId（选填）入参校验"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body['groupId'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase10(self):
        """groupId（选填）缺失"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body.pop('groupId')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase11(self):
        """过期的wps_sid"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid='V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb')
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为401')
        expect = {"errorCode": -2010, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase12(self):
        """非法的wps_sid"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid='abcdefg112233')
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2010, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase13(self):
        """wps_id key缺失"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = {"errorCode": -2010, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase14(self):
        """userid缺失"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        res = self.re.post(url=self.url, body=body, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态值为412')
        expect = {"errorCode": -7, "errorMsg": str}
        # 通用断言
        CheckMethod().output_check(expect, res.json())
