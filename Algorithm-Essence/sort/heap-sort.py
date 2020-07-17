#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : heap-sort.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
堆排序 Heap Sort

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 6
"""


# 元素结构体 key-value 键值对
class Element:
    def __init__(self, key, val=None):
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


# 堆排序 (继承自 Sort 类)
# 空间复杂度(辅助存储)：O(1)
# 时间复杂度-平均/最好/最坏 O(n log n)
# 算法稳定性：不稳定
# 堆排序与(直接)插入排序的相同点在于空间原址性，只需要额外 O(1) 的辅助存储空间。
# 堆排序与(二路)归并排序的相同点在于时间复杂度均为 O(n log n)。
# 但堆排序是不稳定的，这跟(直接)插入排序和(二路)归并排序不同。
class HeapSort(Sort):
    def __init__(self, ele_list, key_name='key', val_name='val'):
        super(HeapSort, self).__init__(ele_list, key_name, val_name)

        # 设置 min_ele_list 用于构建最小堆
        neg_inf = -0x3f3f3f3f
        min_none_node = Element(neg_inf)
        self.min_ele_list = [min_none_node]  # 堆首占位空元素，方便下标计算

        if isinstance(self.ele_list, list) and isinstance(self.min_ele_list, list):
            # 设置 min_ele_list 中的其它元素
            for ele in self.ele_list:
                new_ele = Element(getattr(ele, self.key_name),
                                  getattr(ele, self.val_name))
                self.min_ele_list.append(new_ele)

            # ele_list 用于构建最大堆，给其首位增加空元素
            inf = 0x3f3f3f3f
            max_none_node = Element(inf)
            self.ele_list.insert(0, max_none_node)    # 堆首占位空元素，方便下标计算
            # self.heap_size 表示有多少个堆元素存储在该数组中，数目不超过 ele_list
            self.max_heap_size = len(self.ele_list) - 1  # 实际堆长度比 ele_list 少一
            self.min_heap_size = len(self.min_ele_list) - 1  # 实际堆长度比 min_ele_list 少一

    # 重载 do_sort 方法
    # 排序操作前需已确保每个元素都含指定的 key_name 和 val_name 属性
    def do_sort(self, reverse=False):
        self._heap_sort(reverse=reverse)

    # 用最大堆进行升序排序。循环，每次把最大堆的首元素(当前的最大 key 值) 置于 ele_list 后方
    # 然后减少 max_heap_size，使得下次循环不会考虑被挪动到尾部的那些元素(已排好序)
    # 时间复杂度为 O(n log n)
    def _heap_sort(self, reverse=False):
        if not reverse:
            # key 升序排序(默认) - 利用最大堆
            self.build_max_heap()    # 构建最大堆，时间复杂度为 O(n)
            # ele_list 下标 0 的元素仅作占位，下标 1 的元素不用交换到尾部，因此从下标 2 开始
            for i in reversed(range(2, len(self.ele_list))):
                self._max_exchange(1, i)  # 除已经排好序的元素外，把当前最大元素交换至尾部
                self.max_heap_size -= 1   # 堆大小减一
                self._max_heapify(1)  # 因为堆顶元素改换了，所以需要自顶向下调整最大堆性质 O(log n)
            self.max_heap_size = len(self.ele_list) - 1  # 排序结束后恢复 heap_size
        else:
            # key 降序排序 - 利用最小堆
            self.build_min_heap()    # 构建最小堆，时间复杂度为 O(n)
            for i in reversed(range(2, len(self.min_ele_list))):
                self._min_exchange(1, i)  # 除已经排好序的元素外，把当前最小元素交换至尾部
                self.min_heap_size -= 1   # 堆大小减一
                self._min_heapify(1)  # 因为堆顶元素改换了，所以需要自顶向下调整最大堆性质 O(log n)
            self.min_heap_size = len(self.min_ele_list) - 1  # 排序结束后恢复 heap_size

    # 构建最大堆。时间复杂度为 O(n)
    # 虽然看似是 n 次 O(h) 的过程应该总时间复杂度为 O(n log n)，但这不是紧确界
    # 但由于树高 h 是逐渐升高的，经过数学计算分析，构建堆的时间复杂度为 O(n)
    # 根据堆的定义和性质，可以知道子数组 ele_list[(n>>1)+1..n] 中的元素都是树的叶结点，其余为中间结点
    # 而每个叶结点都可以看成只包含一个元素的堆。自底向上构造最大堆，并利用 max_heapify 维护最大堆性质
    def build_max_heap(self):
        self.max_heap_size = len(self.ele_list) - 1  # 实际堆长度比 ele_list 少一
        # 中间结点从下标 (n>>1) 开始，到 1
        leaf_start_index = (self.max_heap_size >> 1) + 1  # 叶结点在 ele_list 中的起始下标
        for index in reversed(range(1, leaf_start_index)):
            self._max_heapify(index)

    # 构建最小堆。时间复杂度为 O(n)。
    # 类似于构建最大堆的过程。自底向上构造最小堆，并利用 min_heapify 维护最小堆性质
    def build_min_heap(self):
        self.min_heap_size = len(self.min_ele_list) - 1  # 实际堆长度比 min_ele_list 少一
        # 中间结点从下标 (n>>1) 开始，到 1
        leaf_start_index = (self.min_heap_size >> 1) + 1  # 叶结点在 min_ele_list 中的起始下标
        for index in reversed(range(1, leaf_start_index)):
            self._min_heapify(index)

    # 维护最大堆性质。时间复杂度为 O(log n)
    # 假定根结点为 left(i) 和 right(i) 的二叉树都是最大堆
    # 但此时 ele_list[i] 的 key 有可能小于其孩子，违背最大堆的性质
    # max_heapify 通过让 ele_list[i] 的 key 在最大堆中"逐级下降"
    # 从而使得以下标 i 为根的子树重新遵循最大堆的性质
    # def _max_heapify(self, root_index):
    #     if root_index <= 0 or root_index >= len(self.ele_list):
    #         print('_max_heapify: Error Path. root_index:', root_index)
    #     else:
    #         left_index = self._left(root_index)
    #         right_index = self._right(root_index)
    #
    #         # 从当前结点、左孩子、右孩子三者中找出 key 最大者的下标
    #         if left_index <= self.max_heap_size and getattr(self.ele_list[left_index], self.key_name) > \
    #                 getattr(self.ele_list[root_index], self.key_name):
    #             largest = left_index
    #         else:
    #             largest = root_index
    #         if right_index <= self.max_heap_size and getattr(self.ele_list[right_index], self.key_name) > \
    #                 getattr(self.ele_list[largest], self.key_name):
    #             largest = right_index
    #
    #         # 如果当前结点不是最大者，则把最大者交换上来
    #         if largest != root_index:
    #             self._max_exchange(root_index, largest)
    #             self._max_heapify(largest)  # 继续往下调整

    # 改为循环结构的 max_heapify
    # 因为前述递归结构的 max_heapify 可能使某些编译器产生低效的代码
    def _max_heapify(self, root_index):
        if root_index <= 0 or root_index >= len(self.ele_list):
            print('_max_heapify: Error Path. root_index:', root_index)
        else:
            left_index = self._left(root_index)
            right_index = self._right(root_index)

            while left_index <= self.max_heap_size or right_index <= self.max_heap_size:
                # 从当前结点、左孩子、右孩子三者中找出 key 最大者的下标
                if left_index <= self.max_heap_size and getattr(self.ele_list[left_index], self.key_name) > \
                        getattr(self.ele_list[root_index], self.key_name):
                    largest = left_index
                else:
                    largest = root_index
                if right_index <= self.max_heap_size and getattr(self.ele_list[right_index], self.key_name) > \
                        getattr(self.ele_list[largest], self.key_name):
                    largest = right_index

                # 如果当前结点不是最大者，则把最大者交换上来
                if largest != root_index:
                    self._max_exchange(root_index, largest)
                    # 修改下标，往下移动，准备下一轮循环
                    root_index = largest
                    left_index = self._left(root_index)
                    right_index = self._right(root_index)
                else:
                    break

    # 维护最小堆性质。时间复杂度为 O(log n)
    # def _min_heapify(self, root_index):
    #     if root_index <= 0 or root_index >= len(self.min_ele_list):
    #         print('_min_heapify: Error Path. root_index:', root_index)
    #     else:
    #         left_index = self._left(root_index)
    #         right_index = self._right(root_index)
    #
    #         # 从当前结点、左孩子、右孩子三者中找出 key 最小者的下标
    #         if left_index <= self.min_heap_size and getattr(self.min_ele_list[left_index], self.key_name) < \
    #                 getattr(self.min_ele_list[root_index], self.key_name):
    #             smallest = left_index
    #         else:
    #             smallest = root_index
    #         if right_index <= self.min_heap_size and getattr(self.min_ele_list[right_index], self.key_name) < \
    #                 getattr(self.min_ele_list[smallest], self.key_name):
    #             smallest = right_index
    #
    #         # 如果当前结点不是最小者，则把最小者交换上来
    #         if smallest != root_index:
    #             self._min_exchange(root_index, smallest)
    #             self._max_heapify(smallest)  # 继续往下调整

    # 循环结构的 min_heapify
    def _min_heapify(self, root_index):
        if root_index <= 0 or root_index >= len(self.min_ele_list):
            print('_min_heapify: Error Path. root_index:', root_index)
        else:
            left_index = self._left(root_index)
            right_index = self._right(root_index)

            while left_index <= self.min_heap_size or right_index <= self.min_heap_size:
                # 从当前结点、左孩子、右孩子三者中找出 key 最小者的下标
                if left_index <= self.min_heap_size and getattr(self.min_ele_list[left_index], self.key_name) < \
                        getattr(self.min_ele_list[root_index], self.key_name):
                    smallest = left_index
                else:
                    smallest = root_index
                if right_index <= self.min_heap_size and getattr(self.min_ele_list[right_index], self.key_name) < \
                        getattr(self.min_ele_list[smallest], self.key_name):
                    smallest = right_index

                # 如果当前结点不是最小者，则把最小者交换上来
                if smallest != root_index:
                    self._min_exchange(root_index, smallest)
                    # 修改下标，往下移动，准备下一轮循环
                    root_index = smallest
                    left_index = self._left(root_index)
                    right_index = self._right(root_index)
                else:
                    break

    # 下面四个操作利用最大堆实现最大优先队列。前提：已建立最大堆

    # 获取 key 最大的元素
    # 时间复杂度：O(1)
    def get_maximum(self):
        # 最大堆的最大 key 的元素是 index=1 元素
        return self.ele_list[1]  # O(1)

    # 获取并移除 key 最大的元素
    # 时间复杂度：O(log n)
    # TODO 此时，使用同一数组的最小堆要重建，时间复杂度为 O(n)
    def extract_max(self):
        if self.max_heap_size < 1:
            print('Waning: 最大堆已空')
        if self.max_heap_size == 1:
            self.max_heap_size -= 1
            return self.ele_list.pop(1)
        else:
            max_ele = self.ele_list[1]  # 取出最大元素后需要更换堆根
            # self.ele_list[1] = self.ele_list[self.max_heap_size]
            self.ele_list[1] = self.ele_list.pop(self.max_heap_size)
            self.max_heap_size -= 1
            self._max_heapify(1)  # 维护最大堆性质 O(log n)
            return max_ele

    # 将最大堆 ele_list 中的第 index 个元素的键 key 增大为 new_key
    # 时间复杂度：O(log n)
    # TODO 此时，使用同一数组的最小堆要重建，时间复杂度为 O(n)
    def increase_key(self, index, new_key):
        if new_key < getattr(self.ele_list[index], self.key_name):
            print('Waning: 新 key 值小于当前 key')
        else:
            # 修改目标元素的 key 值，并逐级往上维护最大堆性质
            setattr(self.ele_list[index], self.key_name, new_key)
            while index > 1 and getattr(self.ele_list[self._parent(index)], self.key_name) < \
                    getattr(self.ele_list[index], self.key_name):
                # 如果 index 结点的父结点 key 小于 index 结点的 key，那么需要把 index 结点替换上去
                self._max_exchange(index, self._parent(index))
                index = self._parent(index)  # index 上移

    # 往最大堆中插入新元素 (Element 结构体)
    # 时间复杂度：O(log n)
    def max_heap_insert(self, new_ele):
        if hasattr(new_ele, self.key_name) and hasattr(new_ele, self.val_name):
            # 先在 ele_list 末尾插入一个 key 为负无穷 -inf 的元素（注意 val 设置）
            neg_inf = -0x3f3f3f3f
            neg_inf_node = Element(neg_inf, getattr(new_ele, self.val_name))
            self.ele_list.append(neg_inf_node)
            self.max_heap_size += 1
            # 然后再利用 increase_key 方法将此元素的 key 增大
            self.increase_key(self.max_heap_size, getattr(new_ele, self.key_name))
        else:
            print('Waning: 新元素没有属性名为 ', self.key_name,
                  ' 的键，或者没有属性名为 ', self.val_name, ' 的值')

    # 下面四个操作利用最小堆实现最小优先队列。前提：已建立最小堆

    # 获取 key 最小的元素
    # 时间复杂度：O(1)
    def get_minimum(self):
        # 最小堆的最小 key 的元素是 index=1 元素
        return self.min_ele_list[1]  # O(1)

    # 获取并移除 key 最小的元素
    # 时间复杂度：O(log n)
    # TODO 此时，使用同一数组的最大堆要重建，时间复杂度为 O(n)
    def extract_min(self):
        if self.min_heap_size < 1:
            print('Waning: 最小堆已空')
        elif self.min_heap_size == 1:
            self.min_heap_size -= 1
            return self.min_ele_list.pop(1)
        else:
            min_ele = self.min_ele_list[1]  # 取出最小元素后需要更换堆根
            # self.min_ele_list[1] = self.min_ele_list[self.min_heap_size]
            self.min_ele_list[1] = self.min_ele_list.pop(self.min_heap_size)
            self.min_heap_size -= 1
            self._min_heapify(1)  # 维护最小堆性质 O(log n)
            return min_ele

    # 将最小堆 min_ele_list 中的第 index 个元素的键 key 减小为 new_key
    # 时间复杂度：O(log n)
    # TODO 此时，使用同一数组的最大堆要重建，时间复杂度为 O(n)
    def decrease_key(self, index, new_key):
        if new_key > getattr(self.min_ele_list[index], self.key_name):
            print('Waning: 新 key 值大于当前 key')
        else:
            # 修改目标元素的 key 值，并逐级往上维护最小堆性质
            setattr(self.min_ele_list[index], self.key_name, new_key)
            while index > 1 and getattr(self.min_ele_list[self._parent(index)], self.key_name) > \
                    getattr(self.min_ele_list[index], self.key_name):
                # 如果 index 结点的父结点 key 大于 index 结点的 key，那么需要把 index 结点替换上去
                self._min_exchange(index, self._parent(index))
                index = self._parent(index)  # index 上移

    # 往最小堆中插入新元素 (Element 结构体)
    # 时间复杂度：O(log n)
    def min_heap_insert(self, new_ele):
        if hasattr(new_ele, self.key_name) and hasattr(new_ele, self.val_name):
            # 先在 ele_list 末尾插入一个 key 为正无穷 inf 的元素（注意 val 设置）
            inf = 0x3f3f3f3f
            inf_node = Element(inf, getattr(new_ele, self.val_name))
            self.min_ele_list.append(inf_node)
            self.min_heap_size += 1
            # 然后再利用 decrease_key 方法将此元素的 key 减小
            self.decrease_key(self.min_heap_size, getattr(new_ele, self.key_name))
        else:
            print('Waning: 新元素没有属性名为 ', self.key_name,
                  ' 的键，或者没有属性名为 ', self.val_name, ' 的值')

    # 插入新元素(Element 结构体)，同时影响最大堆和最小堆
    # 时间复杂度：O(log n)
    def heap_insert(self, new_ele):
        self.max_heap_insert(new_ele)
        self.min_heap_insert(new_ele)

    # 计算父结点下标 O(1)
    @staticmethod
    def _parent(index):
        return index >> 1

    # 计算左孩子下标 O(1)
    @staticmethod
    def _left(index):
        return index << 1

    # 计算右孩子下标 O(1)
    @staticmethod
    def _right(index):
        return (index << 1) + 1

    # 交换 ele_list 中两个下标的元素 O(1)
    def _max_exchange(self, i, j):
        temp = self.ele_list[i]
        self.ele_list[i] = self.ele_list[j]
        self.ele_list[j] = temp

    # 交换 min_ele_list 中两个下标的元素 O(1)
    def _min_exchange(self, i, j):
        temp = self.min_ele_list[i]
        self.min_ele_list[i] = self.min_ele_list[j]
        self.min_ele_list[j] = temp

    # (重载) 获取最大堆元素列表。去掉用于占位的首位元素
    def get_ele_list(self):
        return self.ele_list[1: 1 + self.max_heap_size]

    # (重载) 获取最大堆元素中 key 的列表。去掉用于占位的首位元素
    def get_key_list(self):
        key_list = []
        for ele in self.ele_list[1: 1 + self.max_heap_size]:
            if hasattr(ele, self.key_name):
                key_list.append(getattr(ele, self.key_name))
            else:
                pass
        return key_list

    # (重载) 获取最大堆元素中 val 的列表。去掉用于占位的首位元素
    def get_val_list(self):
        val_list = []
        for ele in self.ele_list[1: 1 + self.max_heap_size]:
            if hasattr(ele, self.val_name):
                val_list.append(getattr(ele, self.val_name))
            else:
                pass
        return val_list

    # 获取最小堆元素列表。去掉用于占位的首位元素
    def get_min_ele_list(self):
        return self.min_ele_list[1: 1 + self.min_heap_size]

    # 获取最小堆元素中 key 的列表。去掉用于占位的首位元素
    def get_min_key_list(self):
        key_list = []
        for ele in self.min_ele_list[1: 1 + self.min_heap_size]:
            if hasattr(ele, self.key_name):
                key_list.append(getattr(ele, self.key_name))
            else:
                pass
        return key_list

    # 获取最小堆元素中 val 的列表。去掉用于占位的首位元素
    def get_min_val_list(self):
        val_list = []
        for ele in self.min_ele_list[1: 1 + self.min_heap_size]:
            if hasattr(ele, self.val_name):
                val_list.append(getattr(ele, self.val_name))
            else:
                pass
        return val_list

    # (重载) 修改待排序数组。增添用于占位的首位元素，重新计算 heap_size
    def update_ele_list(self, new_ele_list):
        self.__init__(new_ele_list, key_name=self.key_name, val_name=self.val_name)


def main():
    # 键值对列表
    kv_list = [
        [3, 300], [1, 100], [2, 200], [8, 800],
        [7, 700], [9, 900], [3, 301]
    ]

    # Element 元素列表(待排序)
    node_list = []
    if isinstance(kv_list, list) and len(kv_list) > 0:
        for kv in kv_list:
            if isinstance(kv, list) and len(kv) == 2:
                node_list.append(Element(kv[0], kv[1]))

    # _sort = Sort(node_list)
    _sort = HeapSort(node_list)
    print(_sort.get_key_list())  # [3, 1, 2, 8, 7, 9, 3]
    # 建立最大堆
    _sort.build_max_heap()
    print(_sort.get_key_list())  # [9, 8, 3, 1, 7, 2, 3]
    # 建立最小堆
    _sort.build_min_heap()
    print(_sort.get_min_key_list())  # [1, 3, 2, 8, 7, 9, 3]

    # 堆排序。reverse 为 False 升序(默认) / True 降序
    is_reverse = False
    start = time.process_time()
    _sort.do_sort(reverse=is_reverse)  # 堆排序 O(n log n)
    end = time.process_time()

    if not is_reverse:
        print(_sort.get_key_list())  # [1, 2, 3, 3, 7, 8, 9]
        sorted_ele_list = _sort.get_ele_list()
        # 排序之后会破坏最大堆性质，为了下次使用，需重新建最大堆 O(n)
        _sort.build_max_heap()
        print(_sort.get_key_list())  # [9, 7, 8, 3, 2, 1, 3]
    else:
        print(_sort.get_min_key_list())  # [9, 8, 7, 3, 3, 2, 1]
        sorted_ele_list = _sort.get_min_ele_list()
        # 排序之后会破坏最小堆性质，为了下次使用，需重新建最小堆 O(n)
        _sort.build_min_heap()
        print(_sort.get_min_key_list())  # [1, 3, 2, 8, 3, 9, 7]

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 输出键 key 和值 val，可观察堆排序的稳定性
    if isinstance(sorted_ele_list, list) and len(sorted_ele_list) > 0:
        for ele in sorted_ele_list:
            if isinstance(ele, Element):
                print('key:', ele.key, '\tval:', ele.val)

    # 增添结点 (同时影响最大堆和最小堆)
    # 如果想单独对最大堆操作可调用 max_heap_insert
    # 如果想单独对最小堆操作可调用 min_heap_insert
    new_ele = Element(6, 666)
    _sort.heap_insert(new_ele)
    print(_sort.get_key_list())  # [9, 7, 8, 6, 2, 1, 3, 3]
    print(_sort.get_min_key_list())  # [1, 3, 2, 6, 7, 9, 3, 8]

    # 获取并移除 key 最大值、最小值
    # 这里，针对移除操作，最大堆 list 和最小堆 list 是分开处理的
    # 移除最大值是从最大堆移除、移除最小值是从最小堆移除
    max_ele = _sort.extract_max()  # key=9  val=900
    if isinstance(max_ele, Element):
        print('max_ele: key=', max_ele.key, '\tval=', max_ele.val)
    min_ele = _sort.extract_min()  # key=1  val=100
    if isinstance(min_ele, Element):
        print('max_ele: key=', min_ele.key, '\tval=', min_ele.val)

    print(_sort.get_key_list())  # [8, 7, 3, 6, 2, 1, 3]
    print(_sort.get_min_key_list())  # [2, 3, 3, 6, 7, 9, 8]

    # 获取 key 最大值、最小值
    max_ele = _sort.get_maximum()  # key=8  val=800
    if isinstance(max_ele, Element):
        print('max_ele: key=', max_ele.key, '\tval=', max_ele.val)
    min_ele = _sort.get_minimum()  # key=2  val=200
    if isinstance(min_ele, Element):
        print('max_ele: key=', min_ele.key, '\tval=', min_ele.val)


if __name__ == "__main__":
    sys.exit(main())
