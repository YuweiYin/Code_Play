#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : fibonacci-heap.py
@Author  : YuweiYin
@Date    : 2020-05-22
=================================================="""

import sys
import time
import math

"""
斐波那契堆 Fibonacci Heap

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 19
"""


# 元素结构体
class Element:
    def __init__(self, key, val=None):
        self.key = key      # (必备) 关键字 key。按 key 排序，因此 key 必须具有全序关系 (常为整数)
        self.val = val      # (可选) 值对象 val。可为任意对象
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
                union_heap.n += h2.n
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
                # 然后将此孩子链表链接到 H 的根链表。孩子的孩子结点则不改动
                z.child.right = z.right
                z.right.left = z.child
                z.child.left = z
                z.right = z.child
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
        max_d = int(math.log(self.n, phi))  # 最大度数的上界

        # 创建长度为 max_d 的辅助数据 d_arr
        # 如果 d_arr 中某结点关键字 key 为 inf，则表示仅为占位结点
        inf = 0x3f3f3f3f
        d_arr = []
        for i in range(max_d):
            empty_node = Element(inf)
            d_arr.append(empty_node)

        # 循环处理根链表中的每个根结点 cur_root
        # cur_root 可能会被链接到别的结点上，从而不再位于根链表中，也就不再是一个根结点
        ptr = self.min
        assert isinstance(ptr, Element)  # 进入 _consolidate 前已保证本斐波那契堆不是空堆，故有此断言
        while ptr.right != self.min:
            ptr = ptr.right

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
                d_arr[cur_d].key = inf
                # 此时 cur_root 的度数增加了 1，所以要检查此新度数会不会又是重复的
                cur_d += 1
            # 循环处理完后，把 cur_root 加入数组 d_arr 相应的位置
            assert 0 <= cur_d < max_d
            d_arr[cur_d] = cur_root

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
            d_arr[cur_d].key = inf
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


def main():
    # 键值对列表
    kv_list = [
        [3, 301], [4, 100], [5, 200], [8, 800],
        [7, 700], [9, 900], [3, 300]
    ]

    # 建立斐波那契(最小)堆
    start = time.process_time()
    fib_heap = FibonacciHeap(kv_list)
    end = time.process_time()

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 查询最小结点
    fib_heap_min = fib_heap.fib_heap_minimum()
    if isinstance(fib_heap_min, Element):
        print(fib_heap_min.key, fib_heap_min.val)  # 3, 301
    else:
        print('No Minimum Found.')


if __name__ == "__main__":
    sys.exit(main())
