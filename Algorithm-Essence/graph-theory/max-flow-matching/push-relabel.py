#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/max_flow_matching
@File    : push-relabel.py
@Author  : YuweiYin
@Date    : 2020-06-04
=================================================="""

import sys
import time

"""
最大流 Max-Flow

- Push-Relabel 推送-重贴标签方法
    - Push-Relabel 通用的推送-重贴标签算法 O(V^2 E)
    - Relabel-To-Front 前置重贴标签算法 O(V^3)

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


# 用于邻接表的顶点结构体
# 这里是用散列表 (而不是用链表) 来表达某顶点的所有邻接顶点
class VertexList:
    # 构造方法
    def __init__(self, key, val=None, pre_v=None, next_v=None, height=0, exceed=0):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        self.neighbor = dict({})  # 本顶点的邻居字典，key 为邻居的关键字，value 为 Edge 边结构体
        # 如果是有向图，本结点为关联边的出发点 from_v，其邻居关联边的终止点 to_v
        '''下面是用于 Max-Flow 的属性'''
        self.pre_v = pre_v        # 此结点在单链表 L 中的前驱结点
        self.next_v = next_v      # 此结点在单链表 L 中的后继结点 (L 中的结点会保持拓扑排序次序)
        self.height = height      # 此结点的高度(标签)。取值不低于 0
        self.exceed = exceed      # 此结点的超额流量。取值不低于 0

    # 类序列化输出方法
    def __str__(self):
        return 'key:' + str(self.key) + '\theight:' + str(self.height) + '\texceed:' + str(self.exceed)

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
        return list(self.neighbor.keys())

    # 返回本顶点到邻居 neighbor 的 Edge 边结构体
    def get_weight(self, neighbor):
        if neighbor in self.neighbor:
            return self.neighbor[neighbor]
        else:
            return None


# 邻接表+邻接矩阵的图结构
# 输入顶点结构体列表、边结构体列表
class AdjacencyListMatrix:
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
            assert isinstance(vertex, VertexList)
            self.v2index[vertex] = index
            self.key2v_index[vertex.key] = index

        self.adj_l = dict({})        # 本图的顶点字典, key 为顶点的序号，val 为顶点结构体
        for vertex in vertices:
            assert isinstance(vertex, VertexList)
            self.adj_l[vertex.key] = vertex

        # 构建残存网络 Gf(二维方阵)，adj[x][y] 的值为边 (x, y) 的当前流量，而不是边权重
        # 残存网络 Gf 可以有反平行边。如果 adj[x][y] 为 0 表示没有此边
        v_num = len(vertices)  # 顶点数目
        self.graph_f = [[0] * v_num for _ in range(v_num)]

        # 若 edges 合法，则进行边初始化处理
        if isinstance(edges, list):
            for index, edge in enumerate(edges):
                # 断言最大流算法里都是有向边
                assert isinstance(edge, Edge) and edge.is_directed
                # 给邻接链表增加边
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
                # 给邻接矩阵 (残存网络 Gf) 增加边
                from_v = edge.from_v  # 边起点的关键字 key
                to_v = edge.to_v  # 边终点的关键字 key
                capacity = edge.capacity  # 边的容量
                self.key2e_index[(from_v, to_v)] = index
                if from_v in self.key2v_index and to_v in self.key2v_index:
                    # 将顶点关键字 key 转为下标 index，然后初始化 adj[from][to] 为边的最大容量
                    from_index = self.key2v_index[from_v]
                    to_index = self.key2v_index[to_v]
                    assert 0 <= from_index < v_num and 0 <= to_index < v_num
                    self.graph_f[from_index][to_index] = capacity

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

    # 输出邻接矩阵 (残存网络 Gf)
    def print_matrix_info(self):
        assert isinstance(self.graph_f, list)
        for row in self.graph_f:
            print(row)


# 最大流算法
# Push-Relabel 通用的推送-重贴标签算法 O(V^2 E)
# Relabel-To-Front 前置重贴标签算法 O(V^3)
class PushRelabel:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 所有结点的 distance 初始化为 inf

    # 初始化预流
    # 时间复杂度：O(V + E)
    # 该初始化过程 将从源结点 s 发出的所有边都充满流（即理想上 最大流的最大可能取值，也即是切割 ({s}, V-{s}) 的容量），
    # 而其它边上都没有流。对于每个与源结点 s 相邻的结点 v，一开始其超额流 v.e = c(s, v)，
    # 因为流入 v 的流量是 c(s, v)，而流出 v 的流量为 0。并且将 s.e 初始化为所有这些容量之和的相反数。
    # 至于高度(标签)，一开始仅有源结点 s 高度为 `|V|`，其余结点的高度均为 0
    @staticmethod
    def initialize_preflow(adj_lm, source_v_key):
        # 首先确认输入的合法性，并将输入的源结点关键字 转为结点结构体
        assert isinstance(adj_lm, AdjacencyListMatrix)
        assert source_v_key in adj_lm.key2v_index
        source_v_index = adj_lm.key2v_index[source_v_key]
        source_v = adj_lm.vertices[source_v_index]
        assert isinstance(source_v, VertexList)

        # 一开始仅有源结点 s 高度为 `|V|`，其余结点的高度均为 0
        for v in adj_lm.vertices:
            assert isinstance(v, VertexList)
            v.height = 0
            v.exceed = 0
        source_v.height = len(adj_lm.vertices)

        # 让从源结点 s 发出的所有边都充满流，而其它边上都没有流
        # 即理想上 最大流的最大可能取值，也即是切割 ({s}, V-{s}) 的容量
        for edge in adj_lm.edges:
            assert isinstance(edge, Edge)
            edge.flow = 0

        for edge in source_v.neighbor.values():
            assert isinstance(edge, Edge)
            # 根据 v 的关键字获取顶点结构体
            to_v_key = edge.to_v
            assert to_v_key in adj_lm.key2v_index
            to_v_index = adj_lm.key2v_index[to_v_key]
            to_v = adj_lm.vertices[to_v_index]
            assert isinstance(to_v, VertexList)
            # 设置残存网络的边
            # - 若 u == s，则 (u, v).f = c(u, v) 在本实现中意味着残存网络中 cf(u, v) = 0 而 cf(v, u) = c(u, v)
            # - 若 u != s，则 (u, v).f = 0 在本实现中意味着残存网络中 cf(v, u) = c(u, v) 而 cf(v, u) = 0
            adj_lm.graph_f[source_v_index][to_v_index] = 0
            adj_lm.graph_f[to_v_index][source_v_index] = edge.capacity
            # 设置邻居结点 v 的超额流量
            to_v.exceed = edge.capacity
            # 减少源结点的超额流量
            source_v.exceed -= edge.capacity

    # 预流推送操作：把 u 的超额流量 u.e 推送给 v
    # 时间复杂度：O(1)
    @staticmethod
    def push_flow(adj_lm, u, v):
        assert isinstance(adj_lm, AdjacencyListMatrix)
        assert isinstance(u, VertexList) and isinstance(v, VertexList)
        # 需保证此时 u 的超额流量 u.e 大于零，且 u 的高度 u.h 比 v 的高度 v.h 高 1
        # 且残存网络中残存边 (u, v) 的残存容量大于 0，即 cf(u, v) > 0
        assert u.key in adj_lm.key2v_index and v.key in adj_lm.key2v_index
        u_index = adj_lm.key2v_index[u.key]
        v_index = adj_lm.key2v_index[v.key]
        cf_uv = adj_lm.graph_f[u_index][v_index]  # 边 (u, v) 的残存容量
        if u.exceed > 0 and u.height == v.height + 1 and cf_uv > 0:
            # 满足推送的条件
            # 1. 计算 u 的超额量 与 边 (u, v) 的残存容量 二者的较小者，作为推送的流量
            delta_flow = min(u.exceed, cf_uv)
            # 2. 推送后，改变残存网络的相应边的流量
            adj_lm.graph_f[u_index][v_index] -= delta_flow  # 正向边容量 cf 减少
            adj_lm.graph_f[v_index][u_index] += delta_flow  # 反向边容量 cf 增加
            # 3. 推送后，改变结点 u 和 v 的超额流量
            u.exceed -= delta_flow  # u.e 减少
            v.exceed += delta_flow  # v.e 增加
            return True
        else:
            # 不满足推送的条件
            return False

    # 重贴标签操作：把结点 u 的标签(高度)提升到 能够把超额的流量推送给某个邻居结点
    # 时间复杂度：O(V)
    @staticmethod
    def relabel(adj_lm, u):
        assert isinstance(adj_lm, AdjacencyListMatrix) and isinstance(u, VertexList)
        # 需保证此时 u 的超额流量 u.e 大于零，考察 u 的各个邻居结点，选择某个满足如下性质的"最矮的"结点 v
        # 残存网络中残存边 (u, v) 的残存容量大于 0，即 cf(u, v) > 0
        if u.exceed > 0:
            min_h = 0x3f3f3f3f
            assert u.key in adj_lm.key2v_index
            u_index = adj_lm.key2v_index[u.key]
            # 从残存网络矩阵中逐结点考虑
            for v_index, capacity in enumerate(adj_lm.graph_f[u_index]):
                if capacity > 0:
                    v = adj_lm.vertices[v_index]
                    assert isinstance(v, VertexList)
                    if v.height < min_h:
                        min_h = v.height
            # 这里断言一定存在某个可以推送流的边 (u, v)
            assert min_h >= u.height
            u.height = min_h + 1
        else:
            # u 的流量没有超额，不满足重贴标签的条件
            return False

    # 释放溢出结点：把结点 u 的超额的流量推送给某个邻居结点，直至 u 不再具有超额流量，即 u.e == 0
    # 时间复杂度：O(V)
    def discharge(self, adj_lm, u):
        assert isinstance(adj_lm, AdjacencyListMatrix) and isinstance(u, VertexList)
        # 需保证此时 u 的超额流量 u.e 大于零，考察 u 的各个邻居结点，选择某个满足如下性质的"最矮的"结点 v
        # 残存网络中残存边 (u, v) 的残存容量大于 0，即 cf(u, v) > 0
        if u.exceed > 0:
            # 获取 u 的邻居关键字列表，固定此顺序来试图将 u 的超额流量推送给各邻居
            n_list = adj_lm.vertices  # 这里考察所有可能邻居，而不仅是邻接的结点
            list_len = len(n_list)
            cur_index = 0  # 当前考察的邻居下标
            while u.exceed > 0:
                # 如果当前邻居的 index 越界，则需对结点 u 重贴标签、提升高度
                if cur_index >= list_len:
                    self.relabel(adj_lm, u)
                    cur_index = 0  # 重新从头开始考察 u 的邻居
                # 如果 index 不越界，则考察当前邻居
                else:
                    # 获取邻居结点结构体
                    cur_v = n_list[cur_index]
                    assert isinstance(cur_v, VertexList)
                    # 考察此边是否为许可边
                    assert u.key in adj_lm.key2v_index
                    u_index = adj_lm.key2v_index[u.key]
                    # cf_uv = adj_lm.graph_f[u_index][cur_v_index]  # 边 (u, v) 的残存容量
                    cf_uv = adj_lm.graph_f[u_index][cur_index]  # 边 (u, v) 的残存容量
                    if cf_uv > 0 and u.height == cur_v.height + 1:
                        # 如果当前边是许可边，则把 u 的一定量的超额流推送给邻居结点 v
                        # 每次 discharge 中，非饱和推送至多为 1 次
                        self.push_flow(adj_lm, u, cur_v)
                    else:
                        # 否则当前边是非许可边，则进入下个 while 循环，考察下一个邻居结点
                        cur_index += 1
            # 断言此时结点 u 的超额流量为 0
            assert u.exceed == 0
            return True
        else:
            return False

    # 使用 Relabel-To-Front 前置重贴标签算法 计算流网络 adj_m 的最大流
    # 时间复杂度：O(V^3)
    def do_relabel_to_front(self, adj_lm, source_v_key, terminal_v_key):
        # 首先确认输入的合法性，并将输入的源结点和汇点关键字 转为结点结构体
        assert isinstance(adj_lm, AdjacencyListMatrix)
        assert source_v_key in adj_lm.key2v_index and terminal_v_key in adj_lm.key2v_index
        source_v = adj_lm.vertices[adj_lm.key2v_index[source_v_key]]
        terminal_v = adj_lm.vertices[adj_lm.key2v_index[terminal_v_key]]
        assert isinstance(source_v, VertexList) and isinstance(terminal_v, VertexList)
        # 1. 对网络的预流和结点高度进行初始化。
        self.initialize_preflow(adj_lm, source_v_key)

        # 2. 对链表 L 进行初始化，其中包含的是所有可能出现潜在溢出的结点，而结点之间的次序可以是任意的
        #    因为此时没有许可边，所以任意次序都是 Gfh 的一个拓扑排序，此后的循环过程中也会保持链表 L 中结点的次序为拓扑排序
        _list_head = VertexList(key='__list_head__')  # 链表头结点。注意此 key 不能与实际的结点 key 重复
        ptr = _list_head
        for v in adj_lm.vertices:
            assert isinstance(v, VertexList)
            # 将除源结点 s 和汇点 t 的结点都链接到双向链表中
            if v != source_v and v != terminal_v:
                v.pre_v = ptr
                ptr.next_v = v
                ptr = v

        # 3. 对每个结点 u 的 current 指针进行初始化，使该指针指向 u 的邻接链表 u.N 的首元素
        #    在本实现中略去此步骤

        # 4. 获取链表首元素 u，从 u 开始考察处理
        u = _list_head.next_v

        # 5. 在 while 循环中，对链表 L 进行遍历并逐个释放结点
        while u is not None:
            assert isinstance(u, VertexList)
            # 记录释放操作前 u 的高度
            # 如果结点 u 在释放过程中执行了重贴标签操作，其高度会提升，从而方便后面的判断
            old_height = u.height

            # 对结点 u 进行释放操作
            self.discharge(adj_lm, u)

            # 通过高度变化来判断 u 在释放过程中 是否执行过重贴标签操作
            if u.height > old_height:
                # 如果 u 执行过重贴标签操作，则将结点 u 移至链表 L 首部
                # 先判断 u 是否已在首部，如果是，则不改变链表结构
                if u != _list_head.next_v:
                    assert u.pre_v != _list_head and isinstance(u.pre_v, VertexList)
                    # 先让 u 的前驱和后继结点相连
                    u.pre_v.next_v = u.next_v
                    if isinstance(u.next_v, VertexList):
                        u.next_v.pre_v = u.pre_v
                    # 然后把 u 插入到首部
                    assert isinstance(_list_head.next_v, VertexList)
                    _list_head.next_v.pre_v = u
                    u.next_v = _list_head.next_v
                    u.pre_v = _list_head
                    _list_head.next_v = u

            # 以链表 L 中结点 u 的后继结点作为下一次 while 循环处理的结点
            # 如果结点 u 在释放过程中执行过重贴标签操作，那么此时 u 已被移动至 L 首部
            u = u.next_v

        # 3. 最后，当 while 循环结束时，此时流 flow 就是最大流
        # 在本实现中，adj_lm.graph_f 矩阵保存的就是残存网络 Gf 中各个边的流量，最终将实际的流量赋予各个结点的 flow 属性
        adj_lm.max_flow = 0
        for from_index in range(len(adj_lm.graph_f)):
            for to_index in range(len(adj_lm.graph_f[from_index])):
                from_node = adj_lm.vertices[from_index]
                to_node = adj_lm.vertices[to_index]
                assert isinstance(from_node, VertexList) and isinstance(to_node, VertexList)
                # 如果此边是原图中的边，则赋予该边 flow 属性，表示最大流的流量
                if (from_node.key, to_node.key) in adj_lm.key2e_index:
                    edge_index = adj_lm.key2e_index[(from_node.key, to_node.key)]
                    edge = adj_lm.edges[edge_index]
                    edge.flow = adj_lm.graph_f[from_index][to_index]         # 赋予此边流量属性 flow
                    adj_lm.max_flow += adj_lm.graph_f[from_index][to_index]  # 增长图的最大流量值


def main():
    # 构造图同《CLRS》图 26-10 的(含边容量的)有向图用于计算最大流
    # 用于构造邻接矩阵的顶点的 key/val 信息列表
    matrix_vertices_info = [
        ['s', 1], ['x', 200], ['y', 300], ['z', 400], ['t', 500]
    ]
    # 有向边的 from/to/c/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['s', 'x', 12, True], ['s', 'y', 14, True], ['x', 'y', 5, True],
        ['x', 't', 16, True], ['y', 'z', 8, True], ['z', 'x', 7, True],
        ['z', 't', 10, True]
    ]

    # 根据前述列表信息构造结点列表
    matrix_vertices = []
    di_edges = []
    for v in matrix_vertices_info:
        matrix_vertices.append(VertexList(key=v[0], val=v[1]))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], capacity=e[2], is_directed=e[3]))

    # 创建有向图的邻接表/邻接矩阵
    adj_lm = AdjacencyListMatrix(matrix_vertices, di_edges)

    # 执行 O(V^3) Push-Relabel 最大流算法 (Relabel-To-Front)
    source_v_key, terminal_v_key = 's', 't'
    push_relabel = PushRelabel()
    start = time.process_time()
    push_relabel.do_relabel_to_front(adj_lm, source_v_key, terminal_v_key)
    end = time.process_time()

    # 输出结果 & 运行时间
    # max_flow: 24
    # [0, 0, 6, 0, 0]
    # [12, 0, 5, 0, 4]
    # [8, 0, 0, 0, 0]
    # [0, 7, 8, 0, 2]
    # [0, 12, 0, 8, 0]
    print('\nmax_flow:', adj_lm.max_flow)
    adj_lm.print_matrix_info()
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
