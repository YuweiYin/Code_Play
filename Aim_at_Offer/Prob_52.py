# -*- coding:utf-8 -*-

'''
序号：52
题目：正则表达式匹配

题目描述：
请实现一个函数用来匹配包括'.'和'*'的正则表达式。
模式中的字符'.'表示任意一个字符，而'*'表示它前面的字符可以出现任意次（包含0次）。
在本题中，匹配是指字符串的所有字符匹配整个模式。
例如，字符串"aaa"与模式"a.a"和"ab*ac*a"匹配，但是与"aa.a"和"ab*a"均不匹配

时间限制：1秒 空间限制：32768K
本题知识点：字符串
'''
import sys
import getopt
import copy
# import re


class Solution:
    # s, pattern都是字符串
    def match(self, s, pattern):
        # write code here

        # 投机取巧
        # return True if re.match('^' + pattern + '$', s) else False

        # 从左到右分析解
        return self.CoreMatch(s, pattern)

    def CoreMatch(self, s, pattern):
        # 先进行空串匹配检测
        if not self.EmptyMatch(s, pattern):
            return False

        # 从头到尾匹配，如果匹配上了就删除字符串元素和相应的模式
        while len(s) > 0 and len(pattern) > 0:
            # print s, pattern, len(s), len(pattern)
            if s[0] == pattern[0]:
                # 准确匹配上了，但模式串该字符后面有 *，所以要往后看
                if len(pattern) > 1 and pattern[1] == '*':
                    return self.TryPattern(s, pattern)

                # 准确匹配上了一个字符，且该字符后面不是 '*'
                else:
                    s = s[1: ]
                    pattern = pattern[1: ]
                    # print 'Way-3:', s, pattern

            else:
                # 用 . 来模糊匹配掉一个 s 的字符
                if pattern[0] == '.':
                    # 模糊匹配上了，但模式串该字符后面有 *，所以要往后看
                    if len(pattern) > 1 and pattern[1] == '*':
                        return self.TryPattern(s, pattern)

                    # 模糊匹配上了一个字符，且 '.' 后面不是 '*'
                    else:
                        s = s[1: ]
                        pattern = pattern[1: ]
                        # print 'Way-4:', s, pattern

                # 如果模式里的 x 不匹配，但它后面有 *，那么删去 x* 
                elif len(pattern) > 1 and pattern[1] == '*':
                    pattern = pattern[2: ]
                    # print 'Way-5:', s, pattern

                # 不匹配
                else:
                    return False

        # 如果最后原串和模式都空了，那就表示匹配成功
        if len(s) == 0 and len(pattern) == 0:
            return True
        else:
            # 否则最后进行空串匹配检测
            if len(s) == 0:
                return self.EmptyMatch(s, pattern)
            else:
                return False


    def EmptyMatch(self, s, pattern):
        # 在 s 或 pattern 为空串时判断是否匹配
        if s is None or pattern is None:
            return False

        # 如果模式串为空串 ''，那么只有在 s 也为空串 '' 时能匹配成功
        if len(pattern) <= 0:
            if len(s) <= 0:
                return True
            else:
                return False

        # 在 s 为空串 '' 时的模式匹配方法
        if len(s) <= 0:
            # 通过前面的判断语句，此时模式串肯定不为空串了
            # 需遍历模式串，如果每个普通字符或者'.'字符后面
            # 都有一个'*'，则匹配成功，否则匹配失败

            # 如果模式串有奇数个字符，无论如何都不会匹配上 ''
            if (len(pattern) % 2) == 1:
                return False

            i = 0
            while i < len(pattern):
                # 不应出现 '*' 开头的匹配模式
                if pattern[i] == '*':
                    return False

                # 此时模式串至少有两个字符，可以直接寻址 i + 1 不怕越界
                elif pattern[i + 1] == '*':
                    # 如果当前出现的字符后面跟着一个 '*'，则可以匹配，继续往后看
                    i += 2

                # 表示当前出现的字符后面没有跟着一个 '*'，则不可以匹配空串
                else:
                    return False

            # 表示匹配上了
            return True

        # 此时返回的 True 只是表示无异常
        return True


    # 在出现 'x*' 的匹配情况下，尝试所有可能的 x 出现次数来进行模式匹配
    def TryPattern(self, s, pattern):
        # 找到字符串后面第一个不符合此模式的字符
        i = 1
        match_len = 1

        while i < len(s) and (s[i] == pattern[0] or pattern[0] == '.'):
            # 记录最多能够连续匹配多少个字符
            match_len += 1
            i += 1

        # print 'match_len:', match_len

        # 能连续匹配多少个字符，就有多少种可能，分别考虑
        j = match_len
        while j >= 0:
            pat_temp = copy.deepcopy(pattern[2: ])
            k = 0
            while k < j:
                pat_temp = pattern[0] + pat_temp
                k += 1

            # print '尝试 pat_temp:', pat_temp

            # 在该可能下，往下匹配
            if self.CoreMatch(s, pat_temp):
                # print 'pat_temp 匹配成功'
                return True

            else:
                # print 'pat_temp 匹配失败'
                del pat_temp
                j -= 1

        # 所有匹配模式都无法成功，所以最终匹配失败
        return False


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

    s = 'aaabaaaa'
    pattern = 'a*a.ba*a' # True

    # s = 'aaa'
    # pattern = 'a.a' # True
    # pattern = 'ab*ac*a' # True
    # pattern = 'aa.a' # False
    # pattern = 'ab*a' # False

    # s = ''
    # pattern = '.' # False
    # pattern = '.*q*' # True

    # s = 'a'
    # pattern = '.' # True
    # pattern = '.*' # True
    # pattern = '.*a' # True
    # pattern = '.*q' # False

    # s = 'aa'
    # s = 'ab'
    # pattern = '.' # False
    # pattern = '..' # True
    # pattern = '.*' # True

    answer = solution.match(s, pattern)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())
