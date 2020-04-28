#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：10
题目：矩形覆盖

题目描述：
我们可以用 2*1 的小矩形横着或者竖着去覆盖更大的矩形。
请问用n个 2*1 的小矩形无重叠地覆盖一个 2*n 的大矩形，
总共有多少种方法？

时间限制：1秒 空间限制：32768K
本题知识点：递归和循环
"""

import sys
import time


class Solution:
    def rect_cover(self, number):
        # 思路：（和 08 青蛙跳台阶题很类似）
        # 以 ::::: 示例 2*5 的大矩形，
        # 要么以竖着的单个 : 排列，
        # 要么两个小矩形叠成 :: 来排列，
        # 转化成排列组合问题
        count = 0
        for i in range(number):
            if (number - i) < i:
                break
            else:
                count += self.comb(number - i, i)

        return count

    # 求组合数 C(n, m)
    # TODO 为避免分子溢出，可进行优化处理
    @staticmethod
    def comb(n, m):
        # 边界情况
        if m <= 0:
            return 1

        if m == 1 or m == (n - 1):
            return n

        if n <= m:
            return 1

        molecular = 1
        denominator = 1
        temp = n
        for i in range(m):
            molecular *= temp
            temp -= 1

        temp = m
        while temp > 0:
            denominator *= temp
            temp -= 1

        return molecular / denominator


def main():
    number = 5
    solution = Solution()

    start = time.process_time()
    res = solution.rect_cover(number)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
