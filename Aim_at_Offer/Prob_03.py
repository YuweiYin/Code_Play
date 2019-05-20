# -*- coding:utf-8 -*-

'''
序号：03
题目：从尾到头打印链表

题目描述：
输入一个链表，按链表值从尾到头的顺序返回一个ArrayList。

时间限制：1秒 空间限制：32768K
本题知识点：链表
'''
import sys
import getopt


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
        # write code here
        # 先把链表的值依序存储在 old_list 列表里，
        # 再逆序把 old_list 的值存储到 new_list 里
        old_list = []
        new_list = []
        pointer = listNode
        while pointer is not None:
            old_list.append(pointer.val)
            if pointer.next is not None:
                pointer = pointer.next
            else:
                break

        for i in range(len(old_list)):
            new_list.append(old_list.pop())

        return new_list


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
    listNode = ListNode(1)
    listNode.next = ListNode(2)
    listNode.next.next = ListNode(3)
    solution = Solution()
    print solution.printListFromTailToHead(listNode)


if __name__ == "__main__":
    sys.exit(main())

