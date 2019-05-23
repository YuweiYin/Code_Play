# -*- coding:utf-8 -*-

'''
序号：33
题目：丑数

把只包含质因子2、3和5的数称作丑数（Ugly Number）。
例如6、8都是丑数，但14不是，因为它包含质因子7。
习惯上我们把1当做是第一个丑数。求按从小到大的顺序的第N个丑数。

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间空间效率的平衡
'''
import sys
import getopt


class Solution:
    def GetUglyNumber_Solution(self, index):
        # write code here
        if index <= 0:
            return 0

        if index == 1:
            return 1

        ugly_list = [1]

        # 思路：
        # 要求的新元素，是从前面列表里选择一个，
        # 乘 2、乘 3、乘 5，取最小的那个值，但不能与已有的重复

        count = 1
        # mul_n 代表 n 还没乘过的元素的最小下标，从 0 开始
        mul_2, mul_3, mul_5 = 0, 0, 0
        while(count < index):
            new_num = min(
                ugly_list[mul_2] * 2,
                ugly_list[mul_3] * 3,
                ugly_list[mul_5] * 5,
                )

            # 保证 2/3/5 不再去乘 原来乘过的元素了
            if new_num == (ugly_list[mul_2] * 2):
                # print 'mul_2: ', mul_2, '->', mul_2 + 1
                mul_2 += 1
            elif new_num == (ugly_list[mul_3] * 3):
                # print 'mul_3: ', mul_3, '->', mul_3 + 1
                mul_3 += 1
            else:
                # print 'mul_5: ', mul_5, '->', mul_5 + 1
                mul_5 += 1

            # 保证不重复，比如 2 * 3 == 3 * 2
            if new_num in ugly_list:
                continue
            else:
                ugly_list.append(new_num)
                count += 1

        # print ugly_list

        return ugly_list[index - 1]


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

    index = 10

    print solution.GetUglyNumber_Solution(index)


if __name__ == "__main__":
    sys.exit(main())

