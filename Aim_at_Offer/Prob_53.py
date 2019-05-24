# -*- coding:utf-8 -*-

'''
序号：53
题目：表示数值的字符串

题目描述：
请实现一个函数用来判断字符串是否表示数值（包括整数和小数）。
例如，字符串"+100","5e2","-123","3.1416"和"-1E-16"都表示数值。
但是"12e","1a3.14","1.2.3","+-5"和"12e+4.3"都不是。

时间限制：1秒 空间限制：32768K
本题知识点：字符串
'''
import sys
import getopt
import re


class Solution:
    # s字符串
    def isNumeric(self, s):
        # write code here
        # Python 完全匹配需要以 ^ 开头、并以 $ 结尾。r'' 表示不转义
        # [..] 表示多选一，(..) 小括号内为一个整体，\d 表示数字，
        # x? 表示 x 可以出现 0 次或 1 次
        # x* 表示 x 可以出现 0 次或任意正整数次
        # x+ 表示 x 可以出现任意正整数次

        return True if re.match(r'^[+-]?\d*(\.\d+)?([eE][+-]?\d+)?$', s) else False


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

    # s = '+100' # True
    s = '1a3.14'  # False

    answer = solution.isNumeric(s)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
