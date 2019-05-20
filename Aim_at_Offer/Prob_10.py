# -*- coding:utf-8 -*-

'''
序号：10
题目：矩形覆盖

题目描述：
我们可以用2*1的小矩形横着或者竖着去覆盖更大的矩形。
请问用n个2*1的小矩形无重叠地覆盖一个2*n的大矩形，
总共有多少种方法？

时间限制：1秒 空间限制：32768K
本题知识点：递归和循环
'''
import sys
import getopt


class Solution:
    def rectCover(self, number):
        # write code here
        # 思路：（和08青蛙跳台阶题很类似）
        # 以 ::::: 代表 2*n 的大矩形，
        # 要么以竖着的单个 : 排列，
        # 要么两个小矩形叠成 :: 来排列，
        # 转化成排列组合问题
        count = 0
        for i in range(number):
            if (number - i) < i:
                break
            else:
                count += self.comb(number - i, i)

        return count

    def comb(self, n, m):
        if m <= 0:
            return 1

        if m == 1 or m == (n - 1):
            return n

        if n <= m:
            return 1

        molecular = 1
        denominator = 1
        temp = n
        for i in range(m):
            molecular *= temp
            temp -= 1

        temp = m
        while temp > 0:
            denominator *= temp
            temp -= 1

        return molecular / denominator


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
    number = 5
    print solution.rectCover(number)


if __name__ == "__main__":
    sys.exit(main())

