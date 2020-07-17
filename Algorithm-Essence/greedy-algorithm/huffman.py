#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/greedy_algorithm
@File    : huffman.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
哈夫曼编码 Huffman

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 16
"""


# 字符结构体(哈夫曼树结点)
class Character:
    def __init__(self, ch='', freq=0):
        self.ch = ch        # 本字符未经编码的值
        self.freq = freq    # 本字符出现的频率
        self.left = None    # 左孩子
        self.right = None   # 右孩子
        self.parent = None  # 父结点


class Huffman:
    def __init__(self, char_list):
        assert isinstance(char_list, list) and len(char_list) > 0

        # 确保 char_list 中每个元素都是 Character 结构体
        # 并通过 char_list 构造用于最小优先队列的 Element 结构体数组
        ele_list = []
        for ch in char_list:
            assert isinstance(ch, Character)
            ele_list.append(Element(key=ch.freq, val=ch))

        self.c_num = len(ele_list)  # 含有的原字符总数
        self.h_root = None          # 哈夫曼树的根结点
        self.heap = Heap(ele_list)  # 建立最小优先队列(最小二叉堆)
        self.prefix_code = []       # 根据哈夫曼树 左 0 右 1 解析每个字符的前缀码

    # 哈夫曼编码 Huffman Code
    # 返回：哈夫曼树的根结点
    def huffman_code(self):
        # 自顶向下递归实现 (贪心算法) \Theta(n)
        # self._huffman_code_recursive(0, n)
        # 循环实现 (贪心算法) \Theta(n)
        self._huffman_code_iteration()
        return self.h_root

    # 循环实现 (贪心算法)
    # 时间复杂度 \Theta(n)
    # 空间复杂度 \Theta(1)
    def _huffman_code_iteration(self):
        # 字符表 char_list 的长度
        n = self.c_num

        # n 个字符，则需要处理 n-1 次合并操作，产生 n-1 个内部结点
        for i in range(n - 1):
            # 创建新结点 (内部结点)
            new_char = Character()
            # 取出两个最小元素 Element，其 val 为 Character 结构体
            left_ele = self.heap.extract_min()
            right_ele = self.heap.extract_min()
            assert isinstance(left_ele, Element) and isinstance(right_ele, Element)
            assert isinstance(left_ele.val, Character) and isinstance(right_ele.val, Character)
            # 链接父子结点指针
            new_char.left = left_ele.val
            new_char.right = right_ele.val
            left_ele.val.parent = new_char
            right_ele.val.parent = new_char
            # 新结点的 freq 属性为其左右孩子 freq 之和
            new_char.freq = left_ele.val.freq + right_ele.val.freq
            new_ele = Element(key=new_char.freq, val=new_char)
            # 将新结点封装为 Element 对象，并插入最小优先队列中
            self.heap.min_heap_insert(new_ele)
        # 最小优先队列中最后唯一剩下的结点就是树根
        h_root_ele = self.heap.extract_min()
        assert isinstance(h_root_ele, Element)
        self.h_root = h_root_ele.val

    # 获取哈夫曼树的根结点
    def get_huffman_root(self):
        return self.h_root

    # 根据哈夫曼树 左 0 右 1 解析每个字符的前缀码
    def set_prefix_code(self):
        if isinstance(self.h_root, Character):
            self._set_prefix_code(self.h_root, '')
        else:
            self.prefix_code = []

    # 深度优先搜索，叶结点是具体字符
    def _set_prefix_code(self, root, prefix):
        assert isinstance(root, Character) and isinstance(prefix, str)
        # 有左孩子则往左搜索
        if isinstance(root.left, Character):
            prefix += '0'
            self._set_prefix_code(root.left, prefix)
            prefix = prefix[: -1]
        # 有右孩子则往右搜索
        if isinstance(root.right, Character):
            prefix += '1'
            self._set_prefix_code(root.right, prefix)
            prefix = prefix[: -1]
        # 叶结点，写入前缀码
        if not isinstance(root.left, Character) and not isinstance(root.right, Character):
            self.prefix_code.append((root.ch, prefix))

    # 获取每个字符的前缀码
    def get_prefix_code(self):
        return self.prefix_code


# 元素结构体 key-value 键值对
class Element:
    def __init__(self, key, val=None):
        self.key = key  # (必备) 关键字 key。这里把字符的出现频率作为 key
        self.val = val  # (可选) 值对象 val。这里把字符对象作为 val


# (最小)二叉堆 Min-Heap 数据结构
class Heap:
    # 构造最小堆
    # 时间复杂度 O(n)
    def __init__(self, min_ele_list):
        assert isinstance(min_ele_list, list)
        self.min_ele_list = min_ele_list  # min_ele_list 用于构建最小堆
        self.verify_element()

        neg_inf = -0x3f3f3f3f
        min_none_node = Element(neg_inf)
        self.min_ele_list.insert(0, min_none_node)  # 堆首占位空元素，方便下标计算
        self.min_heap_size = len(self.min_ele_list) - 1  # 实际堆长度比 min_ele_list 少一

        self.build_min_heap()  # 构造最小堆

    # 确保 ele_list 中每个元素都是 Element 元素结构体
    # 如果某元素不是 Element 结构体，则将之从 ele_list 中剔除出去
    def verify_element(self):
        for index, ele in enumerate(self.min_ele_list):
            if not isinstance(ele, Element):
                self.min_ele_list.pop(index)

    # 构建最小堆。时间复杂度为 O(n)。
    # 类似于构建最大堆的过程。自底向上构造最小堆，并利用 _min_heapify 维护最小堆性质
    def build_min_heap(self):
        self.min_heap_size = len(self.min_ele_list) - 1  # 实际堆长度比 min_ele_list 少一
        # 中间结点从下标 (n>>1) 开始，到 1
        leaf_start_index = (self.min_heap_size >> 1) + 1  # 叶结点在 min_ele_list 中的起始下标
        for index in reversed(range(1, leaf_start_index)):
            self._min_heapify(index)

    # 维护最小堆性质。时间复杂度为 O(log n)
    # def _min_heapify(self, root_index):
    #     if root_index <= 0 or root_index > self.min_heap_size:
    #         print('_min_heapify: Error Path. root_index:', root_index)
    #     else:
    #         left_index = self._left(root_index)
    #         right_index = self._right(root_index)
    #         root_ele = self.min_ele_list[root_index]
    #         assert isinstance(root_ele, Element)
    #
    #         # 从当前结点、左孩子、右孩子三者中找出 key 最小者的下标
    #         if left_index <= self.min_heap_size and \
    #                 self.min_ele_list[left_index].key < root_ele.key:
    #             smallest = left_index
    #         else:
    #             smallest = root_index
    #         if right_index <= self.min_heap_size and \
    #                 self.min_ele_list[right_index].key < self.min_ele_list[smallest].key:
    #             smallest = right_index
    #
    #         # 如果当前结点不是最小者，则把最小者交换上来
    #         if smallest != root_index:
    #             self._min_exchange(root_index, smallest)
    #             self._max_heapify(smallest)  # 继续往下调整

    # 循环结构的 min_heapify
    def _min_heapify(self, root_index):
        if root_index <= 0 or root_index > self.min_heap_size:
            print('_min_heapify: Error Path. root_index:', root_index)
        else:
            left_index = self._left(root_index)
            right_index = self._right(root_index)
            root_ele = self.min_ele_list[root_index]
            assert isinstance(root_ele, Element)

            while left_index <= self.min_heap_size or right_index <= self.min_heap_size:
                # 从当前结点、左孩子、右孩子三者中找出 key 最小者的下标
                if left_index <= self.min_heap_size and \
                        self.min_ele_list[left_index].key < root_ele.key:
                    smallest = left_index
                else:
                    smallest = root_index
                if right_index <= self.min_heap_size and \
                        self.min_ele_list[right_index].key < self.min_ele_list[smallest].key:
                    smallest = right_index

                # 如果当前结点不是最小者，则把最小者交换上来
                if smallest != root_index:
                    self._min_exchange(root_index, smallest)
                    # 修改下标，往下移动，准备下一轮循环
                    root_index = smallest
                    left_index = self._left(root_index)
                    right_index = self._right(root_index)
                else:
                    break

    # 下面四个操作利用最小堆实现最小优先队列。前提：已建立最小堆

    # 获取 key 最小的元素
    # 操作失败则返回 None
    # 时间复杂度：O(1)
    def get_minimum(self):
        # 最小堆的最小 key 的元素是 index=1 元素
        if 0 < self.min_heap_size and isinstance(self.min_ele_list[1], Element):
            return self.min_ele_list[1]  # O(1)
        else:
            return None

    # 获取并移除 key 最小的元素
    # 操作失败则返回 None
    # 时间复杂度：O(log n)
    def extract_min(self):
        if self.min_heap_size < 1:
            print('extract_min: 最小堆已空, 无法提取最小元素')
            return None
        elif self.min_heap_size == 1:
            self.min_heap_size -= 1
            return self.min_ele_list.pop(1)
        else:
            min_ele = self.min_ele_list[1]  # 取出最小元素后需要更换堆根
            # self.min_ele_list[1] = self.min_ele_list[self.min_heap_size]
            self.min_ele_list[1] = self.min_ele_list.pop(self.min_heap_size)
            self.min_heap_size -= 1
            self._min_heapify(1)  # 维护最小堆性质 O(log n)
            return min_ele

    # 将最小堆 min_ele_list 中的第 index 个元素的键 key 减小为 new_key
    # 操作成功则返回布尔值 True；操作失败则返回布尔值 False
    # 时间复杂度：O(log n)
    def decrease_key(self, index, new_key):
        if 0 < index <= self.min_heap_size and isinstance(self.min_ele_list[index], Element):
            cur_ele = self.min_ele_list[index]
            if new_key > cur_ele.key:
                print('decrease_key: 无法降低 key，因为新 key=', new_key, '大于当前 key=', cur_ele.key)
                return False
            else:
                # 修改目标元素的 key 值，并逐级往上维护最小堆性质
                self.min_ele_list[index].key = new_key
                while index > 1:
                    parent_ele = self.min_ele_list[self._parent(index)]
                    assert isinstance(parent_ele, Element)
                    if parent_ele.key > cur_ele.key:
                        # 如果 index 结点的父结点 key 大于 index 结点的 key，那么需要把 index 结点替换上去
                        self._min_exchange(index, self._parent(index))
                        index = self._parent(index)  # index 上移
                    else:
                        break
                return True
        else:
            # 下标越界或者该元素非 Element 结构体，则 decrease_key 操作失败
            print('decrease_key: 下标越界或者该元素非 Element 结构体，decrease_key 操作失败')
            return False

    # 往最小堆中插入新元素 (Element 结构体)
    # 插入成功则返回布尔值 True；插入失败则返回布尔值 False
    # 时间复杂度：O(log n)
    def min_heap_insert(self, new_ele):
        if isinstance(new_ele, Element):
            # 先在 ele_list 末尾插入一个 key 为正无穷 inf 的元素（注意 val 设置）
            inf = 0x3f3f3f3f
            inf_node = Element(inf, new_ele.val)
            self.min_ele_list.append(inf_node)
            self.min_heap_size += 1

            # 然后再利用 decrease_key 方法将此元素的 key 减小
            if self.decrease_key(self.min_heap_size, new_ele.key):
                # 如果 decrease_key 成功，则返回 True，插入成功
                return True
            else:
                # 如果 decrease_key 失败，则把末尾增添的 inf_node 删掉，并返回 False，插入失败
                print('_min_heap_insert: decrease_key 失败')
                self.min_ele_list.pop()
                self.min_heap_size -= 1
                return False
        else:
            print('min_heap_insert: 插入失败，待插入元素非 Element 结构体')
            return False

    # 辅助函数：计算父结点下标 O(1)
    @staticmethod
    def _parent(index):
        return index >> 1

    # 辅助函数：计算左孩子下标 O(1)
    @staticmethod
    def _left(index):
        return index << 1

    # 辅助函数：计算右孩子下标 O(1)
    @staticmethod
    def _right(index):
        return (index << 1) + 1

    # 辅助函数：交换 min_ele_list 中两个下标的元素 O(1)
    def _min_exchange(self, i, j):
        assert 0 < i <= self.min_heap_size and 0 < j <= self.min_heap_size
        temp = self.min_ele_list[i]
        self.min_ele_list[i] = self.min_ele_list[j]
        self.min_ele_list[j] = temp

    # 获取最小堆元素列表。去掉用于占位的首位元素
    def get_min_ele_list(self):
        return self.min_ele_list[1: 1 + self.min_heap_size]

    # 获取最小堆元素中 key 的列表。去掉用于占位的首位元素
    def get_min_key_list(self):
        key_list = []
        for ele in self.min_ele_list[1: 1 + self.min_heap_size]:
            if isinstance(ele, Element):
                key_list.append(ele.key)
            else:
                pass
        return key_list

    # 获取最小堆元素中 val 的列表。去掉用于占位的首位元素
    def get_min_val_list(self):
        val_list = []
        for ele in self.min_ele_list[1: 1 + self.min_heap_size]:
            if isinstance(ele, Element):
                val_list.append(ele.val)
            else:
                pass
        return val_list

    # 整体替换数组，重构最小堆
    # 时间复杂度 O(n)
    def update_min_ele_list(self, new_min_ele_list):
        self.__init__(new_min_ele_list)


def main():
    # char_array 中的每个元素为二元元组，tuple[0] 为字符的值、tuple[1] 为字符的出现频率
    char_array = [
        ('a', 45), ('b', 13), ('c', 12), ('d', 16), ('e', 9), ('f', 5)
    ]

    # 通过 char_array 构造 Character 数组
    char_list = []
    for ch in char_array:
        char_list.append(Character(ch=ch[0], freq=ch[1]))

    huffman = Huffman(char_list)

    # 建立哈夫曼树
    start = time.process_time()
    # h_root = huffman.huffman_code()
    huffman.huffman_code()
    end = time.process_time()

    # 根据建立好的哈夫曼树获取各个字符的前缀码
    # [('a', '0'), ('c', '100'), ('b', '101'), ('f', '1100'), ('e', '1101'), ('d', '111')]
    huffman.set_prefix_code()
    print(huffman.get_prefix_code())

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
