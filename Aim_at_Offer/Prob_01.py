# -*- coding:utf-8 -*-

'''
序号：01
题目：二维数组中的查找

题目描述：
在一个二维数组中（每个一维数组的长度相同），每一行都按照从左到右递增的顺序排序，
每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，
判断数组中是否含有该整数。

时间限制：1秒 空间限制：32768K
本题知识点：查找
'''
import sys
import getopt


class Solution:
    # array 二维列表
    def Find(self, target, array):
        # write code here
        # 解题思路：
        # 从右上角开始，若target小，则向下走，并删除一行；若target大，则向左走，删除一列
        row = 0
        col = len(array[0]) - 1
        while row < len(array) and col >= 0:
            if target == array[row][col]:
                return True
            elif target > array[row][col]:
                row += 1
            else:
                col -= 1

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
    array = [
        [1, 2, 8, 9],
        [2, 4, 9, 12],
        [4, 7, 10, 13],
        [6, 8, 11, 15]
    ]
    target = 7
    print solution.Find(target, array)


if __name__ == "__main__":
    sys.exit(main())

