#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：67
题目：剪绳子

题目描述：
给你一根长度为 n 的绳子，请把绳子剪成整数长的 m 段（m、n 都是整数，n > 1 并且 m > 1），
每段绳子的长度记为 k[0], k[1], ..., k[m]。请问 k[0] * k[1] * ... * k[m] 可能的最大乘积是多少？
例如，当绳子的长度是 8 时，我们把它剪成长度分别为 2、3、3 的三段，此时得到的最大乘积是 18。

输入描述：
输入一个数 n，意义见题面。（2 <= n <= 60）

示例：
输入：8
输出：18

时间限制：C/C++ 1 秒，其他语言 2 秒
空间限制：C/C++ 64 M，其他语言 128 M
本题知识点：回溯法
"""

import sys
import time


class Solution:
    def __init__(self):
        self.best_product = 1  # 当前最优乘积

    def cut_rope(self, number):
        # 注意：题目要求切分成的子段数目 m > 1

        # 边界情况
        if number <= 1:  # 存在子段为 0
            return 0

        if number == 2:  # 切分为 1、1
            return 1

        if number == 3:  # 切分为 1、2
            return 2

        # 思路 1：
        # 贪心回溯 DFS，探索当前选择能得到的最优解。注意剪枝。
        # 但相较于下述思路 2，回溯法会比较慢。

        # 思路 2：
        # 如果某子段长度仅为 1，不会提升乘积值，所以至少剪切出的子段长度应该至少为 2
        # 根据均值不等式，在固定切分的子段数目 m 时，等分地切分才会使得总乘积最大
        cur_m = 2  # 当前划分的子绳长度
        while cur_m < number:
            cur_res = 1  # 按当前划分来计算子绳长度总乘积
            sub_rope_amount = int(number / cur_m)  # 整段的 cur_m 数目
            left_sub_rope = number % cur_m  # 剩余的子绳长度

            cur_res *= cur_m ** sub_rope_amount

            # 若有剩余的非整段
            if left_sub_rope > 0:
                cur_res *= left_sub_rope

            # 更新最优值
            if self.best_product < cur_res:
                self.best_product = cur_res

            cur_m += 1

        return self.best_product


def main():
    solution = Solution()

    # answer = 18
    number = 8

    start = time.process_time()
    answer = solution.cut_rope(number)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
