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
class TestCreateGroup_Major(unittest.TestCase):
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
    url = host + dataConfig['interface']['CreateGroup']['path']
    optionKeys = dataConfig['interface']['CreateGroup']['optionKeys']
    base = dataConfig['interface']['CreateGroup']['base']
    assertBase = {"responseTime": int, "updateTime": int}

    # 初始化用户便签分组数据
    def setUp(self) -> None:
        ClearNote().clear_group(self.userid, self.wps_sid)

    def testCase01(self):
        """新增分组主流程"""
        step('STEP:新增分组接口请求')
        groupId = str(int(time.time() * 1000)) + '_group_id'
        body = copy.deepcopy(self.base)
        body['groupId'] = groupId
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        CheckMethod().output_check(self.assertBase, res.json())
        # 调用查询分组接口验证新增成功
        body = {
            "lastRequestTime": 0,
            "excludeInValid": True
        }
        res = self.re.post(url=self.host + '/notesvr/get/notegroup', body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual('旅游笔记test', res.json()['noteGroups'][0]['groupName'], msg='新建分组失败')
