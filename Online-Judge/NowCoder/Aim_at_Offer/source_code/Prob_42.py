#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：42
题目：和为 S 的两个数字

题目描述：
输入一个递增排序的数组和一个数字 S，
在数组中查找两个数，使得他们的和正好是 S，
如果有多对数字的和等于 S，输出两个数的乘积最小的。

输出描述：
对应每个测试案例，输出两个数，小的先输出。

时间限制：1秒 空间限制：32768K
本题知识点：知识迁移能力
"""

import sys
import time


class Solution:
    @staticmethod
    def find_numbers_with_sum(array, t_sum):
        if array is None or len(array) <= 1:
            return []

        # 思路：对撞指针、区间夹逼
        # 从两端往中间夹逼，和相等时，差越大乘积越小。且要考虑正负数
        small = 0  # 区间下限下标
        big = len(array) - 1  # 区间上限下标

        answer = []        # 最终答案
        best_mul = 0       # 最优乘积
        # current_mul = 0    # 当前两数乘积
        # current_sum = 0    # 当前两数和
        first_flag = True  # 是否第一次找到合适的两数

        current_sum = array[small] + array[big]  # 当前两数和
        while small < big:
            # print(small, big, array[small], array[big], current_sum)

            # 当前结果相比目标值，小则 small 后移，大则 big 前移
            if current_sum < t_sum:
                current_sum -= array[small]
                current_sum += array[small + 1]
                small += 1

            elif current_sum > t_sum:
                current_sum -= array[big]
                current_sum += array[big - 1]
                big -= 1

            # 当前结果跟目标值 t_sum 相同
            else:
                # 计算乘积，如果优于当前最优乘积，那么更新 answer
                current_mul = array[small] * array[big]

                # 第一次找到合适的两数时，不必比较乘积值，直接加进 answer
                if first_flag:
                    first_flag = False

                    best_mul = current_mul
                    answer.append(array[small])
                    answer.append(array[big])

                else:
                    # 之后找到的合适数对，先比较乘积是否会更小
                    if current_mul < best_mul:
                        best_mul = current_mul

                        # 记录两个数
                        answer = [].append(array[small])
                        answer.append(array[big])

                        # print(best_mul)
                        # print(answer)

                # small 后移
                current_sum -= array[small]
                current_sum += array[small + 1]
                small += 1

        return answer


def main():
    # [3, 7]
    array = [-3, -1, 0, 1, 3, 4, 5, 6, 7, 9, 11, 13]
    t_sum = 10

    start = time.process_time()
    answer = Solution.find_numbers_with_sum(array, t_sum)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
