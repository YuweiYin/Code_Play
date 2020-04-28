#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：30
题目：连续子数组的最大和

题目描述：
HZ 偶尔会拿些专业问题来忽悠那些非计算机专业的同学。
今天测试组开完会后, 他又发话了: 在古老的一维模式识别中,
常常需要计算连续子向量的最大和, 当向量全为正数的时候, 问题很好解决。
但是, 如果向量中包含负数, 是否应该包含某个负数, 并期望旁边的正数会弥补它呢？
例如: {6,-3,-2,7,-15,1,2,2}, 连续子向量的最大和为 8 (从第 0 个开始,到第 3 个为止)。
给一个数组，返回它的最大连续子序列的和，你会不会被他忽悠住？
(子向量的长度至少是1)

时间限制：1秒 空间限制：32768K
本题知识点：数组，时间效率
"""

import sys
import time


class Solution:
    def __init__(self):
        self.best_sum = 0
        self.current_sum = 0
        self.arr = []
        # self.arr_change = []
        self.arr_len = 0

    def find_greatest_sum_of_sub_array(self, array):
        self.arr_len = len(array)
        self.arr = array

        if self.arr_len <= 0:
            return 0

        if self.arr_len == 1:
            return self.arr[0]

        # 思路：
        # 如果 array 中有正数，那么子序列的首位和末位一定是正数，
        # 因为用负数做首末位，肯定只会减小 sum
        # 而且，完全可以把连续的正数看成同一个数，负数亦然
        # 所以可以这样做：遍历一遍，整合连续的正负数块

        # 但是，这也需要不少工作量，还有更简单的做法，如下：
        # 只需遍历一遍，只要使得 sum 为正数，则累加起来，
        # 如果前面 N 个子序列的 sum 为负数，那么直接舍弃前面这一串
        # 因为留着这个前缀就是“累赘”

        all_neg_flag = True  # 数组是否全为负数
        for i in range(self.arr_len):
            if self.arr[i] > 0:
                all_neg_flag = False

            # 如果当前和值 current_sum 为负，则舍弃之
            if self.current_sum < 0:
                self.current_sum = self.arr[i]
            else:
                self.current_sum += self.arr[i]

            # 更新当前最大的和值 best_sum
            if self.best_sum < self.current_sum:
                self.best_sum = self.current_sum

        if all_neg_flag:
            # 如果数组是否全为负数，则取其最大的那一个数作为连续子数组的最大和
            return sorted(self.arr, reverse=True)[0]
        else:
            return self.best_sum

        # # 遍历一遍，整合序列块
        # all_neg_flag = True
        #
        # flag = -1 # -1 表示负数，1 表示正数，0 表示 0，舍弃 0
        # temp_list = []
        # temp_sum = 0
        # for i in range(self.arr_len):
        #     if self.arr[i] > 0:
        #         all_neg_flag = False
        #
        # if all_neg_flag:
        #     temp_list = sorted()
        #
        # for i in range(self.arr_len):
        #     if self.arr[i] > 0:
        #         # 先记录单独一个数时的 sum
        #         self.current_sum += self.arr[i]
        #         if self.current_sum > self.best_sum:
        #             self.best_sum = self.current_sum
        #         j = i
        #         while j < self.arr_len:
        #             if self.arr[j] > 0:
        #                 # 计算两个正数之间的子序列长度


def main():
    solution = Solution()

    array = [6, -3, -2, 7, -15, 1, 2, 2]  # res = 8
    # array = [-6, -3, -2, -7, -15, -1, -2, -2]  # res = -1

    start = time.process_time()
    res = solution.find_greatest_sum_of_sub_array(array)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
