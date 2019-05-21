# -*- coding:utf-8 -*-

'''
序号：16
题目：合并两个排序的链表

题目描述：
输入两个单调递增的链表，输出两个链表合成后的链表，
当然我们需要合成后的链表满足单调不减规则。

时间限制：1秒 空间限制：32768K
本题知识点：链表，代码的鲁棒性
'''
import sys
import getopt


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    # 返回合并后列表
    def Merge(self, pHead1, pHead2):
        # write code here
        if pHead1 is None:
            return pHead2

        if pHead2 is None:
            return pHead1

        # 方法一：将经过的结点值存储在列表里
        # 然后合并构造一个新链表。丢弃原链表
        list1 = []
        list2 = []

        pointer1 = pHead1
        pointer2 = pHead2

        while pointer1 is not None:
            list1.append(pointer1.val)
            pointer1 = pointer1.next

        while pointer2 is not None:
            list1.append(pointer2.val)
            pointer2 = pointer2.next

        new_list = sorted(list1 + list2, reverse=False)

        new_head = ListNode(new_list[0])
        new_pointer = new_head
        print new_pointer.val
        for i in range(len(new_list) - 1):
            new_pointer.next = ListNode(new_list[i + 1])
            new_pointer = new_pointer.next

        return new_head

        # TODO 方法二：遍历并不断修改指针指向（未完）
        # pointer1 = pHead1
        # pointer2 = pHead2

        # # 交换 pointer1 和 pointer2，让首元素更小的做 pointer1
        # if pointer1.val > pointer2.val:
        #     temp = pointer1
        #     pointer1 = pointer2
        #     pointer2 = temp

        # newHead = pointer1
        # while pointer1 is not None:
        #     while pointer2 is not None:
        #         if pointer2.val > pointer1.val:
        #             if pointer1.next is None:
        #                 # 链表 1 到末尾了，直接把链表 2 接到后面
        #                 pointer1.next = pointer2
        #                 return newHead
        #             else:

        # return newHead


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
    pHead1 = ListNode(1)
    pHead1.next = ListNode(3)
    pHead1.next.next = ListNode(5)
    pHead1.next.next.next = ListNode(7)
    pHead1.next.next.next.next = ListNode(9)

    pHead2 = ListNode(2)
    pHead2.next = ListNode(4)
    pHead2.next.next = ListNode(6)
    pHead2.next.next.next = ListNode(7)
    pHead2.next.next.next.next = ListNode(10)

    answer = solution.Merge(pHead1, pHead2)

    pointer = answer
    while pointer is not None:
        print pointer.val
        pointer = pointer.next


if __name__ == "__main__":
    sys.exit(main())

