# -*- coding:utf-8 -*-

'''
序号：60
题目：按之字形顺序打印二叉树

题目描述：
从上到下按层打印二叉树，同一层结点从左至右输出。每一层输出一行。

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
    # 返回二维列表[[1,2],[4,5]]
    def Print(self, pRoot):
        # write code here
        if pRoot is None:
            return []

        answer = [] # 最终答案序列，二维数组
        answer_list = [] # 输出结果序列
        node_list = [] # 宽度优先搜索 BFS 遍历队列
        node_list.append(pRoot)

        if pRoot.left is None and pRoot.right is None:
            answer_list.append(pRoot.val)
            answer.append(answer_list)
            return answer

        while node_list:
            value_list = [] # 本轮的结点值列表
            next_node_list = [] # 下一层的结点列表

            # 每个 while 循环体内处理一整层结点
            for item in node_list:
                # 将该层的所有结点值顺序取出来，存储于 value_list
                value_list.append(item.val)

                # 将该层结点的所有孩子结点取出来，存储于 next_node_list
                if item.left is not None:
                    next_node_list.append(item.left)

                if item.right is not None:
                    next_node_list.append(item.right)

            node_list = next_node_list # 下个 while 循环处理下一层的结点
            answer_list.append(value_list) # 把本层的结点值列表放到 answer_list

            del value_list
            del next_node_list

        # 此时将每层的结点值列表存储于 answer_list 中了
        return answer_list


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

    answer = solution.Print(pRoot)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
