#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：39
题目：平衡二叉树

题目描述：
输入一棵二叉树，判断该二叉树是否是平衡二叉树。

平衡二叉树：
一棵空树，或者其左右子树的高度差的绝对值不超过 1，
并且左右两个子树都是一棵平衡二叉树。

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
    def is_balanced_solution(self, p_root):
        if p_root is None:
            return True

        if p_root.left is None and p_root.right is None:
            return True

        # 如果存在子树不平衡，其返回值会是 -1，并且一直会回传到根节点
        return self.get_depth(p_root) != -1

    def get_depth(self, p_root):
        if p_root is None:
            return 0

        # print(p_root.val)
        # 计算左子树的深度
        left_depth = self.get_depth(p_root.left)
        if left_depth == -1:
            # 直接回传左子树不平衡的信息
            return -1

        # 计算右子树的深度
        right_depth = self.get_depth(p_root.right)
        if right_depth == -1:
            # 直接回传右子树不平衡的信息
            return -1

        # 如果左右子树的深度差距大于 1，则返回 -1
        # -1 这个表明子树不平衡的信息，会一直回传到根节点
        if abs(left_depth - right_depth) > 1:
            return -1
        # 否则返回自己左右子树最长的长度加上 1（本结点）
        # 叶节点的左右子树的深度为 0，其返回值为 1 + max(0, 0) = 1
        else:
            return 1 + max(left_depth, right_depth)


def main():
    solution = Solution()

    p_root = TreeNode(1)
    p_root.left = TreeNode(2)
    p_root.right = TreeNode(3)
    p_root.left.left = TreeNode(4)
    p_root.left.right = TreeNode(5)
    p_root.right.right = TreeNode(6)
    # p_root.right.right.left = TreeNode(7)
    # p_root.right.right.right = TreeNode(8)

    start = time.process_time()
    answer = solution.is_balanced_solution(p_root)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
