#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/graph_theory/shortest_path
@File    : johnson.py
@Author  : YuweiYin
@Date    : 2020-06-02
=================================================="""

import sys
import time
import math

"""
全源最短路径 All Pairs Shortest Path
适用于稀疏图的 Johnson 算法
基于 Dijkstra 和 Bellman-Ford 算法

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
    def __init__(self, key, val=None, distance=0, p=None, h=0):
        self.key = key            # 本顶点的关键字 key (通常为顶点序号、唯一标志符)
        self.val = val            # 本顶点的值元素 val (可自定义为任意对象，为结点附带的信息)
        '''如下为最短路径算法所需的属性'''
        self.distance = distance  # 从源结点到本结点的最短路径权重值
        self.p = p                # 本结点的前驱结点/最短路径树的父结点
        self.h = h                # 本结点用于 Johnson 算法的 h 属性

    # 类序列化输出方法
    def __str__(self):
        return 'Vertex key: ' + str(self.key)


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
        # max_d = int(math.log(self.n, phi))  # 最大度数的上界
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


# (带边权的)邻接矩阵的图结构，通常适合稠密图
# 输入顶点结构体列表、边结构体列表
class AdjacencyMatrix:
    def __init__(self, vertices, edges):
        assert isinstance(vertices, list)

        self.inf = 0x3f3f3f3f - 1    # 初始各边的权重值均为 inf 无穷
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


class BellmanFord:
    def __init__(self):
        self.inf = 0x3f3f3f3f - 1  # 所有结点的 distance 初始化为 inf

    # 初始化每个结点的 distance 和 p 属性
    def initialize_single_source(self, adj_m, source_v):
        assert isinstance(adj_m, AdjacencyMatrix) and isinstance(source_v, VertexMatrix)
        for v in adj_m.vertices:
            assert isinstance(v, VertexMatrix)
            v.distance = self.inf
            v.p = None
        source_v.distance = 0

    # 对边 (u, v) 进行松弛操作
    @staticmethod
    def relax(adj_m, u, v, weight_func=lambda x: x):
        assert isinstance(adj_m, AdjacencyMatrix)
        assert isinstance(u, VertexMatrix) and isinstance(v, VertexMatrix)
        # 获取边 (u, v)
        assert u.key in adj_m.key2v_index and v.key in adj_m.key2v_index
        assert (u.key, v.key) in adj_m.key2e_index
        edge_index = adj_m.key2e_index[(u.key, v.key)]
        edge = adj_m.edges[edge_index]
        assert isinstance(edge, Edge)
        # 检查是否可以对从 s 到 v 的最短路径进行改善
        # 将 s->u 的最短路径距离 加上 u->v 的边权重值
        cur_dis = u.distance + weight_func(edge.weight)
        # cur_dis 与当前得到的 s->v 的最短路径估计 进行比较
        if cur_dis < v.distance:
            # 如果前者更小，则更新估计值 v.d 并修改前驱结点 v.p
            v.distance = cur_dis
            v.p = u

    # 寻找图 adj_m 从源结点 source_v 出发的单源最短路径
    # 这里默认图为邻接矩阵结构，weight_func 为恒等函数
    def do_bf(self, adj_m, source_v, weight_func=lambda x: x):
        assert isinstance(adj_m, AdjacencyMatrix) and isinstance(source_v, VertexMatrix)
        # 1. 对所有结点的 d 值和 p 值进行初始化
        self.initialize_single_source(adj_m, source_v)

        # 2. 循环对图的每条边进行 |V| - 1 次松弛操作，完成各结点的 d、p 值计算
        for i in range(len(adj_m.vertices) - 1):
            # 对每条边进行操作
            for edge in adj_m.edges:
                # 先通过边中存储的的 from/to 关键字获取 u/v 顶点结构体
                assert isinstance(edge, Edge)
                assert edge.from_v in adj_m.key2v_index and edge.to_v in adj_m.key2v_index
                u = adj_m.vertices[adj_m.key2v_index[edge.from_v]]
                v = adj_m.vertices[adj_m.key2v_index[edge.to_v]]
                assert isinstance(u, VertexMatrix) and isinstance(v, VertexMatrix)
                # 进行松弛操作
                self.relax(adj_m, u, v, weight_func)

        # 3. 循环检查图中是否存在负权环，如果有则返回 False
        for edge in adj_m.edges:
            # 先通过边中存储的的 from/to 关键字获取 u/v 顶点结构体
            assert isinstance(edge, Edge)
            assert edge.from_v in adj_m.key2v_index and edge.to_v in adj_m.key2v_index
            u = adj_m.vertices[adj_m.key2v_index[edge.from_v]]
            v = adj_m.vertices[adj_m.key2v_index[edge.to_v]]
            assert isinstance(u, VertexMatrix) and isinstance(v, VertexMatrix)
            # 检测负权环
            if u.distance + weight_func(edge.weight) < v.distance:
                return False

        # 4. 前面已经检测不到负权环了，所以返回 True 表示没有负权环
        return True


class Dijkstra:
    def __init__(self):
        self.inf = 0x3f3f3f3f - 1  # 所有结点的 distance 初始化为 inf
        # 注意这里的 inf 无穷要小于 斐波那契堆 fib_heap_extract_min 中的 inf

    # 初始化每个结点的 distance 和 p 属性
    def initialize_single_source(self, adj_m, source_v):
        assert isinstance(adj_m, AdjacencyMatrix) and isinstance(source_v, VertexMatrix)
        for v in adj_m.vertices:
            assert isinstance(v, VertexMatrix)
            v.distance = self.inf
            v.p = None
        source_v.distance = 0

    # 对边 (u, v) 进行松弛操作
    @staticmethod
    def relax(adj_m, u, v, weight_func=lambda x: x):
        assert isinstance(adj_m, AdjacencyMatrix)
        assert isinstance(u, VertexMatrix) and isinstance(v, VertexMatrix)
        # 获取边 (u, v)
        assert u.key in adj_m.key2v_index and v.key in adj_m.key2v_index
        assert (u.key, v.key) in adj_m.key2e_index
        edge_index = adj_m.key2e_index[(u.key, v.key)]
        edge = adj_m.edges[edge_index]
        assert isinstance(edge, Edge)
        # 检查是否可以对从 s 到 v 的最短路径进行改善
        # 将 s->u 的最短路径距离 加上 u->v 的边权重值
        cur_dis = u.distance + weight_func(edge.weight)
        # cur_dis 与当前得到的 s->v 的最短路径估计 进行比较
        if cur_dis < v.distance:
            # 如果前者更小，则更新估计值 v.d 并修改前驱结点 v.p
            v.distance = cur_dis
            v.p = u

    # 寻找图 adj_m 从源结点 source_v 出发的单源最短路径
    # 这里默认图为邻接矩阵结构，weight_func 为恒等函数
    def do_dijkstra(self, adj_m, source_v, weight_func=lambda x: x):
        assert isinstance(adj_m, AdjacencyMatrix) and isinstance(source_v, VertexMatrix)
        # 1. 对所有结点的 d 值和 p 值进行初始化
        self.initialize_single_source(adj_m, source_v)

        # 2. 将集合 S 初始化为一个空集
        # s_set = []

        # 3. (利用斐波那契堆)创建最小优先队列 Q 并将 V 中全部结点入队
        min_pri_q = FibonacciHeap(kv_list=None)
        v2ele = dict({})  # 顶点的关键字到 Element 对象的映射
        for v in adj_m.vertices:
            assert isinstance(v, VertexMatrix)
            # 每个结点在 Q 中的关键值 key 为其 distance 值
            new_ele = Element(key=v.distance, val=v)  # 封装为 Element 结构体
            v2ele[v.key] = new_ele
            min_pri_q.fib_heap_insert_ele(insert_ele=new_ele)

        # 4. 只要 Q 不空，则继续 while 循环
        while min_pri_q.min is not None:
            # 4.1. 取出 Q 中最小 d 值的结点 u
            u_ele = min_pri_q.fib_heap_extract_min()
            assert isinstance(u_ele, Element)
            u_node = u_ele.val
            assert isinstance(u_node, VertexMatrix) and u_node.key in adj_m.key2v_index
            u_index = adj_m.key2v_index[u_node.key]
            # 4.2. 把结点 u 加入集合 S 中
            # s_set.append(u_vertex)
            # 4.3. 在 for 循环中，对于 u 的每个邻接结点 v，松弛边 (u, v)
            for v_index, edge_weight in enumerate(adj_m.adj_m[u_index]):
                # 如果此边权为 inf，则此边不存在，考虑下一个结点下标
                if edge_weight >= self.inf:
                    continue
                # 如果边存在，获取终点 v
                v_node = adj_m.vertices[v_index]
                assert isinstance(v_node, VertexMatrix)
                # 通过起点和终点获取边 Edge 结构体
                assert (u_node.key, v_node.key) in adj_m.key2e_index
                cur_edge_index = adj_m.key2e_index[(u_node.key, v_node.key)]
                cur_edge = adj_m.edges[cur_edge_index]
                assert isinstance(cur_edge, Edge)
                # 对边 (u, v) 进行松弛操作
                # self.relax(adj_m, u_node, v_node, weight_func)
                # 检查是否可以对从 s 到 v 的最短路径进行改善
                # 将 s->u 的最短路径距离 加上 u->v 的边权重值
                cur_dis = u_node.distance + weight_func(cur_edge.weight)
                # cur_dis 与当前得到的 s->v 的最短路径估计 进行比较
                if cur_dis < v_node.distance:
                    # 如果前者更小，则更新估计值 v.d 并修改前驱结点 v.p
                    v_node.distance = cur_dis
                    v_node.p = u_node
                    # 最小优先队列 Q 执行 decrease_key 操作
                    assert v_node.key in v2ele
                    min_pri_q.fib_heap_decrease_key(v2ele[v_node.key], cur_dis)


class Johnson:
    def __init__(self):
        self.inf = 0x3f3f3f3f - 1  # 所有结点的 distance 初始化为 inf

    # Johnson 全源最短路径算法
    # 寻找图 adj_m 的全源最短路径 (这里默认图为邻接矩阵结构)
    # 时间复杂度 \Theta(VE + V^2 log V)
    # 空间复杂度 \Theta(V^2)
    def do_johnson(self, adj_m):
        assert isinstance(adj_m, AdjacencyMatrix)

        # 1. 新增源结点 s，生成图 G'
        source_v_key = '__source__'  # 需保证不与其它结点的关键字相同
        source_v = VertexMatrix(key=source_v_key)
        new_vertices = [source_v]
        new_edges = []
        for v in adj_m.vertices:
            new_vertices.append(v)
            new_edges.append(Edge(from_v=source_v.key, to_v=v.key, weight=0, is_directed=True))
        for edge in adj_m.edges:
            new_edges.append(edge)
        # 创建新的邻接矩阵 G'
        new_adj_m = AdjacencyMatrix(new_vertices, new_edges)

        # 2. 在图 G' 上运行 Bellman-Ford 算法，使用原始权重函数 w，计算从源结点 s 出发的单源最短路径
        # 设置源结点
        assert source_v_key in new_adj_m.key2v_index
        source_v = new_adj_m.vertices[new_adj_m.key2v_index[source_v_key]]
        # 执行 Bellman-Ford 算法
        bellman_ford = BellmanFord()
        no_neg_cycle = bellman_ford.do_bf(new_adj_m, source_v)

        # 3. 如果 Bellman-Ford 算法返回 False，表示图 G' 含负权环
        if not no_neg_cycle:
            print('The input graph contains a negative-weight cycle!')
            return None

        # 4. 对 V' 中每个结点 v，将 h(v) 的值设置为由 Bellman-Ford 算法所计算出来的最短路径权重 d(s, v)
        for v in new_adj_m.vertices:
            assert isinstance(v, VertexMatrix)
            v.h = v.distance

        # 5. 对 E' 中每条边 (u, v)，重新计算新的权重值 w'(u, v)
        for edge in new_adj_m.edges:
            assert isinstance(edge, Edge)
            # 获取边的端点 u 和 v
            assert edge.from_v in new_adj_m.key2v_index and edge.to_v in new_adj_m.key2v_index
            u_index = new_adj_m.key2v_index[edge.from_v]
            v_index = new_adj_m.key2v_index[edge.to_v]
            u_node = new_adj_m.vertices[u_index]
            v_node = new_adj_m.vertices[v_index]
            assert isinstance(u_node, VertexMatrix) and isinstance(v_node, VertexMatrix)
            edge.weight = edge.weight + u_node.h - v_node.h

        # 6. 设置权重矩阵 D
        n = len(adj_m.vertices)
        matrix_d = [[self.inf for _ in range(n)] for _ in range(n)]

        # 7. 对 V 中每个结点 u
        dijkstra = Dijkstra()
        for u_index, u_node in enumerate(adj_m.vertices):
            # 以 u 为起点、w' 为新的权重函数来运行 Dijkstra 算法
            dijkstra.do_dijkstra(adj_m, u_node)
            # 每次 Dijkstra 算法结束后，对 V 中每个结点 v，还原出最优路径值，并保存在 `d_uv` 表项中
            for v_index, v_node in enumerate(adj_m.vertices):
                matrix_d[u_index][v_index] = v_node.distance + v_node.h - u_node.h
        # 8. 返回最终计算好的全源最短路径权重矩阵 D
        return matrix_d

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

    # 辅助函数：打印矩阵
    @staticmethod
    def print_matrix(matrix):
        assert isinstance(matrix, list)
        for row in matrix:
            print(row)


def main():
    # 构造图同《CLRS》图 25-6 的(带边权)有向图 用于计算全源最短路径
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

    # 执行 \Theta(VE + V^2 log V) Johnson 全源最短路径算法
    johnson = Johnson()
    start = time.process_time()
    matrix_d = johnson.do_johnson(adj_m)
    end = time.process_time()

    # 输出结果 & 运行时间
    # [0, 1, -3, 2, -4]
    # [3, 0, -4, 1, -1]
    # [7, 4, 0, 5, 3]
    # [2, -1, -5, 0, -2]
    # [8, 5, 1, 6, 0]
    print('\nmatrix_d:')
    johnson.print_matrix(matrix_d)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
