# -*- coding:utf-8 -*-

'''
序号：29
题目：最小的K个数

题目描述：
输入n个整数，找出其中最小的K个数。
例如输入4,5,1,6,2,7,3,8这8个数字，
则最小的4个数字是1,2,3,4,。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间效率
'''
import sys
import getopt


class Solution:
    def GetLeastNumbers_Solution(self, tinput, k):
        # write code here
        if len(tinput) <= 0 or len(tinput) < k:
            return []

        # answer = []

        t_list = sorted(tinput, reverse=False)
        # print t_list

        # for i in range(k):
        #     answer.append(t_list[i])

        return t_list[: k]
        # return answer


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

    tinput = [4, 5, 1, 6, 2, 7, 3, 8]
    k = 4

    print solution.GetLeastNumbers_Solution(tinput, k)


if __name__ == "__main__":
    sys.exit(main())

