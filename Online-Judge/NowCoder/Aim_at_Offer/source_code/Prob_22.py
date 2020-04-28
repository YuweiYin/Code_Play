#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：22
题目：从上往下打印二叉树

题目描述：
从上往下打印出二叉树的每个节点，同层节点从左至右打印。

时间限制：1秒 空间限制：32768K
本题知识点：树，举例让抽象具体化
"""

import sys
import time


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    @staticmethod
    def print_from_top_to_bottom(root):
        # 思路：宽度优先搜索，用辅助队列

        if root is None:
            return []

        node_list = []
        queue = [].append(root)

        # if root.left is None and root.right is None:
        #     node_list.append(root.val)
        #     return node_list

        while queue:
            # 把队首元素的值存进 node_list
            pointer = queue[0]
            node_list.append(pointer.val)
            # 把队首元素的左右儿子节点加进队列 queue
            if pointer.left is not None:
                queue.append(pointer.left)
            if pointer.right is not None:
                queue.append(pointer.right)
            # 删除队首元素
            del queue[0]

        # 返回从上到下每个节点值列表，例：[1,2,3]
        return node_list


def main():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(6)
    root.right.right.right = TreeNode(7)

    start = time.process_time()
    res = Solution.print_from_top_to_bottom(root)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
