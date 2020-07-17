#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : lowest-common-ancestor.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
最近公共祖先 (Lowest Common Ancestor, LCA)

参考资料：
https://www.youtube.com/watch?v=HeeyUZmaZg0
"""


# 邻接矩阵，通常适合稠密图
class AdjacencyMatrix:
    def __init__(self, edges):
        node_dict = dict({})

        for edge in edges:
            for node in edge:
                if node not in node_dict:
                    node_dict[node] = 1

        self.node_list = sorted(node_dict.keys())
        node_len = len(self.node_list)

        # 构建邻接矩阵（二维方阵），adj[x][y] 为 True 表示存在边 (x, y)
        self.adj = [[False] * node_len for _ in range(node_len)]
        for edge in edges:
            self.adj[edge[0]][edge[1]] = True
            self.adj[edge[1]][edge[0]] = True

    # 输出展示顶点列表
    def print_node_list(self):
        print(self.node_list)

    # 输出展示邻接矩阵
    def print_adj(self):
        for line in self.adj:
            print(line)


# 邻接表，通常适合稀疏图
# 邻接表的顶点结构（带边权）
class Vertex:
    # 构造方法
    def __init__(self, key):
        # 本顶点的 key
        self.key = key
        # 本顶点的邻居字典，key 为邻居的键，value 为边权
        self.neighbor = dict({})

    # 类序列化输出方法
    def __str__(self):
        return str(self.key) + 'is connected to:' + str([v.key for v in self.neighbor])

    # 增添本顶点的邻居 neighbor，以字典结构存储，weight 为边权
    def add_neighbor(self, neighbor, weight=0):
        self.neighbor[neighbor] = weight

    # 返回本顶点的所有邻接顶点 对象数组
    def get_connections(self):
        return self.neighbor.keys()

    # 获取本顶点的 key 号
    def get_key(self):
        return self.key

    # 返回本顶点到邻居 neighbor 的边权
    def get_weight(self, neighbor):
        return self.neighbor[neighbor]


# 邻接表的图结构
class AdjacencyList:
    # 构造函数，edges 必须是二维数组，内部维度是一系列长度为 2 或者 3 的数组，
    # 分别代表着边的起始顶点 start、终止顶点 end 以及边权(可选)
    def __init__(self, edges, root_key):
        self.v_list = {}          # 本图中的顶点字典，key 为顶点 key，value 为对应的 Vertex 结构体
        self.num_vertices = 0     # 本图中的顶点数目
        self.root_key = root_key  # 若此图为树，root_key 为树根的 key 号 TODO 环路检测
        self.pt = []              # PT：前序遍历列表（从 index 映射到顶点 key）
        self.ptr = dict({})       # PTR：前序遍历逆映射（从顶点 key 映射到 PT 的 index）
        self.et = []              # ET：前序遍历列表（要记录重复路过的结点）
        self.first = []           # First：ET 中每个元素值在 ET 中第一次出现的下标位置
        self.st = None            # 根据 ET 构造的 Sparse Table

        # 若 edges 合法，则进行初始化处理
        if isinstance(edges, list):
            for edge in edges:
                if isinstance(edge, list):
                    if len(edge) == 2:
                        self.add_edge(edge[0], edge[1], 1)
                    elif len(edge) == 3:
                        self.add_edge(edge[0], edge[1], edge[2])

        # 进行前序遍历，并获得 PT、PTR、ET 和 First
        if isinstance(root_key, int):
            self.preorder_traversal(self.root_key)

        # 根据 ET 构造 Sparse Table
        if len(self.et) > 0:
            self.st = SparseTableRMQ(self.et)

    # 判断 key 号为 _key 的顶点是否位于顶点列表中
    def __contains__(self, _key):
        return _key in self.v_list

    # 类迭代器方法
    def __iter__(self):
        return iter(self.v_list.values())

    # 获取图中 key 号为 _key 的顶点，如果没有此顶点则返回 None
    def get_vertex(self, _key):
        if _key in self.v_list:
            return self.v_list[_key]
        else:
            return None

    # 获取本图中所有顶点
    def get_vertices(self):
        return self.v_list.keys()

    # 获取 PT 表
    def get_pt(self):
        return self.pt

    # 获取 PTR 表
    def get_ptr(self):
        return self.ptr

    # 获取 ET 表
    def get_et(self):
        return self.et

    # 获取 First 表
    def get_first(self):
        return self.first

    # 增添本图的顶点
    def add_vertex(self, value):
        # 顶点数目加一
        self.num_vertices = self.num_vertices + 1
        # 构造并增添新顶点
        new_vertex = Vertex(value)
        self.v_list[value] = new_vertex
        # 返回新顶点
        return new_vertex

    # 增添边。参数：start 起点、end 终点、weight 边权
    def add_edge(self, start, end, weight=0):
        # 若边的起点 start 或终点 end 不在顶点列表里，则增添顶点
        if start not in self.v_list:
            self.add_vertex(start)
        if end not in self.v_list:
            self.add_vertex(end)
        # 给起点顶点 start 增加邻居 end，边权为 weight
        self.v_list[start].add_neighbor(self.v_list[end], weight)

    # 则从指定根结点 root 出发，递归前序遍历此树，并记录 PT、PTR、ET 和 First
    # TODO 只有在树结构变化的情况下 ET 和 First 才会更新，所以可以将之与 PT 和 PTR 分开处理
    def preorder_traversal(self, root_key):
        # 用 key 获取 Vertex 对象
        v = self.get_vertex(root_key)
        # 若非空，则记录 PT 和 PTR
        if v is not None:
            # PT 以及 PTR
            self.pt.append(root_key)
            if root_key not in self.ptr:
                self.ptr[root_key] = len(self.pt) - 1
                # ET 记录路过的结点 key 在 PT 中的 index
                self.et.append(len(self.pt) - 1)
                # 需要记录下标位置到 first 数组
                self.first.append(len(self.et) - 1)
        else:
            return
        # 遍历邻居结点
        for neighbor in v.get_connections():
            self.preorder_traversal(neighbor.get_key())
            self.et.append(self.ptr[root_key])  # ET 记录重复路过的结点 key 在 PT 中的 index

    # 计算结点 u 和 v 的最近公共祖先 LCA。
    # 参数 u_key 和 v_key 分别为结点 u 和 v 的 key
    # 时间复杂度 O(1)
    def lca_rmq(self, u_key, v_key):
        u_index = self.ptr[u_key]
        v_index = self.ptr[v_key]
        u_first = self.first[u_index]
        v_first = self.first[v_index]
        min_index = self.st.query_minimum(u_first, v_first)
        return self.pt[min_index]


# RMQ 算法，Sparse Table 结构
class SparseTableRMQ:
    # 构造 Sparse Table
    # 时间复杂度 O(n log n)
    def __init__(self, array):
        self.st_len = len(array)
        self.inf = 0x3f3f3f3f  # 1061109567

        # 构造 log_table 用以计算 log_2 (len(array))
        # 首位 0 仅作占位，这样 log_table[i] 表示对 i 取 log_2 对数，下取整
        self.log_table = (self.st_len + 1) * [0]
        for i in range(2, self.st_len + 1):
            self.log_table[i] = self.log_table[i >> 1] + 1

        # 创建二维列表，row = 1 + log_2 (self.st_len)，col = self.st_len
        # 第 0 row 为原始 array
        self.st = [[self.inf] * self.st_len for _ in range(1 + self.log_table[self.st_len])]
        self.st[0] = array

        # 二维动态规划构造 Sparse Table
        # 状态转移方程：st[i][j] = min( st[i-1][j], st[i-1][j + 2^(i-1)] )
        for i in range(1, len(self.st)):
            j = 0
            while j + (1 << i) <= self.st_len:
                self.st[i][j] = min(self.st[i - 1][j], self.st[i - 1][j + (1 << (i - 1))])
                j += 1

    # 若更新数组值，则需重新建表
    # 时间复杂度 O(n log n)
    # 如果数组长度也变了，那么可以重新构造 SparseTableRMQ 类的对象
    def update(self, index, value):
        # 如果下标合法，且 value 值确实改变了，才进行 update，重建 Sparse Table
        if 0 <= index < len(self.st[0]) and self.st[0][index] != value:
            self.st[0][index] = value
            for i in range(1, len(self.st)):
                j = 0
                while j + (1 << i) <= self.st_len:
                    self.st[i][j] = min(self.st[i - 1][j], self.st[i - 1][j + (1 << (i - 1))])
                    j += 1

    # 查询 [left, right] 闭区间的最小值
    # 0 <= left <= right <= n-1
    # 时间复杂度 O(1)
    def query_minimum(self, left, right):
        if left > right:
            return self.inf

        if left < 0:
            left = 0
        if right >= self.st_len:
            right = self.st_len - 1

        # right - left + 1 为区间长度，对此长度求 log_2 对数、并下取整数
        log_2 = self.log_table[right - left + 1]

        # st[log_2][left] 表示从 index=left 出发、长度为 2^log_2 的区间中的最小值
        # right - (1 << log_2) + 1 表示将索引下标减小 2^log_2 - 1，
        # 这样的话，从此下标开始的 2^log_2 长度的区间的右端点即为 right，该区间的最小值可以直接查 ST 表得到
        # 上述两端区间完全覆盖了 query 区间，因此只需计算上述两区间最小值的较小值即为答案
        return min(self.st[log_2][left], self.st[log_2][right - (1 << log_2) + 1])

    def print_st(self):
        for i in range(len(self.st)):
            print(self.st[i])


def main():
    root_key = 0  # 0 为根结点 root 的 ID
    edges = [
        [0, 5], [5, 7], [5, 1], [5, 8], [7, 2],
        [1, 3], [1, 6], [0, 9], [9, 4]
    ]

    # 创建邻接表，并构造 PT、PTR、ET、First 以及 ST
    adj_l = AdjacencyList(edges, root_key)

    # print(adj_l.get_pt())     # [0, 5, 7, 2, 1, 3, 6, 8, 9, 4]
    # print(adj_l.get_ptr())    # {0: 0, 5: 1, 7: 2, 2: 3, 1: 4, 3: 5, 6: 6, 8: 7, 9: 8, 4: 9}
    # print(adj_l.get_et())     # [0, 1, 2, 3, 2, 1, 4, 5, 4, 6, 4, 1, 7, 1, 0, 8, 9, 8, 0]
    # print(adj_l.get_first())  # [0, 1, 2, 3, 6, 7, 9, 12, 15, 16]

    # adj_l.st.print_st()

    start = time.process_time()
    ans = adj_l.lca_rmq(3, 8)
    end = time.process_time()
    print(ans)  # 5

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
