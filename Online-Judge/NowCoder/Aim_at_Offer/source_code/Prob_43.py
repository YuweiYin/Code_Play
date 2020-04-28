#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：43
题目：左旋转字符串

题目描述：
汇编语言中有一种移位指令叫做循环左移（ROL），
现在有个简单的任务，就是用字符串模拟这个指令的运算结果。
对于一个给定的字符序列 S，请你把其循环左移K位后的序列输出。
例如，字符序列 S="abcXYZdef", 要求输出循环左移 3 位后的结果，
即 "XYZdefabc"。是不是很简单？OK，搞定它！

时间限制：1秒 空间限制：32768K
本题知识点：字符串，知识迁移能力
"""

import sys
import time


class Solution:
    @staticmethod
    def left_rotate_string(s, n):
        if s is None or len(s) <= 0:
            return ''

        # 求余，避免做重复的循环
        s_len = len(s)
        n = n % s_len

        if n == 0:
            return s

        # 直接切片分割，然后连接在一起
        return s[n:] + s[:n]


def main():
    # 'XYZdefabc'
    s = 'abcXYZdef'
    n = 3

    start = time.process_time()
    answer = Solution.left_rotate_string(s, n)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
