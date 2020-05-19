#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : radix-sort.py
@Author  : YuweiYin
@Date    : 2020-05-10
=================================================="""

import sys
import time

"""
线性时间排序 - 基数排序 Radix Sort

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


# 基数排序 (继承自 Sort 类)
# 空间复杂度(辅助存储)：O(n)
# 时间复杂度：O(d(n+k))
# 算法稳定性：稳定
class RadixSort(Sort):
    def __init__(self, ele_list, radix=10, key_name='key', val_name='val'):
        super(RadixSort, self).__init__(ele_list, key_name, val_name)

        self.output_ele_list = [None] * len(self.ele_list)  # 存放排序的 node 输出
        self.max_int = 11  # 十进制，每一位的数字最多有 10 种可能选择，故 max_int = 10+1
        self.radix = radix  # 0x7fffffff = 2,147,483,647 仅有 10 位，所以这里设置 radix 默认值为 10
        self.radix_key_list_name = "radix_key_list"

        # 对每个元素，将其各位拆成长度为 self.radix 的列表，设置用于排序的属性 radix_key_list
        for i in range(len(self.ele_list)):
            cur_key = getattr(self.ele_list[i], self.key_name)
            # 拆成 str 后各位转 int，然后整体转 list，最后反转，列表低位即为数字低位
            radix_key_list = list(reversed(list(map(int, str(cur_key)))))
            # 补 0 至 self.radix 长度
            padding_list = [0] * (self.radix - len(radix_key_list))
            radix_key_list.extend(padding_list)
            setattr(self.ele_list[i], self.radix_key_list_name, radix_key_list)  # 增添属性

    def do_sort(self, reverse=False):
        self._radix_sort(reverse=reverse)

    def _radix_sort(self, reverse=False):
        # 每一位进行排序
        if self.radix > 0:
            for r in range(self.radix - 1):
                self._counting_sort(r)
                # 每轮结束后修改数组
                self.ele_list = self.output_ele_list
                self.output_ele_list = [None] * len(self.ele_list)
            # 最后一轮结束后不修改数组
            self._counting_sort(self.radix - 1)
            # 如果降序，则反转列表
            if reverse:
                self.output_ele_list.reverse()

    def _counting_sort(self, radix):
        temp_list = [0] * self.max_int

        for i in range(len(self.ele_list)):
            cur_key = getattr(self.ele_list[i], self.radix_key_list_name)[radix]
            temp_list[cur_key] += 1
        # 现在 temp_list[cur_key] 存放了 self.ele_list 中 key=cur_key 的元素数目

        for i in range(1, self.max_int):
            temp_list[i] += temp_list[i - 1]
        # 现在 temp_list[cur_key] 存放了 self.ele_list 中 key<=cur_key 的元素数目

        # 输出到 self.output_list
        for i in reversed(range(len(self.ele_list))):
            cur_key = getattr(self.ele_list[i], self.radix_key_list_name)[radix]
            # cur_key = getattr(self.ele_list[i], self.key_name)
            self.output_ele_list[temp_list[cur_key] - 1] = self.ele_list[i]
            temp_list[cur_key] -= 1  # 由于存在 key 相等的元素，因此下次该把同样 key 的元素前移放置

    # 获取已排序的 output 元素的 key-value 列表
    def get_output_kv_list(self):
        return [[ele.key, ele.val] for ele in self.output_ele_list]


def main():
    # 键值对列表
    kv_list = [
        [3, 300], [1, 100], [2, 200], [8, 800],
        [107, 10700], [99, 9900], [3, 301]
    ]

    # kv_list = [[i, 100 * i] for i in range(1000)]
    # kv_list = [[i, 100 * i] for i in reversed(range(1000))]

    # Element 元素列表(待排序)
    node_list = []
    if isinstance(kv_list, list) and len(kv_list) > 0:
        for kv in kv_list:
            if isinstance(kv, list) and len(kv) == 2:
                node_list.append(Element(kv[0], kv[1]))

    # _sort = Sort(node_list)
    # _sort = CountingSort(node_list, 1000)
    _sort = RadixSort(node_list, 10)
    print(_sort.get_key_list())  # [3, 1, 2, 8, 7, 9, 3]

    # 排序。reverse 为 False 升序(默认) / True 降序
    is_reverse = False
    start = time.process_time()
    _sort.do_sort(reverse=is_reverse)  # 计数排序 O(n)
    end = time.process_time()
    # print(_sort.get_output_key_list())
    print('do_sort: Running Time: %.5f ms' % ((end - start) * 1000))

    # 系统排序结果，升序降序均 正确、稳定、高效！
    # sorted_ele_list = _sort.output_ele_list
    sorted_kv_list = _sort.get_output_kv_list()
    print(sorted_kv_list)
    # [[107, 10700], [99, 9900], [8, 800], [3, 301], [3, 300], [2, 200], [1, 100]]


if __name__ == "__main__":
    sys.exit(main())
