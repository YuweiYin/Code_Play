#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : union-find.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
并查集 (Union Find)
不相交集合 (Disjoint Set, DS)
"""


class SetNode:
    def __init__(self, key):
        self.key = key      # 本元素的 key 号
        self.father = self  # 指针，指向本元素的父结点，初始时指向自己
        self.rank = 1       # 本元素所在集合的 rank 秩


class UnionFind:
    # 构造不相交集合
    # 时间复杂度 O(n)
    def __init__(self, key_array):
        self.set_len = len(key_array)
        self.disjoint_set = []    # 存放全体元素 SetNode 结构体
        self.key2node = dict({})  # 将 key 号映射为 SetNode 结构体

        for key in key_array:
            new_node = SetNode(key)
            self.key2node[key] = new_node
            self.disjoint_set.append(new_node)

    # find 操作；查找 key 为 x 的元素所在集合的代表元素。
    # 原始的 find 操作，时间复杂度与查询元素所在集合的秩呈线性关系
    # def find(self, x):
    #     if x in self.key2node:
    #         node_x = self.key2node[x]
    #     else:
    #         return None
    #
    #     while node_x.father != node_x:
    #         node_x = node_x.father
    #     return node_x

    # find 操作经过路径压缩优化后，平均时间复杂度为 O(1)
    def find(self, x):
        if x in self.key2node:
            node_x = self.key2node[x]
        else:
            return None

        while node_x.father != node_x:
            temp = node_x.father
            node_x.father = node_x.father.father
            node_x = temp
        return node_x

    # union 操作；将 key 分别为 x 和 y 的元素 所在的集合合并成一个新集合，返回新集合的代表元素。
    # 原始的 union 操作，选择返回 union 函数首个参数代表，的元素可能导致树过高、不平衡
    # def union(self, x, y):
    #     root_x = self.find(x)
    #     root_y = self.find(y)
    #
    #     if root_x is None or root_y is None:
    #         return None
    #     else:
    #         if root_x != root_y:
    #             # 此处未做优化，默认选择 union 函数首个参数代表的元素作为新集合的代表元素
    #             root_y.father = root_x
    #         return root_x

    # 这里进行按秩合并优化，选择 find 结果中 秩更小的元素作为新集合的代表元素
    # 经过按秩合并优化后，树高至多为 log n，因此平均时间复杂度为 O(1)、最坏时间复杂度为 O(log n)
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x is None or root_y is None:
            return None
        else:
            if root_x != root_y:
                if root_x.rank < root_y.rank:
                    # 如果 root_x 的秩小于 root_y 的秩，则让 root_x 指向 root_y
                    root_x.father = root_y
                    # 修改 y 的秩为 y 秩与 x 秩加一中的较大值，
                    # 因为 root_y 被 root_x 所指不一定使得 root_y 的树高提升。
                    root_y.rank = max(root_y.rank, root_x.rank + 1)
                    return root_y
                else:
                    # 否则让 root_y 指向 root_x
                    root_y.father = root_x
                    # 修改 x 的秩为 x 秩与 y 秩加一中的较大值
                    root_x.rank = max(root_x.rank, root_y.rank + 1)
                    return root_x
            else:
                # 二者相同，任意返回一个。此处选择返回 union 函数首个参数代表的元素
                return root_x

    def print_set(self):
        for node in self.disjoint_set:
            print(node.key)


def main():
    key_array = [3, 1, 2, 8, 7, 9]

    union_find = UnionFind(key_array)
    union_find.union(3, 1)  # 3 <- 1
    union_find.union(1, 2)  # 路径压缩 & 按秩合并 3 <- 2
    union_find.union(8, 7)  # 8 <- 7
    union_find.union(7, 9)  # 路径压缩 & 按秩合并 8 <- 9

    # union_find.print_set()

    start = time.process_time()
    res = union_find.find(2)  # 3
    end = time.process_time()

    if res is not None and isinstance(res, SetNode):
        print('res_key:', res.key)
    else:
        print('find None!')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
