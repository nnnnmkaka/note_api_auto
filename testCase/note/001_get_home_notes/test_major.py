import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.clearNote import ClearNote
from businessCommon.createNote import CreateNotes
from common.yamlRead import YamlRead
from common.caseLog import info, error, step, class_case_log
import copy
from businessCommon.re import Re


@class_case_log
class TestGetHomeNotes_Major(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']
    assertBase = {
        "responseTime": int,
        "webNotes": [
            {"noteId": str, "createTime": int, "star": 0, "remindTime": 0,
             "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
             "title": str,
             "summary": str,
             "thumbnail": "null",
             "contentVersion": int, "contentUpdateTime": int}]}

    # 初始化用户便签数据
    def setUp(self) -> None:
        ClearNote().clear_note(self.userid, self.wps_sid)

    def testCase01(self):
        """获取首页便签主流程"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)

        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        expect = copy.deepcopy(self.assertBase)
        # 修改期望值
        expect['webNotes'][0]['noteId'] = c_notes[0]
        # 通用断言
        CheckMethod().output_check(expect, res.json())

