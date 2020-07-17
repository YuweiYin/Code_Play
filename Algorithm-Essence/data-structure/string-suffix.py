#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : string-suffix.py
@Author  : YuweiYin
=================================================="""

import sys
import time

"""
后缀树 Suffix Tree & 广义后缀树 Generalized Suffix Tree
后缀树线性时间构造方法: Ukkonen (Ukk)在线算法 / McCreight (Mcc)算法
"""


# 后缀树的树结点
class SuffixTreeNode:
    def __init__(self, str_range, is_suffix=False):
        self.str_range = str_range  # tuple(i, j)，表示当前结点的值是原串 [i:j] 的子串
        self.is_suffix = is_suffix  # True 则表示当前结点是后缀串的结束结点
        self.children = dict({})    # 孩子结点(指针)字典，dict[str] 是边的子串值


# 后缀树
class SuffixTree:
    def __init__(self, suffix_str):
        assert isinstance(suffix_str, str)
        # 后缀树串
        self.suffix_str = suffix_str
        # 后缀树的根结点 (不存储具体的字符，但可以匹配空串)
        suf_len = len(suffix_str)
        self.st_root = SuffixTreeNode(str_range=(suf_len, suf_len), is_suffix=True)
        # 用于记录子串出现次数的类成员变量
        self.counter = 0

        # 将 suffix_str 拆为各个后缀子串，插入构建普通的后缀树
        for i in range(suf_len):
            self.suffix_tree_insert(i, suf_len)

        # 压缩(已经建立好的)普通后缀树
        self.compress_trie()

    # 以普通的字典树插入方法，插入后缀串(始末下标)到后缀树中
    def suffix_tree_insert(self, str_start, str_end):
        ptr = self.st_root  # 当前结点指针
        # 逐个匹配当前结点的孩子，如果当前结点不存在 suffix_str[i: i+1] 孩子，则构造之
        for i in range(str_start, str_end):
            # 如果当前结点存在 suffix_str[i: i+1] 孩子，则往下继续搜索
            if self.suffix_str[i] in ptr.children:
                ptr = ptr.children[self.suffix_str[i]]
            # 否则构造 suffix_str[i: i+1] 孩子
            else:
                new_node = SuffixTreeNode(str_range=(i, i + 1), is_suffix=False)  # 创建孩子
                ptr.children[self.suffix_str[i]] = new_node  # 链接孩子
                ptr = new_node  # 往下搜索

        # 处理最后一个字符，设置当前结点的 is_suffix 标志为 True，表示这是后缀结尾
        ptr.is_suffix = True

    # 压缩(已经建立好的)普通后缀树
    def compress_trie(self):
        # 深度优先搜索
        # 如果树中的某一段路径里是这样的：除了该路径的最后一个结点(不一定是叶结点)，其余结点的孩子个数(度数)均为 1
        # 则可将此路径压缩为单个结点
        # 根结点不压缩。对根结点的每个孩子进行处理
        keys = list(self.st_root.children.keys())[:]
        for key in keys:
            ptr = self.st_root.children[key]
            ptr_p = self.st_root
            self._compress_trie(ptr, ptr_p)
        return True

    # 从 root_p 的孩子结点 root 出发，把可压缩的结点均压缩为一个结点，并链接成为 root_p 的孩子
    def _compress_trie(self, root, root_p):
        assert isinstance(root, SuffixTreeNode) and isinstance(root_p, SuffixTreeNode)
        # 记录 root 与 root_p 的边 key
        root_range = root.str_range
        child_key = self.suffix_str[root_range[0]: root_range[1]]
        assert child_key in root_p.children
        ptr = root
        start_index = ptr.str_range[0]  # 记录起始位置
        while len(ptr.children) <= 1:
            end_index = ptr.str_range[1]  # 更新结束位置
            # 处理到了叶结点，如果它不是 root_p 的孩子，那么可压缩此叶结点，否则不压缩
            if len(ptr.children) == 0:
                if ptr != root_p.children[child_key]:
                    root_p.children.pop(child_key)
                    ptr.str_range = (start_index, end_index)
                    root_p.children[self.suffix_str[start_index: end_index]] = ptr
                # 处理完叶结点，即可退出函数
                return
            # 处理度数为 1 的内部结点
            else:
                # # 如果此结点是一个后缀尾，则先压缩到此结点，然后递归调用往下压缩
                # if ptr.is_suffix:
                #     root_p.children.pop(child_key)
                #     ptr.str_range = (start_index, end_index)
                #     root_p.children[self.suffix_str[start_index: end_index]] = ptr
                #     # 递归调用往下压缩
                #     keys = list(ptr.children.keys())[:]
                #     for key in keys:
                #         self._compress_trie(ptr.children[key], ptr)
                #     # 递归处理结束后，即可返回
                #     return
                # # 否则此结点不是后缀尾，则继续往下搜索
                # else:
                #     kv = ptr.children.popitem()
                #     del ptr
                #     # 移至孩子结点
                #     ptr = kv[1]
                # 考虑 ptr 的唯一孩子的情况
                keys = list(ptr.children.keys())[:]
                assert len(keys) == 1
                ptr_kid = ptr.children[keys[0]]
                assert isinstance(ptr_kid, SuffixTreeNode)
                # 如果 ptr 的孩子结点的度数 >= 2，则之后会跳出循环，此时需先压缩至 ptr
                if len(ptr_kid.children) >= 2:
                    # 若 ptr 不是 root_p 的孩子，则可压缩 ptr 结点
                    # 处理完 ptr 结点后，下个 while 判断会跳出循环
                    if ptr != root_p.children[child_key]:
                        root_p.children.pop(child_key)
                        ptr.str_range = (start_index, end_index)
                        root_p.children[self.suffix_str[start_index: end_index]] = ptr
                # 否则 ptr 的孩子结点的度数 <= 1，下一次 while 判断不会跳出循环
                else:
                    # 如果此结点是一个后缀尾，则先压缩到此结点，然后递归调用往下压缩
                    if ptr.is_suffix:
                        root_p.children.pop(child_key)
                        ptr.str_range = (start_index, end_index)
                        root_p.children[self.suffix_str[start_index: end_index]] = ptr
                        # 递归调用往下压缩
                        keys = list(ptr.children.keys())[:]
                        for key in keys:
                            self._compress_trie(ptr.children[key], ptr)
                        # 递归处理结束后，即可返回
                        return
                    # 否则，此结点的孩子结点还能被压缩，因此删除 ptr，继续往下搜索可压缩结点
                    else:
                        del ptr
                # 移至孩子结点
                ptr = ptr_kid

        # 如果出了 while 循环到了此处，当然 ptr 所指结点必定拥有至少 2 个孩子结点，分别递归处理
        assert len(ptr.children) > 1
        keys = list(ptr.children.keys())[:]
        for key in keys:
            self._compress_trie(ptr.children[key], ptr)

    # 检查 query_str 是否为后缀树串 suffix_str 的子串
    # 如果 query_str 在字符串 suffix_str 中，那么 query_str 必定是 suffix_str 中某个后缀串的前缀
    def check_substring(self, query_str):
        return self._check_substring(self.st_root, query_str)

    def _check_substring(self, root, query_str):
        assert isinstance(query_str, str)
        q_len = len(query_str)
        if q_len == 0:
            return True
        # 从当前根结点出发，遍历所有孩子结点
        ptr = root
        # 对所有孩子 (边的 key 串)，若存在首字符匹配，则进入此孩子结点
        for key in ptr.children:
            assert isinstance(key, str) and len(key) > 0
            # 匹配首字符
            if key[0] == query_str[0]:
                # 如果 key 长度不少于 query_str，则看是否能够完全匹配 query_str
                if len(key) >= q_len:
                    if key[:q_len] == query_str:
                        return True
                    else:
                        return False
                # 如果 key 长度少于 query_str，则看 query_str 的部分是否能够匹配 key
                else:
                    # 如果能够匹配，则递归处理 query_str 未被匹配的剩余部分
                    if key == query_str[: len(key)]:
                        return self._check_substring(ptr.children[key], query_str[len(key):])
                    # 否则匹配失败
                    else:
                        return False

        # 如果所有孩子 (边的 key 串) 的首字符都和 query_str 的首字符不匹配，则不存在 query_str 子串
        return False

    # 求 query_str 在后缀树串 suffix_str 中的出现次数
    # 只需计算 query_str 是 suffix_str 的多少个后缀串的前缀
    # 即后缀树中 query_str 的匹配结点 之下(包括匹配结点)的 is_suffix == True 结点数目
    def count_repetition(self, query_str):
        assert isinstance(query_str, str)
        q_len = len(query_str)
        # 默认空串出现次数为 0
        if q_len == 0:
            return 0
        # 获得匹配成功的结点
        match_node = self._find_match_node(self.st_root, query_str)
        # 以匹配成功的结点为根，递归遍历此子树，计算 is_suffix == True 结点数目(包括匹配结点)
        if isinstance(match_node, SuffixTreeNode):
            self.counter = 0
            self._count_repetition(match_node)
            return self.counter
        # 不匹配此串，所以 query_str 的出现次数为 0
        else:
            return 0

    def _find_match_node(self, root, query_str):
        assert isinstance(query_str, str)
        q_len = len(query_str)
        assert q_len > 0
        # 从当前根结点出发，遍历所有孩子结点
        ptr = root
        # 对所有孩子 (边的 key 串)，若存在首字符匹配，则进入此孩子结点
        for key in ptr.children:
            assert isinstance(key, str) and len(key) > 0
            # 匹配首字符
            if key[0] == query_str[0]:
                # 如果 key 长度不少于 query_str，则看是否能够完全匹配 query_str
                if len(key) >= q_len:
                    if key[:q_len] == query_str:
                        return ptr.children[key]
                    else:
                        return None
                # 如果 key 长度少于 query_str，则看 query_str 的部分是否能够匹配 key
                else:
                    # 如果能够匹配，则递归处理 query_str 未被匹配的剩余部分
                    if key == query_str[: len(key)]:
                        return self._find_match_node(ptr.children[key], query_str[len(key):])
                    # 否则匹配失败
                    else:
                        return None

        # 如果所有孩子 (边的 key 串) 的首字符都和 query_str 的首字符不匹配，则不存在 query_str 子串
        return None

    def _count_repetition(self, root):
        assert isinstance(root, SuffixTreeNode)
        if root.is_suffix:
            self.counter += 1
        for key in root.children:
            self._count_repetition(root.children[key])


# 用 Ukkonen 算法快速构建的后缀树的树结点
class UkkSuffixTreeNode:
    def __init__(self, str_range, parent=None):
        self.str_range = str_range  # tuple(lo, hi)，表示当前结点的值是原串 [lo: hi] 的子串
        self.parent = parent        # 本结点的父结点 (只有根结点的 parent 指针为 None)
        self.children = dict({})    # 孩子结点(指针)字典，dict[(lo, hi)] 是边的子串值 str[lo: hi] 左闭右开
        # 若孩子为叶结点，则 hi 为 -1，表示判断 hi 时应该索引 Ukk 算法的尾指针 self.end_index 随着 Ukk 算法进行而增加

    def __str__(self):
        return str(self.str_range)


# 用 Ukkonen 算法快速构建的后缀树
class UkkSuffixTree:
    def __init__(self, suffix_str):
        assert isinstance(suffix_str, str)
        # 后缀树串
        self.suffix_str = suffix_str
        # 后缀树的根结点 (不存储具体的字符，但可以匹配空串)
        suf_len = len(suffix_str)
        self.st_root = UkkSuffixTreeNode(str_range=(suf_len, suf_len))
        # 当前读取的字符数目。对于叶结点，str_range[1] == -1 表示该右界 应该索引 self.end_index
        self.end_index = 0
        # 用于记录子串出现次数的类成员变量
        self.counter = 0

        # 后缀树的(在线)线性构造算法：Ukkonen 算法(Ukk) / McCreight 算法 (Mcc)
        self.ukkonen_build_tree(suffix_str)

    # (压缩的)后缀树的(在线)线性构造算法：Ukkonen 算法
    def ukkonen_build_tree(self, suf_str):
        # 这里通过一个个输入 suf_str 中的字符 来模拟在线输入情况
        assert isinstance(suf_str, str)
        suf_len = len(suf_str)
        remain_start = 0  # 待插入后缀的起始位置
        for remain_end in range(1, suf_len + 1):  # remain_end: 待插入后缀的终止位置
            remain_start = self._ukkonen_build_tree(
                self.st_root, remain_start, remain_end)  # 每次先从根结点插入
        self.end_index = suf_len

    def _ukkonen_build_tree(self, root, remain_start, remain_end, inner_call=False):
        ptr = root

        # 取出当前的各边 str_range
        keys = list(ptr.children.keys())[:]

        # 查看当前各个待插入的后缀 是否为当前(边)子串的前缀
        start = remain_start
        # 从长串到短串依次处理
        while start < remain_end:
            remain_str = self.suffix_str[start: remain_end]
            remain_len = len(remain_str)

            # 如果 ptr 是叶结点，则只需构造新结点插入到当前 root
            if len(ptr.children) == 0:
                new_node = UkkSuffixTreeNode(str_range=(start, -1), parent=ptr)
                ptr.children[(start, -1)] = new_node
                # self.remain_start 加一，表示该位置起始的后缀串已经被插入了
                remain_start += 1
                start += 1
                continue

            # 记录与当前待插入串 remain_str 匹配字符树最多的那个 key 边，即出现 mismatch 时下标最大
            longest_mismatch_key = keys[0]
            longest_mismatch_key_index = 0  # 最大的 key 在 keys 列表中的下标
            longest_mismatch_index = 0
            done_flag = False  # True 则表示当前 remain_str 已经处理完了
            for key_index, key in enumerate(keys):
                # 先将 key (str_range) 映射为具体的子串 str_key
                if key[1] == -1:
                    str_key = self.suffix_str[key[0]: remain_end]
                else:
                    str_key = self.suffix_str[key[0]: key[1]]
                # 然后再检查当前待插入的后缀 remain_str 是否为当前(边)子串 str_key 的前缀
                # 若待插入串不比边子串长 (通常情况)
                if remain_len <= len(str_key):
                    # 若是前缀，则无需插入 remain_str，保持当前 remain_start 不变，处理下个后缀
                    if remain_str == str_key[: remain_len]:
                        # 由于从较长的后缀开始处理的，一旦前面保持不变，后面也要保持不变
                        # 例如 abc 已经是当前树的边子串的前缀了，那么 bc 和 c 也一定会如此
                        return remain_start
                    # 否则，检测首个不匹配处
                    else:
                        # 循环找到不匹配的下标位置
                        mismatch_index = 0
                        while mismatch_index < remain_len and \
                                remain_str[mismatch_index] == str_key[mismatch_index]:
                            mismatch_index += 1
                        # 更新最大的不匹配下标位置
                        if mismatch_index > longest_mismatch_index:
                            longest_mismatch_index = mismatch_index
                            longest_mismatch_key_index = key_index
                            longest_mismatch_key = key
                # 若待插入串比边子串长
                else:
                    # print('len(', remain_str, ') > len(', str_key, ')')
                    # 若二者前面部分 均匹配，且此 key 边对应的孩子 kid 不是叶结点，则往下递归处理剩余未匹配部分
                    if remain_str[: len(str_key)] == str_key:
                        kid = ptr.children[key]
                        assert isinstance(kid, UkkSuffixTreeNode)
                        # 判断 key 边对应的孩子 kid 不是叶结点
                        if len(kid.children) > 0:
                            # 往下递归处理剩余未匹配部分，inner_call=True 表明是内部递归调用，while 循环只会执行一次
                            self._ukkonen_build_tree(kid, start + len(str_key), remain_end, inner_call=True)
                            done_flag = True
                            break

            # for 循环结束后，如果当前 remain_str 尚未处理，则处理之
            if not done_flag:
                # 如果首个位置就不匹配，则无需分裂，只需通过 remain_str 构造新结点插入到当前 root
                if longest_mismatch_index == 0:
                    new_node = UkkSuffixTreeNode(str_range=(start, -1), parent=ptr)
                    ptr.children[(start, -1)] = new_node
                # 如果中途不匹配，则从不匹配位置开始分裂 (新建一个中间结点、一个叶结点，修改原孩子)
                else:
                    # 弹出原孩子、修改其边 key
                    origin_child = ptr.children.pop(longest_mismatch_key)
                    assert isinstance(origin_child, UkkSuffixTreeNode)
                    origin_str_range_0, origin_str_range_1 = origin_child.str_range[0], origin_child.str_range[1]
                    origin_child.str_range = (origin_str_range_0 + longest_mismatch_index, origin_str_range_1)

                    # 增添新的中间结点
                    mid_key = (origin_str_range_0, origin_str_range_0 + longest_mismatch_index)
                    mid_kid = UkkSuffixTreeNode(str_range=mid_key, parent=ptr)
                    ptr.children[mid_key] = mid_kid

                    # 增添新叶结点
                    new_leaf_key = (start + longest_mismatch_index, -1)
                    new_leaf = UkkSuffixTreeNode(str_range=new_leaf_key, parent=mid_kid)
                    # 链接孩子
                    origin_child.parent = mid_kid
                    mid_kid.children[origin_child.str_range] = origin_child
                    mid_kid.children[new_leaf_key] = new_leaf
                    # 更新 keys 列表
                    keys.pop(longest_mismatch_key_index)
                    keys.append(mid_key)
                # remain_start 加一，表示该位置起始的后缀串已经被插入了
                remain_start += 1

            # inner_call = True 内部递归调用 则只处理一次
            if inner_call:
                break

            # while 循环变量 start 加一，表示接下来处理更短的后缀
            start += 1

        # while 循环处理结束后，返回下一次处理(读入新字符)的起始位置 remain_start
        return remain_start


# 广义后缀树的树结点
class GeneralizedSuffixTreeNode:
    def __init__(self, node_val, num_ends=0):
        self.node_val = node_val  # 结点存储的子串值，与连结父结点的边值相同
        self.end_char = set({})   # index in end_char 表示当前结点是 index 号后缀串的结束结点
        self.children = dict({})  # 孩子结点(指针)字典，dict[str] 是边的子串值
        self.num_ends = num_ends  # 以本结点为根的子树中 含有的不同终结符数目


# 广义后缀树 (用多个字符串构成一棵后缀树，每个串的终结字符不同)
class GeneralizedSuffixTree:
    def __init__(self, suffix_str_list):
        assert isinstance(suffix_str_list, list)
        # 后缀树串列表 (隐式增添结束符，index 号后缀串的结束字符就是 index，会存储在树结点的 end_char 集合中)
        self.suf_str_list = suffix_str_list
        # 后缀树的根结点 (不存储具体的字符)
        self.st_root = GeneralizedSuffixTreeNode(node_val='')
        # 用于记录子串出现次数的类成员变量
        self.counter = 0
        # 用于记录构建后缀树的所有字符串的最长公共子串
        self.max_sub = ''  # 当前最长公共子串

        # 后缀树的(在线)线性构造算法：Ukkonen 算法 (Ukk) / TODO McCreight 算法 (Mcc)
        # 对 suffix_str_list 的每个 suffix_str 进行处理
        for index, suffix_str in enumerate(suffix_str_list):
            assert isinstance(suffix_str, str)
            # 将 suffix_str 拆为各个后缀子串，插入构建普通的广义后缀树
            for start_i in range(len(suffix_str)):
                self.g_suffix_tree_insert(suffix_str[start_i:], index)

        # 压缩(已经建立好的)普通广义后缀树
        self.g_compress_trie()

        # 计算出 以每个结点为根的子树中 含有的不同终结符数目
        self.st_root.num_ends = len(suffix_str_list)  # 整棵树拥有所有的终结符
        self.g_compute_all_ends()

    # 以普通的字典树插入方法，插入 index 号后缀串(始末下标)到后缀树中，这些后缀串的结束字符均为 index
    def g_suffix_tree_insert(self, suffix_str, index):
        ptr = self.st_root  # 当前结点指针
        # 逐个匹配当前结点的孩子，如果当前结点不存在 suffix_str[i] 孩子，则构造之
        for char in suffix_str:
            # 如果当前结点存在 char 孩子，则往下继续搜索
            if char in ptr.children:
                ptr = ptr.children[char]
            # 否则构造 char 孩子
            else:
                new_node = GeneralizedSuffixTreeNode(node_val=char)  # 创建孩子
                ptr.children[char] = new_node  # 链接孩子
                ptr = new_node  # 往下搜索

        # 处理最后一个字符，将 index 加入集合 end_char 中，表示这是后缀结尾
        ptr.end_char.add(index)

    # 压缩(已经建立好的)普通后缀树
    def g_compress_trie(self):
        # 深度优先搜索
        # 如果树中的某一段路径里是这样的：除了该路径的最后一个结点(不一定是叶结点)，其余结点的孩子个数(度数)均为 1
        # 则可将此路径压缩为单个结点
        # 根结点不压缩。对根结点的每个孩子进行处理
        keys = list(self.st_root.children.keys())[:]
        for key in keys:
            ptr = self.st_root.children[key]
            ptr_p = self.st_root
            self._g_compress_trie(ptr, ptr_p)
        return True

    # 从 root_p 的孩子结点 root 出发，把可压缩的结点均压缩为一个结点，并链接成为 root_p 的孩子
    def _g_compress_trie(self, root, root_p):
        assert isinstance(root, GeneralizedSuffixTreeNode) and isinstance(root_p, GeneralizedSuffixTreeNode)
        # 记录 root 与 root_p 的边 key
        child_key = root.node_val
        assert child_key in root_p.children
        ptr = root
        new_key = ''  # 记录新的边/点 key 值
        while len(ptr.children) <= 1:
            new_key += ptr.node_val  # 更新边/点 key 值
            # 处理到了叶结点，如果它不是 root_p 的孩子，那么可压缩此叶结点，否则不压缩
            if len(ptr.children) == 0:
                if ptr != root_p.children[child_key]:
                    root_p.children.pop(child_key)
                    ptr.node_val = new_key
                    root_p.children[new_key] = ptr
                # 处理完叶结点，即可退出函数
                return
            # 处理度数为 1 的内部结点
            else:
                # 如果此结点是一个后缀尾，则先压缩到此结点，然后递归调用往下压缩
                if len(ptr.end_char) > 0:
                    # 若 ptr 不是 root_p 的孩子，则可压缩 ptr 结点
                    if ptr != root_p.children[child_key]:
                        root_p.children.pop(child_key)
                        ptr.node_val = new_key
                        root_p.children[new_key] = ptr
                    # 递归调用往下压缩
                    keys = list(ptr.children.keys())[:]
                    for key in keys:
                        self._g_compress_trie(ptr.children[key], ptr)
                    # 递归处理结束后，即可返回
                    return
                # 否则此结点不是后缀尾，则继续往下搜索
                else:
                    # 考虑 ptr 的唯一孩子的情况
                    keys = list(ptr.children.keys())[:]
                    assert len(keys) == 1
                    ptr_kid = ptr.children[keys[0]]
                    assert isinstance(ptr_kid, GeneralizedSuffixTreeNode)
                    # 如果 ptr 的孩子结点的度数 >= 2，则之后会跳出循环，此时需先压缩至 ptr
                    if len(ptr_kid.children) >= 2:
                        # 若 ptr 不是 root_p 的孩子，则可压缩 ptr 结点
                        # 处理完 ptr 结点后，下个 while 判断会跳出循环
                        if ptr != root_p.children[child_key]:
                            root_p.children.pop(child_key)
                            ptr.node_val = new_key
                            root_p.children[new_key] = ptr
                    # 否则删除 ptr，继续往下搜索可压缩结点，不会跳出循环
                    else:
                        del ptr
                    # 移至孩子结点
                    ptr = ptr_kid

        # 如果出了 while 循环到了此处，当然 ptr 所指结点必定拥有至少 2 个孩子结点，分别递归处理
        assert len(ptr.children) > 1
        keys = list(ptr.children.keys())[:]
        for key in keys:
            self._g_compress_trie(ptr.children[key], ptr)

    # 计算出 以每个结点为根的子树中 含有的不同终结符数目
    def g_compute_all_ends(self):
        for key in self.st_root.children:
            self._g_compute_all_ends(self.st_root.children[key])

    def _g_compute_all_ends(self, root):
        assert isinstance(root, GeneralizedSuffixTreeNode)
        # 如果当前结点有未曾出现的结束符，则加入 end_set 集合
        end_set = set({})
        for end_tag in root.end_char:
            if not (end_tag in end_set):
                end_set.add(end_tag)
        # 基本情况：到了叶结点
        if len(root.children) == 0:
            # 设置此叶结点的 num_ends
            root.num_ends = len(root.end_char)
        # 当前结点不是叶结点
        else:
            # 获取本结点所有子结点的结束符号集合 的并集
            for key in root.children:
                kid_end_set = self._g_compute_all_ends(root.children[key])
                # 求结束符的并集
                for end_tag in kid_end_set:
                    if not (end_tag in end_set):
                        end_set.add(end_tag)
            # 设置此非叶结点的 num_ends
            root.num_ends = len(end_set)
        # 返回结束符集合
        return end_set

    # 检查 query_str 是否为某个后缀树串 suffix_str 的子串
    # 如果 query_str 在某个字符串 suffix_str 中，那么 query_str 必定是某个 suffix_str 中某个后缀串的前缀
    def g_check_substring(self, query_str):
        return self._g_check_substring(self.st_root, query_str)

    def _g_check_substring(self, root, query_str):
        assert isinstance(query_str, str)
        q_len = len(query_str)
        if q_len == 0:
            return True
        # 从当前根结点出发，遍历所有孩子结点
        ptr = root
        # 对所有孩子 (边的 key 串)，若存在首字符匹配，则进入此孩子结点
        for key in ptr.children:
            assert isinstance(key, str) and len(key) > 0
            # 匹配首字符
            if key[0] == query_str[0]:
                # 如果 key 长度不少于 query_str，则看是否能够完全匹配 query_str
                if len(key) >= q_len:
                    if key[:q_len] == query_str:
                        return True
                    else:
                        return False
                # 如果 key 长度少于 query_str，则看 query_str 的部分是否能够匹配 key
                else:
                    # 如果能够匹配，则递归处理 query_str 未被匹配的剩余部分
                    if key == query_str[: len(key)]:
                        return self._g_check_substring(ptr.children[key], query_str[len(key):])
                    # 否则匹配失败
                    else:
                        return False

        # 如果所有孩子 (边的 key 串) 的首字符都和 query_str 的首字符不匹配，则不存在 query_str 子串
        return False

    # 求 query_str 在所有后缀树串 suffix_str 中的出现次数
    # 只需计算 query_str 是所有 suffix_str 的多少个后缀串的前缀
    # 即后缀树中 query_str 的匹配结点 之下(包括匹配结点)的各个 end_char 集合元素的总秩
    def g_count_repetition(self, query_str):
        assert isinstance(query_str, str)
        q_len = len(query_str)
        # 默认空串出现次数为 0
        if q_len == 0:
            return 0
        # 获得匹配成功的结点
        match_node = self._g_find_match_node(self.st_root, query_str)
        # 以匹配成功的结点为根，递归遍历此子树，计算各个 end_char 集合元素的总秩(包括匹配结点)
        if isinstance(match_node, GeneralizedSuffixTreeNode):
            self.counter = 0
            self._g_count_repetition(match_node)
            return self.counter
        # 不匹配此串，所以 query_str 的出现次数为 0
        else:
            return 0

    def _g_find_match_node(self, root, query_str):
        assert isinstance(query_str, str)
        q_len = len(query_str)
        assert q_len > 0
        # 从当前根结点出发，遍历所有孩子结点
        ptr = root
        # 对所有孩子 (边的 key 串)，若存在首字符匹配，则进入此孩子结点
        for key in ptr.children:
            assert isinstance(key, str) and len(key) > 0
            # 匹配首字符
            if key[0] == query_str[0]:
                # 如果 key 长度不少于 query_str，则看是否能够完全匹配 query_str
                if len(key) >= q_len:
                    if key[:q_len] == query_str:
                        return ptr.children[key]
                    else:
                        return None
                # 如果 key 长度少于 query_str，则看 query_str 的部分是否能够匹配 key
                else:
                    # 如果能够匹配，则递归处理 query_str 未被匹配的剩余部分
                    if key == query_str[: len(key)]:
                        return self._g_find_match_node(ptr.children[key], query_str[len(key):])
                    # 否则匹配失败
                    else:
                        return None

        # 如果所有孩子 (边的 key 串) 的首字符都和 query_str 的首字符不匹配，则不存在 query_str 子串
        return None

    def _g_count_repetition(self, root):
        assert isinstance(root, GeneralizedSuffixTreeNode)
        self.counter += len(root.end_char)
        for key in root.children:
            self._g_count_repetition(root.children[key])

    # 求构建后缀树的所有字符串的最长公共子串
    # 方法：找到最深的非叶结点 v，且以结点 v 为根的子树含有全部终结符。
    # 注意：这里的"最深"并不是指树深度最深，因为树被压缩了。目标是子串最长
    def longest_substring(self):
        self.max_sub = ''  # 最长公共子串
        # 在广义后缀树的构造函数中，已经计算出了 以每个结点为根的子树中 含有的不同终结符数目
        # 现只需记录 num_ends 等于全部终结符数量 的结点中的最深结点 对应的子串
        cur_sub = ''  # 处理过程中的临时子串
        self._longest_substring(self.st_root, cur_sub)  # 先序遍历
        return self.max_sub

    def _longest_substring(self, root, cur_sub):
        assert isinstance(root, GeneralizedSuffixTreeNode)
        assert 0 <= root.num_ends <= len(self.suf_str_list)
        # 如果以当前结点为根的子树 含有全部终结符，则先处理本结点，然后向下搜索
        # 否则，此子树的任何孩子结点都不可能含有全部终结符，结束搜索
        if root.num_ends == len(self.suf_str_list):
            # 先处理本结点，视"深度"更新 max_sub 最长公共子串
            if len(cur_sub) + len(root.node_val) > len(self.max_sub):
                self.max_sub = cur_sub + root.node_val
            # 向下继续搜索 (其孩子结点对应的子串肯定比当前子串长，但是不一定含有全部终结符)
            for key in root.children:
                self._longest_substring(root.children[key], cur_sub + root.node_val)

    # 求某个字符串的最长回文子串
    # 方法：以此字符串和其反转字符串 构建广义后缀树，然后寻找最长公共子串
    @staticmethod
    def longest_palindrome(pal_str):
        assert isinstance(pal_str, str)
        pal_str_r = pal_str[::-1]  # 逆序串
        g_suf_tree = GeneralizedSuffixTree(suffix_str_list=[pal_str, pal_str_r])
        return g_suf_tree.longest_substring()

    # TODO 计算最长重复子串：找到深度最深(子字符串最长)的非叶结点
    # TODO 计算最长公共前缀


def main():
    # Suffix Trie
    print('\nSuffix Trie:')
    # 用于构造后缀树的字符串
    suffix_str = "banana"
    # suffix_str = "abcabxabcd"
    # 用于匹配的模式串
    pattern_list = ["ant", "nan"]
    # 用于检测出现次数的子串
    count_list = ["ant", "nan", "na", "an", "a", "anan", ""]

    # 创建后缀树
    suffix_tree = SuffixTree(suffix_str)

    # 进行匹配
    start = time.process_time()
    ans_list = []
    for query_str in pattern_list:
        ans_list.append(suffix_tree.check_substring(query_str))
    end = time.process_time()

    # 查看结果 [False, True]
    print(ans_list)
    # 计算运行时间
    print('Suffix Tree - Search: Running Time: %.5f ms' % ((end - start) * 1000))

    # 进行子串出现次数检测
    start = time.process_time()
    ans_list = []
    for query_str in count_list:
        ans_list.append(suffix_tree.count_repetition(query_str))
    end = time.process_time()

    # 查看结果 [0, 1, 2, 2, 3, 1, 0]
    print(ans_list)
    # 计算运行时间
    print('Suffix Tree - Count Repetition: Running Time: %.5f ms' % ((end - start) * 1000))

    # Generalized Suffix Trie
    print('\nGeneralized Suffix Trie:')
    # 用于构造后缀树的字符串列表
    suffix_str_list = ["banana", "ant", "analysis"]
    # 用于匹配的模式串
    pattern_list = ["ant", "nan"]
    # 用于检测出现次数的子串
    count_list = ["ant", "nan", "na", "an", "a", "anan", ""]

    # 创建广义后缀树
    g_suffix_tree = GeneralizedSuffixTree(suffix_str_list)

    # 进行匹配
    start = time.process_time()
    ans_list = []
    for query_str in pattern_list:
        ans_list.append(g_suffix_tree.g_check_substring(query_str))
    end = time.process_time()

    # 查看结果 [True, True]
    print(ans_list)
    # 计算运行时间
    print('Generalized Suffix Tree - Search: Running Time: %.5f ms' % ((end - start) * 1000))

    # 进行子串出现次数检测
    start = time.process_time()
    ans_list = []
    for query_str in count_list:
        ans_list.append(g_suffix_tree.g_count_repetition(query_str))
    end = time.process_time()

    # 查看结果 [1, 1, 3, 4, 6, 1, 0]
    print(ans_list)
    # 计算运行时间
    print('Generalized Suffix Tree - Count Repetition: Running Time: %.5f ms' % ((end - start) * 1000))

    # 求构建后缀树的所有字符串的最长公共子串
    print(g_suffix_tree.longest_substring())  # "an"

    # 求某个字符串的最长回文子串
    # 方法：以此字符串和其反转字符串 构建广义后缀树，然后寻找最长公共子串
    pal_str = "banana"
    print(g_suffix_tree.longest_palindrome(pal_str))  # "anana"

    # 使用 Ukkonen 算法 (Ukk) 线性(在线)构造后缀树 / McCreight 算法 (Mcc)
    print('\nUkkonen Build Suffix Tree:')
    # 用于构造(狭义)后缀树的字符串
    suffix_str = "abcabxabcd"
    # 对比 "普通构造 + 压缩" 方法 与 Ukkonen 构造法的耗时
    start = time.process_time()
    normal_suffix_tree = SuffixTree(suffix_str)
    end = time.process_time()
    assert isinstance(normal_suffix_tree, SuffixTree)  # 此处可设断点查看 普通方法 构建出的后缀树形态
    print('Suffix Tree - Normal Build: Running Time: %.5f ms' % ((end - start) * 1000))  # 0.11700 ms

    start = time.process_time()
    ukk_suffix_tree = UkkSuffixTree(suffix_str)
    end = time.process_time()
    assert isinstance(ukk_suffix_tree, UkkSuffixTree)  # 此处可设断点查看 Ukk 算法 构建出的后缀树形态
    print('Suffix Tree - Ukkonen Build: Running Time: %.5f ms' % ((end - start) * 1000))  # 0.08400 ms


if __name__ == "__main__":
    sys.exit(main())
