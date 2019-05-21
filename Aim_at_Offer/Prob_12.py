# -*- coding:utf-8 -*-

'''
序号：12
题目：数值的整数次方

题目描述：
给定一个double类型的浮点数base和int类型的整数exponent。
求base的exponent次方。

时间限制：1秒 空间限制：32768K
本题知识点：代码的完整性
'''
import sys
import getopt


class Solution:
    def Power(self, base, exponent):
        # write code here
        power = 1
        if exponent == 0:
            # 指数为 0，结果为 1
            return 1
        elif exponent > 0:
            # 正指数
            for i in range(exponent):
                power *= base
        else:
            # 负指数
            base = 1 / float(base)
            for i in range(-exponent):
                power *= base

        return power

        # 直接调用内置函数 pow 也可以
        # return pow(base, exponent)


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
    base = 2
    exponent = -3
    print solution.Power(base, exponent)


if __name__ == "__main__":
    sys.exit(main())

