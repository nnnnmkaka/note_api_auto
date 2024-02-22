import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.clearNote import ClearNote
from businessCommon.createNote import CreateNotes
import copy
from common.yamlRead import YamlRead
from common.caseLog import info, error, step, class_case_log
from common.yamlRead import YamlRead
from businessCommon.re import Re
from parameterized import parameterized


@class_case_log
class TestGetNoteGroup_Handle(unittest.TestCase):
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
    url = host + dataConfig['interface']['GetNoteGroup']['path']
    optionKeys = dataConfig['interface']['GetNoteGroup']['optionKeys']
    base = dataConfig['interface']['GetNoteGroup']['base']
    assertBase = {"noteGroups": [
        {"userId": "254829293", "groupId": "111111", "groupName": "旅游笔记", "order": 0, "valid": 1,
         "updateTime": int}], "requestTime": int}

    # 初始化用户便签分组数据
    def setUp(self) -> None:
        ClearNote().clear_group(self.userid, self.wps_sid)

    def testCase01(self):
        """获取分组列表数量校验:0个分组"""
        # step('PRE-STEP:新建1个分组')
        # group_ids = CreateGroups().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:获取分组列表接口请求')
        body = copy.deepcopy(self.base)
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        # 断言状态码
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 修改期望值
        expect = {"noteGroups": [], "requestTime": int}
        CheckMethod().output_check(expect, res.json())

    def testCase02(self):
        """获取分组列表数量校验:2个分组"""
        step('PRE-STEP:新建10个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 2)
        step('STEP:获取分组列表接口请求')
        body = copy.deepcopy(self.base)
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        # 断言状态码
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 断言获取的分组数量
        self.assertEqual(2, len(res.json()['noteGroups']), msg='获取的分组数量异常，期望值为2')

    def testCase03(self):
        """越权"""
        step('PRE-STEP:新建1个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:获取分组列表接口请求')
        body = copy.deepcopy(self.base)
        res = self.re.post(url=self.url, body=body, userId=self.userid2, sid=self.wps_sid)
        # 断言状态码
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        CheckMethod().output_check(expect, res.json())
