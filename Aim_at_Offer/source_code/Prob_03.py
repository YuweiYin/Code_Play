#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：03
题目：从尾到头打印链表

题目描述：
输入一个链表，按链表值从尾到头的顺序返回一个 ArrayList。

时间限制：1秒 空间限制：32768K
本题知识点：链表
"""

import sys
import time


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    # 解题思路：
    # 先把链表的值依序存储在 old_list 列表里，
    # 再逆序把 old_list 的值存储到 new_list 里
    @staticmethod
    def print_list_from_tail_to_head(list_node):
        # 返回值解释：返回从尾部到头部的列表值序列，例如[1, 2, 3]
        old_list = []
        new_list = []
        pointer = list_node
        while pointer is not None:
            old_list.append(pointer.val)
            if pointer.next is not None:
                pointer = pointer.next
            else:
                break

        for i in range(len(old_list)):
            new_list.append(old_list.pop())

        return new_list


def main():
    list_node = ListNode(1)
    list_node.next = ListNode(2)
    list_node.next.next = ListNode(3)

    start = time.process_time()
    ans = Solution.print_list_from_tail_to_head(list_node)
    end = time.process_time()

    print(ans)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
