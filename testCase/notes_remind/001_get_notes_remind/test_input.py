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
class TestGetNotesRemind_Input(unittest.TestCase):
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
    url = host + dataConfig['interface']['GetNotesRemind']['path']
    optionKeys = dataConfig['interface']['GetNotesRemind']['optionKeys']
    base = dataConfig['interface']['GetNotesRemind']['base']
    assertBase = {"responseTime": int, "webNotes": [
        {"noteId": str, "createTime": int, "star": 0,
         "remindTime": int, "remindType": 1, "infoVersion": 1, "infoUpdateTime": int,
         "groupId": None, "title": str,
         "summary": str, "thumbnail": str, "contentVersion": int,
         "contentUpdateTime": int}]}

    # 初始化用户日历便签数据
    def setUp(self) -> None:
        ClearNote().clear_remind_note(self.userid, self.wps_sid)

    def testCase01(self):
        """remindStartTimez字段缺失"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        # body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body.pop('remindStartTime')
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['', None, 'null'])
    def testCase02(self, v):
        """remindStartTimez字段为空"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = v  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['@&#……￥', "‘ or ‘1=1", '“ or ”1=1'])
    def testCase03(self, v):
        """remindStartTimez字段为特殊字符"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = v  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase04(self):
        """remindEndTime字段缺失"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        # body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body.pop('remindEndTime')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['', None, 'null'])
    def testCase05(self, v):
        """remindEndTime字段为空"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = v  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['@&#……￥', "‘ or ‘1=1", '“ or ”1=1'])
    def testCase06(self, v):
        """remindEndTime字段为特殊字符"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = v  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase07(self):
        """startIndex字段缺失"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body.pop('startIndex')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None, 'null'])
    def testCase08(self, v):
        """startIndex字段为空"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body['startIndex'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['@&#……￥', "‘ or ‘1=1", '“ or ”1=1'])
    def testCase09(self, v):
        """startIndex字段为特殊字符"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body['startIndex'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase10(self):
        """rows字段缺失"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body.pop('rows')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['', None, 'null'])
    def testCase11(self, v):
        """rows字段为空"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body['rows'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['@&#……￥', "‘ or ‘1=1", '“ or ”1=1'])
    def testCase12(self, v):
        """rows字段为特殊字符"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        body['rows'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": ""}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb', 'abcdefg112233'])
    def testCase13(self, v):
        """身份校验：wps_id过期、非法"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=v)
        # 断言状态码
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2010, "errorMsg": ""}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase14(self):
        """身份校验：wps_id缺失"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userid)
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2009, "errorMsg": ""}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase15(self):
        """身份校验：userid非法"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId='aaa112233', sid=self.wps_sid)
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态500')
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase16(self):
        """身份校验：userid缺失"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.wps_sid}'
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        # 断言
        CheckMethod().output_check(expect, res.json())
