import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.clearNote import ClearNote
from businessCommon.createNote import CreateNotes
from common.yamlRead import YamlRead
from common.caseLog import info, error, step, class_case_log
import copy
from businessCommon.re import Re
from parameterized import parameterized


@class_case_log
class TestGetHomeNotes_Handle(unittest.TestCase):
    # 实例化封装的请求方法
    re = Re()
    # 公共参数
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid = envConfig['userId1']
    wps_sid = envConfig['sid1']
    userid2 = envConfig['userId2']
    wps_sid2 = envConfig['sid2']
    assertBase = {"responseTime": int, "webNotes": [
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
        """查询便签数量校验,用户A存在0条便签数据"""
        step('PRE-STEP: 创建0条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 0)
        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询便签数量异常，期望的状态值为0')

    def testCase02(self):
        """查询便签数量校验,用户A存在多条便签数据"""
        step('PRE-STEP: 创建5条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 5)
        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 200
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        self.assertEqual(5, len(res.json()['webNotes']), msg='查询便签数量异常，期望的状态值为5')

    def testCase03(self):
        """查询普通便签接口不返回日历便签"""
        step('PRE-STEP: 创建1条日历便签数据')
        c_notes = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 200
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询便签数量异常，期望的状态值为0')

    def testCase04(self):
        """查询普通便签接口不返回分组便签"""
        step('PRE-STEP: 创建1条日历便签数据')
        c_notes = CreateNotes().create_remind_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 200
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态值为200')
        self.assertEqual(0, len(res.json()['webNotes']), msg='查询便签数量异常，期望的状态值为0')

    def testCase05(self):
        """越权"""
        step('PRE-STEP: 创建1条便签数据')
        c_notes = CreateNotes().create_notes(self.userid, self.wps_sid, 1)
        step('STEP: 获取首页便签的接口请求')
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid2}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url=self.host + path, sid=self.wps_sid2)
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态值为401')
