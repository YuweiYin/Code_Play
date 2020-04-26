#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：37
题目：数字在排序数组中出现的次数

题目描述：
统计一个数字在排序数组中出现的次数。

时间限制：1秒 空间限制：32768K
本题知识点：数组，知识迁移能力
"""

import sys
import time


class Solution:
    @staticmethod
    def get_number_of_k(data, k):
        if data is None or len(data) <= 0:
            return 0

        if k in data:
            # 如果 k 在 data 里，找到第一次出现的位置
            k_sum = 1
            first = data.index(k) + 1
            while first < len(data):
                # 遍历之后的数组元素，等于 k 就增加 sum
                if data[first] == k:
                    k_sum += 1
                    first += 1
                # 不同就直接返回 k_sum
                else:
                    return k_sum
        else:
            # 如果 k 不在 data 里，返回 0
            return 0


def main():
    data = [1, 2, 2, 4, 6, 6, 6, 8]
    k = 6

    start = time.process_time()
    answer = Solution.get_number_of_k(data, k)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
