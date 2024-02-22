import requests


class ClearNote:
    host = 'https://note-api.wps.cn'

    def clear_note(self, userid, sid):
        """
        清空用户下所有普通便签和回收站便签
        :param userid:
        :param sid:
        :return:
        """

        get_note_url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes'
        delete_note_url = self.host + '/v3/notesvr/delete'
        clear_note_url = self.host + '/v3/notesvr/cleanrecyclebin'
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(userid),
            'Content-Type': 'application/json'
        }

        # 获取用户下所有得普通便签
        res = requests.get(get_note_url, headers=headers)
        note_ids = []
        for item in res.json()['webNotes']:
            note_ids.append(item['noteId'])

        # 删除便签
        for noteId in note_ids:
            body = {
                'noteId': noteId
            }
            res = requests.post(delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

        # 清空回收站
        clear_body = {
            'noteIds': ['-1']
        }
        res = requests.post(clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200

    def clear_remind_note(self, userid, sid):
        """
        清空用户下所有日历便签
        :param userid:
        :param sid:
        :return:
        """

        get_note_url = self.host + '/notesvr/web/getnotes/remind'
        delete_note_url = self.host + '/v3/notesvr/delete'
        clear_note_url = self.host + '/v3/notesvr/cleanrecyclebin'
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(userid),
            'Content-Type': 'application/json'
        }

        data = {
            "rows": 300,
            "startIndex": 0,
            "month": "2024/02",
            "remindStartTime": 1706716800000,
            "remindEndTime": 1709222400000
        }
        # 获取用户下所有的日历便签
        res = requests.post(get_note_url, headers=headers, json=data, timeout=3)
        note_ids = []
        for item in res.json()['webNotes']:
            note_ids.append(item['noteId'])

        # 删除便签
        for noteId in note_ids:
            body = {
                'noteId': noteId
            }
            res = requests.post(delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

        # 清空回收站
        clear_body = {
            'noteIds': ['-1']
        }
        res = requests.post(clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200

    def clear_invalid_note(self, userid, sid):
        """
        删除用户下便签到回收站下
        :param userid:
        :param sid:
        :return:
        """

        get_note_url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes'
        delete_note_url = self.host + '/v3/notesvr/delete'
        clear_note_url = self.host + '/v3/notesvr/cleanrecyclebin'
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(userid),
            'Content-Type': 'application/json'
        }

        # 获取用户下所有得普通便签
        res = requests.get(get_note_url, headers=headers)
        note_ids = []
        for item in res.json()['webNotes']:
            note_ids.append(item['noteId'])

        # 删除便签
        for noteId in note_ids:
            body = {
                'noteId': noteId
            }
            res = requests.post(delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

    def clear_group(self, userid, sid):
        """
        清空用户下所有便签分组
        :param userid:
        :param sid:
        :return:
        """

        get_group_url = self.host + '/notesvr/get/notegroup'
        delete_group_url = self.host + '/notesvr/delete/notegroup'
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-User-Key': str(userid),
            'Content-Type': 'application/json'
        }

        # 获取用户下所有得便签分组
        data = {
            "lastRequestTime": 0,
            "excludeInValid": True
        }
        res = requests.post(url=get_group_url, headers=headers, json=data)
        group_ids = []
        for item in res.json()['noteGroups']:
            group_ids.append(item['groupId'])

        # 删除分组
        for groupId in group_ids:
            body = {
                'groupId': groupId
            }
            res = requests.post(delete_group_url, headers=headers, json=body)
            assert res.status_code == 200

# if __name__ == '__main__':
#     userid = '254829293'
#     sid = 'V02SomNtzabvIXCSrQzFYQ-WWE7Xcz800a0cc561000f3062ed'
#     ClearNote().clear_note(userid, sid)
