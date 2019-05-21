# -*- coding:utf-8 -*-

'''
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
'''
import sys
import getopt


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    # 返回镜像树的根节点
    def Mirror(self, root):
        # write code here
        # 思路：从根节点出发，遍历并交替左右结点，递归

        # 如果根结点为空，则返回 None
        if root is not None:

            temp = root.left
            root.left = root.right
            root.right = temp

            self.Mirror(root.left)
            self.Mirror(root.right)

            return root
        else:
            return None

    def PreOrderTraversal(self, pRoot):
        if pRoot is not None:
            print pRoot.val

            self.PreOrderTraversal(pRoot.left)
            self.PreOrderTraversal(pRoot.right)
        else:
            pass

    def MiddleOrderTraversal(self, pRoot):
        if pRoot is not None:
            self.MiddleOrderTraversal(pRoot.left)

            print pRoot.val

            self.MiddleOrderTraversal(pRoot.right)
        else:
            pass

    def PostOrderTraversal(self, pRoot):
        if pRoot is not None:
            self.PostOrderTraversal(pRoot.left)
            self.PostOrderTraversal(pRoot.right)

            print pRoot.val
        else:
            pass


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
    root = TreeNode(8)
    root.left = TreeNode(6)
    root.right = TreeNode(10)
    root.left.left = TreeNode(5)
    root.left.right = TreeNode(7)
    root.right.left = TreeNode(9)
    root.right.right = TreeNode(11)

    solution = Solution()
    answer = solution.Mirror(root)

    if answer is not None:
        solution.PreOrderTraversal(answer)
    else:
        print None


if __name__ == "__main__":
    sys.exit(main())

