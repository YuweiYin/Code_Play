#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：62
题目：二叉搜索树的第 k 个结点

题目描述：
给定一棵二叉搜索树，请找出其中的第 k 小的结点。
例如，（5，3，7，2，4，6，8）中，
按结点数值大小顺序第三小结点的值为4。

时间限制：1秒 空间限制：32768K
本题知识点：树
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
        # 中序遍历序列，二叉搜索树的中序序列就是值从小到大的排列
        self.order_list = []

    # 返回对应节点 TreeNode
    def get_kth_node(self, p_root, k):
        if p_root is None or k <= 0:
            return None

        # 中序遍历，并构成中序序列
        self.middle_order_traversal(p_root)

        kth_node = None
        if k <= len(self.order_list):
            kth_node = self.order_list[k - 1]

        return kth_node

    # 递归中序遍历
    def middle_order_traversal(self, p_root):
        # 左子树
        if p_root.left is not None:
            self.middle_order_traversal(p_root.left)

        # 增添结点
        self.order_list.append(p_root)

        # 右子树
        if p_root.right is not None:
            self.middle_order_traversal(p_root.right)


def main():
    solution = Solution()

    p_root = TreeNode(5)
    p_root.left = TreeNode(3)
    p_root.right = TreeNode(7)
    p_root.left.left = TreeNode(2)
    p_root.left.right = TreeNode(4)
    p_root.right.left = TreeNode(6)
    p_root.right.right = TreeNode(8)

    k = 3  # 4

    start = time.process_time()
    answer = solution.get_kth_node(p_root, k)
    end = time.process_time()

    if answer is not None:
        print(answer.val)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
