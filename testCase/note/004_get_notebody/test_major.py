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
class TestGetNoteBody_Major(unittest.TestCase):
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
    url = host + dataConfig['interface']['GetNoteBody']['path']
    optionKeys = dataConfig['interface']['GetNoteBody']['optionKeys']
    base = dataConfig['interface']['GetNoteBody']['base']
    assertBase = {"responseTime": int,
                  "noteBodies": [{"summary": "test",
                                  "noteId": str,
                                  "infoNoteId": str, "bodyType": 0,
                                  "body": "test", "contentVersion": int,
                                  "contentUpdateTime": int, "title": str, "valid": 1}]}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """获取便签内容主流程"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('PRE-STEP: 获取便签内容接口请求')
        body = copy.deepcopy(self.base)
        body['noteIds'] = [c_notes[0]]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')
        # 修改期望值noteId的值
        expect = copy.deepcopy(self.assertBase)
        expect['noteBodies'][0]['noteId'] = c_notes[0]
        # 断言
        CheckMethod().output_check(expect, res.json())

