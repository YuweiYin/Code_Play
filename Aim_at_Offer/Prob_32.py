# -*- coding:utf-8 -*-

'''
序号：32
题目：把数组排成最小的数

题目描述：
输入一个正整数数组，把数组里所有数字拼接起来排成一个数，
打印能拼接出的所有数字中最小的一个。例如输入数组{3，32，321}，
则打印出这三个数字能排成的最小数字为321323。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间效率
'''
import sys
import getopt


class Solution:
    def PrintMinNumber(self, numbers):
        # write code here
        num_len = len(numbers)

        if num_len <= 0:
            return ''

        if num_len == 1:
            return numbers[0]

        # 思路：转换成字符串后，n[i]+n[i+1] 和 n[i+1]+n[i] 进行比较
        # 按字母序排序，越小越靠前

        array = []
        for i in range(num_len):
            array.append(str(numbers[i]))

        return ''.join(sorted(array, self.cmp, reverse=False))

    # 自定义排序函数
    def cmp(self, x, y):
        # 将 x+y 与 y+x 相比，值更小的元素（x 或者 y）排在前面
        if (x + y) < (y + x):
            return -1
        if (y + x) < (x + y):
            return 1
        return 0


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

    numbers = [3, 32, 1, 321]

    print solution.PrintMinNumber(numbers)


if __name__ == "__main__":
    sys.exit(main())

