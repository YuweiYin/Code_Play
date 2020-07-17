#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/graph_basis
@File    : bfs.py
@Author  : YuweiYin
=================================================="""

import sys
import time
import queue

"""
图的搜索 - 广度优先搜索 (Breadth First Search, BFS)

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
    def __init__(self, key, val=None, distance=0):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        self.neighbor = dict({})  # 本顶点的邻居字典，key 为邻居的关键字，value 为 Edge 边结构体
        # 如果是有向图，本结点为关联边的出发点 from_v，其邻居关联边的终止点 to_v
        '''下面是用于 BFS 的属性'''
        self.color = False        # False 为"白色"，表示未被发现；True 为"黑色"，表示已经探索结束
        self.distance = distance  # 此结点距离源结点的距离 (最短简单路径的边数)
        self.p = None             # 此结点的前驱结点/广度优先搜索树的父结点

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


# 广度优先搜索 (Breadth First Search, BFS)
class BFS:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 初始化各个结点距离源结点的距离为 inf 无穷
        self.path = ''         # 从源结点 s 到目标结点 v 的一条最短路径上的所有结点(的关键字)

    # 输入：graph 图结构，start_key 源顶点的关键字，is_adj_link 为 True 表示图为邻接表结构，False 表示为邻接矩阵结构
    def do_bfs(self, graph, start_key, is_adj_link=True):
        if is_adj_link:
            # 如果图是邻接表结构
            self._bfs_link(graph, start_key)
        else:
            # 如果图是邻接矩阵结构
            self._bfs_matrix(graph, start_key)

    # 对邻接表结构的图 graph，以 start_v 为源结点进行 BFS
    def _bfs_link(self, adj_l, start_key):
        assert isinstance(adj_l, AdjacencyList)
        # 先把 start_key 源顶点的关键字 转为源结点结构体
        if start_key in adj_l.key2index:
            start_index = adj_l.key2index[start_key]
            assert 0 <= start_index < len(adj_l.vertices)
            start_v = adj_l.vertices[start_index]
            assert isinstance(start_v, VertexList)
        else:
            print('输入的 start_key 不是任何顶点的关键字，BFS 失败')
            return

        # 1. 除了源结点 s 外，将其余所有结点 u 的状态标记为“未被发现”，即 color 为白色 white
        # 另外，将 u.d 设置为无穷 inf，表示从源结点不可达结点 u。由于未探索到结点 u，将其前驱结点设置为空 nil
        for v in adj_l.adj_l.values():
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
            assert isinstance(u, VertexList)

            # 4.2. 逐个处理 u 的所有邻接结点 v
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

                # 4.3. 如果 v.color 是白色，表示它未被发现，需要被加入到队列 Q 中。在入队之前，需要设置其属性：
                #     - v.color 颜色设置为灰色，表示它已被发现，但是尚未被探索完（所谓探索结束，是其邻接结点都已被处理）。
                #     - v.d 是 v 到源结点 s 的距离，这个距离等于 u.d 距离加上 1
                #     - v.p 设置前驱/父结点为 u
                #     - 将 v 入队，之后的 while 循环中 会考察 v 的各个邻接结点
                if not v.color:
                    v.color = True
                    v.distance = u.distance + 1
                    v.p = u
                    aux_queue.put(v)
            # 4. for 循环结束，u 的所有邻接结点都被考察了，所以 u 已经被探索结束了。u.color 设置为黑色，保证不会再被加入队列 Q。
            # u.color = True

    # 对邻接矩阵结构的图 graph，以 start_v 为源结点进行 BFS
    def _bfs_matrix(self, adj_m, start_v):
        pass

    # 在计算出 BFS 之后，打印出所有结点(的关键字)及其距离
    @staticmethod
    def print_vertex_distance(adj_l):
        assert isinstance(adj_l, AdjacencyList)
        for v in adj_l.vertices:
            assert isinstance(v, VertexList)
            print(v.key, v.distance)

    # 在计算出 BFS 之后，打印出从源结点 s 到目标结点 v 的一条最短路径上的所有结点(的关键字)
    # 此处图结构为邻接表 adj_l
    def get_path(self, adj_l, start_key, end_key):
        if not isinstance(adj_l, AdjacencyList):
            return 'get_path: 输入的参数类型不合法'
        # 先把 key 关键字 转为顶点点结构体
        if start_key in adj_l.key2index:
            start_index = adj_l.key2index[start_key]
            assert 0 <= start_index < len(adj_l.vertices)
            start_v = adj_l.vertices[start_index]
            assert isinstance(start_v, VertexList)
        else:
            return '输入的 start_key 不是任何顶点的关键字'

        if end_key in adj_l.key2index:
            end_index = adj_l.key2index[end_key]
            assert 0 <= end_index < len(adj_l.vertices)
            end_v = adj_l.vertices[end_index]
            assert isinstance(end_v, VertexList)
        else:
            return '输入的 end_key 不是任何顶点的关键字'

        self.path = ''
        self._get_path(adj_l, start_v, end_v)
        return self.path

    def _get_path(self, adj_l, start_v, end_v):
        if end_v == start_v:
            self.path += str(start_v.key)
        elif not isinstance(end_v.p, VertexList):
            self.path = 'No path from ' + str(start_v.key) + ' to ' + str(end_v.key) + ' exists.'
        else:
            # 先获取其前驱结点/父结点的关键字，再获取本结点的关键字
            self._get_path(adj_l, start_v, end_v.p)
            self.path += str(end_v.key)


def main():
    # 构造图同《CLRS》Chapter 22.2 的 BFS 图
    # 用于构造邻接表的顶点的 key/val 信息列表
    list_vertices_info = [
        ['r', 100], ['s', 200], ['t', 300], ['u', 400],
        ['v', 500], ['w', 600], ['x', 700], ['y', 800]
    ]
    # 无向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    bi_edges_info = [
        ['r', 'v', 1, False], ['r', 's', 1, False], ['s', 'w', 1, False],
        ['w', 't', 1, False], ['w', 'x', 1, False], ['t', 'x', 1, False],
        ['t', 'u', 1, False], ['x', 'u', 1, False], ['x', 'y', 1, False],
        ['u', 'y', 1, False]
    ]

    # 根据前述列表信息构造结点列表
    list_vertices = []
    bi_edges = []
    for v in list_vertices_info:
        list_vertices.append(VertexList(key=v[0], val=v[1]))
    for e in bi_edges_info:
        bi_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    # 创建邻接表 (用邻接链表+无向图 执行 BFS)
    adj_l = AdjacencyList(list_vertices, bi_edges)

    # 执行 BFS 过程
    start_key = 's'
    start = time.process_time()
    bfs = BFS()
    bfs.do_bfs(graph=adj_l, start_key=start_key, is_adj_link=True)
    end = time.process_time()

    # 查看 BFS 结果
    print('\n源顶点为 ', start_key)
    print('BFS 结果 (各顶点关键字 及 与源顶点的距离)')
    bfs.print_vertex_distance(adj_l)

    # 打印(无权)最短路径
    print('\n(无权) 最短路径')
    for v_info in list_vertices_info:
        print(bfs.get_path(adj_l=adj_l, start_key=start_key, end_key=v_info[0]))

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
