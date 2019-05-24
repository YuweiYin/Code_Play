# -*- coding:utf-8 -*-

'''
序号：61
题目：序列化二叉树

题目描述：
请实现两个函数，分别用来序列化和反序列化二叉树

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
    def Serialize(self, root):
        # write code here
        # 如果结点是空，返回 '#'
        if root is None:
            return '#'

        # 递归前序遍历，将结果存储于列表
        answer = []
        answer.append(str(root.val))

        # 左子树
        left = self.Serialize(root.left)
        answer.append(left)

        # 右子树
        right = self.Serialize(root.right)
        answer.append(right)

        # 用 ',' 连接序列化结果
        return ','.join(answer)

    def Deserialize(self, s):
        # write code here
        #  按 ',' 分割序列化字符串
        serialize = s.split(',')

        # 递归反序列化，从 0 号位开始构建，因为前序遍历序列的 0 号位就是树根
        tree, seq_pointer = self.CoreDeserialize(serialize, 0)

        return tree

    def CoreDeserialize(self, s, seq_pointer):
        if seq_pointer >= len(s) or s[seq_pointer] == "#":
            return None, seq_pointer + 1

        # 递归前序遍历，创建结点
        tree = TreeNode(int(s[seq_pointer]))
        seq_pointer += 1

        # 反序列化左子树
        tree.left, seq_pointer = self.CoreDeserialize(s, seq_pointer)

        # 反序列化右子树
        tree.right, seq_pointer = self.CoreDeserialize(s, seq_pointer)

        return tree, seq_pointer

    def PreOrderTraversal(self, pRoot):
        print pRoot.val

        if pRoot.left is not None:
            self.PreOrderTraversal(pRoot.left)

        if pRoot.right is not None:
            self.PreOrderTraversal(pRoot.right)


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

    pRoot = TreeNode(8)
    pRoot.left = TreeNode(6)
    pRoot.right = TreeNode(10)
    pRoot.left.left = TreeNode(5)
    pRoot.left.right = TreeNode(7)
    pRoot.right.left = TreeNode(9)
    pRoot.right.right = TreeNode(11)

    answer = solution.Serialize(pRoot)

    if answer is not None:
        print answer
    else:
        print 'No Answer'

    tree = solution.Deserialize(answer)
    solution.PreOrderTraversal(tree)


if __name__ == "__main__":
    sys.exit(main())
