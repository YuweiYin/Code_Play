#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：01
题目：二维数组中的查找

题目描述：
在一个二维数组中（每个一维数组的长度相同），每一行都按照从左到右递增的顺序排序，
每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，
判断数组中是否含有该整数。

时间限制：1秒 空间限制：32768K
本题知识点：查找
"""

import sys
# import getopt
import time


class Solution:
    # 解题思路：
    # 从右上角元素开始比较，该元素是当前行的最大值、当前列的最小值，
    # 若 target 大，则它比该行所有元素都大，则向下走，并删除一行；
    # 若 target 小，则它比该列所有元素都小，则向左走，并删除一列。
    @staticmethod
    def find(target, array):
        # 参数解释：array 二维列表
        if array is None or len(array) <= 0:
            return False

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


# def main(argv=None):
def main():
    """
    if argv is None:
        argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:], "h", ["help"])
    except getopt.error as e:
        raise e
    """

    # solution = Solution()
    array = [
        [1, 2, 8, 9],
        [2, 4, 9, 12],
        [4, 7, 10, 13],
        [6, 8, 11, 15]
    ]
    target = 7

    # start = time.clock()  # time.clock() 将在 Python 3.8 中废弃
    start = time.process_time()
    ans = Solution.find(target, array)
    # end = time.clock()
    end = time.process_time()

    print(ans)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
