#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/other-topics/matrix-operation
@File    : lup-decomposition.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
- 矩阵运算 Matrix Operation
    - 矩阵检查
        - 合法性检查
        - 加/减法相容性检查 (两矩阵形状/规模相同)
        - 矩阵乘法相容性检查
    - 矩阵转置
    - 矩阵乘法
        - 普通矩阵乘法
        - 分治的矩阵乘法
        - Strassen 算法
    - 矩阵分解
        - LUP 三角分解 (LUP Decomposition) 求解线性方程组
        - SVD 奇异值分解
    - 矩阵求逆
        - 用 LUP 分解方法求矩阵的逆
    - 对称正定矩阵和最小二乘逼近
        - 求超定线性方程组的最小二乘解

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 28
"""


class MatrixOperation:
    # 辅助函数：输出一个矩阵(二维列表)
    # 时间复杂度：O(n)
    @staticmethod
    def print_matrix(matrix):
        if not isinstance(matrix, list) or len(matrix) <= 0:
            print('输入的矩阵不合法，无法输出')
        else:
            for row in matrix:
                print(row)

    # 辅助函数：检查一个 n x n 方阵是否行列数合法
    # 时间复杂度：O(n)
    @staticmethod
    def check_square_matrix(matrix):
        if not isinstance(matrix, list) or len(matrix) <= 0:
            return False
        n_rows = len(matrix)
        for row in matrix:
            if not isinstance(row, list) or len(row) != n_rows:
                return False
        return True

    # 辅助函数：检查一个 m x n 普通矩阵是否行列数合法
    # 时间复杂度：O(m)
    @staticmethod
    def check_matrix(matrix):
        if not isinstance(matrix, list) or len(matrix) <= 0:
            return False
        if not isinstance(matrix[0], list) or len(matrix[0]) <= 0:
            return False
        n_cols = len(matrix[0])
        for row in matrix:
            if not isinstance(row, list) or len(row) != n_cols:
                return False
        return True

    # 辅助函数：检查两个矩阵的形状/规模是否相同，若相同，则对矩阵加法/减法相容
    # 假定两个矩阵的规模均为 m x n
    # 时间复杂度：O(m)
    @staticmethod
    def check_same_shape(m_a, m_b):
        if not isinstance(m_a, list) or len(m_a) <= 0:
            return False
        if not isinstance(m_a[0], list) or len(m_a[0]) <= 0:
            return False
        if not isinstance(m_b, list) or len(m_b) <= 0:
            return False
        if not isinstance(m_b[0], list) or len(m_b[0]) <= 0:
            return False
        a_rows = len(m_a)
        a_cols = len(m_a[0])
        b_rows = len(m_b)
        b_cols = len(m_b[0])
        if a_rows != b_rows or a_cols != b_cols:
            return False
        return True

    # 辅助函数：检查两个矩阵是否(对矩阵乘法)相容 (a 的列数等于 b 的行数)
    # 假定矩阵 m_a 的规模为 p x q、矩阵 m_b 的规模为 q x r
    # 时间复杂度：O(p + q)
    def check_multiply_compatibility(self, m_a, m_b):
        # 先检查两个矩阵是否各自合法
        if not self.check_matrix(m_a) or not self.check_matrix(m_b):
            return False
        a_cols = len(m_a[0])
        b_rows = len(m_b)
        if a_cols != b_rows:
            return False
        return True

    # 辅助函数：矩阵加法
    # 对应位置相加，需约束两矩阵形状相同
    # 时间复杂度 O(n^2)
    def matrix_addition(self, m_a, m_b):
        # 先检查两矩阵的形状/规模是否相同
        if self.check_same_shape(m_a, m_b):
            # 也可以直接把矩阵 m_b 的各值加到 m_a 中，不额外建立矩阵
            res_matrix = [[0 for _ in range(len(m_a[i]))] for i in range(len(m_a))]
            for i in range(len(m_a)):
                for j in range(len(m_a[i])):
                    res_matrix[i][j] = m_a[i][j] + m_b[i][j]
            return res_matrix
        else:
            print('输入的两矩阵形状/规模不同，无法进行矩阵加法')
            return None

    # 辅助函数：矩阵减法
    # 对应位置相减，需约束两矩阵形状相同
    # 时间复杂度 O(n^2)
    def matrix_subtraction(self, m_a, m_b):
        # 先检查两矩阵的形状/规模是否相同
        if self.check_same_shape(m_a, m_b):
            # 也可以直接用矩阵 m_b 的各值去减 m_a 的对应值，不额外建立矩阵
            res_matrix = [[0 for _ in range(len(m_a[i]))] for i in range(len(m_a))]
            for i in range(len(m_a)):
                for j in range(len(m_a[i])):
                    res_matrix[i][j] = m_a[i][j] - m_b[i][j]
            return res_matrix
        else:
            print('输入的两矩阵形状/规模不同，无法进行矩阵减法')
            return None

    # 辅助函数：矩阵转置
    # 时间复杂度 O(n^2)
    # 空间复杂度 O(n^2) 或 O(1)
    # 如果原址转置，覆盖原矩阵，则可以降低空间复杂度到 O(1)
    # 本实现中会创建一个新矩阵
    def matrix_transpose(self, matrix):
        # 先检查 matrix 是否为合法的矩阵
        if self.check_matrix(matrix):
            n_rows = len(matrix)
            n_cols = len(matrix[0])
            res_matrix = [[matrix[i][j] for i in range(n_rows)] for j in range(n_cols)]
            return res_matrix
        else:
            print('输入的对象不是矩阵，无法进行矩阵转置')
            return None

    # 朴素的矩阵乘积运算
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def naive_mm(self, matrix_a, matrix_b):
        # 先检查两矩阵是否对乘法相容
        if self.check_multiply_compatibility(matrix_a, matrix_b):
            n = len(matrix_a)
            res_matrix = [[0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        res_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]
            return res_matrix
        else:
            print('输入的矩阵对乘法不相容，无法进行矩阵乘法')
            return None

    # 针对方阵的普通的分治法
    # T(n) = 8T(n/2) + \Theta(n^2)
    # 时间复杂度 \Theta(n^3)
    def divide_mm(self, matrix_a, matrix_b):
        # 先检查两矩阵是否对乘法相容
        if self.check_multiply_compatibility(matrix_a, matrix_b):
            return self._divide_mm(matrix_a, matrix_b)
        else:
            print('输入的矩阵对乘法不相容，无法进行矩阵乘法')
            return None

    def _divide_mm(self, matrix_a, matrix_b):
        n = len(matrix_a)
        res_matrix = [[0 for _ in range(n)] for _ in range(n)]
        if n == 1:
            res_matrix[0][0] = matrix_a[0][0] * matrix_b[0][0]
        else:
            # 矩阵拆分：从中间划分成四份
            a_11, a_12, a_21, a_22, b_11, b_12, b_21, b_22 = self._matrix_split(matrix_a, matrix_b)

            # 递归进行乘法后相加
            res_11 = self.matrix_addition(self._divide_mm(a_11, b_11), self._divide_mm(a_12, b_21))
            res_12 = self.matrix_addition(self._divide_mm(a_11, b_12), self._divide_mm(a_12, b_22))
            res_21 = self.matrix_addition(self._divide_mm(a_21, b_11), self._divide_mm(a_22, b_21))
            res_22 = self.matrix_addition(self._divide_mm(a_21, b_12), self._divide_mm(a_22, b_22))

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

    # 矩阵乘法的 Strassen 算法
    # 这里假定待乘方阵的大小 n 是 2 的正整数次幂
    # 核心思想是：将普通分治法的 8 次乘法降为 7 次
    # T(n) = 7T(n/2) + \Theta(n^2)
    # 时间复杂度 \Theta(n^{log 7}) = O(n^2.81) = \Omega(n^2.80)
    def strassen_mm(self, matrix_a, matrix_b):
        # 先检查两矩阵是否对乘法相容
        if self.check_multiply_compatibility(matrix_a, matrix_b):
            return self._strassen_mm(matrix_a, matrix_b)
        else:
            print('输入的矩阵对乘法不相容，无法进行矩阵乘法')
            return None

    def _strassen_mm(self, matrix_a, matrix_b):
        n = len(matrix_a)
        res_matrix = [[0 for _ in range(n)] for _ in range(n)]
        if n == 1:
            res_matrix[0][0] = matrix_a[0][0] * matrix_b[0][0]
        else:
            # 矩阵拆分：从中间划分成四份
            a_11, a_12, a_21, a_22, b_11, b_12, b_21, b_22 = self._matrix_split(matrix_a, matrix_b)

            # 计算前述 8 个子矩阵的和或差，得到 10 个新的矩阵 s1..s10
            s_1 = self.matrix_subtraction(b_12, b_22)
            s_2 = self.matrix_addition(a_11, a_12)
            s_3 = self.matrix_addition(a_21, a_22)
            s_4 = self.matrix_subtraction(b_21, b_11)
            s_5 = self.matrix_addition(a_11, a_22)
            s_6 = self.matrix_addition(b_11, b_22)
            s_7 = self.matrix_subtraction(a_12, a_22)
            s_8 = self.matrix_addition(b_21, b_22)
            s_9 = self.matrix_subtraction(a_11, a_21)
            s_10 = self.matrix_addition(b_11, b_12)

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
            res_11 = self.matrix_addition(self.matrix_subtraction(
                self.matrix_addition(p_5, p_4), p_2), p_6)
            res_12 = self.matrix_addition(p_1, p_2)
            res_21 = self.matrix_addition(p_3, p_4)
            res_22 = self.matrix_subtraction(self.matrix_subtraction(
                self.matrix_addition(p_5, p_1), p_3), p_7)

            # 结果合并到 res_11 中
            res_11.extend(res_21)
            res_12.extend(res_22)
            assert len(res_11) == len(res_12)
            for i in range(len(res_11)):
                res_11[i].extend(res_12[i])
            res_matrix = res_11
        # 返回最终结果
        return res_matrix

    # 用 LUP 分解的结果求解线性方程组 Ax = b
    # LUP 分解：P·A = L·U
    # L 是单位下三角矩阵、U 是上三角矩阵，P 是置换矩阵 (用一位向量 p 来表达)
    # 时间复杂度：\Theta(n^2)
    # 空间复杂度：\Theta(n)
    def lup_solve(self, lower, upper, permutation, vector_b):
        # 0. 检查 L 和 U 矩阵是相同形状 n x n 的方阵，且置换"矩阵" p 的长度等于 n
        if not self.check_same_shape(lower, upper):
            print('lup_solve: Error: L 与 U 的形状不同')
            return None
        n = len(lower)
        if len(lower[0]) != n or len(upper) != n or len(upper[0]) != n or \
                len(permutation) != n or len(vector_b) != n:
            print('lup_solve: Error: L 与 U 不为方阵，或者 p、b 输入不合法')
            return None

        # 1. 创建向量 x 和向量 y
        vector_x = [0 for _ in range(n)]
        vector_y = [0 for _ in range(n)]

        # 2. 通过"正向替换"求出 y 的解
        for i in range(n):
            sum_ly = 0
            for j in range(i):
                sum_ly += lower[i][j] * vector_y[j]
            vector_y[i] = vector_b[permutation[i]] - sum_ly

        # 3. 通过"反向替换"求出 x 的解
        for i in reversed(range(n)):
            sum_ux = 0
            for j in range(i + 1, n):
                sum_ux += upper[i][j] * vector_x[j]
            vector_x[i] = (vector_y[i] - sum_ux) / upper[i][i]

        # 4. 返回计算出的解向量
        return vector_x

    # 对方阵 A 进行 LU 分解
    # 限制条件：每次循环时，待分解矩阵的左上角元素不能是 0，否则有除 0 异常；
    # 另外，如果此左上角元素太接近 0，那么会造成比较严重的数值稳定性问题。
    # 如果 A 是对称正定矩阵，那么可以不用担心上述限制条件。
    # 而 LUP 分解针对上述限制条件进行了修正，可适用于任何非奇异矩阵 A 的分解
    # 时间复杂度：\Theta(n^3)
    # 空间复杂度：\Theta(n^2) 或者 O(1)
    # 如果直接把 L 和 U 的元素值(覆盖修改)存储于方阵 A 中，则可以减少空间复杂度至 O(1)
    def lu_decomposition(self, matrix_a):
        # 0. 检查 A 是方阵
        if not self.check_square_matrix(matrix_a):
            print('lu_decomposition: Error: 矩阵 A 不是方阵')
            return None, None

        # 1. 获取矩阵规模
        n = len(matrix_a)

        # 2. 初始化单位下三角矩阵 L 和上三角矩阵 U
        lower = [[0 for _ in range(n)] for _ in range(n)]
        upper = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            lower[i][i] = 1

        # 3. 在外循环中，对不同规模的矩阵进行 LU 分解
        for k in range(n):
            # 3.1. 选取主元为 U[k][k] = A[k][k]
            upper[k][k] = matrix_a[k][k]
            # 除 0 检测
            if upper[k][k] == 0:
                print('lu_decomposition: Error: 主元 upper[k][k] 为 0，会有除 0 异常')
                return None, None
            # 除很接近于 0 的数检测
            if abs(upper[k][k]) < 1e-10:
                print('lu_decomposition: Warning: 主元 upper[k][k] < 1e-10，会影响数值稳定性')

            # 3.2. 在此内循环 (当 k == n - 1 时，内循环不执行) 中，采用向量 v 和 w^{T} 对 L 和 U 进行更新
            for i in range(k + 1, n):
                # 把 v[i] 除以主元 U[k][k] 的结果存放在 L[i][k] 中 (这里除以主元，后面就不用除了)
                lower[i][k] = matrix_a[i][k] / upper[k][k]
                # 把 w[i] 存放在 U[k][i] 中
                upper[k][i] = matrix_a[k][i]

            # 3.3. 在此内循环中，计算舒尔补中的元素，并把结果存放在 A[i][j] 中
            for i in range(k + 1, n):
                for j in range(k + 1, n):
                    matrix_a[i][j] -= lower[i][k] * upper[k][j]

        # 4. 最终返回矩阵 L 和 U
        return lower, upper

    # 对方阵 A 进行 LUP 分解 (可适用于任何非奇异矩阵 A 的分解)
    # 时间复杂度：\Theta(n^3)
    # 空间复杂度：\Theta(n^2) 或者 O(1)
    # 这里直接把 L 和 U 的元素值(覆盖修改)存储于方阵 A 中，减少空间复杂度至 O(1)
    # 当然，如果不希望改变原矩阵 A，可以在算法一开始重新开辟一个二维数组，并赋值为 A 即可。
    def lup_decomposition(self, matrix_a):
        # 0. 检查 A 是方阵
        if not self.check_square_matrix(matrix_a):
            print('lu_decomposition: Error: 矩阵 A 不是方阵')
            return None, None

        # 1. 获取矩阵规模
        n = len(matrix_a)

        # 2. 初始化置换矩阵 P 作为一个长度为 n 的数组 p
        # 其中 p[i] == j 表示置换矩阵 P 的元素 P[i][j] == 1
        permutation = [0 for _ in range(n)]
        for i in range(n):
            permutation[i] = i

        # 3. 在外循环中，对不同规模的矩阵进行 LUP 分解
        for k in range(n):
            # 3.1. 选取主元，利用置换矩阵 P 实现了在矩阵 A 中使用“合适的主元”来计算 L 和 U
            pivot = 0
            _k = k
            for i in range(k, n):
                # 在当前列中寻找最大的主元 pivot
                if abs(matrix_a[i][k]) > pivot:
                    pivot = abs(matrix_a[i][k])
                    _k = i  # _k 作为选取的主元的下标，之后会记录在置换矩阵 P 中
            # 除 0 检测
            if pivot == 0:
                print('lup_decomposition: Error: 输入矩阵为奇异矩阵，无法进行 LUP 分解')
                return None, None
            # 除很接近于 0 的数检测
            if abs(pivot) < 1e-10:
                print('lup_decomposition: Warning: 主元 pivot < 1e-10，会影响数值稳定性')

            # 3.2. 如果选取的主元不是首个元素，则维护置换矩阵 P，并把置换操作应用在矩阵 A 上
            if k != _k:
                # 维护置换矩阵 P
                temp = permutation[k]
                permutation[k] = permutation[_k]
                permutation[_k] = temp
                # 把置换操作应用在矩阵 A 上
                for i in range(n):
                    temp = matrix_a[k][i]
                    matrix_a[k][i] = matrix_a[_k][i]
                    matrix_a[_k][i] = temp

            # 3.3. 在此内循环中，计算舒尔补中的元素，并把结果存放在 A[i][j] 中
            for i in range(k + 1, n):
                matrix_a[i][k] /= matrix_a[k][k]
                for j in range(k + 1, n):
                    matrix_a[i][j] -= matrix_a[i][k] * matrix_a[k][j]

        # 4. 最终返回矩阵 A 和置换矩阵(向量) P
        # 当本函数结束时，矩阵 A 中同时保存了 L 和 U 的元素：
        # - 如果下标 i >  j，则 A[i][j] == L[i][j]
        # - 如果下标 i <= j，则 A[i][j] == U[i][j]
        return matrix_a, permutation

    # 用 LUP 分解方法 求非奇异方阵 A 的逆矩阵
    # 方法：求 A·X=In，In 为单位矩阵，而 X 即为 A 的逆矩阵
    # 用 LUP 分解求 n 个线性方程组 A·Xi = ei
    # 其中 Xi 是方阵 X 的第 i 列列向量，ei 为单位矩阵 In 的第 i 列列向量
    # 时间复杂度：\Theta(n^3)
    # 空间复杂度：\Theta(n^2)
    def lup_reverse(self, matrix_a):
        # 0. 检查 A 是方阵
        if not self.check_square_matrix(matrix_a):
            print('lup_reverse: Error: 矩阵 A 不是方阵')
            return None

        # 1. LUP 分解
        res_lu, permutation = self.lup_decomposition(matrix_a)

        # 2. 根据 LUP 分解的 res_lu 获得 L 矩阵和 U 矩阵
        # - 如果下标 i >  j，则 A[i][j] == L[i][j]
        # - 如果下标 i <= j，则 A[i][j] == U[i][j]
        n = len(res_lu)
        lower = [[0 for _ in range(n)] for _ in range(n)]
        upper = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            lower[i][i] = 1
            for j in range(n):
                if i > j:
                    lower[i][j] = res_lu[i][j]
                else:
                    upper[i][j] = res_lu[i][j]

        # 用 LUP 分解求 n 个线性方程组 A·Xi = ei
        reverse_a = []
        for i in range(n):
            vector_b = [1 if i == j else 0 for j in range(n)]
            res_x = self.lup_solve(lower, upper, permutation, vector_b)
            # 把 res_x 加入二维列表 reverse_a 中 (作为行向量，最后需对 reverse_a 进行转置)
            reverse_a.append(res_x)

        # 对 reverse_a 进行转置后返回结果
        return self.matrix_transpose(reverse_a)


def main():
    mo = MatrixOperation()

    # 矩阵乘法
    print('\n矩阵乘法:')
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
    start = time.process_time()
    res_matrix = mo.strassen_mm(matrix_a, matrix_b)
    end = time.process_time()

    # res_matrix:
    # [1, 20, 15, 16]
    # [5, 44, 35, 40]
    # [9, 68, 55, 64]
    # [13, 92, 75, 88]
    if isinstance(res_matrix, list) and len(res_matrix) > 0:
        print('\nres_matrix:')
        mo.print_matrix(res_matrix)
    else:
        print('矩阵相乘出错!')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # LU 分解
    print('\nLU 分解:')
    # 用于 LU 分解的矩阵，同《CLRS》Chapter 28 中的图 28-1
    matrix_lu = [
        [2, 3, 1, 5],
        [6, 13, 5, 19],
        [2, 19, 10, 23],
        [4, 10, 11, 31]
    ]
    start = time.process_time()
    lower, upper = mo.lu_decomposition(matrix_lu)
    end = time.process_time()

    # lower:
    # [1, 0, 0, 0]
    # [3, 1, 0, 0]
    # [1, 4, 1, 0]
    # [2, 1, 7, 1]
    # upper:
    # [2, 3, 1, 5]
    # [0, 4, 2, 4]
    # [0, 0, 1, 2]
    # [0, 0, 0, 3]
    if isinstance(lower, list) and len(lower) > 0 and \
            isinstance(upper, list) and len(upper) > 0:
        print('\nlower:')
        mo.print_matrix(lower)
        print('\nupper:')
        mo.print_matrix(upper)
    else:
        print('矩阵相乘出错!')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # LUP 分解
    print('\nLUP 分解:')
    # 用于 LUP 分解的矩阵，同《CLRS》Chapter 28 中的图 28-2
    matrix_lup = [
        [2, 0, 2, 0.6],
        [3, 3, 4, -2],
        [5, 5, 4, 2],
        [-1, -2, 3.4, -1]
    ]
    start = time.process_time()
    res_lu, permutation = mo.lup_decomposition(matrix_lup)
    end = time.process_time()

    # res_lu:
    # [5, 5, 4, 2]
    # [0.4, -2, 0.4, -0.2]
    # [-0.2, 0.5, 4, -0.5]
    # [0.6, 0, 0.4, -3]
    # permutation:
    # [2, 0, 3, 1]
    if isinstance(res_lu, list) and len(res_lu) > 0 and \
            isinstance(permutation, list) and len(permutation) > 0:
        print('\nres_lu:')
        mo.print_matrix(res_lu)
        print('\npermutation:')
        print(permutation)
    else:
        print('矩阵相乘出错!')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 用 LUP 分解方法 求解线性方程组 Ax=b
    print('\n用 LUP 分解方法 求解线性方程组:')
    # 用于 LUP 分解的矩阵，同《CLRS》Chapter 28 第一小节中的例子
    matrix_lup_solve = [
        [1, 2, 0],
        [3, 4, 4],
        [5, 6, 3]
    ]
    vector_b = [3, 7, 8]
    # LUP 分解
    res_lu, permutation = mo.lup_decomposition(matrix_lup_solve)
    # 根据 LUP 分解的 res_lu 获得 L 矩阵和 U 矩阵
    # - 如果下标 i >  j，则 A[i][j] == L[i][j]
    # - 如果下标 i <= j，则 A[i][j] == U[i][j]
    n = len(res_lu)
    lower = [[0 for _ in range(n)] for _ in range(n)]
    upper = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        lower[i][i] = 1
        for j in range(n):
            if i > j:
                lower[i][j] = res_lu[i][j]
            else:
                upper[i][j] = res_lu[i][j]
    # 输出展示 L、U 和 P 矩阵
    # lower:
    # [1, 0, 0]
    # [0.2, 1, 0]
    # [0.6, 0.5, 1]
    # upper:
    # [5, 6, 3]
    # [0, 0.8, -0.6]
    # [0, 0, 2.5]
    # permutation:
    # [2, 0, 1]
    print('\nlower:')
    mo.print_matrix(lower)
    print('\nupper:')
    mo.print_matrix(upper)
    print('\npermutation:')
    print(permutation)
    # 使用 L、U、p 和 b 解线性方程组
    start = time.process_time()
    res_x = mo.lup_solve(lower, upper, permutation, vector_b)
    end = time.process_time()

    # 输出解向量
    # res_x:
    # [-1.4, 2.2, 0.6]
    if isinstance(res_x, list) and len(res_x) > 0:
        print('\nres_x:')
        print(res_x)
    else:
        print('解线性方程组出错!')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 用 LUP 分解方法 求非奇异方阵 A 的逆矩阵
    # 方法：求 A·X=In，In 为单位矩阵，而 X 即为 A 的逆矩阵
    # 用 LUP 分解求 n 个线性方程组 A·Xi = ei
    # 其中 Xi 是方阵 X 的第 i 列列向量，ei 为单位矩阵 In 的第 i 列列向量
    print('\n用 LUP 分解方法 求非奇异方阵 A 的逆矩阵:')
    matrix_lup_reverse = [
        [1, 2, 0],
        [3, 4, 4],
        [5, 6, 3]
    ]

    # 这里需要保留原矩阵，所以用副本去执行求逆运算 (本实现中的 LUP 分解过程会覆盖输入的矩阵 A)
    matrix_lup_reverse_copy = [
        [matrix_lup_reverse[i][j] for j in range(len(matrix_lup_reverse))] for i in range(len(matrix_lup_reverse))
    ]
    start = time.process_time()
    reverse_matrix = mo.lup_reverse(matrix_lup_reverse_copy)
    end = time.process_time()

    # 输出结果
    # reverse_matrix:
    # [-1.2, -0.6, 0.8]
    # [1.1, 0.3, -0.4]
    # [-0.2, 0.4, -0.2]
    if isinstance(reverse_matrix, list) and len(reverse_matrix) > 0:
        print('\nreverse_matrix:')
        mo.print_matrix(reverse_matrix)
    else:
        print('解线性方程组出错!')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 将求逆后的矩阵与原矩阵进行左乘/右乘，确认结果为 In 单位矩阵
    print('\n逆矩阵右乘以原矩阵:')
    mm_res_matrix = mo.naive_mm(matrix_lup_reverse, reverse_matrix)
    mo.print_matrix(mm_res_matrix)

    print('\n逆矩阵左乘以原矩阵:')
    mm_res_matrix = mo.naive_mm(reverse_matrix, matrix_lup_reverse)
    mo.print_matrix(mm_res_matrix)


if __name__ == "__main__":
    sys.exit(main())
