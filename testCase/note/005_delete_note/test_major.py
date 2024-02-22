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
class TestDeleteNote_Major(unittest.TestCase):
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
    url = host + dataConfig['interface']['DeleteNote']['path']
    optionKeys = dataConfig['interface']['DeleteNote']['optionKeys']
    base = dataConfig['interface']['DeleteNote']['base']
    assertBase = {"responseTime": int}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """删除便签主流程"""
        step('PRE-STEP:创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        body = copy.deepcopy(self.base)
        body['noteId'] = c_notes[0]
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 断言
        CheckMethod().output_check(self.assertBase, res.json())
        # 通过查询接口验证是否真实删除,valid为0标识已删除
        path = '/v3/notesvr/get/notebody'
        data = {
            "noteIds": [c_notes[0]],
        }
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.wps_sid}',
            'X-user-key': str(self.userid)
        }
        res = requests.post(url=self.host + path, headers=headers, json=data)
        self.assertEqual(0, res.json()['noteBodies'][0]['valid'])

