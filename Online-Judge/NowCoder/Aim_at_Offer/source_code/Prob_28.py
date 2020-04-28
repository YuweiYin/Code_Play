#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：28
题目：数组中出现次数超过一半的数字

题目描述：
数组中有一个数字出现的次数超过数组长度的一半，请找出这个数字。
例如输入一个长度为 9 的数组 {1,2,3,2,2,2,5,4,2}。
由于数字 2 在数组中出现了 5 次，超过数组长度的一半，因此输出 2。
如果不存在则输出 0。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间效率
"""

import sys
import time


class Solution:
    @staticmethod
    def more_than_half_num_solution(numbers):
        num_len = len(numbers)
        # 如果 numbers 数组为空或者只有两个数字，就不会有占比过半的数
        if num_len <= 0 or num_len == 2:
            return 0

        # 如果 numbers 数组仅有一个元素，那么该元素就是占比过半的那个数
        if num_len == 1:
            return numbers[0]

        # 求得“过半”所需达到的最低出现次数
        half = int(num_len / 2) + 1
        # 排好序，让相同值的元素在一起连续出现
        numbers = sorted(numbers, reverse=False)

        # 由于前面的限制，num_len 不低于 3，
        count = 1
        i = 1
        while i < num_len:
            # 从后往前数有多少个连续元素
            if numbers[i] == numbers[i - 1]:
                count += 1
                # 如果达到 half 门限，就找到了占比过半的那个数了
                if count == half:
                    return numbers[i]
            # 当前新的元素与前面不同，于是从头计数
            else:
                count = 1

            i += 1

        # 如果遍历一遍没有找到占比过半的元素，那么就表示不存在该元素
        return 0


def main():
    numbers = [1, 2, 3, 2, 2, 2, 5, 4, 2]
    # numbers = [4, 2, 1, 4, 2, 4]

    start = time.process_time()
    res = Solution.more_than_half_num_solution(numbers)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
