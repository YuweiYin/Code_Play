#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：05
题目：用两个栈实现队列

题目描述：
用两个栈来实现一个队列，完成队列的 Push 和 Pop 操作。
队列中的元素为 int 类型。

时间限制：1秒 空间限制：32768K
本题知识点：队列、栈
"""

import sys
import time


class Solution:
    def __init__(self):
        # 用 list 作为栈，入数据用 append()，出数据用 pop()
        self._stack1 = []
        self._stack2 = []

    def push(self, node):
        # write code here
        self._stack1.append(node)
        print(self._stack1)

    def pop(self):
        # return xx
        if len(self._stack1) <= 0:
            return None
        else:
            # 除了栈底元素，把栈 1 的其余数据给栈 2
            while len(self._stack1) > 1:
                self._stack2.append(self._stack1.pop())

            # 取出栈 1 的栈底元素
            pop = self._stack1.pop()

            # 把栈 2 的全部数据给栈 1
            while len(self._stack2) > 0:
                self._stack1.append(self._stack2.pop())

            return pop


def main():
    solution = Solution()

    start = time.process_time()
    solution.push(1)
    solution.push(2)
    solution.push(3)
    print(solution.pop())
    print(solution.pop())
    print(solution.pop())
    print(solution.pop())

    end = time.process_time()
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())

