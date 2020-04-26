#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：47
题目：求 1+2+3+...+n

题目描述：
求 1+2+3+...+n，要求不能使用乘除法、for、while、if、else、switch、case
等关键字及条件判断语句（A?B:C）。

时间限制：1秒 空间限制：32768K
本题知识点：发散思维能力
"""

import sys
import time


class Solution:
    def __init__(self):
        self.n_sum = 0
        # self.null_res 仅用作接收短路语句的返回值，避免 PEP8 报警
        self.null_res = True

    def sum_solution(self, n):
        # 思路：
        # 不能用循环语句，就用函数递归替代。
        # 不能用判断语句，就用逻辑短路替代。

        # 由于默认递归深度不到 1000，递归深度太深会报错
        # maximum recursion depth exceeded
        # 因此需要手动修改递归调用深度
        sys.setrecursionlimit(1000000)

        return self.sum(n)

    def sum(self, n):
        # Python 在 3.7 版本前，不允许在判断语句中赋值
        # 不能使用语句 n == 0 or (current_sum += self.sum_solution(n - 1)) > 0
        # 转而利用类成员变量和函数来完成该过程
        self.null_res = n == 0 or (self.add(n, self.sum_solution(n - 1))) > 0

        # 在递归栈底 n == 0 时第一次到达此处，所以返回值从 0 开始累积，
        # 前面都不会被逻辑短路，所以都会执行 self.Add 函数
        return self.n_sum

    def add(self, current_number, next_sum):
        self.n_sum += current_number
        # print(current_number, next_sum, self.n_sum)
        return next_sum


def main():
    n = 1000

    solution = Solution()

    start = time.process_time()
    answer = solution.sum_solution(n)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
