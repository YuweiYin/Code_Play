#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：58
题目：对称的二叉树

题目描述：
请实现一个函数，用来判断一颗二叉树是不是对称的。
注意，如果一个二叉树同此二叉树的镜像是同样的，定义其为对称的。

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
    def is_symmetrical(self, p_root):
        if p_root is None or (p_root.left is None and p_root.right is None):
            return True

        # 递归，同时判断左右子树是否镜像
        return self.symmetrical(p_root.left, p_root.right)

    def symmetrical(self, left, right):
        # 左右子树均为 None，表明达到叶节点，这是镜像对称的
        if left is None and right is None:
            return True

        # 如果左右子树不同时为空，则此结点不镜像对称，于是整棵树也不是镜像对称的了
        if left is None:
            return False

        if right is None:
            return False

        # 如果左右的值相等，且左左等于右右，且左右等于右左，则返回真，否则返回假
        return left.val == right.val and \
            self.symmetrical(left.left, right.right) and \
            self.symmetrical(left.right, right.left)  # 注意镜像方向


def main():
    p_root = TreeNode(1)
    p_root.left = TreeNode(2)
    p_root.right = TreeNode(2)
    p_root.left.left = TreeNode(4)
    p_root.right.right = TreeNode(4)

    solution = Solution()

    start = time.process_time()
    answer = solution.is_symmetrical(p_root)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
