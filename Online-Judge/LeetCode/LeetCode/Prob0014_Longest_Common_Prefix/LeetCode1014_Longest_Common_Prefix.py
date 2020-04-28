# -*- coding:utf-8 -*-

'''
题集：LeetCode
序号：14
题目：最长公共前缀 Longest Common Prefix

题目描述：
编写一个函数来查找字符串数组中的最长公共前缀。
如果不存在公共前缀，返回空字符串 ""。
Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "".
'''
import sys
import getopt


class Solution:
    def longestCommonPrefix(self, strs):
        return self.solution1(strs)


    # 方法一
    def solution1(self, strs):
        if not strs:
            return ""

        # 从左到右按字母序排列，得到最大值和最小值
        s_min = min(strs)
        s_max = max(strs)

        for index, item in enumerate(s_min):
            # 只要短串的某字符与长串的该位字符不匹配了，就说明前缀匹配到头了
            if item != s_max[index]:
                # 那么之前的子串就是最长前缀
                return s_max[:index]

        return s_min


    # 方法二
    def solution2(self, strs):
        if not strs:
            return ""
        # 先用 zip 函数将迭代器 *strs 中的各个可迭代对象的各个元素压缩成元组
        # 如果 strs 中的字符串长度不相等，zip 函数只会取最短长度
        # 然后用 map 函数对各个元组进行 set 函数操作，构造成无重复的集合。重复则删掉
        # 最后用 list 函数将这些集合排成列表，赋值给 set_list
        set_list = list(map(set, zip(*strs)))

        res = ""
        for index, item in enumerate(set_list):
            # 将集合内的各个元素排成列表
            item = list(item)

            # 如果集合元素个数大于 1，就表示到此为止，前缀不匹配了
            if len(item) > 1:
                break

            # 否则前缀是匹配的，那就将该字符加入到结果 res 中
            res = res + item[0]

        return res


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

    strs = ["flower", "flow", "flight"]

    print solution.longestCommonPrefix(strs)


if __name__ == "__main__":
    sys.exit(main())
