import requests
import time


class CreateNotes:
    host = 'http://note-api.wps.cn'

    def create_notes(self, userid, sid, nums, groupid=None):
        """
        新建便签数据:主体+数据
        :param userid:
        :param sid:
        :param nums:
        :return:
        """
        note_ids = []
        for i in range(nums):
            # 新建便签主体
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-User-Key': str(userid),
                'Content-Type': 'application/json'
            }

            noteid = str(int(time.time() * 1000)) + '_note_id'
            data = {
                "noteId": noteid,
                "groupId": groupid,
                "star": 0,
                "remindTime": 0,
                "remindType": 0
            }
            res = requests.post(url=self.host + '/v3/notesvr/set/noteinfo', headers=headers, json=data)
            infoVersion = res.json()['infoVersion']

            # 新建便签内容
            data = {
                "title": "test",
                "summary": "test",
                "body": "test",
                "localContentVersion": infoVersion,
                "noteId": noteid,
                "thumbnail": 'null',
                "bodyType": 0
            }
            res = requests.post(url=self.host + '/v3/notesvr/set/notecontent', headers=headers, json=data)
            assert res.status_code == 200

            note_ids.append(noteid)

        return note_ids

    def create_notes_info(self, userid, sid):
        """
        新建便签：主体
        :param userid:
        :param sid:
        :param nums:
        :return:
        """

        # 新建便签主体
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(userid),
            'Content-Type': 'application/json'
        }

        noteid = str(int(time.time() * 1000)) + '_note_id'
        data = {
            "noteId": noteid,
            "star": 0,
            "remindTime": 0,
            "remindType": 0
        }
        res = requests.post(url=self.host + '/v3/notesvr/set/noteinfo', headers=headers, json=data)
        infoVersion = res.json()['infoVersion']

        return infoVersion, noteid

    def create_remind_notes(self, userid, sid, nums):
        """
        新建日历便签数据
        :param userid:
        :param sid:
        :param nums:
        :return:
        """
        note_ids = []
        for i in range(nums):
            # 新建便签主体
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-User-Key': str(userid),
                'Content-Type': 'application/json'
            }

            noteid = str(int(time.time() * 1000)) + '_note_id'
            data = {
                "noteId": noteid,
                "star": 0,
                "remindTime": 1707993000000,   # 2024/2/15
                "remindType": 1
            }
            res = requests.post(url=self.host + '/v3/notesvr/set/noteinfo', headers=headers, json=data)
            infoVersion = res.json()['infoVersion']

            # 新建便签内容
            data = {
                "title": "test",
                "summary": "test",
                "body": "test",
                "localContentVersion": infoVersion,
                "noteId": noteid,
                "thumbnail": 'null',
                "bodyType": 0
            }
            res = requests.post(url=self.host + '/v3/notesvr/set/notecontent', headers=headers, json=data)
            assert res.status_code == 200

            note_ids.append(noteid)

        return note_ids

    def create_groups(self, userid, sid, nums):
        """
        新建分组数据
        :param userid:
        :param sid:
        :param nums:
        :return:
        """
        group_ids = []
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/set/notegroup'
        for i in range(nums):
            # 新建分组
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-User-Key': str(userid),
                'Content-Type': 'application/json'
            }

            groupId = str(int(time.time() * 1000)) + '_group_id'
            data = {
                'groupId': groupId,
                'groupName': '旅游笔记',
                'order': 0
            }
            res = requests.post(url=host + path, headers=headers, json=data)
            group_ids.append(groupId)

        return group_ids


# if __name__ == '__main__':
#     userid = '254829293'
#     sid = 'V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062ed'
#     nums = 3
#     CreateNotes().create_notes(userid, sid, nums)
