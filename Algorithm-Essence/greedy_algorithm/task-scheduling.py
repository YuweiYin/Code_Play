#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/greedy_algorithm
@File    : task-scheduling.py
@Author  : YuweiYin
@Date    : 2020-05-28
=================================================="""

import sys
import time

"""
任务调度问题 Task Scheduling

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 16
"""


# 任务结构体
class Task:
    def __init__(self, task_id, deadline, punish):
        self.task_id = task_id    # 本任务的 id 序号 ai
        self.deadline = deadline  # 本任务的截止完成时间 di
        self.punish = punish      # 超过截止时间未完成 的惩罚因子 wi


class TaskScheduling:
    def __init__(self, task_list):
        assert isinstance(task_list, list) and len(task_list) > 0

        # 确保 task_list 中每个元素都是 Task 结构体
        for task in task_list:
            assert isinstance(task, Task)

        # 按各任务的惩罚因子降序排列 O(n log n)
        task_list = sorted(task_list, key=lambda x: x.punish, reverse=True)

        self.task_list = task_list              # 按惩罚因子降序排列的任务列表
        self.optimal_order = []                 # 最优任务调度顺序
        self.optimal_punish = 0                 # 最优总惩罚因子

    # 单处理器上带截止时间和惩罚的 单位时间任务调度问题
    # 返回：哈夫曼树的根结点
    def task_scheduling(self):
        # 循环实现 (贪心算法) O(n^2)
        self._task_scheduling_iteration()
        return self.optimal_order, self.optimal_punish

    # 循环实现 (贪心算法)
    # 时间复杂度 O(n^2)
    # 空间复杂度 \Theta(n)
    def _task_scheduling_iteration(self):
        n = len(self.task_list)  # 任务总数
        self.optimal_punish = 0  # 最优总惩罚因子

        # 设置 n 个时间槽
        neg_inf = -0x3f3f3f3f
        time_slot = [neg_inf] * n

        # 依次处理 n 个任务，各任务已经按惩罚因子降序排列了
        for i in range(n):
            task = self.task_list[i]
            assert isinstance(task, Task)
            is_slot_founded = False
            # 当处理任务 aj 时，如果存在不晚于 aj 的截止时间 dj 的空余时间槽，则将 aj 分配到其中最晚的那个槽
            for j in reversed(range(task.deadline)):
                if time_slot[j] == neg_inf:
                    is_slot_founded = True
                    time_slot[j] = task.task_id  # 时间槽占位
                    break
            # 如果不存在这样的时间槽，则将 aj 分配到所有空余时间槽最晚的一格中
            if not is_slot_founded:
                self.optimal_punish += task.punish  # 此任务必然延迟
                for j in reversed(range(n)):
                    if time_slot[j] == neg_inf:
                        time_slot[j] = task.task_id
                        break
        # 最优任务调度顺序
        self.optimal_order = time_slot

    # 获取最优任务调度顺序
    def get_optimal_order(self):
        return self.optimal_order

    # 获取最优总惩罚因子
    def get_optimal_punish(self):
        return self.optimal_punish


def main():
    # task_array 中的每个元素为二元元组，下标序号 i+1 即为任务序号 i
    # tuple[0] 为本任务的截止完成时间 di、tuple[1] 为超过截止时间未完成 的惩罚因子 wi
    task_array = [
        (4, 70), (2, 60), (4, 50), (3, 40), (1, 30), (4, 20), (6, 10)
    ]

    # 通过 task_array 构造 Task 数组
    task_list = []
    for index, task in enumerate(task_array):
        task_list.append(Task(task_id=(index + 1), deadline=task[0], punish=task[1]))

    # 建立任务调度器，将各任务按惩罚因子降序排列
    task_scheduler = TaskScheduling(task_list)

    # 进行任务调度，获取最优任务调度顺序、最优总惩罚因子
    start = time.process_time()
    task_scheduler.task_scheduling()
    end = time.process_time()

    # 输出最优任务调度顺序  [4, 2, 3, 1, 7, 6, 5]
    print(task_scheduler.get_optimal_order())
    # 输出最优总惩罚因子  50
    print(task_scheduler.get_optimal_punish())

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
