# -*- coding:utf-8 -*-

'''
序号：27
题目：字符串的排列

题目描述：
输入一个字符串,按字典序打印出该字符串中字符的所有排列。
例如输入字符串abc,则打印出由字符a,b,c所能排列出来的
所有字符串abc,acb,bac,bca,cab和cba。

输入描述：
输入一个字符串,长度不超过9(可能有字符重复),字符只包括大小写字母。

时间限制：1秒 空间限制：32768K
本题知识点：字符串，分解让复杂问题简单
'''
import sys
import getopt


class Solution:
    def __init__(self):
        self.answer = []
        self.s = '' # 存储原字符串
        self.s_len = 0 # 字符串长度
        self.s_current = '' # 当前正在构造的字符串序列
        self.used = [] # 记录位置 i 相应的 s[i] 是否已经使用过了

    def Permutation(self, ss):
        # write code here

        if len(ss) <= 0:
            return []

        # 初始化类成员变量
        self.s = ss
        self.s_len = len(self.s)
        for i in range(self.s_len):
            self.s_current += '\0'
            self.used.append(False)

        # 按字典序排列原字符串
        self.s = sorted(self.s, reverse=False)        

        # 深度优先搜索，遍及所有可能的排列组合
        self.DFS(0)

        return self.answer

    def DFS(self, step):
        # 如果使用完了所有的原串字符，则存储一个构造好的新字符串
        if step == self.s_len:
            self.answer.append(self.s_current)
            return

        # 若还未构造完，则继续构造
        for i in range(self.s_len):
            # 若当前字符 s[i] 已经使用过了，则执行下一轮循环，检查下一个字符
            if self.used[i]:
                continue

            # 若当前字符 s[i] 跟前一个字符是相同的，并且前一个字符还没使用过，
            # 这时也跳过循环，否则会出现重复的 s_current
            if i >= 1 and self.s[i] == self.s[i - 1] and not self.used[i - 1]:
                continue

            # 当前字符没有被使用，且与上一个使用的字符
            # 修改 s_current 的 step 位
            temp_list = list(self.s_current)
            temp_list[step] = self.s[i]
            self.s_current = ''.join(temp_list)

            # 深度优先搜索，改变记录值
            self.used[i] = True
            self.DFS(step + 1)
            self.used[i] = False


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

    ss = 'abca'

    print solution.Permutation(ss)


if __name__ == "__main__":
    sys.exit(main())

