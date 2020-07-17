#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : segment-tree.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
线段树 (Segment Tree, ST)

参考资料：
https://www.youtube.com/watch?v=Oq2E2yGadnU
https://github.com/jakobkogler/Algorithm-DataStructures/blob/master/RangeQuery/SegmentTree.py
"""


class SegmentTree:
    # 构造线段树，一棵完全二叉树（array 长度不为 2 的幂次也无妨）
    # 时间复杂度 O(n)
    # 名为"树"，实则用 数组/list 存储中间结点的值
    # st 的长度为 2 * n，其中后 n 位为叶结点值，
    # 除了第一个元素外的 前 n-1 位为中间结点值
    def __init__(self, array):
        self.arr_len = len(array)
        self.inf = 0x3f3f3f3f  # 1061109567

        self.st = self.arr_len * [self.inf] + array

        for i in reversed(range(1, self.arr_len)):
            self.st[i] = self.merge(self.st[i << 1], self.st[(i << 1) + 1])

        # self.st = (self.arr_len << 1) * [self.inf]
        #
        # i = self.arr_len
        # while i < (self.arr_len << 1):
        #     self.st[i] = array[i - self.arr_len]
        #     i += 1
        #
        # i = self.arr_len - 1
        # while i > 0:
        #     self.st[i] = self.merge(self.st[i << 1], self.st[(i << 1) + 1])
        #     i -= 1

    # 不同的需求可以设计不同的 merge 过程
    # 时间复杂度 O(1)
    @staticmethod
    def merge(a, b):
        # 对于保存区间最小值的线段树来说，merge 的过程应为 min() 函数，
        # 用以取得两个子区间中的最小区间最小值作为当前融合过后的区间的区间最小值
        return min(a, b)

    # 更新数组值、更新树值
    # 时间复杂度 O(log n)
    def update(self, i, value):
        i += self.arr_len
        self.st[i] = value
        while i > 1:
            i >>= 1
            self.st[i] = self.merge(self.st[i << 1], self.st[(i << 1) + 1])

    # 区间查询 [left, right) 左闭右开区间
    # 0 <= left <= right <= n
    # 时间复杂度 O(log n)
    # 从叶结点开始查询。查询时，有三种情况：
    #   case 1. 当前结点所代表的区间完全位于 query 区间之外（与闭区间无交集），则不应考虑当前结点。
    # 	case 2. 当前结点所代表的区间完全位于 query 区间之内（含边界值）
    # 	  case 2.1. 当前结点的父结点所代表的区间也完全位于 query 区间之内（含边界值），
    #               则可以直接查询其父结点值，减少查询量。
    # 	  case 2.2. 当前结点的父结点所代表的区间部分位于 query 区间之内、部分在外，
    #               则分段考虑：先处理位于 query 区间外的部分；后处理位于 query 区间内的部分。
    def minimum(self, left, right):
        # 边界情况
        if left >= right:
            return self.inf
        if right > self.arr_len:
            right = self.arr_len
        if left < 0:
            left = 0

        # 增加偏移量，定位到原始 array 数组位置
        left += self.arr_len
        right += self.arr_len
        minimum = self.inf

        # 区间夹逼
        while left < right:
            if left & 0x1:
                # left 为奇数表示该结点是其父结点的右孩子，
                # 由于 left 左边的值都已经被处理/排除了，
                # 所以这个 left 结点是需要单独考虑、不能再考虑其父结点了
                # 处理其值后将 left 指针右移
                minimum = self.merge(minimum, self.st[left])
                left += 1

            if right & 0x1:
                # right 为奇数同样表示该结点是其父结点的右孩子，
                # 由于 query 区间的 right 为半开区间的边界，故不取其值
                # 这意味着 right 结点的左边一个结点需要单独考虑，不能考虑其父结点了
                # 先将 right 指针左移，然后处理其值
                right -= 1
                minimum = self.merge(minimum, self.st[right])

            # 将 left 和 right 上移一层（索引号除以 2）
            left >>= 1
            right >>= 1

        return minimum

    def print_st(self):
        print(self.st)


def main():
    # array = [1, 5, 3, 7, 3, 2, 5, 7]
    array = [4, 3, 9, 1, 6]  # array 长度为奇数也没问题

    st = SegmentTree(array)
    st.print_st()

    start = time.process_time()
    ans = st.minimum(1, 6)
    end = time.process_time()

    print(ans)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
