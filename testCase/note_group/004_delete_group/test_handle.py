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
class TestDeleteGroup_Handle(unittest.TestCase):
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
    url = host + dataConfig['interface']['DeleteGroup']['path']
    optionKeys = dataConfig['interface']['DeleteGroup']['optionKeys']
    base = dataConfig['interface']['DeleteGroup']['base']
    assertBase = {"responseTime": int}

    # 初始化用户便签分组数据
    def setUp(self) -> None:
        ClearNote().clear_group(self.userid, self.wps_sid)

    def testCase01(self):
        """删除分组：分组不为空时不能删除"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1, group_ids[0])
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(400, res.status_code, msg='状态码异常，期望的状态400')
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase02(self):
        """越权"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1, group_ids[0])
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid2, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        CheckMethod().output_check(expect, res.json())
