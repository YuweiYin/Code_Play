# -*- coding:utf-8 -*-

'''
序号：55
题目：链表中环的入口结点

题目描述：
给一个链表，若其中包含环，请找出该链表的环的入口结点，否则，输出null。

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
    def EntryNodeOfLoop(self, pHead):
        # write code here
        # 思路：快慢双指针
        # 两个指针从链表头出发，慢指针一次走一步，快指针一次走两步
        # 如果快指针到达 None，则表示无环
        # 如果有环，两指针必能在环内相遇，
        # 在相遇之后让其中一个指针回到链表头，然后让二者一次一步前进
        # 再次相遇的点就是环的入口结点，数学证明如下：

        # 假设有环，且环的长度至少为 2，设环长度为 y，设非环部分的长度为 x
        # 设第一次相遇时快/慢指针分别绕了环 i/j 圈，相对于环入口前进了 n - 1 步
        # 所以慢指针总共走了 x + n + i * y 的长度，快指针走了 x + n + j * y 的长度
        # 易知 2 * (x + n + i * y) = x + n + j * y，
        # 所以 x = (j - 2 * i) * y - n
        # 所以把其中一个指针放回链表首部，往前走 x 步，另一个指针走相同步数就等于
        # 弥补了未经过的环长度（可能会绕几圈），最终恰好到达了环入口
        if pHead is None:
            return None

        # 最小环情况
        if pHead.next == pHead:
            return pHead

        p_fast = pHead # 快指针
        p_slow = pHead # 慢指针

        while p_fast is not None and p_slow is not None:
            # 快慢指针一快一慢前进
            p_slow = p_slow.next
            if p_fast.next is not None:
                p_fast = p_fast.next.next
            else:
                return None

            # 第一次相遇了
            if p_slow == p_fast:
                # 让慢纸质指回链表首部 pHead
                p_slow = pHead

                # 让两个指针均以一次一步的速度前进，直到相遇
                while p_slow != p_fast:
                    p_slow = p_slow.next
                    p_fast = p_fast.next

                # 相遇后，返回环入口结点
                return p_slow

        return None


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
    pHead.next.next.next.next.next = ListNode(6) # Entry Node Of Loop
    pHead.next.next.next.next.next.next = ListNode(7)
    pHead.next.next.next.next.next.next.next = ListNode(8)
    pHead.next.next.next.next.next.next.next.next = pHead.next.next.next.next.next

    answer = solution.EntryNodeOfLoop(pHead)

    if answer is not None:
        print answer.val
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
