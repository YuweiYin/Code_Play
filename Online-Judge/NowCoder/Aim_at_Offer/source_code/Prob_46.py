#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：46
题目：孩子们的游戏（圆圈中最后剩下的数）

题目描述：
每年六一儿童节,牛客都会准备一些小礼物去看望孤儿院的小朋友,今年亦是如此。
HF 作为牛客的资深元老,自然也准备了一些小游戏。其中,有个游戏是这样的:
首先, 让小朋友们围成一个大圈。然后, 他随机指定一个数 m,
让编号为 0 的小朋友开始报数。每次喊到 m-1 的那个小朋友要出列唱首歌,
然后可以在礼品箱中任意的挑选礼物, 并且不再回到圈中,
从他的下一个小朋友开始,继续 0...m-1 报数.... 这样下去....
直到剩下最后一个小朋友, 可以不用表演,
并且拿到牛客名贵的“名侦探柯南”典藏版(名额有限哦!!^_^)。
请你试着想下, 哪个小朋友会得到这份礼品呢？(注：小朋友的编号是从 0 到 n-1)

时间限制：1秒 空间限制：32768K
本题知识点：模拟，抽象建模能力
"""

import sys
import time


class Solution:
    @staticmethod
    def last_remaining_solution(n, m):
        # 约瑟夫环问题

        # # 方法一：递推公式
        # # f(n, m) = 0                      (n = 1) 
        # # f(n, m) = [f(n - 1, m) + m] % n  (n > 1)

        # # 由于默认递归深度不到 1000，递归深度太深会报错
        # # maximum recursion depth exceeded
        # # 因此需要手动修改递归调用深度
        # sys.setrecursionlimit(1000000)

        # if n <= 0 or m <= 0:
        #     return -1

        # # 圈子规模缩小到 1，就是最终的目标
        # if n == 1:
        #     return 0

        # # f(n - 1, m) 表示缩圈之后找到的坐标，
        # # + m 是保持偏移量，% n 是保证数据范围
        # return (self.last_remaining_solution(n - 1, m) + m) % n

        # 方法二：用列表模拟游戏过程，注意下标
        if n <= 0 or m <= 0:
            return -1

        n_list = list(range(n))

        answer = -1  # 最终的结果（不断迭代计算）
        start = 0    # 每圈的起始点

        while n_list:
            # 确定本圈获得礼物的小朋友位置
            k = (start + m - 1) % n

            # 弹出该元素
            answer = n_list.pop(k)

            # 缩圈
            n -= 1

            # 出发点移动到弹出点的位置
            start = k

        return answer


def main():
    # answer = 4
    # n = 10
    # m = 4

    # answer = 1027
    n = 4000
    m = 997

    start = time.process_time()
    answer = Solution.last_remaining_solution(n, m)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
