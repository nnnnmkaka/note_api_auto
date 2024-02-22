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
class TestRestoreNotes_Major(unittest.TestCase):
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
        """恢复回收站的便签主流程"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 删除便签')
        ClearNote().clear_invalid_note(self.userid, self.wps_sid)
        path = f'/notesvr/v2/user/{self.userid}/notes'
        body = copy.deepcopy(self.base)
        body['noteIds'] = c_notes
        res = self.re.patch(url=self.host + path, body=body, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')

