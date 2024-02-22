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
class TestGetGroupNote_Handle(unittest.TestCase):
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
    url = host + dataConfig['interface']['GetGroupNote']['path']
    optionKeys = dataConfig['interface']['GetGroupNote']['optionKeys']
    base = dataConfig['interface']['GetGroupNote']['base']
    assertBase = {"responseTime": 0, "webNotes": [
        {"noteId": str, "createTime": int, "star": 0, "remindTime": 0,
         "remindType": 0, "infoVersion": int, "infoUpdateTime": int, "groupId": str,
         "title": str, "summary": str, "thumbnail": str,
         "contentVersion": int, "contentUpdateTime": int}]}

    # 初始化用户便签分组数据
    def setUp(self) -> None:
        ClearNote().clear_group(self.userid, self.wps_sid)

    def testCase01(self):
        """获取分组下的便签数量校验：分组下存在0条便签"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        # step('PRE-STEP:在分组下新建便签')
        # c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1, group_ids[0])
        step('STEP:获取分组下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        expect = {"responseTime": 0, "webNotes": []}
        CheckMethod().output_check(expect, res.json())

    def testCase02(self):
        """获取分组下的便签数量校验：分组下存在5条便签"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建5条便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 5, group_ids[0])
        step('STEP:获取分组下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 断言分组下便签数量
        self.assertEqual(5, len(res.json()['webNotes']), msg='便签数量异常，期望的状态5')

    def testCase03(self):
        """数值限制:startIndex"""
        step('PRE-STEP:新建1个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建3条便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 3, group_ids[0])
        step('STEP:获取分组下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['startIndex'] = 1
        body['groupId'] = group_ids[0]
        body['rows'] = 50
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 断言分组下便签数量
        self.assertEqual(2, len(res.json()['webNotes']), msg='便签数量异常，期望的状态2')

    def testCase04(self):
        """数值限制:rows"""
        step('PRE-STEP:新建1个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建3条便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 3, group_ids[0])
        step('STEP:获取分组下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['startIndex'] = 0
        body['groupId'] = group_ids[0]
        body['rows'] = 1
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 断言分组下便签数量
        self.assertEqual(1, len(res.json()['webNotes']), msg='便签数量异常，期望的状态1')

    def testCase05(self):
        """越权"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1, group_ids[0])
        step('STEP:获取分组下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid2, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        CheckMethod().output_check(expect, res.json())
