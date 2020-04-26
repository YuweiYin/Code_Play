#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：66
题目：机器人的运动范围

题目描述：
地上有一个 m 行和 n 列的方格。一个机器人从坐标 (0, 0) 的格子开始移动，
每一次只能向左，右，上，下四个方向移动一格，但是不能进入行坐标和列坐标的数位之和大于 k 的格子。
例如，当 k 为 18 时，机器人能够进入方格 (35, 37)，因为 3+5+3+7 = 18。
但是，它不能进入方格 (35, 38)，因为 3+5+3+8 = 19。
请问该机器人能够达到多少个格子？

时间限制：1秒 空间限制：32768K
本题知识点：回溯法
"""

import sys
import time


class Solution:
    def __init__(self):
        self.rows = 0     # 行数
        self.cols = 0     # 列数
        self.dic = set()  # 记录已经走过的格子坐标

    def moving_count(self, threshold, rows, cols):
        self.rows, self.cols = rows, cols
        self.dic = set()

        # 从坐标为 (0, 0) 开始搜索解空间
        self.search(threshold, 0, 0)

        # 返回能走的格子总数
        # print(self.dic)
        return len(self.dic)

    # 回溯法
    def search(self, threshold, i, j):
        # 如果机器人不能走坐标为 (i, j) 的格子，或者 (i, j) 格子已经走过了
        if not self.judge(threshold, i, j) or (i, j) in self.dic:
            return

        # 标记该格子已经走过了
        self.dic.add((i, j))

        # 不考虑往左往上走，因为已经走过了
        # 如果还能往右走、不“撞墙”，那就往右走
        if i != self.rows - 1:
            self.search(threshold, i + 1, j)

        # 如果还能往下走、不“撞墙”，那就往下走
        if j != self.cols - 1:
            self.search(threshold, i, j + 1)

        # 回溯

    # 判断机器人在 threshold 的限制下，能否走入坐标为 (i, j) 的格子
    @staticmethod
    def judge(threshold, i, j):
        # 代码解释：str(i) 把数值型数据转换为字符串，list(str(i)) 把各位数字拆开成列表
        # map(int, list(str(i))) 把 int 函数作用于每个 list(str(i)) 的元素，列表元素全转为数值型
        # 最后用 sum 函数加起来，得到 i 各数位之和
        return sum(map(int, list(str(i)))) + sum(map(int, list(str(j)))) <= threshold


def main():
    solution = Solution()

    # answer = 359
    threshold = 15
    rows = 20
    cols = 20

    start = time.process_time()
    answer = solution.moving_count(threshold, rows, cols)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
