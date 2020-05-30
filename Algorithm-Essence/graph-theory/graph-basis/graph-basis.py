#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/graph_basis
@File    : graph-basis.py
@Author  : YuweiYin
@Date    : 2020-05-29
=================================================="""

import sys
import time

"""
图的表示 - 邻接表 & 邻接矩阵

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 22
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
        return str(self.key) + 'is connected to:' + str([v.key for v in self.neighbor])

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


# 用于邻接矩阵的顶点结构体 (比 VertexList 简单)
# 这里是用散列表 (而不是用链表) 来表达某顶点的所有邻接顶点
class VertexMatrix:
    # 构造方法
    def __init__(self, key, val=None):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)

    # 类序列化输出方法
    def __str__(self):
        return 'Vertex key: ' + str(self.key)


# 邻接矩阵的图结构，通常适合稠密图
# 输入顶点结构体列表、边结构体列表
class AdjacencyMatrix:
    def __init__(self, vertices, edges):
        assert isinstance(vertices, list)

        self.edges = edges         # 存储输入的边列表
        self.vertices = vertices   # 存储输入的顶点列表 (可以从下标映射到顶点)
        self.v2index = dict({})    # 由顶点映射到其下标 (既是邻接矩阵的行/列下标，也是 vertices 列表的下标)
        self.key2index = dict({})  # 由顶点的关键字/唯一标志符映射到其下标
        for index, vertex in enumerate(vertices):
            self.v2index[vertex] = index
            self.key2index[vertex.key] = index

        # 构建邻接矩阵(二维方阵)，adj[x][y] 为 True 表示存在边 (x, y)
        # 矩阵中的每个元素，如果是无权图，可以仅为布尔值，True 表示边存在、False 表示边不存在
        # 如果是带权图，可以用实数值代表边的权值，如果边不存在，可以设置为特殊数值，比如 inf 无穷
        # 如果边的信息比较多，矩阵中的每个元素也可以设置为 Edge 边结构体，在其中增添任务需要的信息
        v_num = len(vertices)  # 顶点数目
        self.adj_m = [[False] * v_num for _ in range(v_num)]  # 这里仅仅存储边是否存在的布尔值信息

        # 若 edges 合法，则进行边初始化处理
        if isinstance(edges, list):
            for edge in edges:
                assert isinstance(edge, Edge)
                from_v = edge.from_v  # 边起点的关键字 key
                to_v = edge.to_v      # 边终点的关键字 key
                if from_v in self.key2index and to_v in self.key2index:
                    # 将顶点关键字 key 转为下标 index，然后设置 adj[from][to] 为 True
                    from_index = self.key2index[from_v]
                    to_index = self.key2index[to_v]
                    assert 0 <= from_index < v_num and 0 <= to_index < v_num
                    self.adj_m[from_index][to_index] = True
                    # 如果是无向边，则 adj[to][from] 也设置为 True
                    if not edge.is_directed:
                        self.adj_m[to_index][from_index] = True

    # 判断 key 号为 _key 的顶点是否位于顶点列表中
    def __contains__(self, _key):
        return _key in self.key2index

    # 获取图中 key 号为 _key 的顶点，如果没有此顶点则返回 None
    def get_vertex(self, _key):
        if _key in self.key2index:
            index = self.key2index[_key]
            return self.vertices[index]
        else:
            return None

    # 邻接矩阵 - 图转置
    def graph_transposition(self):
        for edge in self.edges:
            assert isinstance(edge, Edge)
            # 其实如果是无向边，无需处理，但这里还是转了
            # 先获取 key
            from_key = edge.from_v
            to_key = edge.to_v
            # 交换 key
            edge.from_v = to_key
            edge.to_v = from_key
            # 把 key 转成 index
            assert from_key in self.key2index and to_key in self.key2index
            from_index = self.key2index[from_key]
            to_index = self.key2index[to_key]
            # 修改邻接矩阵
            temp = self.adj_m[from_index][to_index]
            self.adj_m[from_index][to_index] = self.adj_m[to_index][from_index]
            self.adj_m[to_index][from_index] = temp


def main():
    # 用于构造邻接表的顶点的 key/val 信息列表
    list_vertices_info = [
        ['r', 100], ['s', 200], ['t', 300], ['u', 400],
        ['v', 500], ['w', 600], ['x', 700], ['y', 800]
    ]
    # 用于构造邻接矩阵的顶点的 key/val 信息列表
    matrix_vertices_info = [
        ['u', 111], ['v', 222], ['w', 333],
        ['x', 444], ['y', 555], ['z', 666]
    ]
    # 无向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    bi_edges_info = [
        ['r', 'v', 1, False], ['r', 's', 1, False], ['s', 'w', 1, False],
        ['w', 't', 1, False], ['w', 'x', 1, False], ['t', 'x', 1, False],
        ['t', 'u', 1, False], ['x', 'u', 1, False], ['x', 'y', 1, False],
        ['u', 'y', 1, False]
    ]
    # 有向边的 from/to/weight/is_directed 信息列表
    di_edges_info = [
        ['u', 'v', 1, True], ['u', 'x', 1, True], ['x', 'v', 1, True],
        ['v', 'y', 1, True], ['y', 'x', 1, True], ['w', 'y', 1, True],
        ['w', 'z', 1, True], ['z', 'z', 1, True]
    ]

    # 根据前述列表信息构造结点列表
    list_vertices = []
    matrix_vertices = []
    bi_edges = []
    di_edges = []

    for v in list_vertices_info:
        list_vertices.append(VertexList(key=v[0], val=v[1]))
    for v in matrix_vertices_info:
        matrix_vertices.append(VertexMatrix(key=v[0], val=v[1]))
    for e in bi_edges_info:
        bi_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    start = time.process_time()

    # 创建邻接表 (用邻接链表+无向图 执行 BFS)
    adj_l = AdjacencyList(list_vertices, bi_edges)

    # 创建邻接矩阵 (用邻接矩阵+有向图 执行 DFS)
    adj_m = AdjacencyMatrix(matrix_vertices, di_edges)

    # 可以设置断点查看 adj_l 邻接表 和 adj_m 邻接矩阵
    end = time.process_time()

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
