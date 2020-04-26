#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：50
题目：数组中重复的数字

题目描述：
在一个长度为 n 的数组里的所有数字都在 0 到 n-1 的范围内。
数组中某些数字是重复的，但不知道有几个数字是重复的。
也不知道每个数字重复几次。请找出数组中任意一个重复的数字。
例如，如果输入长度为 7 的数组 {2,3,1,0,2,5,3}，
那么对应的输出是第一个重复的数字 2。

时间限制：1秒 空间限制：32768K
本题知识点：数组
"""

import sys
import time


class Solution:
    # 这里要特别注意 找到任意重复的一个值并赋值到 duplication[0]
    # 函数返回 True/False
    @staticmethod
    def duplicate(numbers, duplication):
        if numbers is None or len(numbers) <= 1:
            return False

        # 方法一
        # while numbers:
        #     # 判断首元素是否重复：在首元素之后的列表元素里，查看是否存在首元素
        #     if numbers[0] in numbers[1:]:
        #         # 如果重复，这就是第一个重复的元素，记录并输出
        #         duplication.append(numbers[0])
        #         return True
        #     else:
        #         # 如果不重复，继续往后找
        #         numbers.pop(0)

        # 方法二：字典
        dic = dict()
        # 遍历一遍，用字典存储每个词的出现次数
        for item in numbers:
            if item in dic:
                dic[item] += 1
            else:
                dic[item] = 1

        # 再遍历一遍，找到第一个出现次数大于 1 的词
        for item in numbers:
            if dic[item] > 1:
                # 此处有个坑，系统给的 duplication 数组不为 []，
                # 其首位应该是 -1，所以不能直接 append，要判断
                if len(duplication) <= 0:
                    duplication.append(item)
                else:
                    duplication[0] = item

                return True

        return False


def main():
    # numbers = [2, 3, 1, 0, 2, 5, 3]  # 2
    numbers = [2, 1, 3, 1, 4]  # 1
    duplication = []

    start = time.process_time()
    answer = Solution.duplicate(numbers, duplication)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print(duplication)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
