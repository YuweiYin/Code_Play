#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：59
题目：按之字形顺序打印二叉树

题目描述：
请实现一个函数按照之字形打印二叉树，即第一行按照从左到右的顺序打印，
第二层按照从右至左的顺序打印，第三行按照从左到右的顺序打印，其他行以此类推。

时间限制：1秒 空间限制：32768K
本题知识点：树
"""

import sys
import time
# import gc


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    @staticmethod
    def z_print(p_root):
        if p_root is None:
            return []

        answer = []       # 最终答案序列，二维数组
        answer_list = []  # 输出结果序列
        node_list = [p_root]  # 宽度优先搜索 BFS 遍历队列

        # 根结点无子结点的情况
        if p_root.left is None and p_root.right is None:
            answer_list.append(p_root.val)
            answer.append(answer_list)
            return answer

        while node_list:
            value_list = []      # 本轮的结点值列表
            next_node_list = []  # 下一层的结点列表

            # 每个 while 循环体内处理一整层结点
            for item in node_list:
                # 将该层的所有结点值顺序取出来，存储于 value_list
                value_list.append(item.val)

                # 将该层结点的所有孩子结点取出来，存储于 next_node_list
                if item.left is not None:
                    next_node_list.append(item.left)

                if item.right is not None:
                    next_node_list.append(item.right)

            node_list = next_node_list  # 下个 while 循环处理下一层的结点
            answer_list.append(value_list)  # 把本层的结点值列表放到 answer_list

            # del value_list
            # del next_node_list
            # gc.collect()

        # 此时将每层的结点值列表存储于 answer_list 中了
        # 只需按奇偶层分开，不同顺序打印结果就行了
        if answer_list is None:
            return []

        for index, item in enumerate(answer_list):
            # 偶数列顺序打印
            if index % 2 == 0:
                answer.append(item)
            # 奇数列逆序打印
            else:
                answer.append(item[::-1])

        return answer


def main():
    solution = Solution()

    p_root = TreeNode(8)
    p_root.left = TreeNode(6)
    p_root.right = TreeNode(10)
    p_root.left.left = TreeNode(5)
    p_root.left.right = TreeNode(7)
    p_root.right.left = TreeNode(9)
    p_root.right.right = TreeNode(11)

    start = time.process_time()
    answer = solution.z_print(p_root)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
