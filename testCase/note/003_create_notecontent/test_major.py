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
class TestCreateNoteContent_Major(unittest.TestCase):
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
    url = host + dataConfig['interface']['CreateNoteContent']['path']
    optionKeys = dataConfig['interface']['CreateNoteContent']['optionKeys']
    base = dataConfig['interface']['CreateNoteContent']['base']
    assertBase = {
        "responseTime": int,
        "contentVersion": int,
        "contentUpdateTime": int
    }

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """上传便签内容主流程"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())
        # 调用查询便签接口验证数据源
        path = '/v3/notesvr/get/notebody'
        data = {
            "noteIds": [c_noteid],
        }
        res = self.re.post(url=self.host + path, body=data, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(c_noteid, res.json()['noteBodies'][0]['noteId'])

    def testCase02(self):
        """更新便签内容主流程"""
        step('PRE-STEP: 创建1条便签主体')
        c_infoVersion, c_noteid = CreateNotes().create_notes_info(self.userid, self.wps_sid)
        step('STEP: 新建便签内容')
        body = copy.deepcopy(self.base)
        body['localContentVersion'] = c_infoVersion
        body['noteId'] = c_noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())
        step('STEP: 更新便签内容')
        body['title'] = 'test11'
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')

        # 调用查询便签接口验证数据源
        path = '/v3/notesvr/get/notebody'
        data = {
            "noteIds": [c_noteid],
        }
        res = self.re.post(url=self.host + path, body=data, userId=self.userid, sid=self.wps_sid)
        self.assertEqual('test11', res.json()['noteBodies'][0]['title'], msg='便签标题不对')
