#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：35
题目：数组中的逆序对

题目描述：
在数组中的两个数字，如果前面一个数字大于后面的数字，
则这两个数字组成一个逆序对。输入一个数组,求出这个数组中的逆序对的总数 P。
并将 P 对 1000000007 取模的结果输出。即输出 P % 1000000007

输入描述：
题目保证输入的数组中没有的相同的数字

数据范围：
    对于%50的数据,size<=10^4
    对于%75的数据,size<=10^5
    对于%100的数据,size<=2*10^5

示例：
    输入：
    1,2,3,4,5,6,7,0
    输出：
    7

时间限制：2秒 空间限制：32768K
本题知识点：数组，时间空间效率的平衡
"""

import sys
import time


class Solution:
    def __init__(self):
        self.data = []
        self.count = 0
        self.MOD = 1000000007

    def inverse_pairs(self, data):
        if data is None or len(data) <= 1:
            return 0

        # # 方法一：O(n^2) 遍历查找。时间复杂度高，通不过在线测试
        # data_len = len(data)
        # i, j = 0, 0
        # count = 0

        # while i < data_len:
        #     j = i + 1

        #     while j < data_len:
        #         # 判断出现逆序对
        #         if data[i] > data[j]:
        #             count += 1

        #         j += 1

        #     i += 1

        # return count % self.MOD

        # 方法二：分治法 O(nlogn)，二路归并排序，排序过程中检查逆序对
        # 分治法的时间复杂度是没问题的，但是牛客网还是超时、通不过！！！
        # 别的使用 Python 的朋友也是这个情况，所以这道题改用其它语言跑
        # 见 Prob_35.cpp 思路不变
        self.data = data
        self.count = 0

        self.merge_sort_2_way(0, len(self.data) - 1)

        return self.count % self.MOD

    def merge_sort_2_way(self, first, last):
        # 当前处理的子数组元素个数 <= 1 无需排序
        if (last - first) < 1:
            return

        # 拆分左右数组
        mid = int((first + last) / 2)

        # 左右二分分治
        self.merge_sort_2_way(first, mid)
        self.merge_sort_2_way(mid + 1, last)

        # 合并排序，最少从 2 个元素的子数组开始排
        self.merge(self.data, first, mid, last)

    def merge(self, data, first, mid, last):
        # 此时 data[first..mid] 和 data[mid..last] 内部都是有序的
        # 最小的情况举例：first 为 0，mid 为 0，last 为 1

        # 以 mid 为界，左右两个数组对比
        i = first
        j = mid + 1
        sorted_data = []

        # 滑动双指针
        while i <= mid or j <= last:
            # 左边数组的数已经处理完了，把右边数组的元素加进来就行了
            if i > mid:
                sorted_data.append(data[j])
                j += 1

            # 右边数组的数已经处理完了，把左边数组的元素加进来就行了
            elif j > last:
                sorted_data.append(data[i])
                i += 1

            # 左右相比，小的加进来
            elif data[i] < data[j]:
                sorted_data.append(data[i])
                i += 1

            else:
                # 此时出现逆序的情况
                # 由于内部有序 data[i] > data[j] 说明
                # data[i...mid] 都大于 data[j]
                self.count += mid - i + 1
                # print(self.count)

                sorted_data.append(data[j])
                j += 1

        # 修改 self.data 相应位置的值
        self.data[first: last + 1] = sorted_data


def main():
    # data = [1, 2, 3, 4, 5, 6, 7, 0]  # 7
    # data = [1, 8, 3, 4, 5, 6, 7, 0]  # 12
    data = [364, 637, 341, 406, 747, 995, 234, 971, 571,
            219, 993, 407, 416, 366, 315, 301, 601, 650, 418,
            355, 460, 505, 360, 965, 516, 648, 727, 667, 465,
            849, 455, 181, 486, 149, 588, 233, 144, 174, 557,
            67, 746, 550, 474, 162, 268, 142, 463, 221, 882,
            576, 604, 739, 288, 569, 256, 936, 275, 401, 497,
            82, 935, 983, 583, 523, 697, 478, 147, 795, 380,
            973, 958, 115, 773, 870, 259, 655, 446, 863, 735,
            784, 3, 671, 433, 630, 425, 930, 64, 266, 235, 187,
            284, 665, 874, 80, 45, 848, 38, 811, 267, 575]  # res = 2519

    solution = Solution()

    start = time.process_time()
    res = solution.inverse_pairs(data)
    end = time.process_time()

    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
