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
class TestGetInvaildNotes_Major(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']
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
        """查看回收站的便签列表主流程"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        step('STEP: 查看回收站的便签列表接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        CheckMethod().output_check(self.assertBase, res.json())

