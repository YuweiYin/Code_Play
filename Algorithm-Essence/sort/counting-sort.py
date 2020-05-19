#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : counting-sort.py
@Author  : YuweiYin
@Date    : 2020-05-10
=================================================="""

import sys
import time

"""
线性时间排序 - 计数排序 Counting Sort

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 8
https://www.youtube.com/watch?v=Nz1KZXbghj8
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


# 计数排序 (继承自 Sort 类)
# 空间复杂度(辅助存储)：O(n)
# 时间复杂度：O(n)
# 算法稳定性：稳定
# 场景：计数排序假设数据的 key 都属于一个 小区间 内的 整数。
# 缺点：1. key 必须为整数；2. 待排序数组中最大 key 值不能远超数组长度 n。
class CountingSort(Sort):
    def __init__(self, ele_list, max_int, key_name='key', val_name='val'):
        super(CountingSort, self).__init__(ele_list, key_name, val_name)

        self.output_ele_list = [None] * len(self.ele_list)  # 存放排序的 node 输出

        self.max_int = max_int  # 辅助数组的大小，其长度至少要等于输入数组中的最大整数值 + 1
        # 如果 self.max_int 为 O(n) 级别，则为线性时间复杂度。因此该值的设置要特别考量

    # 重载 do_sort 方法
    # 排序操作前需已确保每个元素都含指定的 key_name 和 val_name 属性
    # 时间复杂度：O(n + k)，k=self.max_int
    def do_sort(self, reverse=False):
        self._counting_sort()
        # 如果降序，则反转列表
        if reverse:
            self.output_ele_list.reverse()

    # 计数排序，默认升序
    def _counting_sort(self):
        temp_list = [0] * self.max_int
        # 仅关注整数 key，例如此时 ele_list = [3, 1, 2, 8, 7, 9, 3]
        # temp_list 此时是长度为 self.max_int 的全 0 数组
        # 以最大长度为 10 为例, temp_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(len(self.ele_list)):
            cur_key = getattr(self.ele_list[i], self.key_name)
            temp_list[cur_key] += 1
        # 现在 temp_list[cur_key] 存放了 self.ele_list 中 key=cur_key 的元素数目
        # temp_list = [0, 1, 1, 2, 0, 0, 0, 1, 1, 1]

        for i in range(1, self.max_int):
            temp_list[i] += temp_list[i - 1]
        # 现在 temp_list[cur_key] 存放了 self.ele_list 中 key<=cur_key 的元素数目
        # temp_list = [0, 1, 2, 4, 4, 4, 4, 5, 6, 7]

        # 输出到 self.output_list
        # 查询 temp_list，比如 cur_key=9 的元素，temp_list[9]=7
        # 于是输出数组 output_key_list 中下标为 7-1 的元素 key 应该为 9
        for i in reversed(range(len(self.ele_list))):
            cur_key = getattr(self.ele_list[i], self.key_name)
            self.output_ele_list[temp_list[cur_key] - 1] = self.ele_list[i]
            temp_list[cur_key] -= 1  # 由于存在 key 相等的元素，因此下次该把同样 key 的元素前移放置
            # 比如第一次 cur_key=3 时，查询 temp_list[3]=4，将 key=3 放置于输出数组的 3-1 位置
            # 然后执行 temp_list[3] -= 1，所以第二次 cur_key=3 时，查询到的就是 temp_list[3]=3
            # 而且，这样也能保证排序算法的稳定性！其稳定性是保证 Radix Sort 基数排序正确性的关键。

        # # 如果降序，则反转列表
        # if reverse:
        #     self.output_ele_list.reverse()

    # 交换 ele_list 中两个下标的元素 O(1)
    def _exchange(self, i, j):
        temp = self.ele_list[i]
        self.ele_list[i] = self.ele_list[j]
        self.ele_list[j] = temp

    # 获取已排序的 output 元素列表
    def get_output_ele_list(self):
        return self.output_ele_list

    # 获取已排序的 output 元素列表中 key 的列表
    def get_output_key_list(self):
        if isinstance(self.output_ele_list, list) and len(self.output_ele_list) > 0:
            key_list = []
            for ele in self.output_ele_list:
                if hasattr(ele, self.key_name):
                    key_list.append(getattr(ele, self.key_name))
            return key_list
        else:
            return None

    # 获取已排序的 output 元素列表中 val 的列表
    def get_output_val_list(self):
        if isinstance(self.output_ele_list, list) and len(self.output_ele_list) > 0:
            val_list = []
            for ele in self.output_ele_list:
                if hasattr(ele, self.val_name):
                    val_list.append(getattr(ele, self.val_name))
            return val_list
        else:
            return None

    # 获取原始数组
    def get_ele_list(self):
        return self.output_ele_list

    # 获取原始数组中 key 的列表
    def get_key_list(self):
        if isinstance(self.ele_list, list) and len(self.ele_list) > 0:
            key_list = []
            for ele in self.ele_list:
                if hasattr(ele, self.key_name):
                    key_list.append(getattr(ele, self.key_name))
            return key_list
        else:
            return None

    # 获取原始数组中 val 的列表
    def get_val_list(self):
        if isinstance(self.ele_list, list) and len(self.ele_list) > 0:
            val_list = []
            for ele in self.ele_list:
                if hasattr(ele, self.val_name):
                    val_list.append(getattr(ele, self.val_name))
            return val_list
        else:
            return None

    # (重载) 修改待排序数组
    def update_ele_list_and_max_int(self, new_ele_list, new_max_int):
        self.__init__(new_ele_list, new_max_int, key_name=self.key_name, val_name=self.val_name)


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
    _sort = CountingSort(node_list, 10)
    print(_sort.get_key_list())  # [3, 1, 2, 8, 7, 9, 3]

    # 排序。reverse 为 False 升序(默认) / True 降序
    is_reverse = False
    start = time.process_time()
    _sort.do_sort(reverse=is_reverse)  # 计数排序 O(n)
    end = time.process_time()
    print(_sort.get_output_key_list())
    print('do_sort: Running Time: %.5f ms' % ((end - start) * 1000))

    # 输出键 key 和值 val，可观察计数排序的稳定性：稳定！
    sorted_ele_list = _sort.output_ele_list
    if isinstance(sorted_ele_list, list) and len(sorted_ele_list) > 0:
        for ele in sorted_ele_list:
            if isinstance(ele, Element):
                print('key:', ele.key, '\tval:', ele.val)


if __name__ == "__main__":
    sys.exit(main())
