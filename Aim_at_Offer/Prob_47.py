# -*- coding:utf-8 -*-

'''
序号：47
题目：求1+2+3+...+n

题目描述：
求1+2+3+...+n，要求不能使用乘除法、for、while、if、else、switch、case
等关键字及条件判断语句（A?B:C）。

时间限制：1秒 空间限制：32768K
本题知识点：发散思维能力
'''
import sys
import getopt


class Solution:
    def __init__(self):
        self.n_sum = 0

    def Sum_Solution(self, n):
        # write code here
        # 思路：
        # 不能用循环语句，就用函数递归替代。
        # 不能用判断语句，就用逻辑短路替代。

        # 由于默认递归深度不到 1000，递归深度太深会报错
        # maximum recursion depth exceeded
        # 因此需要手动修改递归调用深度
        sys.setrecursionlimit(1000000)

        return self.Sum(n)

    def Sum(self, n):
        # Python 在 3.7 版本前，不允许在判断语句中赋值
        # 不能使用语句 n == 0 or (current_sum += self.Sum_Solution(n - 1)) > 0
        # 转而利用类成员变量和函数来完成该过程
        n == 0 or (self.Add(n, self.Sum_Solution(n - 1))) > 0

        # 在递归栈底 n == 0 时第一次到达此处，所以返回值从 0 开始累积，
        # 前面都不会被逻辑短路，所以都会执行 self.Add 函数
        return self.n_sum

    def Add(self, current_number, next_sum):
        self.n_sum += current_number
        # print current_number, next_sum, self.n_sum
        return next_sum


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

    n = 1000

    answer = solution.Sum_Solution(n)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

