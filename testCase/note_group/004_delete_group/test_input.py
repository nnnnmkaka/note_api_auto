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
class TestDeleteGroup_Input(unittest.TestCase):
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
        """groupId字段缺失"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body.pop('groupId')
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1010, "errorMsg": "GroupId Requested!"}
        CheckMethod().output_check(expect, res.json())

    @parameterized.expand(['', '@&#……￥'])
    def testCase02(self, v):
        """groupId字段为空or特殊字符"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['‘ or ‘1=1', '“ or ”1=1'])
    def testCase03(self, v):
        """groupId字段:SQL注入"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062eb', 'abcdefg112233'])
    def testCase04(self, v):
        """身份校验：wps_id过期、非法"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=v)
        # 断言状态码
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2010, "errorMsg": ""}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase05(self):
        """身份校验：wps_id缺失"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userid)
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态401')
        expect = {"errorCode": -2009, "errorMsg": ""}
        # 断言
        CheckMethod().output_check(expect, res.json())

    def testCase06(self):
        """身份校验：userid非法"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId='aaa112233', sid=self.wps_sid)
        self.assertEqual(400, res.status_code, msg='状态码异常，期望的状态400')

    def testCase07(self):
        """身份校验：userid缺失"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.wps_sid}'
        }
        res = self.re.post(url=self.url, body=body, headers=headers)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        # 断言
        CheckMethod().output_check(expect, res.json())
