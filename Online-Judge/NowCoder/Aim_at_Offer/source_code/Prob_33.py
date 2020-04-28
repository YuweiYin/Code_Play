#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：33
题目：丑数

题目描述：
把只包含质因子 2、3 和 5 的数称作丑数（Ugly Number）。
例如 6、8 都是丑数，但 14 不是，因为它包含质因子 7。
习惯上我们把 1 当做是第一个丑数。求按从小到大的顺序的第 N 个丑数。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间空间效率的平衡
"""

import sys
import time


class Solution:
    @staticmethod
    def get_ugly_number_solution(index):
        # 边界情况
        if index <= 0:
            return 0

        if index == 1:
            return 1

        # 思路：
        # 要求的新元素，是从前面列表里选择一个，
        # 乘 2、乘 3、乘 5，取最小的那个值，但不能与已有的重复

        ugly_list = [1]  # 丑数列表

        count = 1
        # mul_n 代表 n 还没乘过的元素的最小下标，从 0 开始
        mul_2, mul_3, mul_5 = 0, 0, 0
        while count < index:
            new_num = min(
                ugly_list[mul_2] * 2,
                ugly_list[mul_3] * 3,
                ugly_list[mul_5] * 5,
            )

            # 保证 2/3/5 不再去乘 那些已经乘过的元素了
            if new_num == (ugly_list[mul_2] * 2):
                # print('mul_2: ', mul_2, '->', mul_2 + 1)
                mul_2 += 1
            elif new_num == (ugly_list[mul_3] * 3):
                # print('mul_3: ', mul_3, '->', mul_3 + 1)
                mul_3 += 1
            else:
                # print('mul_5: ', mul_5, '->', mul_5 + 1)
                mul_5 += 1

            # 保证不重复，比如 2 * 3 == 3 * 2
            if new_num in ugly_list:
                continue
            else:
                ugly_list.append(new_num)
                count += 1

        # print(ugly_list)

        return ugly_list[index - 1]


def main():
    index = 10

    start = time.process_time()
    res = Solution.get_ugly_number_solution(index)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
