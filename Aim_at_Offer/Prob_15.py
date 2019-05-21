# -*- coding:utf-8 -*-

'''
序号：15
题目：反转链表

题目描述：
输入一个链表，反转链表后，输出新链表的表头。

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
    # 返回ListNode
    def ReverseList(self, pHead):
        # write code here
        if pHead is None:
            return None

        if pHead.next is None:
            return pHead

        # 方法一：将经过的结点值存储在列表里
        # 然后反向构造一个新链表。丢弃原链表
        pointer = pHead
        node_list = []
        while pointer is not None:
            # 将经过的结点值存储在列表里
            node_list.append(pointer.val)
            pointer = pointer.next

        list_len = len(node_list)
        newHead = ListNode(node_list[list_len - 1])
        pointer = newHead
        for i in range(list_len - 1):
            pointer.next = ListNode(node_list[list_len - 2 - i])
            pointer = pointer.next

        return newHead

        # 方法二：一次遍历过程中，不断修改 next 指针指向
        # pointer1 = pHead
        # pointer2 = pHead.next
        # pointer3 = pointer2

        # while pointer2.next is not None:
        #     pointer3 = pointer2.next
        #     pointer2.next = pointer1

        #     pointer1 = pointer2
        #     pointer2 = pointer3

        # # 此时，pointer2 走到了最后一个结点，只需修改该结点的 next
        # pointer2.next = pointer1

        # # 并且把原链表首结点的 next 指针置空
        # pHead.next = None

        # return pointer2


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
    pHead = ListNode(1)
    pHead.next = ListNode(2)
    pHead.next.next = ListNode(3)
    pHead.next.next.next = ListNode(4)
    pHead.next.next.next.next = ListNode(5)

    answer = solution.ReverseList(pHead)

    pointer = answer
    while pointer is not None:
        print pointer.val
        pointer = pointer.next


if __name__ == "__main__":
    sys.exit(main())

