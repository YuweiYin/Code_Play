#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/dynamic_programming
@File    : optimal-binary-search-tree.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
最优二叉搜索树 Optimal Binary Search Tree

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 15
"""


class OptimalBinarySearchTree:
    def __init__(self, p_arr, q_arr, float_acc):
        assert isinstance(p_arr, list) and len(p_arr) > 0
        assert isinstance(q_arr, list) and len(q_arr) == len(p_arr) + 1
        self.p_arr = p_arr     # 各个关键字 k_i 对应的概率权重 p_i
        self.q_arr = q_arr     # 各个伪关键字 d_i 对应的概率权重 q_i
        self.float_acc = float_acc      # p_arr 和 q_arr 中概率值(浮点数)保留小数点后的位数
        self.optimal_cost = 0x3f3f3f3f  # 最优的期望搜索代价
        self.inf = 0x3f3f3f3f  # 目标是求期望搜索代价的最小值，所以在计算前让代价初始化为 inf

    # 最优二叉搜索树
    # - 若 j == i-1，则 e[i, j] = q_{i-1}
    # - 若 i <= j，则 e[i, j] = min{ e[i, r-1] + e[r+1, j] + w(i,j) }
    # - w[i, j] = w[i, j-1] + pj + qj
    # 返回：o_bst 最优值表、o_bst 最优解表
    def optimal_bst(self):
        assert isinstance(self.p_arr, list) and len(self.p_arr) > 0
        assert isinstance(self.q_arr, list) and len(self.q_arr) == len(self.p_arr) + 1

        # 记关键字数量为 n
        n = len(self.p_arr)

        # 表格 e[1..n+1, 0..n] 来保存 e[i, j] 值
        # 第一维下标上界为 n+1 而不是 n，是因为对于只包含伪关键字 dn 的子树，需要计算并保存 e[n+1, n]
        # 第二维下标下界为 0，是因为对于只包含伪关键字 d0 的子树，需要计算并保存 e[1, 0]。只是用表中满足 i < j 的表项 e[i, j]
        e_table = [[0 for _ in range(n + 1)] for _ in range(n + 2)]

        # 为了避免每次计算 e[i, j] 都要重新计算 w(i, j)，可以将此值保存在表格 w 中
        # 这样每次可以节省 $ \Theta(j-i) $ 次加法运算。
        w_table = [[0 for _ in range(n + 1)] for _ in range(n + 2)]

        # 表格 root[i, j] 记录 包含了关键字 k1, ..., kj 的子树 的根
        # 利用 root 表格可以构建出最优解。只使用此表中满足 1 <= i <= j <= n 的表项 root[i, j]
        # r_table = [[0 for j in range(n)] for i in range(n)]
        r_table = [[0 for _ in range(n + 1)] for _ in range(n + 2)]

        # e[i, i-1] 和 w[i, i-1] 均置为 q_{i-1}
        for i in range(1, n + 2):
            e_table[i][i - 1] = self.q_arr[i - 1]
            w_table[i][i - 1] = self.q_arr[i - 1]

        # 自底向上循环实现 (动态规划) \Theta(n^3)
        e_table, w_table, r_table = self._optimal_bst(e_table, w_table, r_table, n)
        return e_table, w_table, r_table

    # 自底向上循环实现 (动态规划)
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def _optimal_bst(self, e_table, w_table, r_table, n):
        assert isinstance(self.p_arr, list) and len(self.p_arr) > 0
        assert isinstance(self.q_arr, list) and len(self.q_arr) == len(self.p_arr) + 1

        # 对于各个长度(length) 和各个起点(i) 的子关键字序列(子问题)求最优解/值，自底向上分别计算
        # - 若 j == i-1，则 e[i, j] = q_{i-1}
        # - 若 i <= j，则 e[i, j] = min{ e[i, r-1] + e[r+1, j] + w(i,j) }
        # - w[i, j] = w[i, j-1] + pj + qj
        for length in range(1, n + 1):          # 子关键字序列的长度取值范围为 1 ~ n
            # 第一个循环
            for i in range(1, n - length + 2):  # 子关键字序列起点 i 取值范围为 0 ~ n-1
                j = i + length - 1              # 子关键字序列终点 j
                e_table[i][j] = self.inf
                w_table[i][j] = round(w_table[i][j - 1] + self.p_arr[j - 1] + self.q_arr[j], self.float_acc)
                for r in range(i, j + 1):
                    cost = e_table[i][r - 1] + e_table[r + 1][j] + w_table[i][j]
                    if cost < e_table[i][j]:
                        e_table[i][j] = round(cost, self.float_acc)
                        r_table[i][j] = r

        # 此时最优值为 e[1, n]
        self.optimal_cost = e_table[1][n]
        # 返回备忘录 e、w 和 r
        return e_table, w_table, r_table

    # 获取最优值(最优的期望搜索代价) e[1, n]
    def get_optimal_cost(self):
        return self.optimal_cost

    # 根据 r_table 打印最优解
    # 时间复杂度 \Theta(n)
    def print_optimal_bst(self, r_table):
        n = len(self.p_arr)
        # 首先打印树根
        cur_root = r_table[1][n]
        print('k', cur_root, '为根')
        # 然后调用递归算法处理其左右子树
        self._print_optimal_bst(r_table, cur_root, True, 1, cur_root - 1)
        self._print_optimal_bst(r_table, cur_root, False, cur_root + 1, n)

    # 参数 parent_key 是当前子树的父结点序号，is_left 为 True 表示当前子树是其父结点的左孩子，否则反之
    def _print_optimal_bst(self, r_table, parent_key, is_left, i, j):
        # 特殊情况：伪关键字数量比关键字数量多 1，所以仅在如下情况会让 k_j 有右孩子 d_j
        if i > j:
            if i == j + 1 and (not is_left):
                print('叶结点 d', j, '为 k', j, '的右孩子')
            return
        # 基本情况：i == j 表示到了关键字 k 的"叶"结点
        if i == j:
            # 根据当前子树是其父结点的左孩子还是右孩子，分别处理
            if is_left:
                print('k', i, '为 k', parent_key, '的左孩子')
            else:
                print('k', i, '为 k', parent_key, '的右孩子')
            # 处理真正的叶结点：伪关键字 d_{i-1} 和 d_{i}
            print('叶结点 d', i - 1, '为 k', i, '的左孩子')
            print('叶结点 d', i, '为 k', i, '的右孩子')
        # 否则需要检查关键字区间 ki, ..., kj 中的树结构
        else:
            # 通过查看 r_table[i][j] 得到此关键字序列该选择的树根
            cur_root = r_table[i][j]
            # 根据当前子树是其父结点的左孩子还是右孩子，分别处理
            if is_left:
                print('k', cur_root, '为 k', parent_key, '的左孩子')
            else:
                print('k', cur_root, '为 k', parent_key, '的右孩子')
            # 递归处理当前根的左右子树
            self._print_optimal_bst(r_table, cur_root, True, i, cur_root - 1)
            self._print_optimal_bst(r_table, cur_root, False, cur_root + 1, j)


def main():
    # p_arr[i] 是各个关键字 k_i 对应的概率权重 p_i
    # q_arr[i] 是各个伪关键字 d_i 对应的概率权重 q_i
    p_arr = [0.15, 0.10, 0.05, 0.10, 0.20]
    q_arr = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
    float_acc = 2  # p_arr 和 q_arr 中概率值(浮点数)保留小数点后的位数

    o_bst = OptimalBinarySearchTree(p_arr, q_arr, float_acc)

    start = time.process_time()
    e_table, w_table, r_table = o_bst.optimal_bst()
    end = time.process_time()

    print('\noptimal_cost:')
    print(o_bst.get_optimal_cost())  # 2.75

    print('\noptimal_BST:')
    o_bst.print_optimal_bst(r_table)

    print('\ne_table:')
    for row in e_table:
        print(row)

    '''
    [0, 0, 0, 0, 0, 0]
    [0.05, 0.45, 0.9, 1.25, 1.75, 2.75]
    [0, 0.1, 0.4, 0.7, 1.2, 2.0]
    [0, 0, 0.05, 0.25, 0.6, 1.3]
    [0, 0, 0, 0.05, 0.3, 0.9]
    [0, 0, 0, 0, 0.05, 0.5]
    [0, 0, 0, 0, 0, 0.1]
    '''

    print('\nw_table:')
    for row in w_table:
        print(row)
    '''
    [0, 0, 0, 0, 0, 0]
    [0.05, 0.3, 0.45, 0.55, 0.7, 1.0]
    [0, 0.1, 0.25, 0.35, 0.5, 0.8]
    [0, 0, 0.05, 0.15, 0.3, 0.6]
    [0, 0, 0, 0.05, 0.2, 0.5]
    [0, 0, 0, 0, 0.05, 0.35]
    [0, 0, 0, 0, 0, 0.1]
    '''

    print('\nr_table:')
    for row in r_table:
        print(row)
    '''
    [0, 0, 0, 0, 0, 0]
    [0, 1, 1, 2, 2, 2]
    [0, 0, 2, 2, 2, 4]
    [0, 0, 0, 3, 4, 5]
    [0, 0, 0, 0, 4, 5]
    [0, 0, 0, 0, 0, 5]
    [0, 0, 0, 0, 0, 0]
    '''

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
