#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：49
题目：把字符串转换成整数

题目描述：
将一个字符串转换成一个整数，实现 Integer.valueOf(string) 的功能，
当 string 不符合数字要求时返回 0，要求不能使用字符串转换整数的库函数。
数值为 0 或者字符串不是一个合法的数值则返回 0。

输入描述：
    输入一个字符串, 包括数字字母符号, 可以为空

输出描述：
    如果是合法的数值表达则返回该数字，否则返回 0

示例：
输入：
    +2147483647
    1a33

输出：
    2147483647
    0

时间限制：1秒 空间限制：32768K
本题知识点：字符串，综合
"""

import sys
import time


class Solution:
    @staticmethod
    def str2int(s):
        if s is None or len(s) <= 0:
            return 0

        # 判断符号
        answer = 0
        positive = True
        if s[0] == '+':
            s = s[1:]

        elif s[0] == '-':
            s = s[1:]
            positive = False

        # 从末尾开始计算
        i = len(s) - 1
        while i >= 0:
            # 如果字符不是数字，直接退出
            if s[i] < '0' or s[i] > '9':
                return 0
            else:
                # 根据当前位数来计算需要乘以多少次基数
                power = len(s) - 1 - i

                addition = int(s[i])
                while power > 0:
                    addition *= 10
                    power -= 1

                # 把当前结果加入结果
                answer += addition

            i -= 1

        # 如果是负数，则修改符号
        if not positive:
            answer = -answer

        return answer


def main():
    s = '+2147483647'
    # s = '-2147483647'
    # s = '2147483647'
    # s = ''
    # s = '+12abc'
    # s = '1a33'

    start = time.process_time()
    answer = Solution.str2int(s)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
