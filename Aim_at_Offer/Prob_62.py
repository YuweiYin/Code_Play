# -*- coding:utf-8 -*-

'''
序号：62
题目：二叉搜索树的第k个结点

题目描述：
给定一棵二叉搜索树，请找出其中的第k小的结点。
例如，（5，3，7，2，4，6，8）中，
按结点数值大小顺序第三小结点的值为4。

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
    def __init__(self):
        # 中序遍历序列，二叉搜索树的中序序列就是值从小到大的排列
        self.order_list = []

    # 返回对应节点TreeNode
    def KthNode(self, pRoot, k):
        # write code here
        if pRoot is None or k <= 0:
            return None

        # 中序遍历，并构成中序序列
        self.MiddleOrderTraversal(pRoot)

        kthNode = None
        if k <= len(self.order_list):
            kthNode = self.order_list[k - 1]

        return kthNode

    # 递归中序遍历
    def MiddleOrderTraversal(self, pRoot):
        # 左子树
        if pRoot.left is not None:
            self.MiddleOrderTraversal(pRoot.left)

        # 增添结点
        self.order_list.append(pRoot)

        # 右子树
        if pRoot.right is not None:
            self.MiddleOrderTraversal(pRoot.right)


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

    pRoot = TreeNode(5)
    pRoot.left = TreeNode(3)
    pRoot.right = TreeNode(7)
    pRoot.left.left = TreeNode(2)
    pRoot.left.right = TreeNode(4)
    pRoot.right.left = TreeNode(6)
    pRoot.right.right = TreeNode(8)

    k = 3 # 4

    answer = solution.KthNode(pRoot, k)

    if answer is not None:
        print answer.val
    else:
        print 'No Answer'

    # solution.PreOrderTraversal(answer)


if __name__ == "__main__":
    sys.exit(main())
