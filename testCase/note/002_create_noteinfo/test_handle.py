import unittest
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
class TestCreateNoteInfo_Handle(unittest.TestCase):
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
    url = host + dataConfig['interface']['CreateNoteInfo']['path']
    optionKeys = dataConfig['interface']['CreateNoteInfo']['optionKeys']
    base = dataConfig['interface']['CreateNoteInfo']['base']
    assertBase = {
        "responseTime": int,
        "infoVersion": int,
        "infoUpdateTime": int
    }
    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    @parameterized.expand(['0', '1', '2'])
    def testCase01(self, v):
        """star枚举值遍历"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body['star'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    @parameterized.expand(['0', '1', '2'])
    def testCase02(self, v):
        """remindType枚举值遍历"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        body['remindType'] = v
        res = self.re.post(url=self.url, body=body, userId=self.userid, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态200')
        # 通用断言
        CheckMethod().output_check(self.assertBase, res.json())

    def testCase03(self):
        """越权"""
        step('PRE-STEP: 生成一个随机noteid')
        noteid = str(int(time.time() * 1000)) + '_note_id'
        step('STEP: 上传便签信息主体接口请求')
        body = copy.deepcopy(self.base)
        body['noteId'] = noteid
        res = self.re.post(url=self.url, body=body, userId=self.userid2, sid=self.wps_sid)
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态412')
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        # 通用断言
        CheckMethod().output_check(expect, res.json())
