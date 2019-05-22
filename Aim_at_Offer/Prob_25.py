# -*- coding:utf-8 -*-

'''
序号：25
题目：复杂链表的复制

题目描述：
输入一个复杂链表（每个节点中有节点值，以及两个指针，
一个指向下一个节点，另一个特殊指针指向任意一个节点），
返回结果为复制后复杂链表的head。
（注意，输出结果中请不要返回参数中的节点引用，
否则判题程序会直接返回空）

时间限制：1秒 空间限制：32768K
本题知识点：链表，分解让复杂问题简单
'''
import sys
import getopt


class RandomListNode:
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None


class Solution:
    # 返回 RandomListNode
    def Clone(self, pHead):
        # write code here
        if not pHead:
            return None

        # 分解任务，递归构造，克隆链表
        pointer = pHead
        new_node = RandomListNode(pointer.label)
        new_node.random = pointer.random
        new_node.next = self.Clone(pointer.next)

        return new_node


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

    pHead = RandomListNode(1)
    pHead.next = RandomListNode(2)
    pHead.next.next = RandomListNode(3)
    pHead.next.next.next = RandomListNode(4)
    pHead.next.next.next.next = RandomListNode(5)

    answer = solution.Clone(pHead)
    while answer:
        print answer.label
        answer = answer.next


if __name__ == "__main__":
    sys.exit(main())

