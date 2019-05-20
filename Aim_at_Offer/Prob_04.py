# -*- coding:utf-8 -*-

'''
序号：04
题目：重建二叉树

题目描述：
输入某二叉树的前序遍历和中序遍历的结果，请重建出该二叉树。
假设输入的前序遍历和中序遍历的结果中都不含重复的数字。
例如输入前序遍历序列{1,2,4,7,3,5,6,8}和中序遍历序列{4,7,2,1,5,3,8,6}，
则重建二叉树并返回。

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
    # 返回构造的TreeNode根节点
    def reConstructBinaryTree(self, pre, tin):
        # write code here
        # 递归终止条件：如果前序列表只有一个值，那这就是叶节点了
        if len(pre) == 1:
            return TreeNode(pre[0])

        # 构造当前节点（非叶节点）
        root = TreeNode(pre[0])

        # 拆分前序列表和中序列表
        # 前序列表的第一个计为 x，就是当前的节点值
        # 在中序列表中，x 左边的就是左子树节点，右边的就是右子树节点
        # 拆分之后，两边子树使用各自的前序、中序列表去递归构造树结构
        root_index = tin.index(pre[0])
        left_node_num = root_index + 1
        # right_node_num = len(pre) - root_index - 1

        left_pre = pre[1: left_node_num]
        right_pre = pre[left_node_num: ]

        left_tin = tin[0: root_index]
        right_tin = tin[left_node_num: ]

        # 递归构造左子树
        if len(left_pre) <= 0:
            root.left = None
        else:
            root.left = self.reConstructBinaryTree(left_pre, left_tin)

        # 递归构造右子树
        if len(right_pre) <= 0:
            root.right = None
        else:
            root.right = self.reConstructBinaryTree(right_pre, right_tin)

        # 返回该中间节点
        return root


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
    pre = [1, 2, 4, 7, 3, 5, 6, 8]
    tin = [4, 7, 2, 1, 5, 3, 8, 6]
    solution = Solution()
    tree =  solution.reConstructBinaryTree(pre, tin)


if __name__ == "__main__":
    sys.exit(main())

