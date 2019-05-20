# -*- coding:utf-8 -*-

'''
序号：05
题目：用两个栈实现队列

题目描述：
用两个栈来实现一个队列，完成队列的Push和Pop操作。
队列中的元素为int类型。

时间限制：1秒 空间限制：32768K
本题知识点：队列、栈
'''
import sys
import getopt


class Solution:
    def __init__(self):
        # 用 list 作为栈，入数据用 append()，出数据用 pop()
        self._stack1 = []
        self._stack2 = []
    def push(self, node):
        # write code here
        self._stack1.append(node)
        print self._stack1
    def pop(self):
        # return xx
        if len(self._stack1) <= 0:
            return None
        else:
            # 除了栈底元素，把栈1的其余数据给栈2
            while len(self._stack1) > 1:
                self._stack2.append(self._stack1.pop())

            # 取出栈1的栈底元素
            pop = self._stack1.pop()

            # 把栈2的全部数据给栈1
            while len(self._stack2) > 0:
                self._stack1.append(self._stack2.pop())

            return pop


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
    solution.push(1)
    solution.push(2)
    solution.push(3)
    print solution.pop()
    print solution.pop()
    print solution.pop()
    print solution.pop()


if __name__ == "__main__":
    sys.exit(main())

