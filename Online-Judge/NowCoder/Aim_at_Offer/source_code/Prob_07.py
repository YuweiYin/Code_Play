#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：07
题目：斐波那契数列

题目描述：
大家都知道斐波那契数列，现在要求输入一个整数 n，
请你输出斐波那契数列的第 n 项（从 0 开始，第 0 项为 0）。
n <= 39

时间限制：1秒 空间限制：32768K
本题知识点：递推
"""

import sys
import time


class Solution:
    # def fibonacci(self, n):
    #     # 递归方式太慢了，时间复杂度高（指数级别）
    #     if n == 0:
    #         return 0
    #     elif n <= 2:
    #         return 1
    #     else:
    #         return self.fibonacci(n - 2) + self.fibonacci(n - 1)

    @staticmethod
    def fibonacci(n):
        # 一维 DP，缓存中间结果，O(n) 的空间代价
        if n == 0:
            return 0
        elif n <= 2:
            return 1

        number_list = [0, 1, 1]
        for i in range(n - 1):
            # print(i, number_list[i + 1], number_list[i + 2])
            number_list.append(number_list[i + 1] + number_list[i + 2])

        return number_list[n]


def main():
    n = 39

    start = time.process_time()
    res = Solution.fibonacci(n)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
