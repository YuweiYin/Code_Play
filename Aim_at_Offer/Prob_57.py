# -*- coding:utf-8 -*-

'''
序号：57
题目：二叉树的下一个结点

题目描述：
给定一个二叉树和其中的一个结点，请找出中序遍历顺序的下一个结点并且返回。
注意，树中的结点不仅包含左右子结点，同时包含指向父结点的指针。

时间限制：1秒 空间限制：32768K
本题知识点：树
'''
import sys
import getopt


class TreeLinkNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.next = None


class Solution:
    def __init__(self):
        self.mid_list = []

    def GetNext(self, pNode):
        # write code here

        # 方法一：利用 next 父节点轻松回溯
        # 如果该结点有右子树
        if pNode.right:
            # 下一个中序遍历序列结点 就是其右子树的最左子结点
            pointer = pNode.right

            # 一路向左
            while pointer.left is not None:
                pointer = pointer.left

            return pointer

        # 如果该结点没有右子树，则往回走
        while pNode.next is not None:
            # 如果当前结点是其父亲结点的左孩子，Bingo～
            if(pNode.next.left == pNode):
                return pNode.next

            # 沿父节点一路往上遍历
            pNode = pNode.next

        # 到了根节点仍没找到目标结点，返回 None
        return None

        # 方法二：中序遍历并存储序列
        # # 根结点为空对象或没有儿子结点
        # if pNode is None or (pNode.left is None and pNode.right is None):
        #     return None

        # # 中序遍历并将序列存储于类成员变量 self.mid_list 列表中
        # self.mid_list = []
        # self.MiddleOrderTraversal(pNode)

        # # 列表为空对象或空表或长度为 1
        # if self.mid_list is None or len(self.mid_list) <= 1:
        #     return None

        # else:
        #     # 找到根结点
        #     if pNode in self.mid_list:
        #         # 定位根结点在中序列表中的位置
        #         root_index = self.mid_list.index(pNode)

        #         # 找下一个元素，如果有，则返回它
        #         if (root_index + 1) < len(self.mid_list):
        #             return self.mid_list[root_index + 1]
        #         else:
        #             return None
        #     else:
        #         return None

        # return None

    # 递归中序遍历
    def MiddleOrderTraversal(self, pNode):
        if pNode.left is not None:
            self.MiddleOrderTraversal(pNode.left)

        # 存储中序遍历序列
        self.mid_list.append(pNode)

        if pNode.right is not None:
            self.MiddleOrderTraversal(pNode.right)


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

    pNode = TreeLinkNode(1)
    pNode.next = None

    pNode.left = TreeLinkNode(2)
    pNode.left.next = pNode

    pNode.right = TreeLinkNode(3)
    pNode.right.next = pNode

    pNode.left.left = TreeLinkNode(4)
    pNode.left.left.next = pNode.left

    answer = solution.GetNext(pNode)

    if answer is not None:
        print answer.val
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
