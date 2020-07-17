#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/max_flow_matching
@File    : ford-fulkerson.py
@Author  : YuweiYin
=================================================="""

import sys
import time
import queue

"""
最大流 Max-Flow

- Ford-Fulkerson 方法
    - Ford-Fulkerson 算法 O(V |f*|)
    - Edmonds-Karp 算法 O(V E^2)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 26
"""


# 边结构体，表达边的信息，可随任务自定义 (增添其它值元素 val 对象)
class Edge:
    # 构造方法
    def __init__(self, from_v=None, to_v=None, weight=1, is_directed=True, capacity=0):
        self.from_v = from_v  # 边的起始顶点(关键字/序号)
        self.to_v = to_v      # 边的终止顶点(关键字/序号)
        self.weight = weight  # (用于最短路)边的权重值 (默认值为 1，如果全部边的权重都相同，那图 G 就是无权图)
        self.is_directed = is_directed  # True 则表明此边是有向边，False 为无向边
        # 对无向边而言，起始顶点和终止顶点可以互换
        '''下面是用于 Max-Flow 的属性'''
        self.capacity = capacity  # 此边的最大容量
        self.flow = 0             # 此边最大流的流量，初始为 0，取值范围 0 <= flow <= capacity
        # 运行过程中的边流量存储于矩阵中，这里的 self.flow 仅存储最终的本条边的流量

    # 类序列化输出方法
    def __str__(self):
        return str(self.from_v) + '->' + str(self.to_v) + \
               '\t capacity:' + str(self.capacity) + '\t flow:' + str(self.flow) + \
               '\t weight:' + str(self.weight) + '\t is_directed:' + str(self.is_directed)


# 用于邻接矩阵的顶点结构体 (比 VertexList 简单)
# 这里是用散列表 (而不是用链表) 来表达某顶点的所有邻接顶点
class VertexMatrix:
    # 构造方法
    def __init__(self, key, val=None, color=False, distance=0, p=None):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        '''下面是用于 BFS 的属性'''
        self.color = color        # False 为"白色"，表示未被发现；True 为"黑色"，表示已经探索结束
        self.distance = distance  # 此结点距离源结点的距离 (最短简单路径的边数)
        self.p = p                # 此结点的前驱结点/广度优先搜索树的父结点

    # 类序列化输出方法
    def __str__(self):
        return 'Vertex key: ' + str(self.key)


# (带边权的)邻接矩阵的图结构，通常适合稠密图
# 输入顶点结构体列表、边结构体列表
class AdjacencyMatrix:
    def __init__(self, vertices, edges):
        assert isinstance(vertices, list)

        # self.inf = 0x3f3f3f3f        # 初始各边的权重值均为 inf 无穷
        self.max_flow = 0            # 经最大流算法后计算出的最大流值
        self.edges = edges           # 存储输入的边列表
        self.key2e_index = dict({})  # 由(起始,终止)顶点的关键字/唯一标志符映射到边数组下标

        self.vertices = vertices     # 存储输入的顶点列表 (可以从下标映射到顶点)
        self.v2index = dict({})      # 由顶点映射到其下标 (既是邻接矩阵的行/列下标，也是 vertices 列表的下标)
        self.key2v_index = dict({})  # 由顶点的关键字/唯一标志符映射到顶点数组下标
        for index, vertex in enumerate(vertices):
            self.v2index[vertex] = index
            self.key2v_index[vertex.key] = index

        # 构建邻接矩阵(二维方阵)，adj[x][y] 的值为边 (x, y) 的当前流量，而不是边权重
        # 这里用于残存网络 Gf，可以有反平行边。如果 adj[x][y] 为 0 表示没有此边，在 Gf 上运行 BFS
        v_num = len(vertices)  # 顶点数目
        self.adj_m = [[0] * v_num for _ in range(v_num)]

        # 若 edges 合法，则进行边初始化处理
        if isinstance(edges, list):
            for index, edge in enumerate(edges):
                # 断言最大流算法里都是有向边
                assert isinstance(edge, Edge) and edge.is_directed
                from_v = edge.from_v      # 边起点的关键字 key
                to_v = edge.to_v          # 边终点的关键字 key
                capacity = edge.capacity  # 边的容量
                self.key2e_index[(from_v, to_v)] = index
                if from_v in self.key2v_index and to_v in self.key2v_index:
                    # 将顶点关键字 key 转为下标 index，然后初始化 adj[from][to] 为边的最大容量
                    from_index = self.key2v_index[from_v]
                    to_index = self.key2v_index[to_v]
                    assert 0 <= from_index < v_num and 0 <= to_index < v_num
                    self.adj_m[from_index][to_index] = capacity

    # 判断 key 号为 _key 的顶点是否位于顶点列表中
    def __contains__(self, _key):
        return _key in self.key2v_index

    # 获取图中 key 号为 _key 的顶点，如果没有此顶点则返回 None
    def get_vertex(self, _key):
        if _key in self.key2v_index:
            index = self.key2v_index[_key]
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
            assert from_key in self.key2v_index and to_key in self.key2v_index
            from_index = self.key2v_index[from_key]
            to_index = self.key2v_index[to_key]
            # 修改邻接矩阵
            temp = self.adj_m[from_index][to_index]
            self.adj_m[from_index][to_index] = self.adj_m[to_index][from_index]
            self.adj_m[to_index][from_index] = temp

    # 输出邻接矩阵
    def print_matrix_info(self):
        assert isinstance(self.adj_m, list)
        for row in self.adj_m:
            print(row)


# 广度优先搜索 (Breadth First Search, BFS)
class BFS:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 初始化各个结点距离源结点的距离为 inf 无穷
        self.path = []         # 从源结点 s 到目标结点 v 的一条最短路径上的所有结点(的关键字)
        self.end_recursion = False  # 如果此标志为真，则会结束掉递归过程

    # 输入：输入图结构默认为邻接矩阵 adj_m，而 start_key 为源顶点的关键字
    def do_bfs(self, adj_m, start_key):
        assert isinstance(adj_m, AdjacencyMatrix)
        # 先把 start_key 源顶点的关键字 转为源结点结构体
        if start_key in adj_m.key2v_index:
            start_index = adj_m.key2v_index[start_key]
            assert 0 <= start_index < len(adj_m.vertices)
            start_v = adj_m.vertices[start_index]
            assert isinstance(start_v, VertexMatrix)
        else:
            print('输入的 start_key 不是任何顶点的关键字，BFS 失败')
            return

        # 1. 除了源结点 s 外，将其余所有结点 u 的状态标记为“未被发现”，即 color 为白色 white
        # 另外，将 u.d 设置为无穷 inf，表示从源结点不可达结点 u。由于未探索到结点 u，将其前驱结点设置为空 nil
        for v in adj_m.vertices:
            assert isinstance(v, VertexMatrix)
            v.color = False
            v.distance = self.inf
            v.p = None

        # 2. 设置源结点 s 的属性。由于已经发现了 s，所以 s.color 设置为灰色 gray。结点 s 到自身的距离为 0
        # 结点 s 为 BFS 树的树根，所以前驱/父结点 u.p 为空 nil
        start_v.color = True
        start_v.distance = 0
        start_v.p = None

        # 3. 将 s 加入辅助队列 Q，成为其唯一成员
        aux_queue = queue.Queue()  # Python 内建 queue 队列对象
        aux_queue.put(start_v)

        # 4. 在 while 循环中，先进先出地逐个处理队列 Q 中的结点
        while not aux_queue.empty():
            # 4.1. 先取出 Q 队首结点 u
            u = aux_queue.get()
            assert isinstance(u, VertexMatrix) and u.key in adj_m.key2v_index
            u_index = adj_m.key2v_index[u.key]

            # 4.2. 逐个处理 u 的所有邻接结点 v
            for v_index, edge_flow in enumerate(adj_m.adj_m[u_index]):
                # 邻接矩阵中边流量为 0 表示残存网络中没有此边
                if edge_flow <= 0:
                    continue
                # 获取边的终点 v 结构体
                v = adj_m.vertices[v_index]
                assert isinstance(v, VertexMatrix)

                # 4.3. 如果 v.color 是白色，表示它未被发现，需要被加入到队列 Q 中。在入队之前，需要设置其属性：
                #     - v.color 颜色设置为灰色，表示它已被发现，但是尚未被探索完（所谓探索结束，是其邻接结点都已被处理）
                #     - v.d 是 v 到源结点 s 的距离，这个距离等于 u.d 距离加上 1
                #     - v.p 设置前驱/父结点为 u
                #     - 将 v 入队，之后的 while 循环中 会考察 v 的各个邻接结点
                if not v.color:
                    v.color = True
                    v.distance = u.distance + 1
                    v.p = u
                    aux_queue.put(v)
            # 4. for 循环结束，u 的所有邻接结点都被考察了，所以 u 已经被探索结束了。u.color 设置为黑色，保证不会再被加入队列 Q
            # u.color = True

    # 在计算出 BFS 之后，打印出所有结点(的关键字)及其距离
    @staticmethod
    def print_vertex_distance(adj_m):
        assert isinstance(adj_m, AdjacencyMatrix)
        for v in adj_m.vertices:
            assert isinstance(v, VertexMatrix)
            print(v.key, v.distance)

    # 在计算出 BFS 之后，获取从源结点 s 到目标结点 v 的一条最短路径上的所有结点(的关键字)
    # 此处图结构为邻接矩阵 adj_m
    def get_path(self, adj_m, start_key, end_key):
        if not isinstance(adj_m, AdjacencyMatrix):
            # return 'get_path: 输入的参数类型不合法'
            return []
        # 先把 key 关键字 转为顶点点结构体
        if start_key in adj_m.key2v_index:
            start_index = adj_m.key2v_index[start_key]
            assert 0 <= start_index < len(adj_m.vertices)
            start_v = adj_m.vertices[start_index]
            assert isinstance(start_v, VertexMatrix)
        else:
            # return '输入的 start_key 不是任何顶点的关键字'
            return []

        if end_key in adj_m.key2v_index:
            end_index = adj_m.key2v_index[end_key]
            assert 0 <= end_index < len(adj_m.vertices)
            end_v = adj_m.vertices[end_index]
            assert isinstance(end_v, VertexMatrix)
        else:
            # return '输入的 end_key 不是任何顶点的关键字'
            return []

        self.path = []
        self.end_recursion = False
        self._get_path(start_v, end_v)
        return self.path

    def _get_path(self, start_v, end_v):
        if self.end_recursion:
            return
        if end_v == start_v:
            self.path.append(start_v.key)
        elif not isinstance(end_v.p, VertexMatrix):
            # self.path = 'No path from ' + str(start_v.key) + ' to ' + str(end_v.key) + ' exists.'
            self.path = []
            self.end_recursion = True
        else:
            # 先获取其前驱结点/父结点的关键字，再获取本结点的关键字
            self._get_path(start_v, end_v.p)
            self.path.append(end_v.key)


# Ford-Fulkerson 最大流算法 - O(VE^2)
class FordFulkerson:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 所有结点的 distance 初始化为 inf

    # 计算流网络(邻接矩阵) adj_m 的最大流
    def do_edmonds_karp(self, adj_m, source_v_key, terminal_v_key):
        # 首先确认输入的合法性，并将输入的源结点和汇点关键字 转为结点结构体
        assert isinstance(adj_m, AdjacencyMatrix)
        assert source_v_key in adj_m.key2v_index and terminal_v_key in adj_m.key2v_index
        source_v = adj_m.vertices[adj_m.key2v_index[source_v_key]]
        terminal_v = adj_m.vertices[adj_m.key2v_index[terminal_v_key]]
        assert isinstance(source_v, VertexMatrix) and isinstance(terminal_v, VertexMatrix)
        # 1. 将各边的流量 flow 初始化为 0
        for edge in adj_m.edges:
            assert isinstance(edge, Edge)
            edge.flow = 0

        # 2. 在 while 循环中，重复在残存网络 Gf 中寻找一条增广路径 p
        # 然后使用残存容量 cf(p) 来对路径 p 上的流 flow 进行增加
        # 路径 p 上的一条边要么是原来网络中的一条边，要么是原来网络中的边 的反向边
        # 在本实现中，adj_m 中的矩阵保存的就是残存网络 Gf 中各个边的流量
        bfs = BFS()
        is_exist_aug_path = True  # 循环标志 True 表示当前残存网络 Gf 中存在一条增广路径
        while is_exist_aug_path:
            # 2.1. 找出增广路径 aug_path
            bfs.do_bfs(adj_m, source_v.key)
            aug_path = bfs.get_path(adj_m, source_v_key, terminal_v_key)
            if not isinstance(aug_path, list) or len(aug_path) <= 1:
                # 如果不存在增广路径，BFS 会返回空列表。如果返回仅含 1 个元素关键字的列表，是异常情况
                break

            # 2.2. 找出路径 p 中的最小残存容量 cf(u, v)
            min_cf = self.inf
            for i in range(1, len(aug_path)):
                # 根据 key 获取 index
                from_key = aug_path[i - 1]
                to_key = aug_path[i]
                assert from_key in adj_m.key2v_index and to_key in adj_m.key2v_index
                from_index = adj_m.key2v_index[from_key]
                to_index = adj_m.key2v_index[to_key]
                # 更新路径上的最小残存容量 min_cf
                if min_cf > adj_m.adj_m[from_index][to_index]:
                    min_cf = adj_m.adj_m[from_index][to_index]
            assert min_cf < self.inf  # 断言增广路径上的流量值不为 inf

            # 2.3. 在 for 循环中，对路径上 p 的每条边 (u, v) 的流量进行更新
            for i in range(1, len(aug_path)):
                # 根据 key 获取 index
                from_key = aug_path[i - 1]
                to_key = aug_path[i]
                assert from_key in adj_m.key2v_index and to_key in adj_m.key2v_index
                from_index = adj_m.key2v_index[from_key]
                to_index = adj_m.key2v_index[to_key]

                # 如果残存边 (u, v) 是原来流网络中的一条边，则增加其流量 (u, v).f
                # 如果残存边 (u, v) 不是原来流网络中的一条边，则减少其反向边 (v, u) 流量 (v, u).f
                # 在本实现中，增加边 (u, v) 的流量，等于缩减 (u, v) 的剩余容量、增加反平行边 (v, u) 的剩余容量
                adj_m.adj_m[from_index][to_index] -= min_cf
                adj_m.adj_m[to_index][from_index] += min_cf

        # 3. 最后，当 while 循环结束时，不再有增广路径。根据最大流最小切割定理，此时流 flow 就是最大流
        # 在本实现中，adj_m 中的矩阵保存的就是残存网络 Gf 中各个边的流量，最终将实际的流量赋予各个结点的 flow 属性
        adj_m.max_flow = 0
        for from_index in range(len(adj_m.adj_m)):
            for to_index in range(len(adj_m.adj_m[from_index])):
                from_node = adj_m.vertices[from_index]
                to_node = adj_m.vertices[to_index]
                assert isinstance(from_node, VertexMatrix) and isinstance(to_node, VertexMatrix)
                # 如果此边是原图中的边，则赋予该边 flow 属性，表示最大流的流量
                if (from_node.key, to_node.key) in adj_m.key2e_index:
                    edge_index = adj_m.key2e_index[(from_node.key, to_node.key)]
                    edge = adj_m.edges[edge_index]
                    edge.flow = adj_m.adj_m[from_index][to_index]        # 赋予此边流量属性 flow
                    adj_m.max_flow += adj_m.adj_m[from_index][to_index]  # 增长图的最大流量值


def main():
    # 构造图同《CLRS》图 26-6 的(含边容量的)有向图用于计算最大流
    # 用于构造邻接矩阵的顶点的 key/val 信息列表
    matrix_vertices_info = [
        ['s', 1], ['v1', 200], ['v2', 300], ['v3', 400], ['v4', 500], ['t', 0]
    ]
    # 有向边的 from/to/c/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['s', 'v1', 16, True], ['s', 'v2', 13, True], ['v2', 'v1', 4, True],
        ['v1', 'v3', 12, True], ['v2', 'v4', 14, True], ['v3', 'v2', 9, True],
        ['v4', 'v3', 7, True], ['v3', 't', 20, True], ['v4', 't', 4, True]
    ]

    # 根据前述列表信息构造结点列表
    inf = 0x3f3f3f3f  # 需保证与程序中其它 inf 是相同的值
    matrix_vertices = []
    di_edges = []
    for v in matrix_vertices_info:
        matrix_vertices.append(VertexMatrix(key=v[0], val=v[1], distance=inf))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], capacity=e[2], is_directed=e[3]))

    # 创建邻接矩阵 (用邻接矩阵+有向图 执行最大流算法)
    adj_m = AdjacencyMatrix(matrix_vertices, di_edges)

    # 执行 O(VE^2) Ford-Fulkerson 最大流算法
    source_v_key, terminal_v_key = 's', 't'
    ford_fulkerson = FordFulkerson()
    start = time.process_time()
    ford_fulkerson.do_edmonds_karp(adj_m, source_v_key, terminal_v_key)
    end = time.process_time()

    # 输出结果 & 运行时间
    # max_flow: 23
    # [0, 4, 2, 0, 0, 0]
    # [12, 0, 0, 0, 0, 0]
    # [11, 4, 0, 0, 3, 0]
    # [0, 12, 9, 0, 7, 1]
    # [0, 0, 11, 0, 0, 0]
    # [0, 0, 0, 19, 4, 0]
    print('\nmax_flow:', adj_m.max_flow)
    adj_m.print_matrix_info()
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
