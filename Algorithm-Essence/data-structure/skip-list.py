#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : skip-list.py
@Author  : YuweiYin
=================================================="""

# import gc
import sys
import time
import random

"""
跳表 Skip List

参考资料：
https://www.youtube.com/watch?v=2g9OSRKJuzM
"""


# 非循环多域双向链表
class ListNode:
    def __init__(self, key=0, val=None, level=1):
        self.key = key      # 键，按键构造链表
        self.val = val      # 值，结点存储的值，可以为任意对象
        self.pre = []       # 指向前一个结点的指针数组，n 级结点有 n 个 pre。头尾结点最多
        self.next = []      # 指向下一个结点的指针数组，n 级结点有 n 个 next。头尾结点最多
        self.level = level  # 当前结点所在的层级，最低为 1
        # 搜索时先搜索高层级的索引结点，找不到再逐级下降。如果在最低层都找不到，就表示搜索不到


class SkipList:
    # 构造 Skip List 即：具备多级索引结构的链表
    # 时间复杂度 O(n) ? O(n log n) ?
    def __init__(self, kv_array):
        self.tail = ListNode(0x3f3f3f3f)   # 链表尾结点, key 为 inf。这里考虑升序排列链表
        self.head = ListNode(-0x3f3f3f3f)  # 链表头结点, key 为 -inf
        self.node_list = []                # 除头结点外，从首至尾的元素 ListNode 列表
        self.max_level = 0x3f3f3f3f        # 允许的最多层级数
        self.cur_max_level = 1             # 当前所有结点的最大层级数

        self.head.pre.append(None)
        self.head.next.append(self.tail)   # 链表头结点指向尾结点
        self.tail.pre.append(self.head)
        self.tail.next.append(None)  # 链表尾结点指向 None

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 ListNode 并插入 SkipList，保持有序
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.skip_list_insert(kv[0], kv[1], 2)
            # 遍历，更新从首至尾的元素 ListNode 列表
            self.update_node_list()

    # 遍历，更新从首至尾的元素 ListNode 列表
    def update_node_list(self):
        self.node_list = []
        ptr = self.head
        level = 0
        while isinstance(ptr.next[level], ListNode) and \
                ptr.next[level] != self.tail:
            ptr = ptr.next[level]
            self.node_list.append(ptr)

    # 获取从首至尾的元素 ListNode 列表
    def get_node_list(self):
        return self.node_list

    # 获取从首至尾的元素 key 列表
    def get_key_list(self):
        return [node.key for node in self.node_list]

    # Skip List 根据 key 值搜索结点
    # 时间复杂度 O(log n) 与层数有关
    def skip_list_search(self, search_key):
        ptr = self.head  # 从 key 值为 -inf 的链表头结点开始查找
        for level in reversed(range(self.cur_max_level)):
            while isinstance(ptr.next[level], ListNode) and \
                    ptr.next[level].key <= search_key:  # 尾结点 key 为 inf，其 next 均为 None
                # 如果下一个元素的 key 不大于目标 key，则在当前 level 查找
                if ptr.next[level].key == search_key:
                    # 找到了目标 key
                    return ptr.next[level]
                elif ptr.next[level].key < search_key:
                    # 如果下一个元素的 key 小于目标 key，则在当前 level 右移
                    ptr = ptr.next[level]
                else:
                    # 跳出内循环，降低 level 继续搜索
                    break
        if isinstance(ptr, ListNode) and ptr.key == search_key:
            return ptr
        else:
            print('skip_list_search: 找不到 key=', search_key, '的元素')
            return None

    # 辅助操作：新建并返回具有随机层数的结点
    def create_new_node(self, new_key, new_val):
        new_node = ListNode(new_key, new_val)
        random.seed(id(new_node))  # 以新结点对象的唯一标识符 id 作为随机数种子
        new_level = 1
        while random.random() > 0.5:  # 50% 的几率增加一个 level
            new_level += 1
            # 检测是否更新当前最大层数
            if new_level > self.cur_max_level:
                if new_level > self.max_level:
                    # 不能超过预设的最高层数 inf
                    new_level = self.max_level
                    break
                self.cur_max_level = new_level
                # 当前策略：为了避免层数过高，如果更新了最大层数，则不再提升新结点的层数
                # 并且把 Skip List 首尾结点的 level 提升
                self.head.level += 1
                self.tail.level += 1
                self.head.pre.append(None)
                self.head.next.append(self.tail)
                self.tail.pre.append(self.head)
                self.tail.next.append(None)
                # break  # 也可以不加此限制，去掉这个 break，让 level 仅因概率决定
        # 设置新结点的层级并返回新结点
        new_node.level = new_level
        new_node.pre = [None] * new_level
        new_node.next = [None] * new_level
        return new_node

    # Skip List 按 key 插入新结点，并给出 value
    # 时间复杂度 O(log n) 与层数有关
    def skip_list_insert(self, insert_key, insert_val, insert_type=2):
        if insert_type == 1:
            self._skip_list_insert_1(insert_key, insert_val)
        elif insert_type == 2:
            self._skip_list_insert_2(insert_key, insert_val)
        else:
            print('skip_list_insert: Error insert_type=', insert_type)

    # 插入策略 1：逐层插入 时间复杂度 O(n)，对新结点的每个 level 找到其应插入的位置
    def _skip_list_insert_1(self, insert_key, insert_val):
        new_node = self.create_new_node(insert_key, insert_val)
        for level in reversed(range(new_node.level)):
            ptr = self.head
            while isinstance(ptr.next[level], ListNode) and \
                    ptr.next[level].key < new_node.key:  # 尾结点 key 为 inf，其 next 均为 None
                # 如果下一个元素的 key 小于新结点 key，则在当前 level 继续往右搜索
                ptr = ptr.next[level]
            # 此时 ptr 下一个结点的 key 大于等于新结点 key，将新结点插入 ptr 后
            new_node.next[level] = ptr.next[level]
            new_node.pre[level] = ptr
            if isinstance(ptr.next[level], ListNode):
                ptr.next[level].pre[level] = new_node
            ptr.next[level] = new_node
            # 进入下层循环，考虑下一 level 的插入

    # 插入策略 2：利用跳表的 search 策略快速定位每层的插入点
    def _skip_list_insert_2(self, insert_key, insert_val):
        new_node = self.create_new_node(insert_key, insert_val)
        for level in reversed(range(new_node.level)):
            ptr = self.head
            # 这里看似多了一层循环，实则加速了链表查找。
            # 在第 n 层的定位时，利用了已经建立好的 >n 层的索引结点，而不是每层逐元素定位
            for built_level in reversed(range(level, new_node.level)):
                while isinstance(ptr.next[built_level], ListNode) and \
                        ptr.next[built_level].key < new_node.key:  # 尾结点 key 为 inf，其 next 均为 None
                    # 如果下一个元素的 key 小于新结点 key，则在当前 level 继续往右搜索
                    ptr = ptr.next[built_level]
            # 此时 ptr 下一个结点的 key 大于等于新结点 key，将新结点插入 ptr 后
            new_node.next[level] = ptr.next[level]
            new_node.pre[level] = ptr
            if isinstance(ptr.next[level], ListNode):
                ptr.next[level].pre[level] = new_node
            ptr.next[level] = new_node
            # 进入下层循环，考虑下一 level 的插入

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def clear_node_link(node):
        if isinstance(node, ListNode):
            for level in range(node.level):
                node.pre[level] = None
                node.next[level] = None

    # Skip List 根据 key 值删除结点，并返回被删除的结点
    # TODO 可考虑在删除最后一个当前层数最高的结点后，降低总的 cur_max_level
    # 时间复杂度 O(log n) 与层数有关
    def skip_list_delete(self, delete_key):
        ptr = self.head  # 从 key 值为 -inf 的链表头结点开始查找
        for level in reversed(range(self.cur_max_level)):
            while isinstance(ptr.next[level], ListNode) and \
                    ptr.next[level].key <= delete_key:  # 尾结点 key 为 inf，其 next 均为 None
                # 如果下一个元素的 key 不大于目标 key，则在当前 level 查找
                if ptr.next[level].key == delete_key:
                    # 找到了目标 key，从当前层开始向下，把目标结点的所有层的前后结点连接起来
                    return self._skip_list_delete(ptr.next[level])
                elif ptr.next[level].key < delete_key:
                    # 如果下一个元素的 key 小于目标 key，则在当前 level 右移
                    ptr = ptr.next[level]
                else:
                    # 跳出内循环，降低 level 继续搜索
                    break
        if isinstance(ptr, ListNode) and ptr.key == delete_key:
            return self._skip_list_delete(ptr)
        else:
            print('skip_list_delete: 找不到 key=', delete_key, '的元素')
            return None

    def _skip_list_delete(self, node):
        if isinstance(node, ListNode):
            for level in range(node.level):
                if isinstance(node.next[level], ListNode) and \
                        isinstance(node.pre[level], ListNode):
                    node.next[level].pre[level] = node.pre[level]
                    node.pre[level].next[level] = node.next[level]
                elif isinstance(node.next[level], ListNode):
                    node.next[level].pre[level] = node.pre[level]
                elif isinstance(node.pre[level], ListNode):
                    node.pre[level].next[level] = node.next[level]
                else:
                    print('_skip_list_delete: node 不是 ListNode 对象')
            # 清除 node 结点的所有指针域
            self.clear_node_link(node)
            return node
        else:
            print('_skip_list_delete: node 不是 ListNode 对象')


# 随机打乱数组
class ShuffleArray:
    def __init__(self, array):
        self.array = array

    def do_shuffle(self):
        if isinstance(self.array, list) and len(self.array) > 1:
            # 从最高的 index 开始降到 1，每次生成 0～index-1 的随机数，与 index=index 的元素交换
            for i in reversed(range(1, len(self.array))):
                self._exchange(i, self._get_random_int(i - 1))
        else:
            print('The so-called array is NOT a list!')

    # 按下标生成随机数
    def _get_random_int(self, index):
        random.seed(id(self.array[index]))  # 以对象的唯一标识符 id 作为随机数种子
        return random.randint(0, index)     # 生成 0～index 的整型随机数

    # 按下标交换 self.array 中的两个元素
    def _exchange(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp


def main():
    # 以插入的方式，构建 BST/RBT
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    kv_array = [
        [1, 10], [2, 20], [3, 30], [7, 70], [8, 80], [9, 90], [4, 40]
    ]

    # 对于 1000 个元素的 list，对比升序/降序输入、插入策略1/2、生成新结点 level 是否限制，
    # 这三种情况组合下建立 Skip List 的平均耗时
    # 218.73500 ms - 升序 and 插入策略 1 and 生成新结点 level 要限制
    # 154.99300 ms - 升序 and 插入策略 2 and 生成新结点 level 要限制
    # 223.29000 ms - 升序 and 插入策略 1 and 生成新结点 level 不限制
    # 157.48100 ms - 升序 and 插入策略 2 and 生成新结点 level 不限制
    # 13.77600 ms - 降序 and 插入策略 1 and 生成新结点 level 要限制
    # 15.14900 ms - 降序 and 插入策略 2 and 生成新结点 level 要限制
    # 15.01300 ms - 降序 and 插入策略 1 and 生成新结点 level 不限制
    # 14.95700 ms - 降序 and 插入策略 2 and 生成新结点 level 不限制
    # kv_array = [[i, 100 * i] for i in range(1000)]
    # kv_array = [[i, 100 * i] for i in reversed(range(1000))]
    # 可以发现：如果需要让 Skip List 的元素升序排列，则输入是降序比升序好，因为这样每次都插入在头结点后面即可
    # 插入策略 2 会利用之前已经件好的索引结点，因此在数据量大的时候优于插入策略 1，不过在数据量小的时候稍弱一些
    # 对生成新结点的 level 进行限制，不让索引一次性增长太多，会比不限制稍好一点；但不限制会使得高索引结点增多，相对有助于搜索
    # 最佳组合：数据降序输入、使用插入策略 2，生成新结点可考虑不限制 (利于搜索)

    # 对于 1000 个元素的 list，随机打乱输入顺序之后，
    # 前述最佳组合在原本升序输入情况的耗时从 150+ ms 降到了约 90 ms
    # 在原本降序输入情况的耗时从约 15 ms 升到了约 80 ms
    # shuffle_kv_array = ShuffleArray(kv_array)
    # start = time.process_time()
    # shuffle_kv_array.do_shuffle()
    # end = time.process_time()
    # print('随机打乱 List 耗时: %.5f ms' % ((end - start) * 1000))  # 约 10 ms
    # print(shuffle_kv_array.array)

    # 对于 1000 个元素的 list，降序排列后，建立跳表约 14 ms （最佳处理方式）
    # 注意：如果跳表的设计是元素降序排列，那么原始输入的 list 需要升序排列，才能迅速插入
    start = time.process_time()
    sorted_kv_array = sorted(kv_array, key=lambda x: x[0], reverse=True)
    end = time.process_time()
    print('降序排序 List 耗时: %.5f ms' % ((end - start) * 1000))  # 约 0.3 ms

    # 建立 Skip List
    start = time.process_time()
    # skip_list = SkipList(kv_array)
    # skip_list = SkipList(shuffle_kv_array.array)
    skip_list = SkipList(sorted_kv_array)
    end = time.process_time()
    print('建立 Skip List 耗时: %.5f ms' % ((end - start) * 1000))

    # 输出升序排序的结果
    # print(skip_list.get_key_list())  # [1, 2, 3, 4, 7, 8, 9]

    # 搜索值
    search_key = 4
    start = time.process_time()
    ans = skip_list.skip_list_search(search_key)
    end = time.process_time()

    if ans is not None and isinstance(ans, ListNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')

    print('查找一个元素耗时: %.5f ms' % ((end - start) * 1000))

    # 删除结点，预期结果如下：
    # 找不到 key= 17  的结点
    # [1, 2, 3, 4, 7, 8]
    # [1, 2, 4, 7, 8]
    # [1, 2, 4, 8]
    # [1, 2, 4]
    # [1, 4]
    # [4]
    # []
    # 找不到 key= 3  的结点
    delete_key_list = [17, 9, 3, 7, 8, 2, 1, 4, 3]
    for delete_key in delete_key_list:
        deleted_node = skip_list.skip_list_delete(delete_key)
        if isinstance(deleted_node, ListNode):
            # print('删除了 key=', deleted_node.key, ' val=', deleted_node.val, ' 的结点')
            # print('删除了 key=', deleted_node.key, ' 的结点')
            skip_list.update_node_list()
            print(skip_list.get_key_list())
        else:
            print('找不到 key=', delete_key, ' 的结点')

    # 删空之后测试查找。预期如下：
    # 提示：搜索时，Splay Tree 为空，无法找到目标元素。
    # 找不到 key= 4 的元素
    search_key = 4
    ans = skip_list.skip_list_search(search_key)  # 找不到
    if ans is not None and isinstance(ans, ListNode):
        print('找到了 key=', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key=', search_key, '的元素')

    # 重新动态增加（降序测试）
    for key in reversed(range(1, 10)):
        val = key * 100
        skip_list.skip_list_insert(key, val)
        skip_list.update_node_list()
        print(skip_list.get_key_list())

    # 再次测试查找。预期如下：
    # 找到了 key= 4 的元素，其值为: 400
    search_key = 4
    ans = skip_list.skip_list_search(search_key)
    if ans is not None and isinstance(ans, ListNode):
        print('找到了 key=', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key=', search_key, '的元素')


if __name__ == "__main__":
    sys.exit(main())
