#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/dynamic_programming
@File    : cut-rod.py
@Author  : YuweiYin
@Date    : 2020-05-26
=================================================="""

import sys
import time

"""
钢条切割 Cut Rod

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 15
"""


class CutRod:
    def __init__(self, price_list, rod_len):
        assert isinstance(price_list, list) and 0 <= rod_len < len(price_list)
        self.price_list = price_list
        self.rod_len = rod_len

    # 钢条切割
    # 返回：最佳收益(最优值)、最佳切割方案列表(最优解)
    # 如果返回最佳收益为 -1，则为异常
    def cut_rod(self):
        if self.rod_len == 0:
            return 0
        # return self._cut_rod_1(self.rod_len)  # 自顶向下递归实现 (DFS 暴力搜索) O(2^n)
        # return self._cut_rod_2(self.rod_len)  # 自顶向下递归实现 (带备忘录的动态规划) O(n^2)
        return self._cut_rod_3(self.rod_len)  # 自底向上循环实现 (动态规划) O(n^2)

    # 自顶向下递归实现 (DFS 暴力搜索)
    # rn = max_{1<=i<=n} (p_i + r_{n-i})
    # 输入：rest_len 为当前待切割的钢条长度
    # 时间复杂度 O(2^n)
    def _cut_rod_1(self, rest_len):
        assert rest_len >= 0
        # 长度为 0 的钢条收益为 0
        if rest_len == 0:
            return 0, [0]
        # 递归树全遍历的方式查找所有可行解
        best_reward = 0
        best_solution = [-1] * (self.rod_len + 1)  # TODO 最优解
        for i in range(1, rest_len + 1):
            # 取可行解中的最值
            best_reward = max(best_reward, self.price_list[i] + self._cut_rod_1(rest_len - i)[0])
        # 返回最优值
        return best_reward, best_solution

    # 自顶向下递归实现 (带备忘录的动态规划)
    # 输入：rob_len 为待切割的总钢条长度
    # 时间复杂度 O(n^2)
    def _cut_rod_2(self, rob_len):
        assert rob_len >= 0
        # 初始化备忘录
        neg_inf = -0x3f3f3f3f
        reward_memo = [neg_inf] * (self.rod_len + 1)
        # 递归求解
        best_solution = [-1] * (self.rod_len + 1)  # TODO 最优解
        return self._memoized_cut_rob(rob_len, reward_memo), best_solution

    def _memoized_cut_rob(self, rest_len, reward_memo):
        assert rest_len >= 0
        # 一旦目标 rest_len 存在于 reward_memo 表中，则直接查值返回即可
        if reward_memo[rest_len] >= 0:
            return reward_memo[rest_len]
        # 否则与普通回溯法类似处理
        if rest_len == 0:
            best_reward = 0
        else:
            best_reward = 0
            for i in range(1, rest_len + 1):
                best_reward = max(best_reward, self.price_list[i] + self._memoized_cut_rob(rest_len - i, reward_memo))
        # 注意在求得当前 rest_len 的最优值后，需记录于备忘录中
        reward_memo[rest_len] = best_reward
        return best_reward

    # 自底向上循环实现 (动态规划)
    # 输入：rob_len 为待切割的总钢条长度
    # 时间复杂度 O(n^2)
    def _cut_rod_3(self, rob_len):
        assert rob_len >= 0
        # 初始化备忘录
        neg_inf = -0x3f3f3f3f
        reward_memo = [neg_inf] * (self.rod_len + 1)
        reward_memo[0] = 0  # 长度为 0 的钢条收益为 0
        # 用于还原构造最优解的数组
        solutions = [neg_inf] * (self.rod_len + 1)
        # 切割，每次切割的左段(之后不会再切割的部分)长度从 rob_len - 1 到 0 变动
        # 因此当前切割后的剩余长度 rest_len 从 1 到 rob_len 变动，这样可以表达所有切分方案
        for rest_len in range(1, rob_len + 1):
            best_reward = 0
            # 在当前切割后的 rest_len 基础上继续切分，最短为 1、初次循环的 rest_len 也为 1
            # 循环结束后就能得到 以此 rest_len 作为"可变切割部分" 能获得的最大收益了
            for i in range(1, rest_len + 1):
                cur_reward = self.price_list[i] + reward_memo[rest_len - i]
                if best_reward < cur_reward:
                    best_reward = cur_reward
                    # solutions[rest_len] 表示剩余长度为 rest_len 时的最佳切割长度
                    solutions[rest_len] = i
            # 记录此收益到备忘录中，之后查表即可得值
            reward_memo[rest_len] = best_reward
        # 通过 solutions 数组构造最优解
        # solutions[rest_len] 表示剩余长度为 rest_len 时的最佳切割长度
        # 初始的"剩余长度"为总钢条长度 rob_len，每次切割之后 rest_len 减小
        best_solution = []
        _rob_len = rob_len
        while _rob_len > 0:
            best_solution.append(solutions[_rob_len])
            _rob_len -= solutions[_rob_len]
        # 返回 reward_memo[rob_len] 意味着让整个 rob_len 长度都作为"可变切割部分" 能获得的最大收益，即为目标最优值
        return reward_memo[rob_len], best_solution


def main():
    # price_list[i] 表示长度为 i 的钢条的售价
    price_list = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    rod_len = 8

    cr = CutRod(price_list, rod_len)

    start = time.process_time()
    best_reward, best_solution = cr.cut_rod()
    end = time.process_time()

    print('best_reward:', best_reward)      # 22
    print('best_solution:', best_solution)  # [2, 6]

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
