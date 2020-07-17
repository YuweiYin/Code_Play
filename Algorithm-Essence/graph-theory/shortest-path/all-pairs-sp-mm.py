#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/shortest_path
@File    : all-pairs-sp-mm.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
全源最短路径 All Pairs Shortest Path
最短路径和矩阵乘法

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 25
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


# (带边权的)邻接矩阵的图结构，通常适合稠密图
# 输入顶点结构体列表、边结构体列表
class AdjacencyMatrix:
    def __init__(self, vertices, edges):
        assert isinstance(vertices, list)

        self.inf = 0x3f3f3f3f        # 初始各边的权重值均为 inf 无穷
        self.edges = edges           # 存储输入的边列表
        self.key2e_index = dict({})  # 由(起始,终止)顶点的关键字/唯一标志符映射到边数组下标

        self.vertices = vertices     # 存储输入的顶点列表 (可以从下标映射到顶点)
        self.v2index = dict({})      # 由顶点映射到其下标 (既是邻接矩阵的行/列下标，也是 vertices 列表的下标)
        self.key2v_index = dict({})  # 由顶点的关键字/唯一标志符映射到顶点数组下标
        for index, vertex in enumerate(vertices):
            self.v2index[vertex] = index
            self.key2v_index[vertex.key] = index

        # 构建带权重的邻接矩阵(二维方阵)，adj[x][y] 的值为边 (x, y) 的权重值
        v_num = len(vertices)  # 顶点数目
        self.adj_m = [[self.inf] * v_num for _ in range(v_num)]

        # 若 edges 合法，则进行边初始化处理
        if isinstance(edges, list):
            for index, edge in enumerate(edges):
                assert isinstance(edge, Edge)
                from_v = edge.from_v  # 边起点的关键字 key
                to_v = edge.to_v      # 边终点的关键字 key
                weight = edge.weight  # 边的权重值
                self.key2e_index[(from_v, to_v)] = index
                if from_v in self.key2v_index and to_v in self.key2v_index:
                    # 将顶点关键字 key 转为下标 index，然后设置 adj[from][to] 为边权
                    from_index = self.key2v_index[from_v]
                    to_index = self.key2v_index[to_v]
                    assert 0 <= from_index < v_num and 0 <= to_index < v_num
                    self.adj_m[from_index][to_index] = weight
                    # 如果是无向边，则 adj[to][from] 也设置为 weight
                    if not edge.is_directed:
                        self.adj_m[to_index][from_index] = weight

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


class AllPairsShortestPath:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 所有结点的 distance 初始化为 inf

    # 寻找图 adj_m 的全源最短路径
    # 这里默认图为邻接矩阵结构
    # lij^{m} 为从结点 i 到结点 j 的至多包含 m 条边的任意路径中的最小权重
    # lij^{m} = min( lij^{m-1}, min( lik^{m-1} + w(k, j) ) )
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def _extend_shortest_paths(self, matrix_l, matrix_w):
        assert isinstance(matrix_w, list) and len(matrix_w) > 0
        assert isinstance(matrix_l, list) and len(matrix_l) == len(matrix_w)
        # 确保 matrix_l 和 matrix_w 每一行的元素个数都等于列数 n
        n = len(matrix_w)
        for i in range(n):
            assert isinstance(matrix_l[i], list) and len(matrix_l[i]) == n
            assert isinstance(matrix_w[i], list) and len(matrix_w[i]) == n

        res_matrix = [[self.inf for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    res_matrix[i][j] = min(res_matrix[i][j], matrix_l[i][k] + matrix_w[k][j])
        return res_matrix

    # 较慢的全源最短路径算法
    # 时间复杂度 \Theta(n^4)
    # 空间复杂度 \Theta(n^2)
    def slow_all_pairs_shortest_paths(self, adj_m):
        assert isinstance(adj_m, AdjacencyMatrix)
        n = len(adj_m.vertices)
        matrix_l = [[adj_m.adj_m[i][j] for j in range(n)] for i in range(n)]
        for m in range(1, n - 1):
            matrix_l = self._extend_shortest_paths(matrix_l, adj_m.adj_m)
        return matrix_l

    # 稍快的全源最短路径算法 (矩阵快速幂)
    # 时间复杂度 \Theta(n^3 log n)
    # 空间复杂度 \Theta(n^2)
    def faster_all_pairs_shortest_paths(self, adj_m):
        assert isinstance(adj_m, AdjacencyMatrix)
        n = len(adj_m.vertices)
        matrix_l = [[adj_m.adj_m[i][j] for j in range(n)] for i in range(n)]
        m = 1
        while m < n - 1:
            matrix_l = self._extend_shortest_paths(matrix_l, matrix_l)
            m <<= 1
        return matrix_l

    @staticmethod
    def print_matrix(matrix):
        assert isinstance(matrix, list)
        for row in matrix:
            print(row)


def main():
    # 构造图同《CLRS》Chapter 25.1 的(带边权)有向图
    # 用于构造邻接矩阵的顶点的 key/val 信息列表
    matrix_vertices_info = [
        ['1', 100], ['2', 200], ['3', 300], ['4', 400], ['5', 500]
    ]
    # 有向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['1', '2', 3, True], ['1', '3', 8, True], ['1', '5', -4, True],
        ['2', '4', 1, True], ['2', '5', 7, True], ['3', '2', 4, True],
        ['4', '1', 2, True], ['4', '3', -5, True], ['5', '4', 6, True],
        # 主对角线全为 0
        ['1', '1', 0, True], ['2', '2', 0, True], ['3', '3', 0, True],
        ['4', '4', 0, True], ['5', '5', 0, True]
    ]

    # 根据前述列表信息构造结点列表
    matrix_vertices = []
    di_edges = []
    for v in matrix_vertices_info:
        matrix_vertices.append(VertexMatrix(key=v[0], val=v[1]))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    # 创建邻接矩阵 (用邻接矩阵+有向图 执行全源最短路径算法)
    adj_m = AdjacencyMatrix(matrix_vertices, di_edges)

    # 执行 O(n^4) 全源最短路径算法
    all_pairs_sp = AllPairsShortestPath()
    start = time.process_time()
    matrix_l = all_pairs_sp.slow_all_pairs_shortest_paths(adj_m)
    end = time.process_time()

    # 输出结果 & 运行时间
    # [0, 1, -3, 2, -4]
    # [3, 0, -4, 1, -1]
    # [7, 4, 0, 5, 3]
    # [2, -1, -5, 0, -2]
    # [8, 5, 1, 6, 0]
    print('\nmatrix_l:')
    all_pairs_sp.print_matrix(matrix_l)
    print('Running Time: %.5f ms' % ((end - start) * 1000))  # 0.20900 ms

    # 执行 O(n^3 log n) 全源最短路径算法
    start = time.process_time()
    matrix_l = all_pairs_sp.faster_all_pairs_shortest_paths(adj_m)
    end = time.process_time()

    # 输出结果 & 运行时间
    print('\nmatrix_l:')
    all_pairs_sp.print_matrix(matrix_l)
    print('Running Time: %.5f ms' % ((end - start) * 1000))  # 0.13700 ms


if __name__ == "__main__":
    sys.exit(main())
