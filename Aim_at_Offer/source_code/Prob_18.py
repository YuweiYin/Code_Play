#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：18
题目：二叉树的镜像

题目描述：
操作给定的二叉树，将其变换为源二叉树的镜像。

二叉树的镜像定义：源二叉树 
            8
           /  \
          6   10
         / \  / \
        5  7 9 11
        镜像二叉树
            8
           /  \
          10   6
         / \  / \
        11 9 7  5

时间限制：1秒 空间限制：32768K
本题知识点：树，面试思路
"""

import sys
import time


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    # 返回镜像树的根节点
    def mirror(self, root):
        # 思路：从根节点出发，遍历并交替左右结点，递归

        # 如果根结点为空，则返回 None
        if root is not None:

            temp = root.left
            root.left = root.right
            root.right = temp

            self.mirror(root.left)
            self.mirror(root.right)

            return root
        else:
            return None

    # 前序遍历二叉树
    def pre_order_traversal(self, p_root):
        if p_root is not None:
            print(p_root.val)

            self.pre_order_traversal(p_root.left)
            self.pre_order_traversal(p_root.right)
        else:
            pass

    # 中序遍历二叉树
    def middle_order_traversal(self, p_root):
        if p_root is not None:
            self.middle_order_traversal(p_root.left)

            print(p_root.val)

            self.middle_order_traversal(p_root.right)
        else:
            pass

    # 后序遍历二叉树
    def post_order_traversal(self, p_root):
        if p_root is not None:
            self.post_order_traversal(p_root.left)
            self.post_order_traversal(p_root.right)

            print(p_root.val)
        else:
            pass


def main():
    root = TreeNode(8)
    root.left = TreeNode(6)
    root.right = TreeNode(10)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(7)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(11)

    solution = Solution()

    start = time.process_time()
    answer = solution.mirror(root)
    end = time.process_time()

    if answer is not None:
        solution.pre_order_traversal(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
