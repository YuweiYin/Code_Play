# -*- coding:utf-8 -*-

'''
序号：07
题目：斐波那契数列

题目描述：
大家都知道斐波那契数列，现在要求输入一个整数n，
请你输出斐波那契数列的第n项（从0开始，第0项为0）。
n<=39

时间限制：1秒 空间限制：32768K
本题知识点：递推
'''
import sys
import getopt


class Solution:
    def Fibonacci(self, n):
        # write code here
        # 递归方式太慢了，时间复杂度高
        # if n == 0:
        #     return 0
        # elif n <= 2:
        #     return 1
        # else:
        #     return self.Fibonacci(n - 2) + self.Fibonacci(n - 1)

        # 缓存中间结果，O(n)的空间代价
        if n == 0:
            return 0
        elif n <= 2:
            return 1
        number_list = [0, 1, 1]
        for i in range(n - 1):
            # print i, number_list[i + 1], number_list[i + 2]
            number_list.append(number_list[i + 1] + number_list[i + 2])

        return number_list[n]


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
    n = 39
    print solution.Fibonacci(n)


if __name__ == "__main__":
    sys.exit(main())

