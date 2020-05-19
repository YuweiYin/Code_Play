#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : bucket-sort.py
@Author  : YuweiYin
@Date    : 2020-05-11
=================================================="""

import sys
import time

"""
线性时间排序 - 桶排序 Bucket Sort

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


# 被桶 (数组) 所链接的元素链表，非循环双向链表
class ElementListNode:
    def __init__(self, ele=None):
        self.ele = ele        # 本结点包含的 Element 元素
        self.pre_ele = None   # 指向前一个元素结点
        self.next_ele = None  # 指向下一个元素结点


# 桶排序 (继承自 Sort 类)
# 空间复杂度(辅助存储)：O(n)
# 时间复杂度-平均：O(n)
# 算法稳定性：稳定
# 场景：桶排序假设输入数据的 key 是由一个随机过程产生的，该过程将元素均匀、独立地分布在 [0, 1) 半闭半开区间上。
# (即数据服从均匀分布，这样才能保证每个桶中的元素数目比较均衡)
# 限制：1. key 的取值范围为 [0, 1) 半闭半开区间。2. 对数据分布有假设，如果不满足假设，可能会导致很差的效率。
class BucketSort(Sort):
    def __init__(self, ele_list, ele_name='ele', key_name='key', val_name='val'):
        super(BucketSort, self).__init__(ele_list, key_name, val_name)

        self.ele_name = ele_name   # ElementListNode 结点中 Element 元素的属性名
        self.output_ele_list = []  # 存放排序后的 node 输出

    def do_sort(self, reverse=False):
        self._bucket_sort()
        # 如果降序，则反转列表
        if reverse:
            self.output_ele_list.reverse()

    def _bucket_sort(self):
        ele_len = len(self.ele_list)
        # 设置桶列表 bucket_list，其中的元素为该下标所代表的桶的头结点，值为 -inf
        bucket_list = []
        neg_inf = -0x3f3f3f3f
        for i in range(ele_len):
            head_ele = Element(neg_inf, None)
            bucket_list.append(ElementListNode(head_ele))
        for cur_ele in self.ele_list:
            cur_key = getattr(cur_ele, self.key_name)
            bucket_index = int(cur_key * ele_len)  # 获得当前 key 应该被插入的桶 (数组下标)
            if isinstance(bucket_list[bucket_index], ElementListNode):
                # 寻找插入位置，升序排列
                is_insert = False
                ptr = bucket_list[bucket_index]
                while isinstance(ptr.next_ele, ElementListNode):
                    next_ele = getattr(ptr.next_ele, self.ele_name)
                    next_key = getattr(next_ele, self.key_name)
                    if cur_key < next_key:
                        # 找到了插入位置，即 ptr 结点的后面
                        new_node = ElementListNode()
                        setattr(new_node, self.ele_name, cur_ele)
                        ptr.next_ele.pre_ele = new_node
                        new_node.next_ele = ptr.next_ele
                        ptr.next_ele = new_node
                        new_node.pre_ele = ptr
                        is_insert = True
                        break
                    else:
                        ptr = ptr.next_ele
                # 此时 ptr 结点是当前桶的末尾非空结点，如果此前没有插入结点，则新结点应插入尾部
                if not is_insert:
                    new_node = ElementListNode()
                    setattr(new_node, self.ele_name, cur_ele)
                    ptr.next_ele = new_node
                    new_node.pre_ele = ptr.next_ele
                else:
                    pass
            else:
                # 如若此桶为空，则创建新结点。正常情况下不会执行此支路
                new_node = ElementListNode()
                setattr(new_node, self.ele_name, cur_ele)
                bucket_list[bucket_index] = new_node
        # 此时所有结点均已插入桶中，自小到大遍历桶数组，将全部桶结点串在一起，作为输出
        self.output_ele_list = []
        for bucket in bucket_list:
            ptr = bucket.next_ele
            while isinstance(ptr, ElementListNode):
                self.output_ele_list.append(ptr.ele)
                ptr = ptr.next_ele

    # 获取已排序的 output 元素的 key-value 列表
    def get_output_kv_list(self):
        return [[ele.key, ele.val] for ele in self.output_ele_list]


def main():
    # 键值对列表
    kv_list = [
        [0.3, 300], [0.1, 100], [0.2, 200], [0.8, 800],
        [0.107, 10700], [0.99, 9900], [0.3, 301]
    ]

    # Element 元素列表(待排序)
    node_list = []
    if isinstance(kv_list, list) and len(kv_list) > 0:
        for kv in kv_list:
            if isinstance(kv, list) and len(kv) == 2:
                node_list.append(Element(kv[0], kv[1]))

    # _sort = Sort(node_list)
    # _sort = CountingSort(node_list, 1000)
    # _sort = RadixSort(node_list, 10)
    _sort = BucketSort(node_list)
    print(_sort.get_key_list())  # [3, 1, 2, 8, 7, 9, 3]

    # 排序。reverse 为 False 升序(默认) / True 降序
    is_reverse = False
    start = time.process_time()
    _sort.do_sort(reverse=is_reverse)  # 桶排序 O(n)
    end = time.process_time()
    # print(_sort.get_output_key_list())
    print('do_sort: Running Time: %.5f ms' % ((end - start) * 1000))

    # 系统排序结果，升序降序均 正确、稳定、高效！
    # sorted_ele_list = _sort.output_ele_list
    sorted_kv_list = _sort.get_output_kv_list()
    print(sorted_kv_list)
    # [[0.1, 100], [0.107, 10700], [0.2, 200], [0.3, 300], [0.3, 301], [0.8, 800], [0.99, 9900]]


if __name__ == "__main__":
    sys.exit(main())
