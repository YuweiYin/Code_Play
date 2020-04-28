#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：36
题目：两个链表的第一个公共结点

题目描述：
输入两个链表，找出它们的第一个公共结点。

时间限制：1秒 空间限制：32768K
本题知识点：链表，时间空间效率的平衡
"""

import sys
import time


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    @staticmethod
    def find_first_common_node(p_head1, p_head2):
        if p_head1 is None or p_head2 is None:
            return None

        pointer1 = p_head1
        pointer2 = p_head2

        # 让 pointer1/2 分别从链表 1/2 出发，走到尽头就转到另一个链表的首部
        # 设 c = 链表的公共部分长度 a = len(pHead1) - c, b = len(pHead2) - c
        # 那么 pointer1 走过 a + c + b 的路途时，pointer2 走过 b + c + a 的路途
        # 如果两个链表有公共部分，这时二者应该处于同一结点，也即是目标结点
        # 如果两个链表没有公共部分，即 c = 0，那么两个指针在走过 a + b 的路途后，
        # 都到达链表尾部，指针为 None，还是相等，跳出循环
        # 相等的条件：二者皆为 None， 或者二者为相同结点
        while pointer1 != pointer2:
            if pointer1 is None:
                # pointer1 走到了链表尾，转去从链表 2 出发
                pointer1 = p_head2
            else:
                # pointer1 往后走
                pointer1 = pointer1.next
            
            if pointer2 is None:
                # pointer2 走到了链表尾，转去从链表 1 出发
                pointer2 = p_head1
            else:
                # pointer2 往后走
                pointer2 = pointer2.next

        return pointer1


def main():
    p_head1 = ListNode(1)
    p_head1.next = ListNode(3)
    p_head1.next.next = ListNode(6)
    p_head1.next.next.next = ListNode(7)
    p_head1.next.next.next.next = ListNode(9)

    p_head2 = ListNode(2)
    p_head2.next = ListNode(4)
    p_head2.next.next = p_head1.next.next.next

    start = time.process_time()
    answer = Solution.find_first_common_node(p_head1, p_head2)
    end = time.process_time()

    if answer is not None:
        print(answer.val)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
