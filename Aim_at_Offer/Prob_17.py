# -*- coding:utf-8 -*-

'''
序号：17
题目：树的子结构

题目描述：
输入两棵二叉树A，B，判断B是不是A的子结构。
（ps：我们约定空树不是任意一个树的子结构）

时间限制：1秒 空间限制：32768K
本题知识点：树，代码的鲁棒性
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
        # 存储前序中序后序遍历结果，本题用不上
        # 本意：通过分析前中后序遍历结果来分析子树结构
        self.pre_list = []
        self.mid_list = []
        self.post_list = []

    def HasSubtree(self, pRoot1, pRoot2):
        # write code here
        # 思路：
        # 从根节点出发，先比较两个二叉树的根节点是否相同，
        # 若根相同，则比较各自的左子树和右子树是否完全相同，相同可说明B是A的子结构
        # 当两个二叉树的根节点不相同，则从A树的左子树开始找是否存在和B相等的子树；
        # 如果左边没找到，则从A树的右子树开始找是否存在和B相等的子树，递归进行

        # 如果两个二叉树中有一个为空，则返回 False
        if pRoot1 is None or pRoot2 is None:
            return False

        answer = False
        # 如果两个二叉树根节点的值相同，则比较这两个二叉树是否相同
        if pRoot1.val == pRoot2.val:
            answer = self.JudgeSubTree(pRoot1, pRoot2)

        # 如果不相同，则从 A 树 pRoot1 的左子树找 pRoot2，递归
        if not answer:
            answer = self.HasSubtree(pRoot1.left, pRoot2)

        # 如果左边不相同，则从 A 树 pRoot1 的右子树找 pRoot2，递归
        if not answer:
            answer = self.HasSubtree(pRoot1.right, pRoot2)

        return answer

    def PreOrderTraversal(self, pRoot):
        if pRoot is not None:
            self.pre_list.append(pRoot.val)
            # print pRoot.val

            self.PreOrderTraversal(pRoot.left)
            self.PreOrderTraversal(pRoot.right)
        else:
            pass

    def MiddleOrderTraversal(self, pRoot):
        if pRoot is not None:
            self.MiddleOrderTraversal(pRoot.left)

            self.mid_list.append(pRoot.val)
            # print pRoot.val

            self.MiddleOrderTraversal(pRoot.right)
        else:
            pass

    def PostOrderTraversal(self, pRoot):
        if pRoot is not None:
            self.PostOrderTraversal(pRoot.left)
            self.PostOrderTraversal(pRoot.right)

            self.post_list.append(pRoot.val)
            # print pRoot.val
        else:
            pass

    def JudgeSubTree(self, pRoot1, pRoot2):
        # 先判断小二叉树 pRoot2 是否为空，为空则返回 True
        if pRoot2 is None:
            return True

        # 当小二叉树 pRoot2 不为空时，判断大二叉树 pRoot1 是否为空，为空则返回 False
        if pRoot1 is None:
            return False

        # 如果根节点匹配上了，则对左右子树进行匹配
        if pRoot1.val == pRoot2.val:
            return self.JudgeSubTree(pRoot1.left,
                pRoot2.left) and self.JudgeSubTree(pRoot1.right, pRoot2.right)
        
        # 默认返回值
        return False


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
    pRoot1 = TreeNode(1)
    pRoot1.left = TreeNode(2)
    pRoot1.right = TreeNode(3)
    pRoot1.left.left = TreeNode(4)
    pRoot1.left.right = TreeNode(5)

    pRoot2 = TreeNode(2)
    pRoot2.left = TreeNode(4)
    pRoot2.right = TreeNode(5)

    solution = Solution()
    answer = solution.HasSubtree(pRoot1, pRoot2)

    print answer


if __name__ == "__main__":
    sys.exit(main())

