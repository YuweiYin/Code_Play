#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：29
题目：最小的 K 个数

题目描述：
输入 n 个整数，找出其中最小的 K 个数。
例如输入 4,5,1,6,2,7,3,8 这 8 个数字，
则最小的 4 个数字是 1,2,3,4。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间效率
"""

import sys
import time


class Solution:
    @staticmethod
    def get_least_numbers_solution(t_input, k):
        if len(t_input) <= 0 or len(t_input) < k:
            return []

        # answer = []

        t_list = sorted(t_input, reverse=False)
        # print t_list

        # for i in range(k):
        #     answer.append(t_list[i])

        return t_list[: k]
        # return answer


def main():
    t_input = [4, 5, 1, 6, 2, 7, 3, 8]
    k = 4

    start = time.process_time()
    res = Solution.get_least_numbers_solution(t_input, k)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
