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
class TestGetGroupNote_Major(unittest.TestCase):
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
        """获取分组下的便签主流程"""
        step('PRE-STEP:新建一个分组')
        group_ids = CreateNotes().create_groups(self.userid, self.wps_sid, 1)
        step('PRE-STEP:在分组下新建便签')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1, group_ids[0])
        step('STEP:获取分组下的便签接口请求')
        body = copy.deepcopy(self.base)
        body['groupId'] = group_ids[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 修改期望值
        expect = copy.deepcopy(self.assertBase)
        expect['webNotes'][0]['groupId'] = group_ids[0]
        expect['webNotes'][0]['noteId'] = c_notes[0]
        CheckMethod().output_check(expect, res.json())


