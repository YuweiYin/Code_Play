#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：64
题目：滑动窗口的最大值

题目描述：
给定一个数组和滑动窗口的大小，找出所有滑动窗口里数值的最大值。
例如，如果输入数组 {2,3,4,2,6,2,5,1} 及滑动窗口的大小 3，
那么一共存在 6 个滑动窗口，他们的最大值分别为 {4,4,6,6,6,5}；
针对数组 {2,3,4,2,6,2,5,1} 的滑动窗口有以下 6 个：
{[2,3,4],2,6,2,5,1}, {2,[3,4,2],6,2,5,1}, {2,3,[4,2,6],2,5,1},
{2,3,4,[2,6,2],5,1}, {2,3,4,2,[6,2,5],1}, {2,3,4,2,6,[2,5,1]}

时间限制：1秒 空间限制：32768K
本题知识点：栈和队列
"""

import sys
import time


class Solution:
    @staticmethod
    def max_in_windows(num, size):
        # 边界情况
        if num is None or len(num) <= 0 or size <= 0:
            return []

        # 数组长度不足窗口大小，则只返回一个值，即全数组最大值
        if len(num) <= size:
            i = 0
            current_best = num[0]
            while i < len(num):
                if current_best < num[i]:
                    current_best = num[i]

                i += 1

            return [current_best]

        answer = []

        i = 0
        # 从头找到窗口
        while i < (len(num) - size + 1):
            current_best = num[i]

            # 在当前窗口找到最大值
            j = i + 1
            while j < (size + i):
                if num[j] > current_best:
                    current_best = num[j]

                j += 1

            # 把当前窗口的最大值加进结果列表
            answer.append(current_best)

            # 窗口滑动
            i += 1

        return answer


def main():
    num = [2, 3, 4, 2, 6, 2, 5, 1]
    size = 3

    start = time.process_time()
    answer = Solution.max_in_windows(num, size)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
