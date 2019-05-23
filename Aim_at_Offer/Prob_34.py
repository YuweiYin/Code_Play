# -*- coding:utf-8 -*-

'''
序号：34
题目：第一个只出现一次的字符

题目描述：
在一个字符串(0<=字符串长度<=10000，
全部由字母组成)中找到第一个只出现一次的字符,并返回它的位置, 
如果没有则返回 -1（需要区分大小写）。

时间限制：1秒 空间限制：32768K
本题知识点：字符串，时间空间效率的平衡
'''
import sys
import getopt


class Solution:
    def FirstNotRepeatingChar(self, s):
        # write code here
        if s is None or len(s) <= 0:
            return -1

        # s 仅有一个字符，直接返回之
        s_len = len(s)
        if s_len == 1:
            return s[0]

        # 遍历一遍，对于字符串首的元素，查找是否重复
        s_temp = s
        while s_temp is not None:
            # 如果仅剩一个字符，结果就是该字符了
            if len(s_temp) == 1:
                return s.find(s_temp[0])

            # 如果有重复，就删去所有的该元素，并继续观察字符串首
            if s_temp.find(s_temp[0], 1) > 0:
                s_temp = s_temp.replace(s_temp[0], '')
                # print s_temp

            # 如果不重复，就输出该首位元素在原串 s 中的下标位置
            else:
                return s.find(s_temp[0])

        return -1


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

    s = 'abbcdfgeafce' # d 4
    # s = 'abbcadc' # d 5

    print solution.FirstNotRepeatingChar(s)


if __name__ == "__main__":
    sys.exit(main())

