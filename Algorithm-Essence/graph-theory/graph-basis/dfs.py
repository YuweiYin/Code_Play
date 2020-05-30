#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/graph_basis
@File    : dfs.py
@Author  : YuweiYin
@Date    : 2020-05-30
=================================================="""

import sys
import time

"""
图的搜索 - 深度优先搜索 (Depth First Search, BFS)

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
    def __init__(self, key, val=None, discover=0, finish=0):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        self.neighbor = dict({})  # 本顶点的邻居字典，key 为邻居的关键字，value 为 Edge 边结构体
        # 如果是有向图，本结点为关联边的出发点 from_v，其邻居关联边的终止点 to_v
        '''下面是用于 DFS 的属性'''
        self.color = False        # False 为"白色"，表示未被发现；True 为"黑色"，表示已经完成探索
        self.discover = discover  # 此结点被发现的时间戳 (在此时间前为颜色为白)
        self.finish = finish      # 此结点完成探索的时间戳 (在此时间后为颜色为黑)
        self.p = None             # 此结点的前驱结点/深度优先搜索树的父结点

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


# 深度优先搜索 (Depth First Search, BFS)
class DFS:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 初始化各个结点被发现和结束探索的时间均为 inf 无穷
        self.timestamp = 0     # 时间戳

    # 输入：graph 图结构，is_adj_link 为 True 表示图为邻接表结构，False 表示为邻接矩阵结构
    def do_dfs(self, graph, is_adj_link=True):
        if is_adj_link:
            # 如果图是邻接表结构
            self._dfs_link(graph)
        else:
            # 如果图是邻接矩阵结构
            self._dfs_matrix(graph)

    def _dfs_link(self, adj_l):
        assert isinstance(adj_l, AdjacencyList)
        # 1. 初始化图 G 的每个顶点 u \in G.V，让其颜色为白色 white、前驱结点/父结点为空 nil
        for v in adj_l.adj_l.values():
            v.color = False
            v.discover = self.inf
            v.finish = self.inf
            v.p = None

        # 2. 初始化时间戳 time
        self.timestamp = 0

        # 3. 以每个白色的结点作为 DFS 算法的源结点（也即 DFS 树的根结点）调用 `DFS_VISIT` 过程进行深度优先搜索。
        for u in adj_l.adj_l.values():
            if not u.color:
                self._dfs_visit(adj_l, u)

    # 以 u 为 DFS 树根结点，开始对邻接表结构的图 graph 进行 DFS
    def _dfs_visit(self, adj_l, u):
        assert isinstance(adj_l, AdjacencyList) and isinstance(u, VertexList)
        # 1. 时间戳增长，并赋予给结点 u 的发现时间 u.d
        # 由于 u 已被发现，其颜色置为灰色 gray（已被发现状态）
        self.timestamp += 1
        u.discover = self.timestamp
        u.color = True  # 这里省了灰色状态，直接赋为黑色

        # 2. 对于 u 的每个邻接结点 v，如果 v 是白色的（未被发现状态）
        # 则将 v 的前驱置为 u，并以 v 为起点递归地进行 DFS 搜索
        for edge in u.neighbor.values():
            assert isinstance(edge, Edge)
            # 先从 u 的关联边 edge 中得到邻接结点 v 的关键字
            if edge.is_directed:
                # 有向边，则邻接结点 v 的关键字是 edge 的终止结点
                v_key = edge.to_v
            else:
                # 无向边，则先设置邻接结点 v 的关键字是 edge 的终止结点
                v_key = edge.to_v
                # 但如果终止结点是 u，那么设置 邻接结点 v 的关键字是 edge 的起始结点
                if v_key == u.key:
                    v_key = edge.from_v
                # 如果起始结点也是 u，则表示该边为无向图的自环，不必再处理
            # 再从关键字 v_key 获取结点 v
            assert v_key in adj_l.key2index
            v_index = adj_l.key2index[v_key]
            v = adj_l.vertices[v_index]
            assert isinstance(v, VertexList)

            if not v.color:
                v.p = u
                self._dfs_visit(adj_l, v)

        # 3. 由于此时 u 的邻接结点都已被处理结束，故置 u 的颜色为黑色（处理完毕状态）
        # 随后时间戳增长，并赋予给结点 u 的完成时间 u.f
        # u.color = True
        self.timestamp += 1
        u.finish = self.timestamp

    # 对邻接矩阵结构的图 graph 进行 DFS
    def _dfs_matrix(self, adj_m):
        pass

    # 在计算出 DFS 之后，打印出所有结点(的关键字)及其发现时间 discover 与结束探索时间 finish
    @staticmethod
    def print_vertex_time(adj_l):
        assert isinstance(adj_l, AdjacencyList)
        for v in adj_l.vertices:
            assert isinstance(v, VertexList)
            print(v.key, v.discover, v.finish)


def main():
    # 构造图同《CLRS》Chapter 22.3 的 DFS 图
    # 用于构造邻接矩阵的顶点的 key/val 信息列表
    list_vertices_info = [
        ['u', 111], ['v', 222], ['w', 333],
        ['x', 444], ['y', 555], ['z', 666]
    ]
    # 有向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['u', 'v', 1, True], ['u', 'x', 1, True], ['x', 'v', 1, True],
        ['v', 'y', 1, True], ['y', 'x', 1, True], ['w', 'y', 1, True],
        ['w', 'z', 1, True], ['z', 'z', 1, True]
    ]

    # 根据前述列表信息构造结点列表
    list_vertices = []
    di_edges = []
    for v in list_vertices_info:
        list_vertices.append(VertexList(key=v[0], val=v[1]))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    # 创建邻接表 (用邻接链表+有向图 执行 DFS)
    adj_l = AdjacencyList(list_vertices, di_edges)

    # 执行 DFS 过程
    start = time.process_time()
    dfs = DFS()
    dfs.do_dfs(graph=adj_l, is_adj_link=True)
    end = time.process_time()

    # 查看 DFS 结果
    print('DFS 结果 (各顶点关键字 及其 发现时间 与结束探索时间)')
    dfs.print_vertex_time(adj_l)

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
