#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：51
题目：构建乘积数组

题目描述：
给定一个数组 a[0, 1, ..., n-1], 请构建一个数组 b[0, 1, ..., n-1],
其中 b 中的元素 b[i] = a[0] * a[1] * ... * a[i-1] * a[i+1] * ... * a[n-1]。
注意不能使用除法。

时间限制：1秒 空间限制：32768K
本题知识点：数组
"""

import sys
import time


class Solution:
    @staticmethod
    def multiply(a):
        if a is None or len(a) <= 0:
            return []

        a_len = len(a)
        if a_len == 1:
            return a

        # 列表元素循环右移，每次右移一位，形成一个新数组
        # 最终结果列表就是：这些新数组的相应位置元素的乘积
        # 但这个方法是 O(n^2) 的复杂度
        # b = []
        # mul_matrix = []
        # i = 1
        # while i < a_len:
        #     mul_matrix.append(a[i:] + a[:i])
        #     i += 1

        # # print(mul_matrix)

        # i = 0
        # mul_len = len(mul_matrix)
        # while i < a_len:
        #     mul = 1
        #     j = 0
        #     while j < mul_len:
        #         mul *= mul_matrix[j][i]
        #         j += 1

        #     b.append(mul)
        #     i += 1

        # return b

        # 方法二：改进效率
        # 还是看成矩阵，但是缓存每一行的两段乘积，对角线的值为 1
        # b0: 1 2 3 4 5
        # b1: 1 1 3 4 5
        # b2: 1 2 1 4 5
        # b3: 1 2 3 1 5
        # b4: 1 2 3 4 1
        # 
        b = [1]

        # 存储下三角的每行乘积
        # b0:
        # b1: 1
        # b2: 1 2
        # b3: 1 2 3
        # b4: 1 2 3 4
        i = 1
        while i < a_len:
            b.append(b[i - 1] * a[i - 1])

            i += 1

        # 再乘以上三角的每行乘积
        # b0:   2 3 4 5
        # b1:     3 4 5
        # b2:       4 5
        # b3:         5
        # b4:
        i = a_len - 2
        mul = 1
        while i >= 0:
            # 每行乘积都迭代存储在 mul 里了
            mul *= a[i + 1]
            b[i] *= mul

            i -= 1

        return b


def main():
    solution = Solution()

    a = [1, 2, 3, 4, 5]

    start = time.process_time()
    answer = solution.multiply(a)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
