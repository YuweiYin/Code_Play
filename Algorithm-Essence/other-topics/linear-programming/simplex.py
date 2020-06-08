#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/other-topics/linear-programming
@File    : simplex.py
@Author  : YuweiYin
@Date    : 2020-06-06
=================================================="""

import sys
import time

"""
- 线性规划 Linear Programming
    - 单纯形算法 Simplex Algorithm

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 29
"""


class LinearProgramming:
    def __init__(self):
        self.inf = 0x3f3f3f3f

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

    # 主元过程
    # 用非基本变量集合 N (non_basic_set) 中下标为 index_e 的元素 x_e 作为替入变量
    # 去替换 基本变量集合 B (basic_set) 中下标为 index_l 的元素 x_l
    # 并修改整个约束条件 Ax <= b (涉及到 matrix_a 和 vector_b) 以及目标函数的系数向量 vector_c
    # 目标函数的(当前)最优值为标量值 scalar_v
    def pivot(self, non_basic_set, basic_set, matrix_a, vector_b, vector_c, scalar_v, index_l, index_e):
        # 检查输入的合法性
        assert isinstance(non_basic_set, set) and isinstance(basic_set, set)
        assert isinstance(vector_b, list) and isinstance(vector_c, list)
        assert len(vector_b) > 0 and len(vector_c) > 0
        assert index_e in non_basic_set and index_l in basic_set
        if not self.check_matrix(matrix_a):
            print('pivot: 输入的约束条件系数矩阵 A 不合法!')
            return None

        # 1. 创建新系数矩阵 A' (matrix_a_hat)
        #    并通过重写 x_l 在左边的等式将 x_e 置于等式左边，来计算 x_e 的新等式中的系数
        m = len(matrix_a)  # rows
        n = len(matrix_a[0])  # cols
        a_le = matrix_a[index_l][index_e]
        if a_le == 0:
            print('pivot: a_le == 0 会出现除 0 错误')
            return None
        matrix_a_hat = [[0 for _ in range(n)] for _ in range(m)]
        vector_b_hat = [0 for _ in range(len(vector_b))]
        vector_b_hat[index_e] = vector_b[index_l] / a_le
        # 从 N 中删除 e、从 B 中删除 l
        non_basic_set.discard(index_e)
        basic_set.discard(index_l)
        # 重算系数，存储于 matrix_a_hat 中
        for j in non_basic_set:
            matrix_a_hat[index_e][j] = matrix_a[index_l][j] / a_le
        matrix_a_hat[index_e][index_l] = 1 / a_le

        # 2. 通过将每个 x_e 替换为这个新等式的右边 来更新剩下的等式
        for i in basic_set:
            vector_b_hat[i] = vector_b[i] - matrix_a[i][index_e] * vector_b_hat[index_e]
            for j in non_basic_set:
                matrix_a_hat[i][j] = matrix_a[i][j] - matrix_a[i][index_e] * matrix_a_hat[index_e][j]
            matrix_a_hat[i][index_l] = - matrix_a[i][index_e] * matrix_a_hat[index_e][index_l]

        # 3. 对目标函数进行前述同样地替换
        scalar_v_hat = scalar_v + vector_c[index_e] * vector_b_hat[index_e]
        vector_c_hat = [0 for _ in range(len(vector_c))]
        for j in non_basic_set:
            vector_c_hat[j] = vector_c[j] - vector_c[index_e] * matrix_a_hat[index_e][j]
        vector_c_hat[index_l] = - vector_c[index_e] * matrix_a_hat[index_e][index_l]

        # 4. 更新非基本变量集合 N 和基本变量集合 B
        non_basic_set.add(index_l)
        basic_set.add(index_e)

        # 5. 最后返回新的松弛型
        return non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat

    # 初始化单纯形算法
    # 输入线性规划标准型，返回其松弛型
    # 如果初始线性规划不可行，则报告之
    def initialize_simplex(self, matrix_a, vector_b, vector_c):
        # 检查输入的合法性
        assert isinstance(vector_b, list) and isinstance(vector_c, list)
        assert len(vector_b) > 0 and len(vector_c) > 0
        if not self.check_matrix(matrix_a):
            print('initialize_simplex: 输入的约束条件系数矩阵 A 不合法!')
            return None

        # 1. 在给定 N 和 B，对于所有 i \in B 有 x'_i = b_i，以及对于所有 j \in N 有 x'_j = 0 的条件下
        #    隐含地测试 L 的初始松弛型的基本解
        min_index = 0
        min_b = vector_b[0]
        for index, b in enumerate(vector_b):
            if b < min_b:
                min_b = b
                min_index = index

        # 2. 如果这个基本解是可行的，即对所有的 i \in N \cup B 有 x'_j >= 0，则直接返回这个松弛型
        m = len(matrix_a)  # rows
        n = len(matrix_a[0])  # cols
        if min_b >= 0:
            # 行/列数均增加 m，因为多了 m 个基本变量(松弛变量)
            # 设置松弛型的系数矩阵 A
            matrix_a_hat = [[0 for _ in range(n + m)] for _ in range(m << 1)]
            for i in range(m):
                for j in range(n):
                    matrix_a_hat[i + m][j] = matrix_a[i][j]
            # 设置松弛型的常数向量 b
            vector_b_hat = [0 for _ in range(m << 1)]
            for i in range(m):
                vector_b_hat[i + m] = vector_b[i]
            # 设置松弛型的目标函数系数向量 c
            vector_c_hat = [0 for _ in range(n + m)]
            for i in range(m):
                vector_c_hat[i] = vector_c[i]
            return set(range(n)), set(range(n, n + m)), matrix_a_hat, vector_b_hat, vector_c_hat, 0

        # 3. 否则，构造辅助线性规划 L_{aux}
        #    因为 L 的初始基本解是不可行的，所以 L_{aux} 的松弛型的初始基本解也一定不可行
        #    为了找到一个基本可行解，将执行一个主元 (pivot) 操作
        # 设置松弛型的系数矩阵 A，除了松弛型本应增加的 m 个基本变量外，还额外增加 x_0 非基本变量
        matrix_a_aux = [[0 for _ in range(n + m + 1)] for _ in range((m << 1) + 1)]
        for i in range(1, m + 1):
            matrix_a_aux[i + m][0] = -1  # 系数矩阵 A 中，原本的每个约束均增加 - x_0 项
            for j in range(n):
                matrix_a_aux[i + m][j + 1] = matrix_a[i - 1][j]
        # 设置松弛型的常数向量 b，其中 x_0 变量被加在首部
        vector_b_aux = [0 for _ in range((m << 1) + 1)]
        for i in range(1, m + 1):
            vector_b_aux[i + m] = vector_b[i - 1]
        # 设置松弛型的目标函数系数向量 c，此时目标函数为 z = - x_0
        vector_c_aux = [0 for _ in range(n + m + 1)]
        vector_c_aux[0] = -1
        # 设置非基本变量集合 N、基本变量集合 B 和初始最优值 v
        non_basic_set = set(range(n + 1))  # n + 1 个非基本变量，包括 x_0 变量
        basic_set = set(range(n + 1, n + 1 + m))  # m 个基本变量
        scalar_v = 0

        # 4. 选择 l = n + k + 1 作为基本变量的下标，该基本变量将是下面一个主元操作的替出变量
        #    因为基本变量是 `x_{n+1}, x_{n+2}, ..., x_{n+m}`，替出变量 `x_l` 将是负值最大的变量
        index_l = n + min_index + 1  # 这里 min_index 就是算法描述里的 k

        # 5. 执行对 PIVOT 的调用，以 x_0 为替入变量，x_l 为替出变量。由此 `PIVOT` 的调用产生的基本解是可行的
        non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat = self.pivot(
            non_basic_set, basic_set, matrix_a_aux, vector_b_aux, vector_c_aux, scalar_v, index_l, 0
        )

        # 6. 现在有了一个基本解可行的松弛型，可以重复调用 PIVOT 来完全求解出辅助线性规划
        #    此 while 循环同单纯形算法的主体部分
        m = len(matrix_a_hat)  # rows
        n = len(matrix_a_hat[0])  # cols
        delta = [0 for _ in range(m)]
        loop_flag = True  # 继续循环标志
        while loop_flag:
            # 2.1. 如果目标函数中所有系数 c_j 都是负值，那么 while 循环将终止
            loop_flag = False
            index_e = 0
            for index, c in enumerate(vector_c_hat):
                if c > 0:
                    # 在非基本变量集合 N 中选择一个变量 x_e 作为替出变量，其系数 c_e 在目标函数中为正值
                    index_e = index
                    loop_flag = True
                    break
            if not loop_flag:
                break

            # 2.2. 检查每个约束，然后挑选出一个约束：此约束能够最严格地限制 x_e 值增加的幅度，而又不违反任何非负约束
            # 与此约束相关联的基本变量是 x_l，它会作为替入变量
            index_l = 0
            delta_min = self.inf
            for i in basic_set:
                a_ie = matrix_a_hat[i][index_e]
                if a_ie > 0:
                    delta[i] = vector_b_hat[i] / a_ie
                    if delta[i] < delta_min:
                        delta_min = delta[i]
                        index_l = i
                else:
                    delta[i] = self.inf

            # 2.3. 如果没有约束能够限制替入变量所增加的幅度，那么算法返回“无界”
            if delta_min == self.inf:
                print('initialize_simplex: 无界! 没有约束能够限制替入变量所增加的幅度')
                return None
            # 2.4. 否则，调用 `PIVOT` 过程来交换替出变量与替入变量的角色
            else:
                non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat = self.pivot(
                    non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat, index_l, index_e
                )

        # 7. 获得辅助线性规划的最终解
        vector_x_bar = [0 for _ in range(n)]
        for i in range(n):
            if i in basic_set:
                vector_x_bar[i] = vector_b_hat[i]
            else:
                vector_x_bar[i] = 0

        # 8. 测试是否找到了一个 x_0 项为 0 的 L_{aux} 的最优解，如果找到了，进入分支：
        if vector_x_bar[0] == 0:
            # 9.1. 可以生成一个 L 的松弛型，其基本解是可行的。
            #      为了做到这一点，首先处理退化情形，其中 x_0 可能仍然是基本变量，其值为 x'_0 = 0
            if 0 in basic_set:
                # 先挑选 index_e，采用任何满足 a_0e != 0 的 e \in N 作为替入变量
                index_e = -1
                for index, a in enumerate(matrix_a_hat[0]):
                    if a != 0:
                        index_e = index
                        break
                if index_e < 0:
                    print('initialize_simplex: 挑选 index_e 出错')
                    return None

                # 然后执行 PIVOT 操作，把 x_0 从基本变量集合中移除。
                # 退化转动没有改变任何变量的值，新的基本解仍然可行
                non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat = self.pivot(
                    non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat, 0, index_e
                )

            # 9.3. 删除所有 x_0 项，并且恢复 L 的原始目标函数，使其只包含非基本变量
            #      原始目标函数 (系数向量为 vector_c) 可能包含了基本变量和非基本变量
            reduced_vector_c = [0 for _ in range(len(vector_c_hat))]
            for i, c in enumerate(vector_c):
                if c != 0:
                    index = i + 1
                    if index in basic_set:
                        # 若当前值是基本元素，则查看 A 矩阵，将相应的系数向量(逐元素地)加给 c 向量
                        for j, a in enumerate(matrix_a_hat[index]):
                            reduced_vector_c[j] -= c * a  # 由于 A 矩阵的系数值是实际值的相反数，所以这里是减法
                        # 另外，scalar_v_hat 要加上该行的常数项 b
                        scalar_v_hat += c * vector_b_hat[index]
                    else:
                        # 若当前值是非基本元素，则直接加给 c 向量
                        reduced_vector_c[index] = c
            res_vector_c = reduced_vector_c[1:]
            assert 0 in non_basic_set
            # 非基本变量集合删去 x_0 (即删去 x_0 的下标 0)
            non_basic_set.discard(0)
            # 基本变量和非基本变量集合 中的元素(下标) 均减一
            res_non_basic_set = set()
            res_basic_set = set()
            for index in non_basic_set:
                res_non_basic_set.add(index - 1)
            for index in basic_set:
                res_basic_set.add(index - 1)
            # 从 A, b 中删除 x_0
            res_matrix_a = [[matrix_a_hat[i + 1][j + 1] for j in range(n - 1)] for i in range(m - 1)]
            res_vector_b = [vector_b_hat[i + 1] for i in range(len(vector_b_hat) - 1)]

            # 9.4. 返回前述修改后的松弛型
            return res_non_basic_set, res_basic_set, res_matrix_a, res_vector_b, res_vector_c, scalar_v_hat
        else:
            # 10. 否则，初始线性规划 L 是不可行的
            print('initialize_simplex: 初始线性规划是不可行的')
            return None

    # 输入线性规划标准型，用单纯形算法求解
    def simplex(self, matrix_a, vector_b, vector_c):
        # 检查输入的合法性
        assert isinstance(vector_b, list) and isinstance(vector_c, list)
        assert len(vector_b) > 0 and len(vector_c) > 0
        if not self.check_matrix(matrix_a):
            print('simplex: 输入的约束条件系数矩阵 A 不合法!')
            return None

        # 1. 调用过程 INITIALIZE_SIMPLEX(A, b, c)
        #    要么确定这个线性规划是不可行的，要么返回一个初始基本解可行的松弛型
        non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat = self.initialize_simplex(
            matrix_a, vector_b, vector_c
        )
        # scalar_v_hat = 0
        m = len(matrix_a_hat)  # rows
        n = len(matrix_a_hat[0])  # cols
        delta = [0 for _ in range(m)]

        # 2. 此 while 循环是单纯形算法的主体部分
        loop_flag = True  # 继续循环标志
        while loop_flag:
            # 2.1. 如果目标函数中所有系数 c_j 都是负值，那么 while 循环将终止
            loop_flag = False
            index_e = 0
            for index, c in enumerate(vector_c_hat):
                if c > 0:
                    # 在非基本变量集合 N 中选择一个变量 x_e 作为替出变量，其系数 c_e 在目标函数中为正值
                    index_e = index
                    loop_flag = True
                    break
            if not loop_flag:
                break

            # 2.2. 检查每个约束，然后挑选出一个约束：此约束能够最严格地限制 x_e 值增加的幅度，而又不违反任何非负约束
            #      与此约束相关联的基本变量是 x_l，它会作为替入变量
            index_l = 0
            delta_min = self.inf
            for i in basic_set:
                a_ie = matrix_a_hat[i][index_e]
                if a_ie > 0:
                    delta[i] = vector_b_hat[i] / a_ie
                    if delta[i] < delta_min:
                        delta_min = delta[i]
                        index_l = i
                else:
                    delta[i] = self.inf

            # 2.3. 如果没有约束能够限制替入变量所增加的幅度，那么算法返回“无界”
            if delta_min == self.inf:
                print('simplex: 无界! 没有约束能够限制替入变量所增加的幅度')
                return None
            # 2.4. 否则，调用 `PIVOT` 过程来交换替出变量与替入变量的角色
            else:
                non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat = self.pivot(
                    non_basic_set, basic_set, matrix_a_hat, vector_b_hat, vector_c_hat, scalar_v_hat, index_l, index_e
                )

        # 3. 通过把所有的非基本变量设为 0 以及把每个基本变量 x'_i 设为 b_i
        #    来计算初始线性规划的一个解向量 (x'_1, x'2, ..., x'_n)
        vector_x_bar = [0 for _ in range(n)]
        for i in range(n):
            if i in basic_set:
                vector_x_bar[i] = vector_b_hat[i]
            else:
                vector_x_bar[i] = 0

        # 4. 最后返回解向量
        return vector_x_bar, scalar_v_hat


def main():
    lp = LinearProgramming()

    # 单纯形算法 求解 线性规划(标准型)
    print('\n单纯形算法(初始解可行):')
    # 用于单纯形算法的线性规划标准型，同《CLRS》Chapter 29 中的式 (29.53)~(29.57)
    # 约束条件为 Ax <= b (向量中逐元素比较)
    # 目标函数为 z = c * x^{T} (向量内积)
    # 另外默认有非负约束 x_i >= 0
    matrix_a = [
        [1, 1, 3],  # 约束条件 1 * x_1 + 1 * x_2 + 3 * x_3 <= 30
        [2, 2, 5],  # 约束条件 2 * x_1 + 2 * x_2 + 5 * x_3 <= 24
        [4, 1, 2]   # 约束条件 4 * x_1 + 1 * x_2 + 2 * x_3 <= 36
    ]
    vector_b = [30, 24, 36]
    vector_c = [3, 1, 2]  # 这里目标函数为 z = 3 * x_1 + 1 * x_2 + 2 * x_3
    start = time.process_time()
    res = lp.simplex(matrix_a, vector_b, vector_c)
    end = time.process_time()

    if isinstance(res, tuple):
        assert len(res) == 2
        vector_x_bar, scalar_v_hat = res[0], res[1]
        # scalar_v_hat: 28
        # vector_x_bar: [8.0, 4.0, 0, 18.0, 0, 0]
        print('\nscalar_v_hat:')
        print(scalar_v_hat)
        if isinstance(vector_x_bar, list) and len(vector_x_bar) > 0:
            print('\nvector_x_bar:')
            print(vector_x_bar)
        else:
            print('单纯形算法出错!')
    else:
        print('单纯形算法无结果')

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 单纯形算法 求解 线性规划(标准型)
    print('\n单纯形算法(初始解不可行):')
    # 用于单纯形算法的线性规划标准型，同《CLRS》Chapter 29 中的式 (29.102)~(29.105)
    # 约束条件为 Ax <= b (向量中逐元素比较)
    # 目标函数为 z = c * x^{T} (向量内积)
    # 另外默认有非负约束 x_i >= 0
    matrix_a = [
        [2, -1],  # 约束条件 2 * x_1 - 1 * x_2 <= 2
        [1, -5]   # 约束条件 1 * x_1 - 5 * x_2 <= -4
    ]
    vector_b = [2, -4]
    vector_c = [2, -1]  # 这里目标函数为 z = 2 * x_1 - 1 * x_2
    start = time.process_time()
    res = lp.simplex(matrix_a, vector_b, vector_c)
    end = time.process_time()

    if isinstance(res, tuple):
        assert len(res) == 2
        vector_x_bar, scalar_v_hat = res[0], res[1]
        # scalar_v_hat: 2
        # vector_x_bar: [14/9, 10/9, 0, 0] = [1.55555555..., 1.11111111..., 0, 0]
        print('\nscalar_v_hat:')
        print(scalar_v_hat)
        if isinstance(vector_x_bar, list) and len(vector_x_bar) > 0:
            print('\nvector_x_bar:')
            print(vector_x_bar)
        else:
            print('单纯形算法出错!')
    else:
        print('单纯形算法无结果')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
