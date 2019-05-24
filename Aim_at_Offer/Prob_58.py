# -*- coding:utf-8 -*-

'''
序号：58
题目：对称的二叉树

题目描述：
请实现一个函数，用来判断一颗二叉树是不是对称的。
注意，如果一个二叉树同此二叉树的镜像是同样的，定义其为对称的。

时间限制：1秒 空间限制：32768K
本题知识点：树
'''
import sys
import getopt


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSymmetrical(self, pRoot):
        # write code here
        if pRoot is None or (pRoot.left is None and pRoot.right is None):
            return True

        # 递归，同时判断左右子树是否镜像
        return self.Symmetrical(pRoot.left, pRoot.right)

    def Symmetrical(self, left, right):
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
            self.Symmetrical(left.left, right.right) and \
            self.Symmetrical(left.right, right.left) # 注意镜像方向


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
    pRoot.right = TreeNode(2)
    pRoot.left.left = TreeNode(4)
    pRoot.right.right = TreeNode(4)

    answer = solution.isSymmetrical(pRoot)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
