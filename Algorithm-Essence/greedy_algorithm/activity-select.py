#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/greedy_algorithm
@File    : activity-select.py
@Author  : YuweiYin
@Date    : 2020-05-28
=================================================="""

import sys
import time

"""
活动选择问题 Activity Select

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 16
"""


# 活动结构体
class Activity:
    def __init__(self, start, finish, info=None):
        self.start = start    # 活动开始时间
        self.finish = finish  # 活动结束时间
        self.info = info      # 关于此活动的其它信息


class ActivitySelect:
    def __init__(self, activity_list):
        assert isinstance(activity_list, list) and len(activity_list) > 0

        # 确保 activity_list 中每个元素都是 Activity 结构体
        # \Theta(n)
        for activity in activity_list:
            assert isinstance(activity, Activity)
        # 按结束时间 finish 升序排列 TODO 使用优先队列来维护 activity_list
        # O(n log n)
        activity_list = sorted(activity_list, key=lambda x: x.finish, reverse=False)

        self.activity_list = activity_list  # 活动列表 Activity 结构体数组
        self.optimal_set = []  # 最优解：最大兼容活动子集(仅存储下标)
        self.optimal_val = 0   # 最优值：最大兼容活动子集的秩

    # 活动选择问题 Activity Select
    # 返回：最优值表、最优解表
    def activity_select(self):
        assert isinstance(self.activity_list, list) and len(self.activity_list) > 0

        # 记活动总数量为 n
        n = len(self.activity_list)

        # 重置最优值和最优解
        self.optimal_val = 1
        self.optimal_set = [0]  # 最先结束的活动必然要选

        # 自顶向下递归实现 (贪心算法) \Theta(n)
        # self._activity_select_recursive(0, n)
        # 循环实现 (贪心算法) \Theta(n)
        self._activity_select_iteration()
        return self.optimal_val, self.optimal_set

    # 自顶向下递归实现 (贪心算法)
    # 输入：k 为前一个贪心选择的活动 ak 的下标。n 为总活动数目
    # 时间复杂度 \Theta(n)
    # 空间复杂度 \Theta(1)
    def _activity_select_recursive(self, k, n):
        assert isinstance(self.activity_list, list) and len(self.activity_list) > 0

        # 从活动 ak 的后一个活动开始考虑
        m = k + 1
        # 如果 m 未至最末，从左至右(结束时间的升序)逐个考察每个任务。如果不与 ak 兼容，则检查下一个，直至兼容
        # 活动兼容：区间无重合(这里默认每个活动的时间为 左闭右开的区间)
        while m < n and self.activity_list[m].start < self.activity_list[k].finish:
            m += 1
        # 如果未扫描至末端，则表示活动 am 即为当前可行的贪心选择
        if m < n:
            self.optimal_val += 1        # 将最优值(子集的秩)加一
            self.optimal_set.append(m)   # 将 am 加入最优解(仅存储下标)
            self._activity_select_recursive(m, n)  # 继续递归 (尾递归，可改为循环)

    # 循环实现 (贪心算法)
    # 时间复杂度 \Theta(n)
    # 空间复杂度 \Theta(1)
    def _activity_select_iteration(self):
        assert isinstance(self.activity_list, list) and len(self.activity_list) > 0

        # 从活动 ak 的后一个活动开始考虑
        n = len(self.activity_list)
        k = 0

        # 如果 m 未至最末，从左至右(结束时间的升序)逐个考察每个任务。如果不与 ak 兼容，则检查下一个，直至兼容
        for m in range(1, n):
            # 活动兼容：区间无重合(这里默认每个活动的时间为 左闭右开的区间)
            if self.activity_list[m].start >= self.activity_list[k].finish:
                self.optimal_val += 1       # 将最优值(子集的秩)加一
                self.optimal_set.append(m)  # 将 am 加入最优解(仅存储下标)
                k = m  # 修改 k 值，表示当前的贪心选择为活动 ak，并且下个迭代开始时 m = k + 1

    # 获取最优值(最大兼容活动子集的秩)
    def get_optimal_val(self):
        return self.optimal_val

    # 获取最优解(最大兼容活动子集)
    def get_optimal_set(self):
        return self.optimal_set


def main():
    # activity_array 中的每个元素为二元元组，tuple[0] 为活动开始时间、tuple[1] 为活动结束时间
    activity_array = [
        (1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (12, 16),
        (5, 9), (6, 10), (8, 11), (8, 12), (2, 14)
    ]

    activity_list = []
    for activity in activity_array:
        activity_list.append(Activity(activity[0], activity[1]))

    a_s = ActivitySelect(activity_list)

    start = time.process_time()
    optimal_val, optimal_set = a_s.activity_select()
    end = time.process_time()

    print('\noptimal_val:')
    print(optimal_val)

    print('\noptimal_set:')
    print(optimal_set)

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
