#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：56
题目：删除链表中重复的结点

题目描述：
在一个排序的链表中，存在重复的结点，请删除该链表中重复的结点，
重复的结点不保留，返回链表头指针。
例如，链表 1->2->3->3->4->4->5 处理后为 1->2->5

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
    @staticmethod
    def delete_duplication(p_head):
        if p_head is None:
            return None

        if p_head.next is None:
            return p_head

        pointer = p_head

        node_list = []       # 依序存储结点
        value_list = []      # 依序存储结点值
        duplicate_list = []  # 依序存储结点出现次数

        while pointer is not None:
            if pointer.val in value_list:
                # 重复了，先根据重复值来找到前面的结点
                duplicate_index = value_list.index(pointer.val)

                # 前面结点的重复次数增加（可能不精确，但是重复的结点相应值至少大于 1）
                duplicate_list[duplicate_index] += 1

                # 设置当前结点的重复次数，至少大于 1
                duplicate_list.append(duplicate_list[duplicate_index])
            else:
                # 设置新出现结点的重复次数为 0
                duplicate_list.append(0)

            # 存储结点和结点值
            node_list.append(pointer)
            value_list.append(pointer.val)

            # 指针后移
            pointer = pointer.next

        # 挑出重复次数为 0 的结点
        answer_list = []
        i = 0
        while i < len(node_list):
            if duplicate_list[i] == 0:
                answer_list.append(node_list[i])
            # else:
            #     pop_node = node_list.pop(i)
            #     del pop_node
            #     i -= 1

            i += 1

        answer_len = len(answer_list)

        # 没有不重复的结点
        if answer_len <= 0:
            return None

        # 设置不重复结点的 next 指针
        i = 0
        while i < answer_len - 1:
            answer_list[i].next = answer_list[i + 1]
            i += 1

        # 设置最后一个不重复结点的 next 指针为 None
        answer_list[answer_len - 1].next = None

        # 返回头结点
        return answer_list[0]


def main():
    p_head = ListNode(1)
    p_head.next = ListNode(2)
    p_head.next.next = ListNode(3)
    p_head.next.next.next = ListNode(3)
    p_head.next.next.next.next = ListNode(4)
    p_head.next.next.next.next.next = ListNode(4)
    p_head.next.next.next.next.next.next = ListNode(5)

    start = time.process_time()
    answer = Solution.delete_duplication(p_head)
    end = time.process_time()

    while answer is not None:
        print(answer.val)
        answer = answer.next

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
