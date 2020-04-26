#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：12
题目：数值的整数次方

题目描述：
给定一个 double 类型的浮点数 base 和 int 类型的整数 exponent。
求 base 的 exponent 次方。

时间限制：1秒 空间限制：32768K
本题知识点：代码的完整性
"""

import sys
import time


class Solution:
    @staticmethod
    def power(base, exponent):
        power = 1
        if exponent == 0:
            # 指数为 0，结果为 1
            return 1
        elif exponent > 0:
            # 正指数
            for i in range(exponent):
                power *= base
        else:
            # 负指数
            base = 1 / float(base)
            for i in range(-exponent):
                power *= base

        return power

        # 直接调用内置函数 pow 也可以
        # return pow(base, exponent)


def main():
    base = 2
    exponent = -3

    start = time.process_time()
    res = Solution.power(base, exponent)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
