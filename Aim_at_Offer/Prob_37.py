# -*- coding:utf-8 -*-

'''
序号：37
题目：数字在排序数组中出现的次数

题目描述：
统计一个数字在排序数组中出现的次数。

时间限制：1秒 空间限制：32768K
本题知识点：数组，知识迁移能力
'''
import sys
import getopt


class Solution:
    def GetNumberOfK(self, data, k):
        # write code here
        if data is None or len(data) <= 0:
            return 0

        k_sum = 0
        if k in data:
            # 如果 k 在 data 里，找到第一次出现的位置
            k_sum = 1
            first = data.index(k) + 1
            while first < len(data):
                # 遍历之后的数组元素，等于 k 就增加 sum
                if data[first] == k:
                    k_sum += 1
                    first += 1
                # 不同就直接退出循环
                else:
                    break
        else:
            # 如果 k 不在 data 里，返回 0
            return 0

        return k_sum


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

    data = [1, 2, 2, 4, 6, 6, 6, 8]
    k = 6

    answer = solution.GetNumberOfK(data, k)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

