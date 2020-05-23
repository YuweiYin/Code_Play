#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/mathematics/probability_statistics
@File    : hiring.py
@Author  : YuweiYin
@Date    : 2020-05-23
=================================================="""

import sys
import time
import math
import random

"""
雇用问题 (Hiring)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 5
"""


# 应聘者结构体
class Candidate:
    def __init__(self, c_id, ability=0, salary=1, interview=0):
        self.c_id = c_id            # 该应聘者的编号
        self.ability = ability      # 该应聘者的能力, 据此来决定是否雇用 (默认设置为自然数, 良序集)
        self.salary = salary        # 雇用此应聘者需要花费的总金额 (默认值为 1, 便于分析)
        self.interview = interview  # 与此应聘者进行面试需要花费的总金额 (默认值为 0, 相比于 salary 可忽略, 便于分析)


class Hiring:
    def __init__(self, candidate_array):
        for candidate in candidate_array:
            assert isinstance(candidate, Candidate)

        self.candidate_array = candidate_array  # 应聘者列表 (面试前不可知)
        self.total_num = len(candidate_array)   # 应聘者总数 (此处假定已知)
        self.cur_hire = Candidate(-0x3f3f3f3f, ability=-0x3f3f3f3f)  # 当前雇用在位的应聘者, 此信息面试官可知
        self.total_cost = 0                     # 整个应聘过程中的总花费 (雇用过程结束后才可知)

    # 执行雇用过程
    # 面试前既不知道有多少应聘者、也更不知道其 id 或 ability
    def do_hire(self):
        # return self._do_hire_1()
        # return self._do_hire_2()
        return self._do_online_hire()

    # 执行雇用过程
    # 面试前既不知道有多少应聘者、也更不知道其 id 或 ability
    # 返回面试与雇用的总花费
    def _do_hire_1(self):
        # 设置初始值
        self.total_cost = 0
        self.cur_hire = Candidate(-0x3f3f3f3f, ability=-0x3f3f3f3f)
        # 循环处理每位应聘者
        for candidate in self.candidate_array:
            assert isinstance(candidate, Candidate)
            # 一旦当前应聘者分数更高，就雇用
            if candidate.ability > self.cur_hire.ability:
                self.total_cost += candidate.interview + candidate.salary
                self.cur_hire = candidate
        # 返回面试与雇用的总花费
        return self.total_cost

    # 执行随机化的雇用过程
    # 面试前有应聘者的名单，因此知道应聘者数目，也知道其 id，但不知道各位应聘者的 ability
    # 很显然，如果面试前就已经知道了各位应聘者的确切 ability，那么一般只需要找到最大值就完成雇用了
    # 返回面试与雇用的总花费
    def _do_hire_2(self):
        # 先随机打乱数组，再执行与 _do_hire_1 相同的算法
        shuffler = ShuffleArray(self.candidate_array)
        shuffler.do_shuffle()
        # 设置初始值
        self.total_cost = 0
        self.cur_hire = Candidate(-0x3f3f3f3f, ability=-0x3f3f3f3f)
        # 循环处理每位应聘者
        for candidate in shuffler.array:
            assert isinstance(candidate, Candidate)
            # 一旦当前应聘者分数更高，就雇用
            if candidate.ability > self.cur_hire.ability:
                self.total_cost += candidate.interview + candidate.salary
                self.cur_hire = candidate
        # 返回面试与雇用的总花费
        return self.total_cost

    # 执行在线雇用过程
    # 面试前知道有多少应聘者，但不知道其 id 名单 (所以不能进行随机化) 以及能力值分数 ability
    # 返回面试的次数
    def _do_online_hire(self):
        n = len(self.candidate_array)
        k = int(n / math.e)  # 经证明，k = n/e 可以使得选到最佳应聘者的概率下界最大化，成功概率至少为 1/e
        self.cur_hire = Candidate(-0x3f3f3f3f, ability=-0x3f3f3f3f)
        if n == 1:
            # 仅一名待面试的应聘者，直接雇用
            assert isinstance(self.candidate_array[0], Candidate)
            self.cur_hire = self.candidate_array[0]
            return 1
        elif n > 1 and isinstance(k, int) and 0 < k < n:
            # 待面试的应聘者超过 1 人，取前 k 人淘汰，并记录这 k 人中的最高分 best_ability
            best_ability = -0x3f3f3f3f
            for i in range(k):
                assert isinstance(self.candidate_array[i], Candidate)
                if self.candidate_array[i].ability > best_ability:
                    best_ability = self.candidate_array[i].ability

            # 随后面试的 n - k 人中，一旦有比 best_ability 更高分的人出现，则直接雇用，不面试剩下的人了
            for i in range(k, n):
                assert isinstance(self.candidate_array[i], Candidate)
                # 如果面试到最后一个人，直接雇用
                if i == n - 1:
                    self.cur_hire = self.candidate_array[i]
                    return n
                else:
                    if self.candidate_array[i].ability > best_ability:
                        self.cur_hire = self.candidate_array[i]
                        return i + 1
            # 不应运行到此处
            return 0
        else:
            # 表示参数类型/范围错误，或者 n == 0 没有应聘者
            return 0

    # 获取当前雇用在位的应聘者
    def get_cur_hire(self):
        return self.cur_hire

    # 打印当前雇用在位的应聘者
    def print_cur_hire(self):
        assert isinstance(self.cur_hire, Candidate)
        print('id:', self.cur_hire.c_id, '\tability:', self.cur_hire.ability,
              '\tsalary:', self.cur_hire.salary, '\tinterview:', self.cur_hire.interview)


# 随机打乱数组
class ShuffleArray:
    def __init__(self, array):
        self.array = array

    def do_shuffle(self):
        if isinstance(self.array, list) and len(self.array) > 1:
            # 从最高的 index 开始降到 1，每次生成 0～index-1 的随机数，与 index=index 的元素交换
            for i in reversed(range(1, len(self.array))):
                self._exchange(i, self._get_random_int(i - 1))
        else:
            print('The so-called array is NOT a list!')

    # 按下标生成随机数
    def _get_random_int(self, index):
        random.seed(id(self.array[index]))  # 以对象的唯一标识符 id 作为随机数种子
        return random.randint(0, index)     # 生成 0～index 的整型随机数

    # 按下标交换 self.array 中的两个元素
    def _exchange(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp


def main():
    ab_array = [3, 1, 2, 8, 7, 9]  # 应聘者的能力数组 (面试前不可知)

    candidate_array = []
    for index, ab in enumerate(ab_array):
        new_c = Candidate(index, ability=ab)
        candidate_array.append(new_c)

    hire = Hiring(candidate_array)

    start = time.process_time()
    print('hire_cost:', hire.do_hire())
    end = time.process_time()
    hire.print_cur_hire()
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
