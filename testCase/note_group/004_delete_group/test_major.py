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
class TestDeleteGroup_Major(unittest.TestCase):
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
        """删除分组主流程"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('STEP:删除分组接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        CheckMethod().output_check(self.assertBase, res.json())
        step('STEP:调用查询分组接口，验证分组已被删除')
        path = '/notesvr/get/notegroup'
        data = {
            "lastRequestTime": 0,
            "excludeInValid": True
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.wps_sid}',
            'X-user-key': str(self.userid)
        }
        res = requests.post(url=self.host + path, headers=headers, json=data)
        # 断言状态码
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')
        # 断言分组已被删除
        self.assertNotIn(group_ids[0], res.json()['noteGroups'], msg='删除分组失败')



