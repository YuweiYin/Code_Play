#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：09
题目：变态跳台阶

题目描述：
一只青蛙一次可以跳上 1 级台阶，
也可以跳上 2 级... 它也可以跳上 n 级。
求该青蛙跳上一个 n 级的台阶总共有多少种跳法。

时间限制：1秒 空间限制：32768K
本题知识点：递归和循环
"""

import sys
import time


class Solution:
    def jump_floor_ii(self, number):
        if number <= 0:
            return 1

        count = 0
        # 每次都可以选择各种可能的跳跃高度
        for i in range(number):
            # 跳跃之后，计算剩余的台阶数
            floor_left = number - i - 1

            if floor_left <= 0:
                # 若剩余台阶数为 0，则表示已经走完一程
                count += 1
            else:
                # 否则继续往上跳跃，递归
                count += self.jump_floor_ii(floor_left)

        return count

    @staticmethod
    def jump_floor_ii_2(number):
        if number <= 0:
            return 1
        else:
            return 2 ** (number - 1)


def main():
    # solution = Solution()
    number = 5

    # 从实验规律看，结果都是 2^(number - 1)
    # res solution.jump_floor_2(1) # 1
    # res = solution.jump_floor_2(2) # 2
    # res = solution.jump_floor_2(3) # 4
    # res = solution.jump_floor_2(4) # 8
    # res = solution.jump_floor_2(5) # 16
    # res = solution.jump_floor_2(6) # 32

    start = time.process_time()
    # res = solution.jump_floor_ii(number)
    res = Solution.jump_floor_ii_2(number)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
