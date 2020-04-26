#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：06
题目：旋转数组的最小数字

题目描述：
把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。
输入一个非减排序的数组的一个旋转，输出旋转数组的最小元素。
例如数组 {3,4,5,1,2} 为 {1,2,3,4,5} 的一个旋转，该数组的最小值为 1。
NOTE: 给出的所有元素都大于 0，若数组大小为 0，请返回 0。

时间限制：3秒 空间限制：32768K
本题知识点：查找
"""

import sys
import time


class Solution:
    @staticmethod
    def min_number_in_rotate_array(rotate_array):
        if len(rotate_array) <= 0:
            return 0
        elif len(rotate_array) == 1:
            return rotate_array[0]
        else:
            # 由于原数组时非减排序，那么旋转数组就是两段非减序列
            # 只要查找到单调性突变的位置就好了
            for i in range(len(rotate_array) - 1):
                if rotate_array[i] > rotate_array[i + 1]:
                    return min(rotate_array[0], rotate_array[i + 1])

            return rotate_array[0]


def main():
    rotate_array = [3, 4, 5, 1, 2]
    # rotate_array = [5]

    start = time.process_time()
    res = Solution.min_number_in_rotate_array(rotate_array)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
