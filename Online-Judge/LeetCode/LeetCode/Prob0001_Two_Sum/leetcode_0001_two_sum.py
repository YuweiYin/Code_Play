#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : LeetCode/Prob0001_Two_Sum
@File    : leetcode_0001_two_sum.py
@Author  : YuweiYin
=================================================="""

# import gc
import sys
import time
from typing import List

"""
1. Two Sum

Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.

给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

Example:
    Given nums = [2, 7, 11, 15], target = 9,
    Because nums[0] + nums[1] = 2 + 7 = 9,
    return [0, 1].
"""


class Solution:
    def __init__(self):
        pass

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dic = dict({})

        for i, num in enumerate(nums):
            # 计算当前元素值与目标值的差值
            diff = target - num

            # 如果哈希表中已有该差值对应的元素坐标，则返回之
            if diff in dic:
                return [dic[diff], i]

            # 将键值对(当前元素值, 当前元素坐标) 存储进哈希表
            dic[num] = i

        # 找不到
        return []


def main():
    # 设置测试数据
    nums = [2, 7, 11, 15]
    target = 9

    # 调用解决方案，获得处理结果
    solution = Solution()

    start = time.process_time()
    res = solution.twoSum(nums, target)
    end = time.process_time()

    # 输出展示结果
    print(res)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
