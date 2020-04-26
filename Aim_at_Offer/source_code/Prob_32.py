#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：32
题目：把数组排成最小的数

题目描述：
输入一个正整数数组，把数组里所有数字拼接起来排成一个数，
打印能拼接出的所有数字中最小的一个。例如输入数组{3，32，321}，
则打印出这三个数字能排成的最小数字为 321323。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间效率
"""

import sys
import time


class Solution:
    def print_min_number(self, numbers):
        # 边界情况
        num_len = len(numbers)

        if num_len <= 0:
            return ''

        if num_len == 1:
            return numbers[0]

        # 思路：转换成字符串后，n[i]+n[i+1] 和 n[i+1]+n[i] 进行字典序比较，取升序

        array = []
        for i in range(num_len):
            array.append(str(numbers[i]))

        key = self.cmp_to_key(self.cmp)
        # print(array)
        # print(sorted(array))
        # print(sorted(array, key=key, reverse=False))

        # return ''.join(sorted(array, self.cmp, reverse=False))  # Python 2
        return ''.join(sorted(array, key=key, reverse=False))

    # 自定义排序函数（Python 2）
    @staticmethod
    def cmp(x, y):
        # 将 x+y 与 y+x 相比，值更小的元素（x 或者 y）排在前面
        if (x + y) < (y + x):
            return -1
        if (y + x) < (x + y):
            return 1
        return 0

    # Python 2 的 cmp 转为 Python 3 的 key
    # 参考自 https://github.com/python/cpython/blob/3.8/Lib/functools.py
    @staticmethod
    def cmp_to_key(my_cmp):
        """Convert a cmp= function into a key= function"""

        class K(object):
            __slots__ = ['obj']

            def __init__(self, obj):
                self.obj = obj

            def __lt__(self, other):
                return my_cmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return my_cmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return my_cmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return my_cmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return my_cmp(self.obj, other.obj) >= 0

            __hash__ = None

        return K


def main():
    solution = Solution()

    # numbers = [3, 32, 321]  # res = 321323
    numbers = [3, 32, 1, 321]  # res = 1321323

    start = time.process_time()
    res = solution.print_min_number(numbers)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
