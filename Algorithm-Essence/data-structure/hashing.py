#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : hashing.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
哈希散列 Hashing

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 11
MIT 6.006 Introduction to Algorithms, Fall 2011
    8. Hashing with Chaining - https://www.youtube.com/watch?v=0M_kIqhwbFo
    9. Table Doubling, Karp-Rabin - https://www.youtube.com/watch?v=BRO7mVIFt08
    10. Open Addressing, Cryptographic Hashing - https://www.youtube.com/watch?v=rvdJDijO2Ro
MIT 6.046J Design and Analysis of Algorithms, Spring 2015
    8. Randomization: Universal & Perfect Hashing - https://www.youtube.com/watch?v=z0lJ2k0sl1g
MIT 6.854J Advanced Algorithms
    Lecture 06, 09/18: Hashing - https://www.youtube.com/watch?v=z8DD-ikAjzM
MIT 6.854 (Advanced Algorithms), Spring 2016
    Lecture 3: Consistent Hashing and Random Trees - https://www.youtube.com/watch?v=hM547xRIdzc
"""


# 元素结构体 key-value 键值对
class Element:
    def __init__(self, key, val=None):
        self.key = key  # (必备) 键 key。按 key 排序，因此 key 必须具有全序关系（常为整数）
        self.val = val  # (可选) 值 value。可为任意对象


# 哈希链接表中的元素链表，非循环双向链表（双向使得按元素删除时能够做到 O(1) 的最坏运行时间）
class ElementListNode:
    def __init__(self, ele=None):
        self.ele = ele        # 本结点包含的 Element 元素
        self.pre_ele = None   # 指向前一个元素结点
        self.next_ele = None  # 指向下一个元素结点


# 哈希表
class HashTable:
    def __init__(self, ele_list, hash_table_type=0, hash_func_type=0,
                 ele_name='ele', key_name='key', val_name='val'):
        self.ele_list = ele_list  # 初始化的 key, val 数组，可以为空
        self.key_name = key_name  # Element 元素结构体中 key 键属性的名称
        self.val_name = val_name  # Element 元素结构体中 val 值属性的名称
        self.ele_name = ele_name  # 哈希链接表中，ElementListNode 结点中 Element 元素的属性名
        self.hash_table_type = hash_table_type  # 哈希表解决冲突的方式：0/1 分别为链接法/开放寻址法
        self.hash_func_type = hash_func_type    # 哈希函数类型：0/1/2 分别为除法散列/乘法散列/全域散列
        self.load_factor_grow_ch = 0.9   # 哈希链接表，当装载因子为 0.9 时扩张哈希表大小，并重新哈希 rehash
        self.load_factor_grow_oa = 0.75  # 开放寻址法，当装载因子为 0.75 时扩张哈希表大小，并重新哈希 rehash
        self.load_factor_shrink = 0.25   # 当装载因子为 0.25 时缩减哈希表大小，并重新哈希 rehash
        self._verify_key_val()

    # 获取 self.ele_list 元素列表
    def get_ele_list(self):
        return [[ele.key, ele.val] for ele in self.ele_list]

    # 确保 ele_list 中每个元素都有 key_name 属性和 val_name 属性
    # 如果某元素没有这两个属性，则将之从 ele_list 中剔除出去
    def _verify_key_val(self):
        new_ele_list = []
        for ele in self.ele_list:
            if hasattr(ele, self.key_name) and hasattr(ele, self.val_name):
                new_ele_list.append(ele)
            else:
                pass
        self.ele_list = new_ele_list

    # 预哈希 Pre-Hashing 将输入的原始 key 转为一个自然数
    def _pre_hashing(self):
        pass

    # 对外字典操作接口：按关键字 key 或者按元素对象 ele，
    # 进行查询 search、插入 insert、删除 delete 操作。

    # 按关键字 key 查询哈希表
    # 查询成功则返回目标元素对象，否则返回 None
    def do_search_key(self, key):
        if self.hash_table_type == 0:
            return self._search_key_chaining(key)
        elif self.hash_table_type == 1:
            return self._search_key_oa(key)
        else:
            print('do_search_key: Error hash_table_type:', self.hash_table_type)
            return None

    # 按元素对象 ele 查询哈希表
    # 查询成功则返回目标元素对象，否则返回 None
    def do_search_ele(self, ele):
        if self.hash_table_type == 0:
            return self._search_ele_chaining(ele)
        elif self.hash_table_type == 1:
            return self._search_ele_oa(ele)
        else:
            print('do_search_ele: Error hash_table_type:', self.hash_table_type)
            return None

    # 按关键字 key 插入元素到哈希表
    # 插入成功则返回 True，否则返回 False
    def do_insert_key(self, key):
        if self.hash_table_type == 0:
            return self._insert_key_chaining(key)
        elif self.hash_table_type == 1:
            return self._insert_key_oa(key)
        else:
            print('do_insert_key: Error hash_table_type:', self.hash_table_type)
            return False

    # 将元素对象 ele 插入哈希表
    # 插入成功则返回 True，否则返回 False
    def do_insert_ele(self, ele):
        if self.hash_table_type == 0:
            return self._insert_ele_chaining(ele)
        elif self.hash_table_type == 1:
            return self._insert_ele_oa(ele)
        else:
            print('do_insert_ele: Error hash_table_type:', self.hash_table_type)
            return False

    # 按关键字 key 从哈希表中删除元素对象
    # 删除成功则返回目标元素对象，否则返回 None
    def do_delete_key(self, key):
        if self.hash_table_type == 0:
            return self._delete_key_chaining(key)
        elif self.hash_table_type == 1:
            return self._delete_key_oa(key)
        else:
            print('do_delete_key: Error hash_table_type:', self.hash_table_type)
            return None

    # 从哈希表中删除元素对象 ele
    # 删除成功则返回目标元素对象，否则返回 None
    def do_delete_ele(self, ele):
        if self.hash_table_type == 0:
            return self._delete_ele_chaining(ele)
        elif self.hash_table_type == 1:
            return self._delete_ele_oa(ele)
        else:
            print('do_delete_ele: Error hash_table_type:', self.hash_table_type)
            return None

    # 哈希散列函数 Hash Function

    # 除法散列法 Division Hashing
    # h(k) = k \mod p
    # 先根据当前数据特征选择 p 值
    # 好的 p 值：不接近 2 的整数次幂的较大素数
    def _division_hashing(self, key):
        pass

    # 乘法散列法 Multiplication Hashing
    # h(k) = \floor(p (kA \mod 1))
    # A 常被某个被随机选定的数字
    # Knuth 认为 A = (\sqrt(5) - 1) / 2 (约等于 0.6180339887...) 是一个比较理想的值
    # 乘法散列法的一个优点是对 p 的选择不是特别关键
    # 一般选择 p 为 2 的某个幂次 (p = 2^q，q 为某个正整数) 而非素数
    def _multiplication_hashing(self, key):
        pass

    # 全域散列法 Universal Hashing
    # h(k) = ((kA + b) \mod p) \mod m
    # 等价于 h(k) = ((kA) \mod 2^w) >> (w - r)
    # 其中 p 为某个大素数（大于全域），而 m 是哈希表长度
    # a 和 b 是从闭区间 [0, p-1] 中随机取值的
    # 对于全域散列法，在最坏情况下，冲突的概率是 1/m
    # 即：对任意 k1 != k2 而言，Pr{h(k1) = h(k2)} = 1/m
    def _universal_hashing(self, key):
        pass

    # 获得(大)素数
    # 大素数要在 Polynomial Time 多项式时间内找到
    def _get_prime(self):
        pass

    # 散列表的动态扩张 grow
    def _table_doubling(self):
        pass

    # 散列表的动态缩小 shrink
    def _table_shrink(self):
        pass

    # 重新哈希 rehash
    def _rehash(self):
        pass

    # 开放寻址法 - 探查 Probing

    # 线性探查 Linear Probing
    # h(k, i) = (h'(k) + i) \mod m
    # 其中 h' 为辅助散列函数，可以为普通的散列函数 h(k)
    # i 的取值为 0, 1, 2, ..., m-1，而 m 是哈希表长度
    def _linear_probing(self, key, index):
        pass

    # 二次探查 Quadratic Probing
    # h(k, i) = (h'(k) + c_1 * i + c_2 * i^2) \mod m
    # 其中 h' 为辅助散列函数，可以为普通的散列函数 h(k)
    # i 的取值为 0, 1, 2, ..., m-1，而 m 是哈希表长度
    def _quadratic_probing(self, key, index):
        pass

    # 双重散列 Double Hashing
    # h(k, i) = (h_1(k) + i * h_2(k)) \mod m
    # 其中 h_1 和 h_2 为辅助散列函数，可以为普通的散列函数 h(k)
    # i 的取值为 0, 1, 2, ..., m-1，而 m 是哈希表长度
    def _double_hashing(self, key, index):
        pass

    # 哈希链接表 Hash Chaining Table 字典操作

    def _search_key_chaining(self, key):
        pass

    def _search_ele_chaining(self, ele):
        pass

    def _insert_key_chaining(self, key):
        pass

    def _insert_ele_chaining(self, ele):
        pass

    def _delete_key_chaining(self, key):
        pass

    def _delete_ele_chaining(self, ele):
        pass

    # 开放寻址法 Open Addressing 字典操作

    def _search_key_oa(self, key):
        pass

    def _search_ele_oa(self, ele):
        pass

    def _insert_key_oa(self, key):
        pass

    def _insert_ele_oa(self, ele):
        pass

    def _delete_key_oa(self, key):
        pass

    def _delete_ele_oa(self, ele):
        pass

    # 完全散列 Perfect Hashing

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


def main():
    # 键值对列表
    kv_list = [
        [3, 300], [1, 100], [2, 200], [8, 800],
        [107, 10700], [99, 9900], [3, 301]
    ]

    # Element 元素列表(待排序)
    node_list = []
    if isinstance(kv_list, list) and len(kv_list) > 0:
        for kv in kv_list:
            if isinstance(kv, list) and len(kv) == 2:
                node_list.append(Element(kv[0], kv[1]))

    hash_chaining_table = HashTable(node_list, hash_table_type=0)
    # hash_open_addressing = HashTable(node_list, hash_table_type=1)

    start = time.process_time()
    hash_chaining_table.do_search_key(8)  # 哈希表查找
    end = time.process_time()
    print('hash_chaining_table: do_search_key. Running Time: %.5f ms' % ((end - start) * 1000))

    # start = time.process_time()
    # hash_open_addressing.do_search_key(8)  # 哈希表查找
    # end = time.process_time()
    # print('hash_chaining_table: do_search_key. Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
