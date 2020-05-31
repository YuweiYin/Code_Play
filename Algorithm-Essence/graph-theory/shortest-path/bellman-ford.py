#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/shortest_path
@File    : bellman-ford.py
@Author  : YuweiYin
@Date    : 2020-05-31
=================================================="""

import sys
import time

"""
单源最短路径 Single Source Shortest Path
含负权值加权图的最短路径 - Bellman-Ford 算法

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 24
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
    def __init__(self, key, val=None, distance=0, p=None):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        self.neighbor = dict({})  # 本顶点的邻居字典，key 为邻居的关键字，value 为 Edge 边结构体
        # 如果是有向图，本结点为关联边的出发点 from_v，其邻居关联边的终止点 to_v
        '''如下为最短路径算法所需的属性'''
        self.distance = distance  # 从源结点 s 到本结点的最短路径权重值
        self.p = p                # 本结点的前驱结点/最短路径树的父结点

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

    # 输出每个结点的信息
    def print_vertex_info(self):
        for v in self.vertices:
            if isinstance(v.p, VertexList):
                print(v.key, '\tdistance:', v.distance, '\tp:', v.p.key)
            else:
                print('Shortest Path Tree root:', v.key, '\tdistance:', v.distance)


class BellmanFord:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 所有结点的 distance 初始化为 inf

    # 初始化每个结点的 distance 和 p 属性
    def initialize_single_source(self, adj_l, source_v):
        assert isinstance(adj_l, AdjacencyList) and isinstance(source_v, VertexList)
        for v in adj_l.vertices:
            assert isinstance(v, VertexList)
            v.distance = self.inf
            v.p = None
        source_v.distance = 0

    # 对边 (u, v) 进行松弛操作
    @staticmethod
    def relax(u, v, weight_func=lambda x: x):
        assert isinstance(u, VertexList) and isinstance(v, VertexList)
        # 获取边 (u, v)
        assert v.key in u.neighbor
        edge = u.neighbor[v.key]
        # 检查是否可以对从 s 到 v 的最短路径进行改善
        # 将 s->u 的最短路径距离 加上 u->v 的边权重值
        cur_dis = u.distance + weight_func(edge.weight)
        # cur_dis 与当前得到的 s->v 的最短路径估计 进行比较
        if cur_dis < v.distance:
            # 如果前者更小，则更新估计值 v.d 并修改前驱结点 v.p
            v.distance = cur_dis
            v.p = u

    # 寻找图 adj_l 从源结点 source_v 出发的单源最短路径
    # 这里默认图为邻接表结构，weight_func 为恒等函数
    def do_bf(self, adj_l, source_v, weight_func=lambda x: x):
        assert isinstance(adj_l, AdjacencyList) and isinstance(source_v, VertexList)
        # 1. 对所有结点的 d 值和 p 值进行初始化
        self.initialize_single_source(adj_l, source_v)

        # 2. 循环对图的每条边进行 |V| - 1 次松弛操作，完成各结点的 d、p 值计算
        for i in range(len(adj_l.vertices) - 1):
            # 对每条边进行操作
            for edge in adj_l.edges:
                # 先通过边中存储的的 from/to 关键字获取 u/v 顶点结构体
                assert isinstance(edge, Edge)
                assert edge.from_v in adj_l.key2index and edge.to_v in adj_l.key2index
                u = adj_l.vertices[adj_l.key2index[edge.from_v]]
                v = adj_l.vertices[adj_l.key2index[edge.to_v]]
                assert isinstance(u, VertexList) and isinstance(v, VertexList)
                # 进行松弛操作
                self.relax(u, v, weight_func)

        # 3. 循环检查图中是否存在负权环，如果有则返回 False
        for edge in adj_l.edges:
            # 先通过边中存储的的 from/to 关键字获取 u/v 顶点结构体
            assert isinstance(edge, Edge)
            assert edge.from_v in adj_l.key2index and edge.to_v in adj_l.key2index
            u = adj_l.vertices[adj_l.key2index[edge.from_v]]
            v = adj_l.vertices[adj_l.key2index[edge.to_v]]
            assert isinstance(u, VertexList) and isinstance(v, VertexList)
            # 检测负权环
            if u.distance + weight_func(edge.weight) < v.distance:
                return False

        # 4. 前面已经检测不到负权环了，所以返回 True 表示没有负权环
        return True


def main():
    # 构造图同《CLRS》Chapter 24.1 的(带边权)有向图
    # 用于构造邻接表的顶点的 key/val 信息列表
    list_vertices_info = [
        ['s', 100], ['t', 200], ['x', 300], ['y', 400], ['z', 500]
    ]
    # 有向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['s', 't', 6, True], ['s', 'y', 7, True], ['t', 'y', 8, True],
        ['t', 'x', 5, True], ['x', 't', -2, True], ['t', 'z', -4, True],
        ['y', 'z', 9, True], ['z', 's', 2, True], ['z', 'x', 7, True],
        ['y', 'x', -3, True]
    ]

    # 根据前述列表信息构造结点列表
    list_vertices = []
    di_edges = []
    for v in list_vertices_info:
        list_vertices.append(VertexList(key=v[0], val=v[1]))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    # 创建邻接表 (用邻接链表+无向图 执行最短路径算法)
    adj_l = AdjacencyList(list_vertices, di_edges)

    # 设置源结点
    source_v_key = 's'
    assert source_v_key in adj_l.key2index
    source_v = adj_l.vertices[adj_l.key2index[source_v_key]]

    # 执行 Bellman-Ford 算法
    start = time.process_time()
    bellman_ford = BellmanFord()
    no_neg_cycle = bellman_ford.do_bf(adj_l, source_v)
    end = time.process_time()

    # 输出结果
    if no_neg_cycle:
        # 如果没有负权环，则 Bellman-Ford 算法能够正确获得单源最短路径的结果
        # Shortest Path Tree root: s 	distance: 0
        # t 	distance: 2 	p: x
        # x 	distance: 4 	p: y
        # y 	distance: 7 	p: s
        # z 	distance: -2 	p: t
        adj_l.print_vertex_info()
    else:
        # 如果含有负权环，则 Bellman-Ford 算法能够检测出来
        print('图中含有总权重为负值的环路(负权环)!')
        # 如果把 t->x 的边权从 5 改为小于 2 的值 ['t', 'x', <2, True] 就出现负权环了

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
