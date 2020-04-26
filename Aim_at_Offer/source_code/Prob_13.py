#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：13
题目：调整数组顺序使奇数位于偶数前面

题目描述：
输入一个整数数组，实现一个函数来调整该数组中数字的顺序，
使得所有的奇数位于数组的前半部分，所有的偶数位于数组的后半部分，
并保证奇数和奇数，偶数和偶数之间的相对位置不变。

时间限制：1秒 空间限制：32768K
本题知识点：代码的完整性
"""

import sys
import time


class Solution:
    @staticmethod
    def reorder_array(array):
        odd_array = []
        even_array = []

        if len(array) <= 0:
            return []
        else:
            for i in range(len(array)):
                temp_item = array[i]
                if (temp_item % 2) == 0:
                    even_array.append(temp_item)
                else:
                    odd_array.append(temp_item)

            return odd_array + even_array


def main():
    array = [1, 4, 5, 6, 3, 2]

    start = time.process_time()
    res = Solution.reorder_array(array)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
