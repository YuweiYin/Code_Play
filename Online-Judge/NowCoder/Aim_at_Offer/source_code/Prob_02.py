#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：02
题目：替换空格

题目描述：
请实现一个函数，将一个字符串中的每个空格替换成“%20”。
例如，当字符串为 We Are Happy. 则经过替换之后的字符串为We%20Are%20Happy。

时间限制：1秒 空间限制：32768K
本题知识点：字符串
"""

import sys
import time


class Solution:
    @staticmethod
    def replace_space(s):
        # 参数解释：s 源字符串
        if s.find(' ') >= 0:
            s_list = s.split(' ')
            s = '%20'.join(s_list)
        return s


def main():
    s = "We Are Happy."

    start = time.process_time()
    ans = Solution.replace_space(s)
    end = time.process_time()

    print(ans)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
