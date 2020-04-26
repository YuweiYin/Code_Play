#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：15
题目：反转链表

题目描述：
输入一个链表，反转链表后，输出新链表的表头。

时间限制：1秒 空间限制：32768K
本题知识点：链表，代码的鲁棒性
"""

# import gc
import sys
import time


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    @staticmethod
    def reverse_list(p_head):
        if p_head is None:
            return None

        if p_head.next is None:
            return p_head

        # 方法一：将经过的结点值存储在列表里
        # 然后反向构造一个新链表。丢弃原链表
        pointer = p_head
        node_list = []
        while pointer is not None:
            # 将经过的结点值存储在列表里
            node_list.append(pointer.val)
            pointer = pointer.next

        # # 可选：回收内存空间
        # pointer1 = p_head
        # pointer2 = p_head.next
        # while pointer2 is not None:
        #     # 删除不再使用的链表元素
        #     del pointer1
        #     pointer1 = pointer2
        #     pointer2 = pointer2.next
        #
        # del pointer1
        # gc.collect()

        list_len = len(node_list)
        new_head = ListNode(node_list[list_len - 1])
        pointer = new_head
        for i in range(list_len - 1):
            pointer.next = ListNode(node_list[list_len - 2 - i])
            pointer = pointer.next

        return new_head

        # # 方法二：一次遍历过程中，不断修改 next 指针指向
        # pointer1 = p_head
        # pointer2 = p_head.next
        # pointer3 = pointer2
        #
        # while pointer2.next is not None:
        #     pointer3 = pointer2.next
        #     pointer2.next = pointer1
        #
        #     pointer1 = pointer2
        #     pointer2 = pointer3
        #
        # # 此时，pointer2 走到了最后一个结点，只需修改该结点的 next
        # pointer2.next = pointer1
        #
        # # 并且把原链表首结点的 next 指针置空
        # p_head.next = None
        #
        # return pointer2


def main():
    p_head = ListNode(1)
    p_head.next = ListNode(2)
    p_head.next.next = ListNode(3)
    p_head.next.next.next = ListNode(4)
    p_head.next.next.next.next = ListNode(5)

    start = time.process_time()
    answer = Solution.reverse_list(p_head)
    end = time.process_time()

    pointer = answer
    while pointer is not None:
        print(pointer.val)
        pointer = pointer.next

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
