import unittest


class CheckMethod(unittest.TestCase):
    def output_check(self, expect, actual):
        """
        通用的断言方法
        :param expect: 字典类型，接口返回的期望结果
        :param actual: 字典类型，接口返回的实际结果
        :return:
        """
        # 校验字段返回的个数与期望值相符，没有多余的字段
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='keys len error!')
        for k, v in expect.items():
            # 校验接口文档中的字段名存在于实际的接口返回字段中
            self.assertIn(k, actual.keys(), msg=f'key:【{k}】 not in response!')
            # 校验字段类型与接口文档一致
            if isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f'key:【{k}】 type error!')
            elif isinstance(v, list):
                self.assertEqual(len(v), len(actual[k]), msg=f'key:【{k}】 len error!')
                for i in range(len(v)):
                    if isinstance(v[i], type):
                        self.assertEqual(v[i], type(actual[k][i]), msg=f'list value:【{v[i]}】type error!')
                    elif isinstance(v[i], dict):
                        # 使用递归的方法，校验有嵌套字典类型的返回字段值
                        self.output_check(v[i], actual[k][i])
                    else:
                        self.assertEqual(v[i], actual[k][i],  msg=f'list value:【{v[i]}】value error!')
            elif isinstance(v, dict):
                self.output_check(v, actual[k])  # 使用递归的方法，校验有嵌套字典类型的返回字段值
            else:
                self.assertEqual(v, actual[k], msg=f'key:【{k}】 value error!')

# expect = {"responseTime": int, "webNotes": [
#     {"noteId": "9f166c769d0943a4b5341dee06ff839a", "createTime": 1705835948329, "star": 0,
#      "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": 1705835948329, "groupId": None,
#      "title": "RvVuinGbrtYHSAxgkC1TXg==", "summary": "6GSZCxH5vZTX5vgfB/q547O85G1q9kQhpoQHUcVkB/g=",
#      "thumbnail": "null", "contentVersion": 10, "contentUpdateTime": 1705836144617}]}
#
# actual = {"responseTime": 0, "webNotes": [
#     {"noteId": "9f166c769d0943a4b5341dee06ff839a", "createTime": 1705835948329, "star": 0,
#      "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": 1705835948329, "groupId": None,
#      "title": "RvVuinGbrtYHSAxgkC1TXg==", "summary": "6GSZCxH5vZTX5vgfB/q547O85G1q9kQhpoQHUcVkB/g=",
#      "thumbnail": "null", "contentVersion": 10, "contentUpdateTime": 1705836144617}]}
#
# CheckMethod().output_check(expect, actual)
