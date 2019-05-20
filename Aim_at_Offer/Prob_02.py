# -*- coding:utf-8 -*-

'''
序号：02
题目：替换空格

题目描述：
请实现一个函数，将一个字符串中的每个空格替换成“%20”。
例如，当字符串为We Are Happy.则经过替换之后的字符串为We%20Are%20Happy。

时间限制：1秒 空间限制：32768K
本题知识点：字符串
'''
import sys
import getopt


class Solution:
    # s 源字符串
    def replaceSpace(self, s):
        # write code here
        if s.find(' ') >= 0:
            s_list = s.split(' ')
            s = '%20'.join(s_list)
        return s


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
    s = "We Are Happy."
    print solution.replaceSpace(s)


if __name__ == "__main__":
    sys.exit(main())

