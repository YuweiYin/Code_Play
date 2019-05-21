# -*- coding:utf-8 -*-

'''
序号：14
题目：链表中倒数第k个结点

题目描述：
输入一个链表，输出该链表中倒数第k个结点。

时间限制：1秒 空间限制：32768K
本题知识点：代码的鲁棒性
'''
import sys
import getopt


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def FindKthToTail(self, head, k):
        # write code here

        if k <= 0:
            return None

        if head is None:
            return None

        # 方法一：用列表记录经过的结点
        # pointer = head
        # node_list = []
        # while pointer is not None:
        #     # 将经过的结点存储在列表里
        #     node_list.append(pointer)
        #     # 保证列表只存 k 个结点
        #     if len(node_list) > k:
        #         # 超过之后就删除先经过的（队列模式）
        #         del node_list[0]
        #     pointer = pointer.next

        # if len(node_list) == k:
        #     return node_list[0]
        # else:
        #     return None

        # 方法二：用两个相隔 k-1 的指针同步前进
        pointer1 = head
        pointer2 = head

        for i in range(k - 1):
            pointer2 = pointer2.next
            if pointer2 is None:
                return None

        while pointer2.next is not None:
            pointer1 = pointer1.next
            pointer2 = pointer2.next

        return pointer1


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
    listNode = ListNode(1)
    listNode.next = ListNode(2)
    listNode.next.next = ListNode(3)
    listNode.next.next.next = ListNode(4)
    listNode.next.next.next.next = ListNode(5)
    k = 3
    answer = solution.FindKthToTail(listNode, k)
    if answer is not None:
        print answer.val
    else:
        print None


if __name__ == "__main__":
    sys.exit(main())

