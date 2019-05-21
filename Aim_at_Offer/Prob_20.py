# -*- coding:utf-8 -*-

'''
序号：20
题目：包含min函数的栈

题目描述：
定义栈的数据结构，请在该类型中实现一个能够得到栈中
所含最小元素的min函数（时间复杂度应为O（1））。

时间限制：1秒 空间限制：32768K
本题知识点：栈，举例让抽象具体化
'''
import sys
import getopt


class Solution:
    def __init__(self):
        self.stack = []
        self.sorted_list = []

    def push(self, node):
        # write code here
        self.stack.append(node)
        self.sorted_list.append(node)
        self.sorted_list = sorted(self.sorted_list, reverse=False)

    def pop(self):
        # write code here
        stack_len = len(self.stack)
        pop = self.stack[stack_len - 1]
        del self.stack[stack_len - 1]
        self.sorted_list.remove(pop) # 按值删除元素
        return pop

    def top(self):
        # write code here
        return self.stack[len(self.stack) - 1]

    def min(self):
        # write code here
        return self.sorted_list[0]

    def display(self):
        print self.stack
        print self.sorted_list


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

    solution.push(3)
    solution.push(2)
    solution.push(1)
    print solution.pop()
    solution.push(4)

    print solution.top()
    print solution.min()

    solution.display()


if __name__ == "__main__":
    sys.exit(main())

