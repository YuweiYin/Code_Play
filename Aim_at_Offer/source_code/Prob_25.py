#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：25
题目：复杂链表的复制

题目描述：
输入一个复杂链表（每个节点中有节点值，以及两个指针，
一个指向下一个节点，另一个特殊指针指向任意一个节点），
返回结果为复制后复杂链表的 head。
（注意，输出结果中请不要返回参数中的节点引用，
否则判题程序会直接返回空）

时间限制：1秒 空间限制：32768K
本题知识点：链表，分解让复杂问题简单
"""

import sys
import time


class RandomListNode:
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None


class Solution:
    def clone(self, p_head):
        if not p_head:
            return None

        # 分解任务，递归构造，克隆链表
        pointer = p_head
        new_node = RandomListNode(pointer.label)
        new_node.random = pointer.random
        new_node.next = self.clone(pointer.next)

        # 返回 RandomListNode
        return new_node


def main():
    solution = Solution()

    p_head = RandomListNode(1)
    p_head.next = RandomListNode(2)
    p_head.next.next = RandomListNode(3)
    p_head.next.next.next = RandomListNode(4)
    p_head.next.next.next.next = RandomListNode(5)

    start = time.process_time()
    answer = solution.clone(p_head)
    end = time.process_time()

    while answer:
        print(answer.label)
        answer = answer.next

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
