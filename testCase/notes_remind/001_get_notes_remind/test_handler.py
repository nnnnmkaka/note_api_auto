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
class TestGetNotesRemind_Handle(unittest.TestCase):
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
        """查看日历下的便签：开始时间大于结束时间"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1709222400000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1706716800000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -7, "errorMsg": "remindTime Requested!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())

    def testCase02(self):
        """查看日历下的便签：查询一天的日历便签"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1707926400000'  # 2024-02-15 00:00:00
        body['remindEndTime'] = '1708012800000'  # 2024-02-16 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase03(self):
        """越权"""
        step('PRE-STEP:新建一条日历便签')
        note_ids = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP:查看日历下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['month'] = '2024/02'
        body['remindStartTime'] = '1706716800000'  # 2024-02-01 00:00:00
        body['remindEndTime'] = '1709222400000'  # 2024-03-01 00:00:00
        res = self.re.post(url=self.url, body=body, userId=self.userid2, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        CheckMethod().output_check(expect, res.json())
