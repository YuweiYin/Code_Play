#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : range-min-max-query.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
区间最值查询 Sparse Table (Range Minimum/Maximum Query, RMQ)

参考资料：
https://www.youtube.com/watch?v=9FLPwDn6L08
"""


class SparseTableRMQ:
    # 构造 Sparse Table
    # 时间复杂度 O(n log n)
    def __init__(self, array):
        self.st_len = len(array)
        self.inf = 0x3f3f3f3f  # 1061109567

        # 构造 log_table 用以计算 log_2 (len(array))
        # 首位 0 仅作占位，这样 log_table[i] 表示对 i 取 log_2 对数，下取整
        self.log_table = (self.st_len + 1) * [0]
        for i in range(2, self.st_len + 1):
            self.log_table[i] = self.log_table[i >> 1] + 1

        # 创建二维列表，row = 1 + log_2 (self.st_len)，col = self.st_len
        # 第 0 row 为原始 array
        self.st = [[self.inf] * self.st_len for _ in range(1 + self.log_table[self.st_len])]
        self.st[0] = array

        # 二维动态规划构造 Sparse Table
        # 状态转移方程：st[i][j] = min( st[i-1][j], st[i-1][j + 2^(i-1)] )
        for i in range(1, len(self.st)):
            j = 0
            while j + (1 << i) <= self.st_len:
                self.st[i][j] = min(self.st[i - 1][j], self.st[i - 1][j + (1 << (i - 1))])
                j += 1

    # 若更新数组值，则需重新建表
    # 时间复杂度 O(n log n)
    # 如果数组长度也变了，那么可以重新构造 SparseTableRMQ 类的对象
    def update(self, index, value):
        # 如果下标合法，且 value 值确实改变了，才进行 update，重建 Sparse Table
        if 0 <= index < len(self.st[0]) and self.st[0][index] != value:
            self.st[0][index] = value
            for i in range(1, len(self.st)):
                j = 0
                while j + (1 << i) <= self.st_len:
                    self.st[i][j] = min(self.st[i - 1][j], self.st[i - 1][j + (1 << (i - 1))])
                    j += 1

    # 查询 [left, right] 闭区间的最小值
    # 0 <= left <= right <= n-1
    # 时间复杂度 O(1)
    def query_minimum(self, left, right):
        if left > right:
            return self.inf

        if left < 0:
            left = 0
        if right >= self.st_len:
            right = self.st_len - 1

        # right - left + 1 为区间长度，对此长度求 log_2 对数、并下取整数
        log_2 = self.log_table[right - left + 1]

        # st[log_2][left] 表示从 index=left 出发、长度为 2^log_2 的区间中的最小值
        # right - (1 << log_2) + 1 表示将索引下标减小 2^log_2 - 1，
        # 这样的话，从此下标开始的 2^log_2 长度的区间的右端点即为 right，该区间的最小值可以直接查 ST 表得到
        # 上述两端区间完全覆盖了 query 区间，因此只需计算上述两区间最小值的较小值即为答案
        return min(self.st[log_2][left], self.st[log_2][right - (1 << log_2) + 1])

    def print_st(self):
        for i in range(len(self.st)):
            print(self.st[i])


def main():
    array = [5, 2, 4, 7, 6, 3, 1, 2]

    st = SparseTableRMQ(array)
    # st.print_st()

    start = time.process_time()
    ans = st.query_minimum(1, 6)
    end = time.process_time()
    print(ans)  # 1

    print(st.query_minimum(1, 5))    # 2
    print(st.query_minimum(-1, 16))  # 1
    print(st.query_minimum(4, 4))    # 6
    print(st.query_minimum(4, 3))    # inf

    st.update(3, 0)
    print(st.query_minimum(1, 5))  # 0
    print(st.query_minimum(-1, 16))  # 0
    print(st.query_minimum(4, 4))  # 6
    print(st.query_minimum(4, 3))  # inf

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
