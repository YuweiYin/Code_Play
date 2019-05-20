# -*- coding:utf-8 -*-

'''
序号：09
题目：变态跳台阶

题目描述：
一只青蛙一次可以跳上1级台阶，
也可以跳上2级……它也可以跳上n级。
求该青蛙跳上一个n级的台阶总共有多少种跳法。

时间限制：1秒 空间限制：32768K
本题知识点：递归和循环
'''
import sys
import getopt


class Solution:
    def jumpFloorII(self, number):
        # write code here
        if number <= 0:
            return 1

        count = 0
        # 每次都可以选择各种可能的跳跃高度
        for i in range(number):
            # 跳跃之后，计算剩余的台阶数
            floor_left = number - i - 1

            if floor_left <= 0:
                # 若剩余台阶数为 0，则表示已经走完一程
                count += 1
            else:
                # 否则继续往上跳跃，递归
                count += self.jumpFloorII(floor_left)

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
    number = 4
    print solution.jumpFloorII(number)
    # print solution.jumpFloorII(1) # 1
    # print solution.jumpFloorII(2) # 2
    # print solution.jumpFloorII(3) # 4
    # print solution.jumpFloorII(4) # 8
    # print solution.jumpFloorII(5) # 16
    # print solution.jumpFloorII(6) # 32
    # 从实验规律看，结果都是 2^number


if __name__ == "__main__":
    sys.exit(main())

