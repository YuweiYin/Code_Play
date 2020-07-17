#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/shortest_path
@File    : dijkstra.py
@Author  : YuweiYin
=================================================="""

import sys
import time
import math

"""
单源最短路径 Single Source Shortest Path
非负权值加权图的最短路径 - Dijkstra 算法

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


# 元素结构体
class Element:
    def __init__(self, key, val=None):
        self.key = key      # (必备) 关键字 key。按每个顶点的 min_w 属性作为最小优先队列 Q 的 key
        self.val = val      # (可选) 值对象 val。每个顶点 Vertex 结构体
        self.left = self    # 本结点所在循环双向链表的 左兄弟结点
        self.right = self   # 本结点所在循环双向链表的 右兄弟结点
        self.parent = None  # 本结点的父结点
        self.child = None   # 本结点的(某一个)孩子结点
        self.degree = 0     # 本结点的孩子链表中的孩子数目
        self.mark = False   # 指示本结点自从上一次成为另一个孩子的结点后，是否失去过孩子


# 斐波那契(最小)堆 Fibonacci Min-Heap 数据结构
class FibonacciHeap:
    # 创建一个新的斐波那契堆 H
    # 此构造函数即为 make_fib_heap 过程
    # (摊还/实际)时间复杂度 O(1)
    def __init__(self, kv_list=None):
        # 斐波那契堆 H 就是本类(对象) self，有如下两个属性
        self.min = None  # 指向 H 中具有最小关键字的树的根结点
        self.n = 0       # 表示 H 中当前含有的结点总数目

        # 如果传入的 kv_list 为列表，则以插入的方式构建斐波那契堆 H
        # 如果传入的 kv_list 不为列表或者内容不合法，则是一个空斐波那契堆
        if isinstance(kv_list, list):
            for kv in kv_list:
                assert isinstance(kv, list) and len(kv) == 2
                self.fib_heap_insert(kv[0], kv[1])

    '''如下为 5 个可合并堆的基本操作'''

    # 创建并返回一个新的斐波那契堆
    # 构造函数即为 make_fib_heap 过程
    # (摊还/实际)时间复杂度 O(1)
    # def make_fib_heap(self):
    #     self.min = None  # 指向 H 中具有最小关键字的树的根结点
    #     self.n = 0       # 表示 H 中当前含有的结点总数目

    # 根据 key/val 构造结点，并插入到斐波那契堆 H 中
    # 操作成功返回 True，否则返回 False
    # (摊还/实际)时间复杂度 O(1)
    def fib_heap_insert(self, insert_key, insert_val):
        # 根据 key/val 创建一个新的 Element 结点
        insert_ele = Element(insert_key, insert_val)
        # 判断当前斐波那契堆 H 是否为空
        if isinstance(self.min, Element):
            # 如果 H 不为空，先插入当前新结点到根链表
            insert_ele.right = self.min.right
            assert isinstance(self.min.right, Element)  # 由于是循环双向链表，所以有此断言
            self.min.right.left = insert_ele
            self.min.right = insert_ele
            insert_ele.left = self.min

            # 然后再检查是否需要更改 H.min
            if insert_key < self.min.key:
                self.min = insert_ele
        else:
            # 如果 H 为空，则使得当前新结点 为 H 的根链表中唯一的结点
            self.min = insert_ele
        # 结点总数目加一
        self.n += 1
        return True

    # 根据 Element 对象构造结点，并插入到斐波那契堆 H 中
    # 操作成功返回 True，否则返回 False
    # (摊还/实际)时间复杂度 O(1)
    def fib_heap_insert_ele(self, insert_ele):
        if isinstance(insert_ele, Element):
            # 判断当前斐波那契堆 H 是否为空
            if isinstance(self.min, Element):
                # 如果 H 不为空，先插入当前新结点到根链表
                insert_ele.right = self.min.right
                assert isinstance(self.min.right, Element)  # 由于是循环双向链表，所以有此断言
                self.min.right.left = insert_ele
                self.min.right = insert_ele
                insert_ele.left = self.min

                # 然后再检查是否需要更改 H.min
                if insert_ele.key < self.min.key:
                    self.min = insert_ele
            else:
                # 如果 H 为空，则使得当前新结点 为 H 的根链表中唯一的结点
                self.min = insert_ele
            # 结点总数目加一
            self.n += 1
            return True
        else:
            return False

    # 合并两个斐波那契堆
    # 操作成功返回 True，否则返回 False
    # (摊还/实际)时间复杂度 O(1)
    # (此为静态函数，不对本斐波那契堆 self 作用)
    @staticmethod
    def fib_heap_union(h1, h2):
        if isinstance(h1, FibonacciHeap) and isinstance(h2, FibonacciHeap):
            # h1 和 h2 均为斐波那契堆，考察二者是否为空堆
            if isinstance(h1.min, Element) and isinstance(h2.min, Element):
                # 二者均不为空，则正常合并。
                # 先构建一个新的空斐波那契堆，并设置 min 为 h1.min
                union_heap = FibonacciHeap()
                union_heap.min = h1.min

                # 将 h2 连接到 union_heap 中 (两个循环双向链表的连接)
                assert isinstance(union_heap.min.right, Element)
                assert isinstance(h2.min.left, Element)
                union_heap.min.right.left = h2.min.left
                h2.min.left.right = union_heap.min.right
                union_heap.min.right = h2.min
                h2.min.left = union_heap.min

                # 检查是否需要更新 min
                if h2.min.key < union_heap.min.key:
                    union_heap.min = h2.min
                # 增加结点数目
                union_heap.n = h1.n + h2.n
                # 返回合并后的斐波那契堆
                return union_heap
            elif isinstance(h1.min, Element):
                # 如果仅 h1 为非空堆，则返回 h1
                return h1
            elif isinstance(h2.min, Element):
                # 如果仅 h2 为非空堆，则返回 h2
                return h2
            else:
                # 如果 h1 和 h2 均为空堆，则任意返回其中一个 (这里返回 h1)
                return h1
        elif isinstance(h1, FibonacciHeap):
            # 如果仅 h1 为斐波那契堆，则返回 h1
            return h1
        elif isinstance(h2, FibonacciHeap):
            # 如果仅 h2 为斐波那契堆，则返回 h2
            return h2
        else:
            # 如果 h1 和 h2 均不为斐波那契堆，则返回空
            return None

    # 查询最小结点
    # (摊还/实际)时间复杂度 O(1)
    def fib_heap_minimum(self):
        return self.min

    # 查询最小结点 - 输出其 key/val
    # (摊还/实际)时间复杂度 O(1)
    def fib_heap_print_min_kv(self):
        if isinstance(self.min, Element):
            print(self.min.key, self.min.val)
        else:
            print('Fibonacci Heap is Empty!')

    # 抽取最小结点 (查找、删除、返回)
    # (摊还)时间复杂度 O(log n)
    def fib_heap_extract_min(self):
        z = self.min  # 待删除的结点 z
        if isinstance(z, Element):
            # 判断待删结点 z 是否有孩子结点
            # 如果没有孩子结点，则跳过下面的分支，直接删除 z，并寻找替代的 min
            if isinstance(z.child, Element):
                # 如果待删结点 z 有孩子结点，则把其所有孩子均移至根链表
                # 先遍历此孩子链表，将其父指针均置为空
                ptr = z.child
                ptr.parent = None
                while ptr.right != z.child:
                    ptr = ptr.right
                    ptr.parent = None
                # 然后将此孩子链表链接到 H 的根链表 (两个循环双向链表的连接)
                # 孩子的孩子结点则不改动
                z.child.right.left = z.left
                z.left.right = z.child.right
                z.child.right = z
                z.left = z.child
                # 清除 z 的孩子指针
                z.child = None

            # 从根链表中删除结点 z
            if z.right == z:
                # 本堆仅有 z 一个结点，删除之后堆为空
                assert z.left == z and self.n == 1
                self.min = None
                self.n = 0
            else:
                # 本堆不止 z 一个结点，则正常删除 z (通过修改链表指针链接)
                self.min = z.right  # 将 min 改为 z.right，但它不一定是根链表中的最小结点，之后会修复此性质
                z.right.left = z.left
                z.left.right = z.right
                # 合并根链表中的结点，减少根链表的结点数目，并修复性质：让 self.min 确实为最小元素
                self._consolidate()
                self.n -= 1
            # 返回被删结点 z
            return z
        else:
            # self.min 不是 Element 对象，表明此斐波那契堆为空堆
            return None

    # 辅助函数：合并斐波那契堆 H 的根链表
    # 重复执行如下步骤，直到根链表中的每个结点有不同的 degree 度数
    # 1. 在根链表中找到两个具有相同度数的根 x 和 y。不失一般性，假定 x.key <= y.key
    # 2. 把 y 链接到 x：从根链表中移除 y，调用 _fib_heap_link 过程，使 y 成为 x 的孩子
    # 过程 2 将 x.degree 属性增加 1，并清除 y 上的 mark 标记
    def _consolidate(self):
        # 辅助数组 d_arr 用于记录根结点对应的度数的轨迹
        # 如果 d_arr[i] == y，那么当前的 y 是一个具有 y.degree == i 的结点
        # d_arr 数组的长度为最大度数的上界 D(H.n)，可以证明 D(H.n) <= \floor(log_{phi} n) = O(log n)
        phi = (1 + math.sqrt(5)) / 2  # 黄金分割率 golden_ratio ~= 1.61803
        # phi = round(phi, 5)  # 四舍五入仅保留小数点后几位，可加速下面的对数运算
        max_d = int(math.log(self.n, phi)) + 1  # 最大度数的上界

        # 创建长度为 max_d 的辅助数据 d_arr
        # 如果 d_arr 中某结点关键字 key 为 inf，则表示仅为占位结点
        inf = 0x3f3f3f3f
        d_arr = []
        for i in range(max_d):
            empty_node = Element(inf)
            d_arr.append(empty_node)

        # 循环处理根链表中的每个根结点 cur_root
        ptr = self.min.right
        assert isinstance(ptr, Element)  # 进入 _consolidate 前已保证本斐波那契堆不是空堆，故有此断言
        while ptr != self.min:
            # ptr 可能会成为别的结点的子结点，所以不再是根结点，因此下一个检查的也就不是 ptr.right 了
            next_root = ptr.right  # 记录下一个应该检查的根结点
            cur_root = ptr
            assert isinstance(cur_root, Element)
            cur_d = cur_root.degree  # 当前结点的度数
            assert 0 <= cur_d < max_d

            # 若存在与当前根结点 cur_root 相同度数的结点 y，需要合并这两个结点
            while d_arr[cur_d].key != inf:
                y = d_arr[cur_d]  # 取出此结点 y，让它加入 cur_root 的孩子链表
                assert isinstance(y, Element)
                # 如果原本在 trace 数组里的结点 y 的关键字 key 更小，则交换 cur_root 和 y
                if y.key < cur_root.key:
                    temp = y
                    y = cur_root
                    cur_root = temp
                # 让结点 y 加入结点 cur_root 的孩子链表
                self._fib_heap_link(cur_root, y)
                # 让 d_arr[cur_d] 变为占位元素
                empty_node = Element(inf)
                d_arr[cur_d] = empty_node
                # 此时 cur_root 的度数增加了 1，所以要检查此新度数会不会又是重复的
                cur_d += 1
            # 循环处理完后，把 cur_root 加入数组 d_arr 相应的位置
            assert 0 <= cur_d < max_d
            d_arr[cur_d] = cur_root
            ptr = next_root

        # 外层 while 循环忽略了 self.min 结点，所以此时要对 self.min 结点做相同的处理
        cur_root = self.min
        assert isinstance(cur_root, Element)
        cur_d = cur_root.degree  # 当前结点的度数
        assert 0 <= cur_d < max_d

        # 若存在与当前根结点 cur_root 相同度数的结点 y，需要合并这两个结点
        while d_arr[cur_d].key != inf:
            y = d_arr[cur_d]  # 取出此结点 y，让它加入 cur_root 的孩子链表
            assert isinstance(y, Element)
            # 如果原本在 trace 数组里的结点 y 的关键字 key 更小，则交换 cur_root 和 y
            if y.key < cur_root.key:
                temp = y
                y = cur_root
                cur_root = temp
            # 让结点 y 加入结点 cur_root 的孩子链表
            self._fib_heap_link(cur_root, y)
            # 让 d_arr[cur_d] 变为占位元素
            empty_node = Element(inf)
            d_arr[cur_d] = empty_node
            # 此时 cur_root 的度数增加了 1，所以要检查此新度数会不会又是重复的
            cur_d += 1
        # 循环处理完后，把 cur_root 加入数组 d_arr 相应的位置
        assert 0 <= cur_d < max_d
        d_arr[cur_d] = cur_root

        # 最后，对处理好后的 d_arr 进行遍历
        self.min = None
        for i in range(max_d):
            if isinstance(d_arr[i], Element) and d_arr[i].key != inf:
                # 如果 d_arr[i] 不是占位元素，则将之插入到根链表
                new_root = d_arr[i]
                if isinstance(self.min, Element):
                    # 如果此时 self.min 存在，则将 d_arr[i] 结点插入根链表
                    new_root.right = self.min.right
                    self.min.right.left = new_root
                    new_root.left = self.min
                    self.min.right = new_root
                    # 并视情况更新 self.min
                    if new_root.key < self.min.key:
                        self.min = new_root
                else:
                    # 如果此时 self.min 为空，则创建一个仅含 d_arr[i] 结点的根链表
                    new_root.left = new_root.right = new_root
                    new_root.parent = None
                    self.min = new_root

    # 辅助函数：让结点 y 加入结点 cur_root 的孩子链表
    def _fib_heap_link(self, cur_root, y):
        assert isinstance(y, Element) and isinstance(cur_root, Element)
        assert self.n >= 2 and y.right != y  # 此时根链表至少有两个结点
        # 1. 将结点 y 从根链表中移除
        y.right.left = y.left
        y.left.right = y.right

        # 2. 让 y 加入 cur_root 的孩子链表，并增加 cur_root 的度数
        if isinstance(cur_root.child, Element):
            # 如果 cur_root 已有孩子结点，则正常插入
            y.parent = cur_root
            y.right = cur_root.child.right
            cur_root.child.right.left = y
            y.left = cur_root.child
            cur_root.child.right = y
        else:
            # 否则让 y 成为 cur_root 的唯一孩子结点
            cur_root.child = y
            y.parent = cur_root
            y.left = y.right = y
        cur_root.degree += 1

        # 3. 重置结点 y 的 mark 标志为 False (此时没有失去孩子)
        y.mark = False

    '''如下为 2 个斐波那契堆可以额外完成的操作'''

    # 减小某结点的关键字 key
    # (摊还)时间复杂度 O(1)
    # 操作成功则返回 True，否则返回 False
    def fib_heap_decrease_key(self, x, new_k):
        if isinstance(x, Element):
            if x.key < new_k:
                # 只能降 key，不能升 key
                return False
            elif x.key == new_k:
                # 已满足目标
                return True
            else:
                x.key = new_k
                # 如果父结点存在，则观察是否需要维护最小堆性质
                y = x.parent
                if isinstance(y, Element) and x.key < y.key:
                    # 结点 x 比其父结点 y 的关键字 key 更小，需要维护最小堆性质
                    self._cut(x, y)  # 从 y 中移除 x，并将 x 加入根链表
                    self._cascading_cut(y)  # y 失去了孩子 x，进行处理
                # 视情况更新 self.min
                if x.key < self.min.key:
                    self.min = x
                return True
        else:
            return False

    # 辅助函数：切断 x 与其父结点 y 的关联，并将 x 加入根链表
    def _cut(self, x, y):
        assert isinstance(x, Element) and isinstance(y, Element)
        # 1. 将 x 从其父结点 y 的孩子链表中移除，并减小 y 的度数
        if x == x.right:
            # 如果 x 是 y 的唯一孩子
            assert x == x.left and y.child == x
            y.child = None
        else:
            # 如果 x 不是 y 的唯一孩子，则正常移除 x
            x.right.left = x.left
            x.left.right = x.right
            # 如果 y 的 child 指针当前指向了 x，则要更换 child 指针的指向
            if y.child == x:
                y.child = x.right
        y.degree -= 1

        # 2. 把 x 加入到根链表中
        assert isinstance(self.min, Element)
        x.right = self.min.right
        self.min.right.left = x
        x.left = self.min
        self.min.right = x

        # 3. 修改 x 的父指针、重置 mark 标记
        x.parent = None
        x.mark = False

    # 辅助函数：
    def _cascading_cut(self, y):
        assert isinstance(y, Element)
        z = y.parent
        # 如果 y 的父结点不是空，表示 y 不是根结点
        if isinstance(z, Element):
            if not y.mark:
                # 如果此前 y 没有失去过孩子，则此时记录 y 失去过孩子
                # 因为 _cascading_cut 函数调用前 执行了 _cut 函数
                y.mark = True
            else:
                # 继续向上处理：
                # 先调用 _cut 函数：从 z 中移除 y，并将 y 移至根链表
                self._cut(y, z)
                # 然后递归调用 _cascading_cut 函数，处理父结点 z
                self._cascading_cut(z)

    # 删除某结点
    # 假定在斐波那契堆中任何关键字的当前值均大于 -inf 负无穷
    # 则删除操作仅需调用之前实现好的两个操作
    # 删除成功则返回被删除的结点，否则返回 None
    # (摊还)时间复杂度 O(log n)
    def fib_heap_delete(self, x):
        neg_inf = -0x3f3f3f3f
        if isinstance(x, Element) and x.key > neg_inf:
            # 1. 把待删除结点的关键字 key 降到负无穷 -inf，从而成为了 self.min
            if self.fib_heap_decrease_key(x, neg_inf):
                # 2. 如果降 key 成功，则把最小值抽取出来
                return self.fib_heap_extract_min()
            else:
                return None
        else:
            return None


class Dijkstra:
    def __init__(self):
        self.inf = 0x3f3f3f3f - 1  # 所有结点的 distance 初始化为 inf
        # 注意这里的 inf 无穷要小于 斐波那契堆 fib_heap_extract_min 中的 inf

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
    def do_dijkstra(self, adj_l, source_v, weight_func=lambda x: x):
        assert isinstance(adj_l, AdjacencyList) and isinstance(source_v, VertexList)
        # 1. 对所有结点的 d 值和 p 值进行初始化
        self.initialize_single_source(adj_l, source_v)

        # 2. 将集合 S 初始化为一个空集
        # s_set = []

        # 3. (利用斐波那契堆)创建最小优先队列 Q 并将 V 中全部结点入队
        min_pri_q = FibonacciHeap(kv_list=None)
        v2ele = dict({})  # 顶点的关键字到 Element 对象的映射
        for v in adj_l.vertices:
            assert isinstance(v, VertexList)
            # 每个结点在 Q 中的关键值 key 为其 distance 值
            new_ele = Element(key=v.distance, val=v)  # 封装为 Element 结构体
            v2ele[v.key] = new_ele
            min_pri_q.fib_heap_insert_ele(insert_ele=new_ele)

        # 4. 只要 Q 不空，则继续 while 循环
        while min_pri_q.min is not None:
            # 4.1. 取出 Q 中最小 d 值的结点 u
            u_ele = min_pri_q.fib_heap_extract_min()
            assert isinstance(u_ele, Element)
            u_vertex = u_ele.val
            assert isinstance(u_vertex, VertexList)
            # 4.2. 把结点 u 加入集合 S 中
            # s_set.append(u_vertex)
            # 4.3. 在 for 循环中，对于 u 的每个邻接结点 v，松弛边 (u, v)
            for edge in u_vertex.neighbor.values():
                # 先通过边中存储的的 from/to 关键字获取 u/v 顶点结构体
                assert isinstance(edge, Edge)
                assert edge.from_v in adj_l.key2index and edge.to_v in adj_l.key2index
                u = adj_l.vertices[adj_l.key2index[edge.from_v]]
                v = adj_l.vertices[adj_l.key2index[edge.to_v]]
                assert isinstance(u, VertexList) and isinstance(v, VertexList)
                # 对边 (u, v) 进行松弛操作
                # self.relax(u, v, weight_func)
                # 检查是否可以对从 s 到 v 的最短路径进行改善
                # 将 s->u 的最短路径距离 加上 u->v 的边权重值
                cur_dis = u.distance + weight_func(edge.weight)
                # cur_dis 与当前得到的 s->v 的最短路径估计 进行比较
                if cur_dis < v.distance:
                    # 如果前者更小，则更新估计值 v.d 并修改前驱结点 v.p
                    v.distance = cur_dis
                    v.p = u
                    # 最小优先队列 Q 执行 decrease_key 操作
                    assert v.key in v2ele
                    min_pri_q.fib_heap_decrease_key(v2ele[v.key], cur_dis)


def main():
    # 构造图同《CLRS》Chapter 24.3 的(带非负边权)有向图
    # 用于构造邻接表的顶点的 key/val 信息列表
    list_vertices_info = [
        ['s', 100], ['t', 200], ['x', 300], ['y', 400], ['z', 500]
    ]
    # 有向边的 from/to/weight/is_directed 信息列表
    # is_directed 为 True 表示此边为有向边，否则为无向边
    di_edges_info = [
        ['s', 't', 10, True], ['s', 'y', 5, True], ['t', 'y', 2, True],
        ['t', 'x', 1, True], ['y', 't', 3, True], ['y', 'x', 9, True],
        ['y', 'z', 2, True], ['x', 'z', 4, True], ['z', 'x', 6, True],
        ['z', 's', 7, True]
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

    # 执行 Dijkstra 算法
    # Shortest Path Tree root: s 	distance: 0
    # t 	distance: 8 	p: y
    # x 	distance: 9 	p: t
    # y 	distance: 5 	p: s
    # z 	distance: 7 	p: y
    start = time.process_time()
    dijkstra = Dijkstra()
    dijkstra.do_dijkstra(adj_l, source_v)
    end = time.process_time()

    # 输出结果
    adj_l.print_vertex_info()

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
