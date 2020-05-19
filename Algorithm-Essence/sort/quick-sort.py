#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : quick-sort.py
@Author  : YuweiYin
@Date    : 2020-05-09
=================================================="""

import sys
import time
import random

"""
快速排序 Quick Sort

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 7
"""


# 元素结构体 key-value 键值对
class Element:
    def __init__(self, key=0, val=None):
        self.key = key  # (必备) 键 key。按 key 排序，因此 key 必须具有全序关系（常为整数）
        self.val = val  # (可选) 值 value。可为任意对象


# 排序算法的基类
class Sort:
    # 构造待排序数组
    # 时间复杂度 O(n)、空间复杂度 O(n)
    # 参数 ele_list 是 Element 元素结构体的列表，该结构体中必须要有一个 key 属性用于排序
    # 参数 key 是一个字符串，表示如何取得 ele_list 中各元素的 key
    # 参数 val 是一个字符串，表示如何取得 ele_list 中各元素的 val
    # 通过 getattr(object, name[, default]) 函数取对象属性。默认值设置为 None
    def __init__(self, ele_list, key_name='key', val_name='val'):
        self.ele_list = ele_list
        self.key_name = key_name
        self.val_name = val_name

        self.verify_key_val()

    # 确保 ele_list 中每个元素都有 key_name 属性和 val_name 属性
    # 如果某元素没有这两个属性，则将之从 ele_list 中剔除出去
    def verify_key_val(self):
        new_ele_list = []
        for ele in self.ele_list:
            if hasattr(ele, self.key_name) and hasattr(ele, self.val_name):
                new_ele_list.append(ele)
            else:
                pass
        self.ele_list = new_ele_list

    # 获取元素列表
    def get_ele_list(self):
        return self.ele_list

    # 获取元素中 key 的列表
    def get_key_list(self):
        key_list = []
        for ele in self.ele_list:
            if hasattr(ele, self.key_name):
                key_list.append(getattr(ele, self.key_name))
            else:
                pass
        return key_list

    # 获取元素中 val 的列表
    def get_val_list(self):
        val_list = []
        for ele in self.ele_list:
            if hasattr(ele, self.val_name):
                val_list.append(getattr(ele, self.val_name))
            else:
                pass
        return val_list

    # 修改待排序数组
    def update_ele_list(self, new_ele_list):
        self.ele_list = new_ele_list
        self.verify_key_val()  # 清除不含指定 key、val 的元素

    # 修改 key 属性名称
    def update_key_name(self, new_key_name):
        if isinstance(new_key_name, str):
            self.key_name = new_key_name
            self.verify_key_val()  # 清除不含指定 key、val 的元素
        else:
            pass

    # 修改 val 属性名称
    def update_val_name(self, new_val_name):
        if isinstance(new_val_name, str):
            self.val_name = new_val_name
            self.verify_key_val()  # 清除不含指定 key、val 的元素
        else:
            pass

    # 执行排序 (待重载)
    def do_sort(self, reverse=False):
        pass


# 快速排序 (继承自 Sort 类)
# 空间复杂度(辅助存储)-平均/最好/最坏：O(log n) / O(1) / O(n)
# 时间复杂度-平均/最好/最坏 O(n log n) / O(n log n) / O(n^2)
# 期望时间复杂度 O(n log n)，且其中的常数因子很小，实际应用时很高效
# 算法稳定性：不稳定
# 快速排序是十分经典和常用的排序算法，同归并排序一样，快排利用了分治法 Divide and Conquer 思想。
class QuickSort(Sort):
    # 重载 do_sort 方法
    # 排序操作前需已确保每个元素都含指定的 key_name 和 val_name 属性
    def do_sort(self, reverse=False):
        self._quick_sort(0, len(self.ele_list) - 1, reverse=reverse)

    # 快速排序
    # 每次从数组 A 中选取主元 p(pivot) 下标，
    # 如果 reverse 为 False，升序排列，则如下操作：
    # 让 A[l..p-1] 中的每个元素都小于等于 A[p]
    # 让 A[p+1..r] 中的每个元素都大于等于 A[p]
    # 如果 reverse 为 False，升序排列，则将如上操作的"大于"与"小于"互换
    def _quick_sort(self, l, r, reverse=False):
        # 当待排序数组的左下标等于右下标时为基本情况：
        # 该数组只有一个元素。这自然是已排好序的，无需处理
        if l < r:
            # p = self._partition(l, r, reverse=reverse)             # 固定选择选取主元、划分区间
            # p = self._randomized_partition(l, r, reverse=reverse)  # 随机选取主元
            p = self._mid_three_partition(l, r, reverse=reverse)   # 三数取中法
            # p = self._mid_three_randomized_partition(l, r, reverse=reverse)  # 随机三数取中法
            if p >= 0:
                self._quick_sort(l, p - 1, reverse=reverse)  # 在左子数组中递归
                self._quick_sort(p + 1, r, reverse=reverse)  # 在右子数组中递归
            else:
                print('_quick_sort: Error Path. l=', l, '\tr=', r, '\tp=', p)

    # 从数组 A 中选取主元下标 p、划分区间
    # 使得位于下标 p 之前的元素值都小于等于 A[p]，之后的都大于等于 A[p]
    # 若为降序排列，则反之。
    # 简单的快排主元选取，可以总是选取 A[r] 即最右元素作为主元，
    def _partition(self, l, r, reverse=False):
        if 0 <= l < r < len(self.ele_list):
            p_key = getattr(self.ele_list[r], self.key_name)
            # 做法：快慢双指针。
            # i 为慢指针，只有在某个比 p_key 小的元素被换到数组前半部分后，才会增长
            # j 为快指针，逐个往后判断当前元素的 key 是否小于等于 p_key
            i = l - 1
            if not reverse:
                for j in range(l, r):  # j = l..r-1
                    if getattr(self.ele_list[j], self.key_name) <= p_key:
                        i += 1
                        self._exchange(i, j)
            else:
                for j in range(l, r):  # j = l..r-1
                    if getattr(self.ele_list[j], self.key_name) >= p_key:
                        i += 1
                        self._exchange(i, j)
            self._exchange(i + 1, r)
            return i + 1  # 返回主元元素最终的下标位置，即为划分子区间的下标
        else:
            print('_partition: Error Path. l=', l, '\tr=', r)
            return -1

    # _partition 中选取主元缺乏随机性，如果数组本就有序，或几乎有序，则很影响快排效率
    # 几乎有序的场景也不少，比如往一个有序的数组中新插入某个值，再重新排序
    # 常有两种改进方式：1. 根据随机数，随机选取主元。2. 三数取中划分。
    def _randomized_partition(self, l, r, reverse=False):
        if 0 <= l < r < len(self.ele_list):
            if r - l > 1:  # r - l > 1 表示当前子数组元素有至少 3 个元素
                p_index = self._get_random_int(l, r)
                self._exchange(p_index, r)  # 把主元交换到 index=r 即可
            return self._partition(l, r, reverse=reverse)  # 调用原本的 partition 函数
        else:
            print('_mid_three_partition: Error Path. l=', l, '\tr=', r)
            return -1

    # (常用)三数取中划分：若当前数组区间的元素不少于 3，
    # 取最左、中间、最右这三个元素的 key 中位数者作为主元
    def _mid_three_partition(self, l, r, reverse=False):
        if 0 <= l < r < len(self.ele_list):
            if r - l > 3:  # r - l > 3 表示当前子数组元素有至少 5 个元素
                mid_index = int((l + r) >> 1)
                p_index = self._get_mid_key_index(l, mid_index, r)
                self._exchange(p_index, r)  # 把主元交换到 index=r 即可
            return self._partition(l, r, reverse=reverse)  # 调用原本的 partition 函数
        else:
            print('_mid_three_partition: Error Path. l=', l, '\tr=', r)
            return -1

    # 随机三数取中划分：若当前数组区间的元素不少于 3，
    # 则先从中随机选出 3 个元素，再取其中位数作为主元
    def _mid_three_randomized_partition(self, l, r, reverse=False):
        if 0 <= l < r < len(self.ele_list):
            if r - l > 3:  # r - l > 3 表示当前子数组元素有至少 5 个元素
                p_index1 = self._get_random_int(l, r)
                p_index2 = self._get_random_int(l, r)
                p_index3 = self._get_random_int(l, r)
                p_index = self._get_mid_key_index(p_index1, p_index2, p_index3)
                self._exchange(p_index, r)  # 把主元交换到 index=r 即可
            return self._partition(l, r, reverse=reverse)  # 调用原本的 partition 函数
        else:
            print('_mid_three_randomized_partition: Error Path. l=', l, '\tr=', r)
            return -1

    # 辅助函数：交换 self.ele_list 中下标 i 和下标 j 的两个元素
    # 参数范围 0 <= i,j < ele_len
    def _exchange(self, i, j):
        if i != j:
            ele_len = len(self.ele_list)
            if 0 <= i < ele_len and 0 <= i < ele_len:
                temp = self.ele_list[i]
                self.ele_list[i] = self.ele_list[j]
                self.ele_list[j] = temp
            else:
                # 数组越界
                print('_exchange: Error Path. i=', i, '\tj=', j)
        else:
            # 下标相同，无需处理
            pass

    # 辅助函数：获取闭区间 [l, r] 范围内的一个随机整数
    # 注意：调用前要确保 l <= r
    @staticmethod
    def _get_random_int(l, r):
        time_int = int(time.time())
        random.seed(time_int)  # 每次根据当前时间更换随机数种子
        return random.randint(l, r)

    # 辅助函数：三数取中
    # 输入三个下标。根据这三个下标对应元素的 key 值，取中位数者的下标返回。
    # 注意：调用前要确保 0 <= a,b,c < len(self.ele_list)
    def _get_mid_key_index(self, index1, index2, index3):
        key1 = getattr(self.ele_list[index1], self.key_name)
        key2 = getattr(self.ele_list[index2], self.key_name)
        key3 = getattr(self.ele_list[index3], self.key_name)
        if key1 <= key2:
            if key2 <= key3:
                return index2
            elif key1 <= key3:
                return index3
            else:
                return index1
        else:
            # 此时 key2 < key1
            if key1 <= key3:
                return index1
            elif key2 <= key3:
                return index3
            else:
                return index2


def main():
    # 键值对列表
    kv_list = [
        [3, 300], [1, 100], [2, 200], [8, 800],
        [7, 700], [9, 900], [3, 301]
    ]

    # kv_list = [[x, 100 * x] for x in range(1000)]  # (三数取中法)排序耗时 4.40400 ms
    # kv_list = [[x, 100 * x] for x in reversed(range(1000))]  # (三数取中法)排序耗时 10.60200 ms
    # random.seed(7)
    # kv_list = []
    # for i in range(1000):
    #     cur_key = random.randint(0, 1000)
    #     kv_list.append([cur_key, cur_key * 100])  # (三数取中法)排序耗时 6.75700 ms

    # Element 元素列表(待排序)
    node_list = []
    if isinstance(kv_list, list) and len(kv_list) > 0:
        for kv in kv_list:
            if isinstance(kv, list) and len(kv) == 2:
                node_list.append(Element(kv[0], kv[1]))

    # _sort = Sort(node_list)
    _sort = QuickSort(node_list)
    print(_sort.get_key_list())  # [3, 1, 2, 8, 7, 9, 3]

    start = time.process_time()
    _sort.do_sort(reverse=False)
    end = time.process_time()

    print(_sort.get_key_list())  # [1, 2, 3, 3, 7, 8, 9]
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    sorted_ele_list = _sort.get_ele_list()
    if isinstance(sorted_ele_list, list) and len(sorted_ele_list) > 0:
        for ele in sorted_ele_list:
            if isinstance(ele, Element):
                print('key:', ele.key, '\tval:', ele.val)


if __name__ == "__main__":
    sys.exit(main())
