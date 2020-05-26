#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/dynamic_programming
@File    : matrix-chain-order.py
@Author  : YuweiYin
@Date    : 2020-05-26
=================================================="""

import sys
import time

"""
矩阵链乘法 Matrix Chain Order

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 15
"""


# 矩阵结构体
class Matrix:
    # 构造时确保矩阵非空且行列合法
    def __init__(self, arr_2d):
        assert isinstance(arr_2d, list) and len(arr_2d) > 0 and len(arr_2d[0]) > 0
        self.matrix = arr_2d
        self.row_num = len(arr_2d)
        self.col_num = len(arr_2d[0])
        # 确保每一行的元素个数都等于列数
        for row in range(len(arr_2d)):
            assert isinstance(row, list) and len(row) == self.col_num


class MatrixChainOrder:
    def __init__(self, p_arr):
        assert isinstance(p_arr, list) and len(p_arr) > 1
        self.p_arr = p_arr       # p 数组给出各矩阵的规模
        self.optimal_paren = ''  # 最优括号化方案 (字符串)

    # 矩阵乘积运算 计算 A * B 的结果
    # 其中矩阵 A 的规模为 P*Q、矩阵 B 的规模为 Q*R
    # TODO 输入真实的矩阵序列，先以 matrix_chain_order 算法分析计算顺序，再按顺序调用本函数进行运算
    # 时间复杂度 \Theta(P*Q*R)
    # 空间复杂度 \Theta(P*R)
    @staticmethod
    def matrix_multiply(matrix_a, matrix_b):
        assert isinstance(matrix_a, Matrix) and isinstance(matrix_b, Matrix)
        # 先确保输入的两矩阵是相容的
        if matrix_a.col_num != matrix_b.row_num:
            print('matrix_multiply: incompatible dimensions')
            return None
        res_matrix = [[0 for j in range(matrix_b.col_num)] for i in range(matrix_a.row_num)]
        for i in range(matrix_a.row_num):
            for j in range(matrix_b.col_num):
                for k in range(matrix_a.col_num):
                    res_matrix[i][j] += matrix_a.matrix[i][k] * matrix_b.matrix[k][j]
        return res_matrix

    # 矩阵链乘最佳计算顺序
    # 返回：最佳收益(最优值)、最佳切割方案列表(最优解)
    # 如果返回最佳收益为 -1，则为异常
    def matrix_chain_order(self):
        assert isinstance(self.p_arr, list) and len(self.p_arr) > 1
        # return self._matrix_chain_order_1()  # 自顶向下递归实现 (DFS 暴力搜索) O(2^n)
        # return self._matrix_chain_order_2()  # 自顶向下递归实现 (带备忘录的动态规划) O(n^2)
        return self._matrix_chain_order_3()  # 自底向上循环实现 (动态规划) O(n^2)

    # TODO 自顶向下递归实现 (DFS 暴力搜索)
    # 如果 i = j 则 m[i, j] = 0
    # 如果 i < j 则 m[i, j] = min{m[i, k] + m[k+1, j] + p_{i-1} * p_k * pj}  \forall k \in [i, j)
    # 时间复杂度 O(2^n)
    def _matrix_chain_order_1(self):
        pass

    # TODO 自顶向下递归实现 (带备忘录的动态规划)
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def _matrix_chain_order_2(self):
        pass

    # 自底向上循环实现 (动态规划)
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def _matrix_chain_order_3(self):
        assert isinstance(self.p_arr, list) and len(self.p_arr) > 1
        # 矩阵数量为 p 数组长度减一
        matrix_num = len(self.p_arr) - 1
        # 备忘录表格 m[i, j] 表示计算矩阵 A_{i..j} 所需标量乘法次数的最小值
        # 因此，原问题的最优解（计算 A_{1..n}）所需的最低代价就是 m[1, n] 的值
        # 备忘录 s[i, j] 保存链乘 Ai...Aj 最优括号化方案的各个分割点位置 k
        # 即：使得 m[i, j] = m[i, k] + m[k+1, j] + p_{i-1} * p_k * pj 成立的 k 值
        inf = 0x3f3f3f3f  # 目标是求代价最小值，所以备忘录各个位置初始化为 inf
        m_table = [[inf for j in range(matrix_num)] for i in range(matrix_num)]
        s_table = [[inf for j in range(matrix_num)] for i in range(matrix_num)]
        # m_table 主对角线的值均置为 0
        for i in range(matrix_num):
            m_table[i][i] = 0
        # 对于每种 chain_len 链长(子问题)求最优解/值，自底向上分别计算
        for chain_len in range(2, matrix_num + 1):
            # i 为当前链的起始位置
            for i in range(matrix_num - chain_len + 1):
                # j 为当前链的终止位置
                j = i + chain_len - 1
                # 对于每个切分点 k 计算代价，i <= k < j
                for k in range(i, j):
                    # 计算代价时仅依赖于已经求出的 m[i, k] 和 m[k+1, j]
                    # 注意这里 i 从下标 0 开始，于是原公式里的 p_{i-1} * p_k * pj 需改为 p_i * p_{k+1} * p_{j+1}
                    cost = m_table[i][k] + m_table[k + 1][j] + self.p_arr[i] * self.p_arr[k + 1] * self.p_arr[j + 1]
                    if cost < m_table[i][j]:
                        m_table[i][j] = cost
                        s_table[i][j] = k
        # 返回备忘录 m 和 s
        return m_table, s_table

    # 根据 s_table 获取最优解的括号化方案 (字符串)
    def get_optimal_paren(self, s_table):
        self.optimal_paren = ''
        self._get_optimal_paren(s_table, 0, len(self.p_arr) - 2)
        return self.optimal_paren

    def _get_optimal_paren(self, s_table, lo, hi):
        if lo == hi:
            self.optimal_paren += 'A' + str(lo + 1)
        else:
            self.optimal_paren += '('
            self._get_optimal_paren(s_table, lo, s_table[lo][hi])
            self._get_optimal_paren(s_table, s_table[lo][hi] + 1, hi)
            self.optimal_paren += ')'


def main():
    # 这里仅为了确定计算的最优顺序，而不是为了计算矩阵乘积值
    # 所以链乘的矩阵序列是 相邻两两相容的，因此这里用 p 数组给出各矩阵的规模
    # 假设有 A_0..A_{n-1} 这 n 个矩阵，那么 A_i 矩阵的规模为 p[i] * p[i-1]
    # 因此若有 n 个矩阵，则 p 数组的长度就为 n+1
    p_arr = [30, 35, 15, 5, 10, 20, 25]

    mco = MatrixChainOrder(p_arr)

    start = time.process_time()
    m_table, s_table = mco.matrix_chain_order()
    end = time.process_time()

    print('\noptimal_paren:')
    print(mco.get_optimal_paren(s_table))  # ((A1(A2A3))((A4A5)A6))

    print('\nm_table:')
    for row in m_table:
        print(row)
    print('\ns_table:')
    for row in s_table:
        print(row)

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
