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
class TestCleanRecycleBin_Handle(unittest.TestCase):
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
    url = host + dataConfig['interface']['CleanRecycleBin']['path']
    optionKeys = dataConfig['interface']['CleanRecycleBin']['optionKeys']
    base = dataConfig['interface']['CleanRecycleBin']['base']
    assertBase = {"responseTime": int}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    @parameterized.expand(['0', '1', '-2'])
    def testCase01(self, v):
        """noteIds无效枚举值"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 清空回收站接口请求')
        body = copy.deepcopy(self.base)
        body['noteIds'] = [v]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        CheckMethod().output_check(self.assertBase, res.json())
        step('STEP: 调用查询接口验证没有被清空')
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/0/rows/999/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        self.assertNotEqual(0, len(res.json()['webNotes']), msg='')

    def testCase02(self):
        """越权"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 清空回收站接口请求')
        body = copy.deepcopy(self.base)
        res = self.re.post(url=self.url, body=body, userId=self.userid2, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态值为412')
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        CheckMethod().output_check(expect, res.json())
