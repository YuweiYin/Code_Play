#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/minimum_spanning_tree
@File    : mst-kruskal.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
最小生成树 (Minimum Spanning Tree, MST)
Kruskal 算法

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 23
"""


# 边结构体，表达边的信息，可随任务自定义 (增添其它值元素 val 对象)
class Edge:
    # 构造方法
    def __init__(self, from_v=None, to_v=None, weight=1, is_directed=True):
        self.from_v = from_v  # 边的起始顶点(关键字/序号)
        self.to_v = to_v      # 边的终止顶点(关键字/序号)
        self.weight = weight  # 边的权重值 (默认值为 1，如果全部边的权重都相同，那图 G 就是无权图)
        self.is_directed = is_directed  # True 则表明此边是有向边，False 为无向边
        # 对无向边而言，起始顶点和终止顶点可以互换

    # 类序列化输出方法
    def __str__(self):
        return str(self.from_v) + '->' + str(self.to_v) +\
               '\t weight:' + str(self.weight) + '\t is_directed:' + str(self.is_directed)


# 用于邻接表的顶点结构体
# 这里是用散列表 (而不是用链表) 来表达某顶点的所有邻接顶点
class VertexList:
    # 构造方法
    def __init__(self, key, val=None):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        self.neighbor = dict({})  # 本顶点的邻居字典，key 为邻居的关键字，value 为 Edge 边结构体
        # 如果是有向图，本结点为关联边的出发点 from_v，其邻居关联边的终止点 to_v

    # 类序列化输出方法
    def __str__(self):
        return str(self.key) + ' is connected to:' + str([v.key for v in self.neighbor])

    # 增添本顶点的邻居 neighbor，以字典结构存储
    # 注意：如果不允许图有自环/自圈，那么在增添邻居/边 的时候要禁止增添 self.neighbor[self.key] 项。这里暂不限制
    def add_neighbor(self, key, weight=1, is_directed=True):
        # 如果 neighbor 字典里已有此 key，则会覆盖。起到了更新边信息的作用
        self.neighbor[key] = Edge(from_v=self.key, to_v=key, weight=weight, is_directed=is_directed)

    # 以 Edge 边结构体来增添本顶点的邻居 neighbor
    def add_edge(self, edge):
        # 检查输入 edge 的合法性
        if isinstance(edge, Edge):
            # 如果 edge 是有向边，那么本结点需要是 edge 的出发点 from_v
            if edge.is_directed:
                if edge.from_v == self.key:
                    self.neighbor[edge.to_v] = edge
            # 如果 edge 是无向边，那么本结点需要是 edge 的出发点 from_v 或结束点 to_v 之一
            else:
                if edge.from_v == self.key:
                    self.neighbor[edge.to_v] = edge
                elif edge.to_v == self.key:
                    # 先把 from_v 和 to_v 交换
                    edge.to_v = edge.from_v
                    edge.from_v = self.key
                    self.neighbor[edge.to_v] = edge

    # 返回本顶点的所有邻接顶点(的关键字/序号) 数组
    def get_connections(self):
        return self.neighbor.keys()

    # 返回本顶点到邻居 neighbor 的 Edge 边结构体
    def get_weight(self, neighbor):
        if neighbor in self.neighbor:
            return self.neighbor[neighbor]
        else:
            return None


# 邻接表的图结构，通常适合稀疏图
# 输入顶点结构体列表、边结构体列表
class AdjacencyList:
    # 构造函数，edges 必须是二维数组，内部维度是一系列长度为 2 或者 3 的数组，
    # 分别代表着边的起始顶点 start、终止顶点 end 以及边权(可选)
    def __init__(self, vertices, edges):
        assert isinstance(vertices, list)

        self.edges = edges         # 存储输入的边列表
        self.vertices = vertices   # 存储输入的顶点列表 (可以从下标映射到顶点)
        self.v2index = dict({})    # 由顶点映射到其下标 (既是邻接矩阵的行/列下标，也是 vertices 列表的下标)
        self.key2index = dict({})  # 由顶点的关键字/唯一标志符映射到其下标
        for index, vertex in enumerate(vertices):
            self.v2index[vertex] = index
            self.key2index[vertex.key] = index

        self.adj_l = dict({})      # 本图的顶点字典, key 为顶点的序号，val 为顶点结构体
        for vertex in vertices:
            assert isinstance(vertex, VertexList)
            self.adj_l[vertex.key] = vertex

        # 若 edges 合法，则进行边初始化处理
        if isinstance(edges, list):
            for edge in edges:
                assert isinstance(edge, Edge)
                # 如果是有向边
                if edge.is_directed:
                    from_v = edge.from_v
                    if from_v in self.adj_l:
                        self.adj_l[from_v].add_edge(edge)
                # 如果是无向边
                else:
                    from_v = edge.from_v
                    to_v = edge.to_v
                    if from_v in self.adj_l:
                        self.adj_l[from_v].add_edge(edge)
                    if to_v in self.adj_l:
                        self.adj_l[to_v].add_edge(edge)

    # 判断 key 号为 _key 的顶点是否位于顶点列表中
    def __contains__(self, _key):
        return _key in self.adj_l

    # 类迭代器方法
    def __iter__(self):
        return iter(self.adj_l.values())

    # 获取图中 key 号为 _key 的顶点，如果没有此顶点则返回 None
    def get_vertex(self, _key):
        if _key in self.adj_l:
            return self.adj_l[_key]
        else:
            return None

    # 邻接表 - 图转置
    def graph_transposition(self):
        for edge in self.edges:
            assert isinstance(edge, Edge)
            # 其实如果是无向边，无需处理，但这里还是转了
            temp = edge.from_v
            edge.from_v = edge.to_v
            edge.to_v = temp


class SetNode:
    def __init__(self, key, val=None):
        self.key = key      # 本元素的 key 号
        self.father = self  # 指针，指向本元素的父结点，初始时指向自己
        self.rank = 1       # 本元素所在集合的 rank 秩
        '''如下为 MST 算法所需的属性'''
        self.val = val      # 该并查集结点附带的值元素，即顶点结构体


class UnionFind:
    # 构造不相交集合
    # 时间复杂度 O(n)
    def __init__(self, set_list):
        self.disjoint_set = set_list  # 存放全体元素 SetNode 结构体
        self.key2node = dict({})      # 将 key 号映射为 SetNode 结构体

        for set_node in set_list:
            assert isinstance(set_node, SetNode)
            self.key2node[set_node.key] = set_node

    # find 操作；查找 key 为 key_x 的元素所在集合的代表元素。
    # find 操作经过路径压缩优化后，平均时间复杂度为 O(1)
    def find(self, key_x):
        if key_x in self.key2node:
            node_x = self.key2node[key_x]
        else:
            return None

        while node_x.father != node_x:
            temp = node_x.father
            node_x.father = node_x.father.father
            node_x = temp
        return node_x

    # union 操作；将 key 分别为 key_x 和 key_y 的元素 所在的集合合并成一个新集合，返回新集合的代表元素。
    # 这里进行按秩合并优化，选择 find 结果中 秩更小的元素作为新集合的代表元素
    # 经过按秩合并优化后，树高至多为 log n，因此平均时间复杂度为 O(1)、最坏时间复杂度为 O(log n)
    def union(self, key_x, key_y):
        root_x = self.find(key_x)
        root_y = self.find(key_y)

        if isinstance(root_x, SetNode) and isinstance(root_y, SetNode):
            if root_x != root_y:
                if root_x.rank < root_y.rank:
                    # 如果 root_x 的秩小于 root_y 的秩，则让 root_x 指向 root_y
                    root_x.father = root_y
                    # 修改 y 的秩为 y 秩与 x 秩加一中的较大值，
                    # 因为 root_y 被 root_x 所指不一定使得 root_y 的树高提升
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
        else:
            return None

    def print_set(self):
        for node in self.disjoint_set:
            print(node.key)


class Kruskal:
    # 寻找图 adj_l 的一棵最小生成树
    # 这里默认图为邻接表结构，weight_func 为恒等函数
    @staticmethod
    def do_mst(adj_l, weight_func=lambda x: x):
        assert isinstance(adj_l, AdjacencyList)
        # 1. 将集合 A 初始化为一个空集合，并创建 |V| 棵树（不相交集合），每棵树仅包含一个结点
        mst_set = []   # 集合 A
        set_list = []  # 用于构造并查集的 SetNode 列表
        for v in adj_l.vertices:
            assert isinstance(v, VertexList)
            # 封装顶点结构体为 SetNode 结构体
            set_list.append(SetNode(key=v.key, val=v))
        union_find = UnionFind(set_list=set_list)

        # 2. 把边集合 E 中的所有边都按照权重的非降序排序
        adj_l.edges = sorted(adj_l.edges, key=lambda x: weight_func(x.weight), reverse=False)

        # 3. 在 for 循环中，按权重非降序地选取边 (u, v)
        for edge in adj_l.edges:
            assert isinstance(edge, Edge)
            # 检查边 (u, v) 的两个端点 u 和 v 是否属于同一个集合(同一棵树)，如果不属于同一集合，则 (u, v) 是安全边；
            # 如果二者属于同一个集合，则不能加入此边，否则会形成环路，不符合树的定义。
            if union_find.find(edge.from_v) != union_find.find(edge.to_v):
                # 将安全边 (u, v) 加入集合 A
                mst_set.append(edge)
                # 把安全边的两个端点合并到同一个集合(同一棵树)中
                union_find.union(edge.from_v, edge.to_v)

        # 4. 返回集合(树) A
        return mst_set


def main():
    # 构造图同《CLRS》Chapter 23.2 的(带边权)连通无向图
    # 用于构造邻接表的顶点的 key/val 信息列表
    list_vertices_info = [
        ['a', 100], ['b', 200], ['c', 300], ['d', 400], ['e', 500],
        ['f', 600], ['g', 700], ['h', 800], ['i', 900]
    ]
    # 无向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    bi_edges_info = [
        ['a', 'b', 4, False], ['a', 'h', 8, False], ['b', 'h', 11, False],
        ['b', 'c', 8, False], ['c', 'i', 2, False], ['i', 'h', 7, False],
        ['i', 'g', 6, False], ['h', 'g', 1, False], ['c', 'f', 4, False],
        ['g', 'f', 2, False], ['c', 'd', 7, False], ['d', 'f', 14, False],
        ['d', 'e', 9, False], ['e', 'f', 10, False]
    ]

    # 根据前述列表信息构造结点列表
    list_vertices = []
    bi_edges = []
    for v in list_vertices_info:
        list_vertices.append(VertexList(key=v[0], val=v[1]))
    for e in bi_edges_info:
        bi_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    # 创建邻接表 (用邻接链表+无向图 执行 MST 算法)
    adj_l = AdjacencyList(list_vertices, bi_edges)

    # 执行 MST-Kruskal 算法
    start = time.process_time()
    mst_set = Kruskal.do_mst(adj_l)
    end = time.process_time()

    # 输出结果
    if isinstance(mst_set, list):
        total_weight = 0
        for edge in mst_set:
            assert isinstance(edge, Edge)
            total_weight += edge.weight
            print(edge)
        print('total_weight:', total_weight)  # 37
    else:
        print('No Answer!')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
