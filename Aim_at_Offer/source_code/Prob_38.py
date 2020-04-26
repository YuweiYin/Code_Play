#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：38
题目：二叉树的深度

题目描述：
输入一棵二叉树，求该树的深度。
从根结点到叶结点依次经过的结点（含根、叶结点）
形成树的一条路径，最长路径的长度为树的深度。

时间限制：1秒 空间限制：32768K
本题知识点：树，知识迁移能力
"""

import sys
import time


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.best_depth = 0     # 全局最优值
        self.current_depth = 0  # 当前深度

    def tree_depth(self, p_root):
        if p_root is None:
            return 0

        # 方法一
        # return 1 + max(self.TreeDepth(pRoot.left), self.TreeDepth(pRoot.right))

        # 方法二：前序遍历
        if p_root.left is None and p_root.right is None:
            return 1

        # 前序遍历
        self.pre_order_traversal(p_root)

        return self.best_depth

    def pre_order_traversal(self, p_root):
        self.current_depth += 1
        # 如果当前深度优于最优值，则修改最优值
        if self.current_depth > self.best_depth:
            self.best_depth = self.current_depth

        if p_root.left is not None:
            # 遍历左子树
            self.pre_order_traversal(p_root.left)
            # 回溯，深度减 1
            self.current_depth -= 1

        if p_root.right is not None:
            # 遍历右子树
            self.pre_order_traversal(p_root.right)
            # 回溯，深度减 1
            self.current_depth -= 1


def main():
    solution = Solution()

    p_root = TreeNode(1)
    p_root.left = TreeNode(2)
    p_root.right = TreeNode(3)
    p_root.left.left = TreeNode(4)
    p_root.left.right = TreeNode(5)
    p_root.right.right = TreeNode(6)
    p_root.right.right.left = TreeNode(7)
    p_root.right.right.right = TreeNode(8)
    p_root.right.right.right.left = TreeNode(9)

    start = time.process_time()
    answer = solution.tree_depth(p_root)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
