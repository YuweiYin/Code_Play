#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：48
题目：不用加减乘除做加法

题目描述：
写一个函数，求两个整数之和，
要求在函数体内不得使用 +、-、*、/ 四则运算符号。

时间限制：1秒 空间限制：32768K
本题知识点：发散思维能力
"""

import sys
import time


class Solution:
    @staticmethod
    def add(num1, num2):
        # 位运算：& 按位与，| 按位或，^ 按位异或，~ 按位取反，<< >> 左移右移
        # 对于二进制加法 a + b， a ^ b 就是当前位的结果，(a & b) << 1 就是进位的值

        # 直到进位为 0 时停止
        while num2 != 0:
            # print(num1, num2, num1 ^ num2, (num1 & num2) << 1)
            # print(bin(num1), bin(num2), bin(num1 ^ num2), bin((num1 & num2) << 1))

            current_sum = (num1 ^ num2) & 0xFFFFFFFF  # 当前位结果，考虑负数
            current_carry = ((num1 & num2) << 1) & 0xFFFFFFFF  # 进位值，考虑负数

            num1 = current_sum
            num2 = current_carry

        return num1 if num1 <= 0x7FFFFFFF else ~(num1 ^ 0xFFFFFFFF)

        # if num1 < num2:
        #     temp = num1
        #     num1 = num2
        #     num2 = temp

        # num1_bin = list(bin(num1)[2: ])
        # num2_bin = list(bin(num2)[2: ])

        # num1_bin.reverse()
        # num2_bin.reverse()

        # print(num1_bin)
        # print(num2_bin)

        # calc_list = []
        # addition = 0
        # i = 0
        # j = 0
        # while i < len(num2_bin):
        #     # 位运算：& 按位与，| 按位或，^ 按位异或，- 按位取反，<< >> 左移右移
        #     # 对于二进制加法 a + b， a ^ b 就是当前位的结果，a & b 就是进位 
        #     current_sum = int(num1_bin[i]) + int(num2_bin[i]) + addition
        #     if current_sum >= 3:
        #         calc_list.append('1')
        #         addition = 1
        #     elif current_sum == 2:
        #         calc_list.append('0')
        #         addition = 1
        #     else:
        #         calc_list.append(str(current_sum))
        #         addition = 0

        #     i += 1

        # i = len(num2_bin)
        # while i < len(num1_bin):
        #     current_sum = int(num1_bin[i]) + addition
        #     if current_sum >= 3:
        #         calc_list.append('1')
        #         addition = 1
        #     elif current_sum == 2:
        #         calc_list.append('0')
        #         addition = 1
        #     else:
        #         calc_list.append(str(current_sum))
        #         addition = 0

        #     i += 1

        # if addition > 0:
        #     calc_list.append('1')

        # calc_list.reverse()

        # answer = '0b' + ''.join(calc_list)

        # return(int(answer, 2))


def main():
    solution = Solution()

    num1 = -7
    num2 = 3

    start = time.process_time()
    answer = solution.add(num1, num2)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
