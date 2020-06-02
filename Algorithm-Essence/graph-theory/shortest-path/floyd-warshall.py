#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/shortest_path
@File    : floyd-warshall.py
@Author  : YuweiYin
@Date    : 2020-06-01
=================================================="""

import sys
import time

"""
全源最短路径 All Pairs Shortest Path
Floyd-Warshall 算法 & 计算有向图的传递闭包 Transitive Closure

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


class FloydWarshall:
    def __init__(self):
        self.inf = 0x3f3f3f3f  # 所有结点的 distance 初始化为 inf

    # Floyd-Warshall 全源最短路径算法
    # 寻找图 adj_m 的全源最短路径 (这里默认图为邻接矩阵结构)
    # 时间复杂度 \Theta(n^3)
    # 空间复杂度 \Theta(n^2)
    def do_floyd_warshall(self, adj_m):
        assert isinstance(adj_m, AdjacencyMatrix)

        # 初始化
        n = len(adj_m.vertices)
        # 权重矩阵 D：dij^{k} 为从结点 i 到结点 j 的所有中间结点全部取自集合 {1, 2, ..., k} 的一条最短路径的权重
        # - 若 k == 0，则 dij^{k} = w(i, j)
        # - 若 k >= 1，则 dij^{k} = min( dij^{k-1}, dik^{k-1} + dkj^{k-1} )
        # D^{n} = (dij^{n}) 给出的就是最终答案：对于所有的 i, j \in V，有 dij^{n} = d(i, j) 最优值
        matrix_d = [[adj_m.adj_m[i][j] for j in range(n)] for i in range(n)]

        # 前驱矩阵 P = Pij
        # 对 k == 0
        # - 若 i == j 或 wij == inf，则 pij^{0} = inf
        # - 若 i != j 或 wij < inf，则 pij^{0} = i
        # 对 k >= 1
        # - 若 dij^{k-1} <= dik^{k-1} + dkj^{k-1}，则 pij^{k} = pij^{k-1}
        # - 若 dij^{k-1} > dik^{k-1} + dkj^{k-1}，则 pij^{k} = pkj^{k-1}
        matrix_p = [[i if adj_m.adj_m[i][j] < self.inf else self.inf for j in range(n)] for i in range(n)]

        # 前驱矩阵 P 主对角线置为 inf
        for i in range(n):
            matrix_p[i][i] = self.inf

        # 主循环
        for k in range(n):
            # 由于计算过程中下标无重叠，所以可以不用每次都新建两个 n x n 矩阵
            # new_d = [[self.inf for _ in range(n)] for _ in range(n)]
            # new_p = [[matrix_p[i][j] for j in range(n)] for i in range(n)]
            for i in range(n):
                for j in range(n):
                    case_ij = matrix_d[i][j]
                    case_ikj = matrix_d[i][k] + matrix_d[k][j]
                    if case_ij <= case_ikj:
                        # new_d[i][j] = case_ij
                        matrix_d[i][j] = case_ij
                    else:
                        # new_d[i][j] = case_ikj
                        # new_p[i][j] = matrix_p[k][j]
                        matrix_d[i][j] = case_ikj
                        matrix_p[i][j] = matrix_p[k][j]
            # matrix_d = new_d
            # matrix_p = new_p

        # 返回(加权)距离矩阵 D 和前驱矩阵 P
        return matrix_d, matrix_p

    # 根据前驱矩阵 P 获取某结点 i 到 j 的一条最短路径(上的所有结点)
    # 输入的是结点 i 和 j 的关键字 key
    def print_shortest_path(self, adj_m, matrix_p, i_key, j_key):
        # 检查输入的合法性
        assert isinstance(adj_m, AdjacencyMatrix)
        n = len(adj_m.vertices)
        assert isinstance(matrix_p, list) and len(matrix_p) == n
        for row in matrix_p:
            assert len(row) == n

        assert i_key in adj_m.key2v_index and j_key in adj_m.key2v_index
        i = adj_m.key2v_index[i_key]
        j = adj_m.key2v_index[j_key]
        self._print_shortest_path(adj_m, matrix_p, i, j)

    # 输入的是结点 i 和 j 的下标
    def _print_shortest_path(self, adj_m, matrix_p, i, j):
        assert isinstance(adj_m, AdjacencyMatrix)
        if i == j:
            print(adj_m.vertices[i])
        elif matrix_p[i][j] == self.inf:
            print('no path from', adj_m.vertices[i].key, 'to', adj_m.vertices[j].key)
        else:
            self._print_shortest_path(adj_m, matrix_p, i, matrix_p[i][j])
            print(adj_m.vertices[j])

    # 计算有向图的传递闭包
    def transitive_closure(self, adj_m):
        assert isinstance(adj_m, AdjacencyMatrix)
        n = len(adj_m.vertices)

        # 传递闭包 T 矩阵
        # - 在 k 为 0 时，有：
        #     - 若 i != j 且 (i, j) \notin E，则 tij^{0} = 0
        #     - 若 i == j 或 (i, j) \in E，则 tij^{0} = 1
        matrix_t = [[False for _ in range(n)] for _ in range(n)]

        # 传递闭包 T 矩阵的初始化
        for i in range(n):
            for j in range(n):
                # 主对角线，以及有边的位置 都置为 True
                if i == j or adj_m.adj_m[i][j] < self.inf:
                    matrix_t[i][j] = True

        # 主循环
        # - 对于 k >= 1，有：
        #     - tij^{k} = tij^{k-1} \lor ( tik^{k-1} \land tkj^{k-1} )
        for k in range(n):
            # 由于计算过程中下标无重叠，所以可以不用每次都新建 new_t 这个 n x n 矩阵
            # new_t = [[matrix_t[i][j] for j in range(n)] for i in range(n)]
            for i in range(n):
                for j in range(n):
                    matrix_t[i][j] = matrix_t[i][j] or (matrix_t[i][k] and matrix_t[k][j])
                    # new_t[i][j] = matrix_t[i][j] or (matrix_t[i][k] and matrix_t[k][j])
            # matrix_t = new_t

        # 返回传递闭包矩阵
        return matrix_t

    # 辅助函数：打印矩阵
    @staticmethod
    def print_matrix(matrix):
        assert isinstance(matrix, list)
        for row in matrix:
            print(row)


def main():
    # 构造图同《CLRS》图 25-2 的(带边权)有向图 用于计算全源最短路径
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
        # 主对角线权重全为 0
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

    # 执行 \Theta(n^3) Floyd-Warshall 全源最短路径算法
    floyd_warshall = FloydWarshall()
    start = time.process_time()
    matrix_d, matrix_p = floyd_warshall.do_floyd_warshall(adj_m)
    end = time.process_time()

    # 输出结果 & 运行时间
    # [0, 1, -3, 2, -4]
    # [3, 0, -4, 1, -1]
    # [7, 4, 0, 5, 3]
    # [2, -1, -5, 0, -2]
    # [8, 5, 1, 6, 0]
    print('\nmatrix_d:')
    floyd_warshall.print_matrix(matrix_d)
    # [1061109567, 2, 3, 4, 0]
    # [3, 1061109567, 3, 1, 0]
    # [3, 2, 1061109567, 1, 0]
    # [3, 2, 3, 1061109567, 0]
    # [3, 2, 3, 4, 1061109567]
    print('\nmatrix_p:')
    floyd_warshall.print_matrix(matrix_p)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 根据前驱矩阵 获取结点 i 到结点 j 的一条最短路径
    i_key = '1'
    j_key = '2'
    floyd_warshall.print_shortest_path(adj_m, matrix_p, i_key, j_key)  # 1->5->4->3->2

    '''下面是传递闭包的计算'''

    # 构造图同《CLRS》图 25-5 的(无权)有向图 用于计算传递闭包
    # (对传递闭包而言，如果只关心结点间的可达性，则无需考虑边权)
    # 用于构造邻接矩阵的顶点的 key/val 信息列表
    matrix_vertices_info = [
        ['1', 100], ['2', 200], ['3', 300], ['4', 400]
    ]
    # 有向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['2', '3', 1, True], ['2', '4', 1, True], ['3', '2', 1, True],
        ['4', '1', 1, True], ['4', '3', 1, True],
        # 主对角线权重也都是 1
        ['1', '1', 1, True], ['2', '2', 1, True], ['3', '3', 1, True],
        ['4', '4', 1, True]
    ]

    # 根据前述列表信息构造结点列表
    matrix_vertices = []
    di_edges = []
    for v in matrix_vertices_info:
        matrix_vertices.append(VertexMatrix(key=v[0], val=v[1]))
    for e in di_edges_info:
        di_edges.append(Edge(from_v=e[0], to_v=e[1], weight=e[2], is_directed=e[3]))

    # 创建邻接矩阵 (用邻接矩阵+有向图 计算传递闭包)
    adj_m = AdjacencyMatrix(matrix_vertices, di_edges)

    # 执行 \Theta(n^3) 基于 Floyd-Warshall 的传递闭包计算
    floyd_warshall = FloydWarshall()
    start = time.process_time()
    matrix_t = floyd_warshall.transitive_closure(adj_m)
    end = time.process_time()

    # 输出结果 & 运行时间
    # [True, False, False, False]
    # [True, True, True, True]
    # [True, True, True, True]
    # [True, True, True, True]
    print('\nmatrix_t:')
    floyd_warshall.print_matrix(matrix_t)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
