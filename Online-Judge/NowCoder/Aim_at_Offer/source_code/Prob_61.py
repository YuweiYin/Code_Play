#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：61
题目：序列化二叉树

题目描述：
请实现两个函数，分别用来序列化和反序列化二叉树

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
    def serialize(self, root):
        # 如果结点是空，返回 '#'
        if root is None:
            return '#'

        # 递归前序遍历，将结果存储于列表
        answer = [str(root.val)]

        # 左子树
        left = self.serialize(root.left)
        answer.append(left)

        # 右子树
        right = self.serialize(root.right)
        answer.append(right)

        # 用 ',' 连接序列化结果
        return ','.join(answer)

    def deserialize(self, s):
        #  按 ',' 分割序列化字符串
        serialize = s.split(',')

        # 递归反序列化，从 0 号位开始构建，因为前序遍历序列的 0 号位就是树根
        tree, seq_pointer = self.core_deserialize(serialize, 0)

        return tree

    def core_deserialize(self, s, seq_pointer):
        if seq_pointer >= len(s) or s[seq_pointer] == "#":
            return None, seq_pointer + 1

        # 递归前序遍历，创建结点
        tree = TreeNode(int(s[seq_pointer]))
        seq_pointer += 1

        # 反序列化左子树
        tree.left, seq_pointer = self.core_deserialize(s, seq_pointer)

        # 反序列化右子树
        tree.right, seq_pointer = self.core_deserialize(s, seq_pointer)

        return tree, seq_pointer

    def pre_order_traversal(self, p_root):
        print(p_root.val)

        if p_root.left is not None:
            self.pre_order_traversal(p_root.left)

        if p_root.right is not None:
            self.pre_order_traversal(p_root.right)


def main():
    solution = Solution()

    p_root = TreeNode(8)
    p_root.left = TreeNode(6)
    p_root.right = TreeNode(10)
    p_root.left.left = TreeNode(5)
    p_root.left.right = TreeNode(7)
    p_root.right.left = TreeNode(9)
    p_root.right.right = TreeNode(11)

    start = time.process_time()
    answer = solution.serialize(p_root)
    end = time.process_time()

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    start = time.process_time()
    tree = solution.deserialize(answer)
    end = time.process_time()

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    solution.pre_order_traversal(tree)


if __name__ == "__main__":
    sys.exit(main())
