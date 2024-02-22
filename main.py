import unittest
from BeautifulReport import BeautifulReport
import os
import sys
import time
sys.path.append('path_to_your_module')  # 替换为你的模块所在路径

ENVIRON = "Online"  # 线上 Online 测试环境 Offline
Dir = os.path.dirname(os.path.abspath(__file__))


def run(test_suite):
    # 定义输出的文件位置和名字
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    filename = f"{now}_report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir='./report')


if __name__ == '__main__':
    run_pattern = 'all'  # all 全量测试用例执行/smoking 冒烟测试执行/指定执行文件
    if run_pattern == 'all':
        pattern = 'test*.py'
    elif run_pattern == 'smoking':
        pattern = 'test_major*.py'
    else:
        pattern = run_pattern + '.py'

    suite = unittest.TestLoader().discover('./testCase', pattern=pattern)

    run(suite)
