# -*- coding:utf-8 -*-

'''
序号：26
题目：二叉搜索树与双向链表

题目描述：
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的双向链表。
要求不能创建任何新的结点，只能调整树中结点指针的指向。

时间限制：1秒 空间限制：32768K
本题知识点：树、链表，分解让复杂问题简单
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
        # self.sorted_node_list = []
        self.pre_node = None
        self.head_node = None

    def Convert(self, pRootOfTree):
        # write code here
        # 思路：
        # 对于二叉搜索树，中序遍历的结果就是从小到大的序列
        # 先通过中序遍历得到有序的节点列表，
        # 再修改节点的 left 和 right 指针，构建成双链表
        # 不过上述列表缓存的方法在线测试时超时了。

        if not pRootOfTree:
            return None

        self.MiddelOrderTraversal(pRootOfTree)

        # 先把链表节点有序地存储在列表里，然后修改指针指向
        # list_len = len(self.sorted_node_list)
        # for i in range(list_len):
        #     # 修改 left 和 right 指针指向
        #     self.sorted_node_list[i].left = self.sorted_node_list[(i - 1) % list_len]
        #     self.sorted_node_list[i].right = self.sorted_node_list[(i + 1) % list_len]

        return self.head_node

    def MiddelOrderTraversal(self, root):
        if root is None:
            return None

        # 递归遍历左子树
        if root.left is not None:
            self.MiddelOrderTraversal(root.left)

        # print 'root.val = ', root.val
        # self.sorted_node_list.append(root)

        # 修改当前节点 root 的 left 指针指向 pre_node
        root.left = self.pre_node
        # 若 pre_node 不为空，则修改 pre_node 的 right 指针指向当前节点 root
        if self.pre_node is not None:
            # print 'self.pre_node.val = ', self.pre_node.val
            self.pre_node.right = root

        # 记录 pre_node 为当前节点 root
        self.pre_node = root

        # 第一个找到的节点是最小节点，设为头节点
        if self.head_node is None:
            self.head_node = root

        # 递归遍历右子树
        if root.right is not None:
            self.MiddelOrderTraversal(root.right)


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

    pRootOfTree = TreeNode(7)
    pRootOfTree.left = TreeNode(3)
    pRootOfTree.left.left = TreeNode(1)
    pRootOfTree.left.right = TreeNode(4)
    pRootOfTree.right = TreeNode(9)
    pRootOfTree.right.left = TreeNode(8)
    pRootOfTree.right.right = TreeNode(10)

    answer = solution.Convert(pRootOfTree)

    pointer = answer

    count = 0
    while pointer:
        # 如果是循环链表，防止无限输出
        if count >= 10:
            break
        print pointer.val
        # pointer = pointer.left
        pointer = pointer.right
        count += 1


if __name__ == "__main__":
    sys.exit(main())

