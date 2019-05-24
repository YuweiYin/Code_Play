# -*- coding:utf-8 -*-

'''
序号：44
题目：翻转单词顺序列

题目描述：
牛客最近来了一个新员工Fish，
每天早晨总是会拿着一本英文杂志，写些句子在本子上。
同事Cat对Fish写的内容颇感兴趣，有一天他向Fish借来翻看，
但却读不懂它的意思。例如，“student. a am I”。
后来才意识到，这家伙原来把句子单词的顺序翻转了，
正确的句子应该是“I am a student.”。
Cat对一一的翻转这些单词顺序可不在行，你能帮助他么？

时间限制：1秒 空间限制：32768K
本题知识点：字符串，知识迁移能力
'''
import sys
import getopt


class Solution:
    def ReverseSentence(self, s):
        # write code here
        if s is None or len(s) <= 0:
            return ''

        # 本题默认用空格分开单词
        if s.find(' ') >= 0:
            # 如果有空格，通过 split 分开单词
            s_list = s.split(' ')
            # 翻转列表顺序
            s_list.reverse()
            # 加入空格合成新字符串
            return ' '.join(s_list)

        else:
            # 如果 s 中没有空格分开，那就直接输出 s
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

    s = 'student. a am I' # 'I am a student.'
    # s = 'Hello.' # 'Hello.'
    # s = 'Hello. ' # ' Hello.'
    # s = '' # ''
    # s = ' ' # ' '
    # s = '   ' # '   '

    answer = solution.ReverseSentence(s)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

