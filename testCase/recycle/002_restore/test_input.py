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
class TestRestoreNotes_Input(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']
    dataConfig = YamlRead().data_config()
    base = dataConfig['interface']['RestoreNotes']['base']
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
        path = f'/notesvr/v2/user/notes'
        body = copy.deepcopy(self.base)
        body['noteIds'] = c_notes
        res = self.re.patch(url=self.host + path, body=body, sid=self.wps_sid)
        self.assertEqual(405, res.status_code, msg='状态码异常，期望的状态值为405')

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase02(self, v):
        """userid字段:入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        path = f'/notesvr/v2/{v}/user/notes'
        body = copy.deepcopy(self.base)
        body['noteIds'] = c_notes
        res = self.re.patch(url=self.host + path, body=body, sid=self.wps_sid)
        self.assertEqual(405, res.status_code, msg='状态码异常，期望的状态值为405')

    def testCase03(self):
        """noteIds字段:缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        path = f'/notesvr/v2/{self.userid}/user/notes'
        body = copy.deepcopy(self.base)
        body.pop('noteIds')
        res = self.re.patch(url=self.host + path, body=body, sid=self.wps_sid)
        self.assertEqual(405, res.status_code, msg='状态码异常，期望的状态值为405')

    @parameterized.expand([' ', '你好abc', 'None', '‘ or ‘1=1', '“ or ”1=1'])
    def testCase04(self, v):
        """noteIds字段:入参校验"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        path = f'/notesvr/v2/{self.userid}/user/notes'
        body = copy.deepcopy(self.base)
        body['noteIds'] = c_notes
        res = self.re.patch(url=self.host + path, body=body, sid=self.wps_sid)
        self.assertEqual(405, res.status_code, msg='状态码异常，期望的状态值为405')

    @parameterized.expand(['V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb', 'abcdefg112233'])
    def testCase05(self, v):
        """身份校验：过期or非法的wps_sid"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        path = f'/notesvr/v2/{self.userid}/user/notes'
        body = copy.deepcopy(self.base)
        body['noteIds'] = c_notes
        res = self.re.patch(url=self.host + path, body=body, sid=v)
        self.assertEqual(405, res.status_code, msg='状态码异常，期望的状态值为405')

    def testCase06(self):
        """身份校验：wps_sid缺失"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        path = f'/notesvr/v2/{self.userid}/user/notes'
        body = copy.deepcopy(self.base)
        body['noteIds'] = c_notes
        res = self.re.patch(url=self.host + path, body=body, headers={})
        self.assertEqual(405, res.status_code, msg='状态码异常，期望的状态值为405')
