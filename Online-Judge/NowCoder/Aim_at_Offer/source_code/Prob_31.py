#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：31
题目：整数中 1 出现的次数（从 1 到 n 整数中 1 出现的次数）

题目描述：
求出 1~13 的整数中 1 出现的次数,并算出 100~1300 的整数中 1 出现的次数？
为此他特别数了一下 1~13 中包含1的数字有 1、10、11、12、13 因此共出现 6 次,
但是对于后面问题他就没辙了。ACMer 希望你们帮帮他,并把问题更加普遍化,
可以很快的求出任意非负整数区间中1出现的次数（从 1 到 n 中 1 出现的次数）。

时间限制：1秒 空间限制：32768K
本题知识点：时间效率
"""

import sys
import time


class Solution:
    @staticmethod
    def number_of_1_between_1_and_n_solution(n):
        if n <= 0:
            return 0

        if n == 1:
            return 1

        # 方法 1: 数字转字符串，连接存储在一起，最后 count
        # n_str = ''
        # i = 1
        # while i <= n:
        #     n_str += str(i)
        #     i += 1

        # return n_str.count('1', 0, len(n_str))

        # 方法 2: 循环内每次都 count
        count = 1
        i = 2
        while i <= n:
            count += str(i).count('1')
            i += 1

        return count


def main():
    n = 1300

    start = time.process_time()
    res = Solution.number_of_1_between_1_and_n_solution(n)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
