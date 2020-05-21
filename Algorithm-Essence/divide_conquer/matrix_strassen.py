#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/divide_conquer
@File    : matrix-strassen.py
@Author  : YuweiYin
@Date    : 2020-05-21
=================================================="""

import sys
import time

"""
矩阵乘法的 Strassen 算法

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 4
"""


class SquareMatrixMultiply:
    def __init__(self, matrix_a, matrix_b):
        # 默认 matrix_a 和 matrix_b 是同样大小的方阵。下面检查此性质 O(n) 时间
        assert isinstance(matrix_a, list) and len(matrix_a) > 0
        a_len = len(matrix_a)
        assert isinstance(matrix_b, list) and len(matrix_b) == a_len
        for i in range(a_len):
            assert isinstance(matrix_a[i], list) and len(matrix_a[i]) == a_len
            assert isinstance(matrix_b[i], list) and len(matrix_b[i]) == a_len

        self.matrix_a = matrix_a
        self.matrix_b = matrix_b

    # 矩阵乘法运算 (此处默认为方阵)
    # 返回乘积结果
    def square_matrix_multiply(self):
        # return self._naive_mm()
        # return self._divide_mm(self.matrix_a, self.matrix_b)
        return self._strassen_mm(self.matrix_a, self.matrix_b)

    # 朴素的矩阵乘积运算
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def _naive_mm(self):
        n = len(self.matrix_a)
        res_matrix = [[0 for i in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    res_matrix[i][j] += self.matrix_a[i][k] * self.matrix_b[k][j]
        return res_matrix

    # 普通的分治法
    # T(n) = 8T(n/2) + \Theta(n^2)
    # 时间复杂度 \Theta(n^3)
    def _divide_mm(self, matrix_a, matrix_b):
        n = len(matrix_a)
        res_matrix = [[0 for i in range(n)] for i in range(n)]
        if n == 1:
            res_matrix[0][0] = matrix_a[0][0] * matrix_b[0][0]
        else:
            # 矩阵拆分：从中间划分成四份
            a_11, a_12, a_21, a_22, b_11, b_12, b_21, b_22 = self._matrix_split(matrix_a, matrix_b)

            # 递归进行乘法后相加
            res_11 = self._matrix_addition(self._divide_mm(a_11, b_11), self._divide_mm(a_12, b_21))
            res_12 = self._matrix_addition(self._divide_mm(a_11, b_12), self._divide_mm(a_12, b_22))
            res_21 = self._matrix_addition(self._divide_mm(a_21, b_11), self._divide_mm(a_22, b_21))
            res_22 = self._matrix_addition(self._divide_mm(a_21, b_12), self._divide_mm(a_22, b_22))

            # 结果合并到 res_11 中
            res_11.extend(res_21)
            res_12.extend(res_22)
            assert len(res_11) == len(res_12)
            for i in range(len(res_11)):
                res_11[i].extend(res_12[i])
            res_matrix = res_11
        # 返回最终结果
        return res_matrix

    # 辅助函数：矩阵拆分
    # 从中间划分成四份
    # 时间复杂度 O(n)
    @staticmethod
    def _matrix_split(m_a, m_b):
        assert len(m_a) == len(m_b)
        mid = len(m_a) >> 1

        a_1 = m_a[:mid]  # 前半 mid 行
        a_2 = m_a[mid:]  # 后半 mid 行
        a_11 = [row[:mid] for row in a_1]
        a_12 = [row[mid:] for row in a_1]
        a_21 = [row[:mid] for row in a_2]
        a_22 = [row[mid:] for row in a_2]

        b_1 = m_b[:mid]  # 前半 mid 行
        b_2 = m_b[mid:]  # 后半 mid 行
        b_11 = [row[:mid] for row in b_1]
        b_12 = [row[mid:] for row in b_1]
        b_21 = [row[:mid] for row in b_2]
        b_22 = [row[mid:] for row in b_2]

        return a_11, a_12, a_21, a_22, b_11, b_12, b_21, b_22

    # 辅助函数：矩阵加法
    # 对应位置相加，需约束两矩阵形状相同
    # 时间复杂度 O(n^2)
    @staticmethod
    def _matrix_addition(m_a, m_b):
        assert len(m_a) == len(m_b)
        # 也可以直接把矩阵 m_b 的各值加到 m_a 中，不额外建立矩阵
        res_matrix = [[0 for j in range(len(m_a[i]))] for i in range(len(m_a))]
        for i in range(len(m_a)):
            assert len(m_a[i]) == len(m_b[i])
            for j in range(len(m_a[i])):
                res_matrix[i][j] = m_a[i][j] + m_b[i][j]
        return res_matrix

    # 辅助函数：矩阵减法
    # 对应位置相减，需约束两矩阵形状相同
    # 时间复杂度 O(n^2)
    @staticmethod
    def _matrix_subtraction(m_a, m_b):
        assert len(m_a) == len(m_b)
        # 也可以直接用矩阵 m_a 的各值减去 m_b 相应各值，不额外建立矩阵
        res_matrix = [[0 for j in range(len(m_a[i]))] for i in range(len(m_a))]
        for i in range(len(m_a)):
            assert len(m_a[i]) == len(m_b[i])
            for j in range(len(m_a[i])):
                res_matrix[i][j] = m_a[i][j] - m_b[i][j]
        return res_matrix

    # 矩阵乘法的 Strassen 算法
    # 这里假定待乘方阵的大小 n 是 2 的正整数次幂
    # 核心思想是：将普通分治法的 8 次乘法降为 7 次
    # T(n) = 7T(n/2) + \Theta(n^2)
    # 时间复杂度 \Theta(n^{log 7}) = O(n^2.81) = \Omega(n^2.80)
    def _strassen_mm(self, matrix_a, matrix_b):
        n = len(matrix_a)
        res_matrix = [[0 for i in range(n)] for i in range(n)]
        if n == 1:
            res_matrix[0][0] = matrix_a[0][0] * matrix_b[0][0]
        else:
            # 矩阵拆分：从中间划分成四份
            a_11, a_12, a_21, a_22, b_11, b_12, b_21, b_22 = self._matrix_split(matrix_a, matrix_b)

            # 计算前述 8 个子矩阵的和或差，得到 10 个新的矩阵 s1..s10
            s_1 = self._matrix_subtraction(b_12, b_22)
            s_2 = self._matrix_addition(a_11, a_12)
            s_3 = self._matrix_addition(a_21, a_22)
            s_4 = self._matrix_subtraction(b_21, b_11)
            s_5 = self._matrix_addition(a_11, a_22)
            s_6 = self._matrix_addition(b_11, b_22)
            s_7 = self._matrix_subtraction(a_12, a_22)
            s_8 = self._matrix_addition(b_21, b_22)
            s_9 = self._matrix_subtraction(a_11, a_21)
            s_10 = self._matrix_addition(b_11, b_12)

            # 利用前述所有子矩阵，进行 7 次递归的矩阵乘法，得到 p1..p7
            p_1 = self._strassen_mm(a_11, s_1)
            p_2 = self._strassen_mm(s_2, b_22)
            p_3 = self._strassen_mm(s_3, b_11)
            p_4 = self._strassen_mm(a_22, s_4)
            p_5 = self._strassen_mm(s_5, s_6)
            p_6 = self._strassen_mm(s_7, s_8)
            p_7 = self._strassen_mm(s_9, s_10)

            # 对 p1..p7 进行加减运算得到最终结果的四个部分
            # res_11 = p_5 + p_4 - p_2 + p_6
            # res_22 = p_5 + p_1 - p_3 - p_7
            res_11 = self._matrix_addition(self._matrix_subtraction(self._matrix_addition(p_5, p_4), p_2), p_6)
            res_12 = self._matrix_addition(p_1, p_2)
            res_21 = self._matrix_addition(p_3, p_4)
            res_22 = self._matrix_subtraction(self._matrix_subtraction(self._matrix_addition(p_5, p_1), p_3), p_7)

            # 结果合并到 res_11 中
            res_11.extend(res_21)
            res_12.extend(res_22)
            assert len(res_11) == len(res_12)
            for i in range(len(res_11)):
                res_11[i].extend(res_12[i])
            res_matrix = res_11
        # 返回最终结果
        return res_matrix


def main():
    matrix_a = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    matrix_b = [
        [1, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 2, 1, 2],
        [0, 3, 2, 1]
    ]

    smm = SquareMatrixMultiply(matrix_a, matrix_b)

    start = time.process_time()
    res_matrix = smm.square_matrix_multiply()
    end = time.process_time()

    # res: [[1, 20, 15, 16], [5, 44, 35, 40], [9, 68, 55, 64], [13, 92, 75, 88]]
    if isinstance(res_matrix, list) and len(res_matrix) > 0:
        for i in range(len(res_matrix)):
            print(res_matrix[i])
    else:
        print('矩阵相乘出错!')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
