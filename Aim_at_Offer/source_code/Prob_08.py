#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：08
题目：跳台阶

题目描述：
一只青蛙一次可以跳上 1 级台阶，也可以跳上 2 级。
求该青蛙跳上一个 n 级的台阶总共有多少种跳法
（先后次序不同算不同的结果）。

时间限制：1秒 空间限制：32768K
本题知识点：递归和循环
"""

import sys
import time


class Solution:
    def jump_floor(self, number):
        # 思路：
        # 至少有一种跳跃方式：每次都只跳 1 级台阶。
        # 也就是说从 n 次跳跃的可能性中，选择 0 次二级跳，可能性组合有 C(n, 0) 种
        # 然后也可以只选择 1 次二级跳，意味着
        # 从 n-1 次跳跃中，选择 1 次二级跳，可能性组合有 C(n-1, 1) 种
        # 以此类推，保证 C(x, y) 中 x >= y 即可
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
    number = 6
    solution = Solution()

    start = time.process_time()
    res = solution.jump_floor(number)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
