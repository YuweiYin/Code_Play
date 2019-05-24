# -*- coding:utf-8 -*-

'''
序号：54
题目：字符流中第一个不重复的字符

题目描述：
请实现一个函数用来找出字符流中第一个只出现一次的字符。
例如，当从字符流中只读出前两个字符"go"时，第一个只出现一次的字符是"g"。
当从该字符流中读出前六个字符“google"时，第一个只出现一次的字符是"l"。

输出描述：
如果当前字符流没有存在出现一次的字符，返回#字符。

时间限制：1秒 空间限制：32768K
本题知识点：字符串
'''
import sys
import getopt


class Solution:
    def __init__(self):
        self.char_list = []

    # 返回对应char
    def FirstAppearingOnce(self):
        # write code here
        if self.char_list is None or len(self.char_list) <= 0:
            return '#'

        c_len = len(self.char_list)

        # 列表长度为 1，直接返回这个唯一的元素
        if c_len == 1:
            return self.char_list[0]

        # 用字典来存储每个字符出现的次数
        i = 0
        dic = dict()
        while i < c_len:
            if self.char_list[i] in dic:
                dic[self.char_list[i]] += 1
            else:
                dic[self.char_list[i]] = 1
            i += 1

        # 再遍历一遍，找出第一个出现次数为 1 的字符
        i = 0
        while i < c_len:
            if dic[self.char_list[i]] == 1:
                return self.char_list[i]
            i += 1

        return '#'

    def Insert(self, char):
        # write code here
        self.char_list.append(char)


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

    solution.Insert('g')
    solution.Insert('o')

    print solution.FirstAppearingOnce()

    solution.Insert('o')
    solution.Insert('g')
    solution.Insert('l')
    solution.Insert('e')

    print solution.FirstAppearingOnce()

    # if answer is not None:
    #     print answer
    # else:
    #     print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
