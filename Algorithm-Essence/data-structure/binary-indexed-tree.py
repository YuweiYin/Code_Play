#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : binary-indexed-tree.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
树状数组 Fenwick Tree (Binary Indexed Tree, BIT)

参考资料：
https://www.youtube.com/watch?v=v_wj_mOAlig
https://github.com/jakobkogler/Algorithm-DataStructures/blob/master/RangeQuery/BinaryIndexedTree.py
"""


class BinaryIndexedTree:
    # 使用 Add 操作构造线状数组，时间复杂度 O(n log n)
    def __init__(self, array):
        self.bit_len = len(array) + 1

        # 首位为 0 仅作占位，不影响求和值，让实际值从下标 1 开始
        self.bit = self.bit_len * [0]

        for i in range(len(array)):
            self.add(i, array[i])

    # 把 array 中下标为 index 的元素值 增长 value，并维护 BIT，时间复杂度 O(log n)
    # 对应 BIT 数组，直接影响的是 self.bit 中下标为 index + 1 的元素
    def add(self, index, value):
        if 0 <= index < self.bit_len:
            index += 1  # BIT 首位为 0 仅作占位，需绕过
            while index < self.bit_len:
                self.bit[index] += value
                index += index & (-index)

    # 求前 num 个元素值的和，时间复杂度 O(log n)
    def sum(self, num):
        # 边界情况
        if num <= 0:
            return 0
        if num >= self.bit_len:
            num = self.bit_len - 1

        res = 0
        while num:  # num 到 0 则终止循环
            res += self.bit[num]
            num -= num & (-num)
        return res

    # 求闭区间 [from, to] 中元素值的和，时间复杂度 O(log n)
    # 序号从 1 开始
    def range_sum(self, from_index, to_index):
        # 边界情况
        if from_index > to_index:
            return 0
        if from_index <= 0:
            from_index = 1
        if to_index >= self.bit_len:
            to_index = self.bit_len - 1

        # 返回前 to 项和与前 from - 1 项和之差，即为闭区间 [from, to] 之总和
        return self.sum(to_index) - self.sum(from_index - 1)

    def print_bit(self):
        print(self.bit)


def main():
    array = [1, 7, 3, 0, 5, 8, 3, 2, 6, 2, 1, 1, 4, 5]
    print(array)

    bit = BinaryIndexedTree(array)
    bit.print_bit()  # [0, 1, 8, 3, 11, 5, 13, 3, 29, 6, 8, 1, 10, 4, 9]

    start = time.process_time()
    ans = bit.sum(100)
    end = time.process_time()
    print('bit.sum(13):', ans)  # 48

    bit.add(0, 20)
    bit.print_bit()  # [0, 21, 28, 3, 31, 5, 13, 3, 49, 6, 8, 1, 10, 4, 9]

    print('bit.sum(13):', bit.sum(13))  # 63
    print('bit.range_sum(0, 13):', bit.range_sum(0, 13))  # 63
    print('bit.range_sum(1, 13):', bit.range_sum(1, 13))  # 63
    print('bit.range_sum(2, 13):', bit.range_sum(2, 13))  # 42
    print('bit.range_sum(3, 13):', bit.range_sum(3, 13))  # 35
    print('bit.range_sum(-1, 18):', bit.range_sum(-1, 18))  # 68

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
