# -*- coding:utf-8 -*-

'''
序号：38
题目：二叉树的深度

题目描述：
输入一棵二叉树，求该树的深度。
从根结点到叶结点依次经过的结点（含根、叶结点）
形成树的一条路径，最长路径的长度为树的深度。

时间限制：1秒 空间限制：32768K
本题知识点：树，知识迁移能力
'''
import sys
import getopt


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.best_depth = 0 # 全局最优解
        self.current_depth = 0 # 当前深度

    def TreeDepth(self, pRoot):
        # write code here
        if pRoot is None:
            return 0

        if pRoot.left is None and pRoot.right is None:
            return 1

        # 前序遍历
        self.PreOrderTraversal(pRoot)

        return self.best_depth

    def PreOrderTraversal(self, pRoot):
        self.current_depth += 1
        # 如果当前解优于最优解，则修改最优解
        if self.current_depth > self.best_depth:
            self.best_depth = self.current_depth

        if pRoot.left is not None:
            # 遍历左子树
            self.PreOrderTraversal(pRoot.left)
            # 回溯，深度减 1
            self.current_depth -= 1

        if pRoot.right is not None:
            # 遍历右子树
            self.PreOrderTraversal(pRoot.right)
            # 回溯，深度减 1
            self.current_depth -= 1


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    # Main Logic Part

    solution = Solution()

    pRoot = TreeNode(1)
    pRoot.left = TreeNode(2)
    pRoot.right = TreeNode(3)
    pRoot.left.left = TreeNode(4)
    pRoot.left.right = TreeNode(5)
    pRoot.right.right = TreeNode(6)
    pRoot.right.right.left = TreeNode(7)
    pRoot.right.right.right = TreeNode(8)
    pRoot.right.right.right.left = TreeNode(9)

    answer = solution.TreeDepth(pRoot)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

