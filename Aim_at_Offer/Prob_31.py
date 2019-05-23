# -*- coding:utf-8 -*-

'''
序号：31
题目：整数中1出现的次数（从1到n整数中1出现的次数）

题目描述：
求出1~13的整数中1出现的次数,并算出100~1300的整数中1出现的次数？
为此他特别数了一下1~13中包含1的数字有1、10、11、12、13因此共出现6次,
但是对于后面问题他就没辙了。ACMer希望你们帮帮他,并把问题更加普遍化,
可以很快的求出任意非负整数区间中1出现的次数（从1 到 n 中1出现的次数）。

时间限制：1秒 空间限制：32768K
本题知识点：时间效率
'''
import sys
import getopt


class Solution:
    def NumberOf1Between1AndN_Solution(self, n):
        # write code here
        if n <= 0:
            return 0

        if n == 1:
            return 1

        # 方法1: 数字转字符串，连接存储在一起，最后 count
        # n_str = ''
        # i = 1
        # while i <= n:
        #     n_str += str(i)
        #     i += 1

        # return n_str.count('1', 0, len(n_str))

        # 方法2: 循环内每次都 count
        count = 1
        i = 2
        while i <= n:
            count += str(i).count('1')
            i += 1

        return count


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

    n = 1300

    print solution.NumberOf1Between1AndN_Solution(n)


if __name__ == "__main__":
    sys.exit(main())

