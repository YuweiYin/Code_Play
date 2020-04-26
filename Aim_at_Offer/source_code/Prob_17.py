#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：17
题目：树的子结构

题目描述：
输入两棵二叉树 A，B，判断 B 是不是 A 的子结构。
（ps：我们约定空树不是任意一个树的子结构）

时间限制：1秒 空间限制：32768K
本题知识点：树，代码的鲁棒性
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
        # 存储前序中序后序遍历结果，本题用不上
        # 本意：通过分析前中后序遍历结果来分析子树结构
        self.pre_list = []
        self.mid_list = []
        self.post_list = []

    def has_sub_tree(self, p_root1, p_root2):
        # 思路：
        # 从根节点出发，先比较两个二叉树的根节点是否相同，
        # 若根相同，则比较各自的左子树和右子树是否完全相同，相同可说明 B 是 A 的子结构
        # 当两个二叉树的根节点不相同，则从 A 树的左子树开始找是否存在和 B 相等的子树；
        # 如果左边没找到，则从 A 树的右子树开始找是否存在和 B 相等的子树，递归进行

        # 如果两个二叉树中有一个为空，则返回 False
        if p_root1 is None or p_root2 is None:
            return False

        answer = False
        # 如果两个二叉树根节点的值相同，则比较这两个二叉树是否相同
        if p_root1.val == p_root2.val:
            answer = self.judge_sub_tree(p_root1, p_root2)

        # 如果不相同，则从 A 树 p_root1 的左子树找 p_root2，递归
        if not answer:
            answer = self.has_sub_tree(p_root1.left, p_root2)

        # 如果左边不相同，则从 A 树 p_root1 的右子树找 p_root2，递归
        if not answer:
            answer = self.has_sub_tree(p_root1.right, p_root2)

        return answer

    # 当二叉树根节点的值相同的时候，判断 p_root2 是否为 p_root1 的子树
    def judge_sub_tree(self, p_root1, p_root2):
        # 先判断小二叉树 pRoot2 是否为空，为空则返回 True
        if p_root2 is None:
            return True

        # 当小二叉树 pRoot2 不为空时，判断大二叉树 pRoot1 是否为空，为空则返回 False
        if p_root1 is None:
            return False

        # 如果根节点匹配上了，则递归地对左右子树进行匹配
        if p_root1.val == p_root2.val:
            return self.judge_sub_tree(p_root1.left, p_root2.left) and \
                self.judge_sub_tree(p_root1.right, p_root2.right)

        # 默认返回值
        return False

    # 前序遍历二叉树
    def pre_order_traversal(self, p_root):
        if p_root is not None:
            self.pre_list.append(p_root.val)
            # print(p_root.val)

            self.pre_order_traversal(p_root.left)
            self.pre_order_traversal(p_root.right)
        else:
            pass

    # 中序遍历二叉树
    def middle_order_traversal(self, p_root):
        if p_root is not None:
            self.middle_order_traversal(p_root.left)

            self.mid_list.append(p_root.val)
            # print(p_root.val)

            self.middle_order_traversal(p_root.right)
        else:
            pass

    # 后序遍历二叉树
    def post_order_traversal(self, p_root):
        if p_root is not None:
            self.post_order_traversal(p_root.left)
            self.post_order_traversal(p_root.right)

            self.post_list.append(p_root.val)
            # print(p_root.val)
        else:
            pass


def main():
    p_root1 = TreeNode(1)
    p_root1.left = TreeNode(2)
    p_root1.right = TreeNode(3)
    p_root1.left.left = TreeNode(4)
    p_root1.left.right = TreeNode(5)

    p_root2 = TreeNode(2)
    p_root2.left = TreeNode(4)
    p_root2.right = TreeNode(5)

    solution = Solution()

    start = time.process_time()
    answer = solution.has_sub_tree(p_root1, p_root2)
    end = time.process_time()

    print(answer)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
