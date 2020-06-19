#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : string-trie.py
@Author  : YuweiYin
@Date    : 2020-06-17
=================================================="""

import sys
import time

"""
Trie (Retrieve + Tree) 字典树 & 01 字典树
后缀树 Suffix Tree & 广义后缀树 Generalized Suffix Tree
"""


# Trie 字典树的树结点
class TrieNode:
    def __init__(self, char, is_word=False):
        self.char = char          # 当前结点存储的字符 (在本实现中此属性可不使用)
        self.is_word = is_word    # True 则表示当前字符可以是某个单词的结尾
        self.children = dict({})  # 孩子结点(指针)字典，dict[char] 表示 char 字符映射到的孩子结点


# Trie 字典树 / 前缀树
class StringTrie:
    def __init__(self, word_list=None):
        # Trie 的根结点 (不存储具体的字符)
        self.trie_root = TrieNode(char=None)

        # 如果单词表不空，则依次插入每个单词，构建 Trie
        if isinstance(word_list, list):
            for word in word_list:
                self.trie_insert(word)

    # 在 Trie 中搜索单词
    # 如果搜索到了，则返回 True，否则返回 False
    def trie_search(self, word):
        assert isinstance(word, str)
        ptr = self.trie_root  # 当前结点指针
        # 逐个匹配当前结点的孩子
        for char in word:
            # 如果当前结点存在 char 孩子，则往下继续搜索
            if char in ptr.children:
                ptr = ptr.children[char]
            # 否则找不到目标单词
            else:
                return False

        # 处理最后一个字符，如果当前结点是单词结尾，则返回 True
        if ptr.is_word:
            return True
        # 否则找不到目标单词，返回 False
        else:
            return False

    # 插入单词到 Trie
    def trie_insert(self, word):
        assert isinstance(word, str)
        ptr = self.trie_root  # 当前结点指针
        # 逐个匹配当前结点的孩子，如果当前结点不存在 char 孩子，则构造之
        for char in word:
            # 如果当前结点存在 char 孩子，则往下继续搜索
            if char in ptr.children:
                ptr = ptr.children[char]
            # 否则构造 char 孩子
            else:
                new_node = TrieNode(char=char, is_word=False)  # 创建孩子
                ptr.children[char] = new_node  # 链接孩子
                ptr = new_node  # 往下搜索

        # 处理最后一个字符，设置当前结点的 is_word 标志为 True，表示这是单词结尾
        ptr.is_word = True

    # 从 Trie 中删除单词
    def trie_delete(self, word):
        assert isinstance(word, str)
        # 先搜索单词，并记录搜索过程的结点序列
        node_seq = []  # 处理时先进后出，模拟栈
        ptr = self.trie_root  # 当前结点指针
        # 逐个匹配当前结点的孩子
        for char in word:
            # 如果当前结点存在 char 孩子，则往下继续搜索
            if char in ptr.children:
                # 如果能搜索到单词，则搜索路径上除了最后一个结点外都会加入 node_seq
                node_seq.append(ptr)
                ptr = ptr.children[char]
            # 否则找不到目标单词，删除失败
            else:
                return False

        # 处理最后一个字符，如果当前结点是单词结尾，则找到了目标单词，进行删除
        assert isinstance(ptr, TrieNode)
        if ptr.is_word:
            # 删除分如下几种情况：
            # 如果此时 ptr 不是叶结点，那么将 ptr.is_word 置为 False 即可
            if len(ptr.children) > 0:
                ptr.is_word = False
            # 如果此时 ptr 是叶结点，则从 ptr 开始往前删除结点，直到删除至某个结点 v
            # v 要么有兄弟结点，要么 v.is_word == True，则停止删除
            # 如果中途没有上述那样的 v 结点，则会将 node_seq 中的所有结点均删除
            else:
                # 逐个处理搜索路径上的每个结点
                while len(node_seq) > 0:
                    ptr_p = node_seq.pop()  # ptr 所指结点的父结点，ptr_p 至高会等于树根，但不会删除树根
                    assert isinstance(ptr_p, TrieNode) and len(ptr_p.children) >= 1
                    # 修改父结点指针
                    assert ptr.char in ptr_p.children
                    ptr_p.children.pop(ptr.char)
                    # 删除 ptr 所指结点
                    del ptr
                    # 如果父结点是某个单词的结尾字符，或者 ptr 有兄弟结点，则结束删除过程
                    if ptr_p.is_word or len(ptr_p.children) > 0:
                        break
                    # 否则上移 ptr，继续删除
                    else:
                        ptr = ptr_p

            return True
        # 否则找不到目标单词，删除失败、返回 False
        else:
            return False


# 01 字典树: 主要用于解决求异或最值的问题
class Trie01:
    # 这里处理 32 进制数，因此设计 01 字典树是一棵最多 32 层的二叉树
    # 其每个结点的两条边分别表示二进制的某一位的值为 0 还是为 1，将某个路径上边的值连起来就得到一个二进制串
    # 每个结点主要有 4 个属性：结点编号(下标)、结点值、两条边指向的下一结点(孩子)的编号(下标)。
    def __init__(self, number_list):
        # 处理的数字最大位数
        self.number_bits = 32
        # 01 字典树中至多处理的数字总量
        self.max_numbers = 64
        # 当前树中的结点个数 (初始仅有根结点，但根结点不代表任何数字)
        self.n_nodes = 0

        # node_val[i] 表示结点的值
        # 结点值 node_val[i] == 0 时表示到当前节点 i 为止 不能形成一个数，否则 node_val[i] 等于某个数值
        self.node_val = [0 for _ in range(self.number_bits * self.max_numbers)]

        # node_edge[i] 表示一个结点，node_edge[i][0] 和 node_edge[i][1] 表示节点的两条边指向的结点
        # node_edge[0] 表示 01 字典树的根结点，其边对应着二进制串的最高位
        # 边值 node_edge[i][j] == 0 表示此边目前不存在 (因为都是从根出发，不会指回到根结点)
        self.node_edge = [[0 for _ in range(2)] for _ in range(self.number_bits * self.max_numbers)]

        # 如果输入的数字列表不为空，则据此构建 01 字典树
        if isinstance(number_list, list):
            for number in number_list:
                self.trie_01_insert(number)

    # 向 01 字典树中插入数字 number
    def trie_01_insert(self, number):
        assert isinstance(number, int)
        cur_index = 0  # 从根结点开始
        for i in reversed(range(self.number_bits)):
            highest_bit = (number >> i) & 0x1
            if self.node_edge[cur_index][highest_bit] == 0:
                # 如果当前边不存在，则增添边
                self.n_nodes += 1
                self.node_edge[cur_index][highest_bit] = self.n_nodes
            # 移至下一结点(下标)
            cur_index = self.node_edge[cur_index][highest_bit]
        # 最后设置结点值为 number，表示从根到此结点的二进制串是一个树中的数
        self.node_val[cur_index] = number

    # 通过贪心的策略来寻找与 x 异或结果最大的数，优先找和 x 二进制的 未处理的最高位 值不同的边对应的点，
    # 因为异或操作处理值不同的的两个二进制数 (0 xor 1 或者 1 xor 0) 得 1，否则得 0，所以此贪心策略可保证结果最大。
    def trie_01_xor_max(self, number):
        assert isinstance(number, int)
        cur_index = 0  # 从根结点开始
        for i in reversed(range(self.number_bits)):
            highest_bit = (number >> i) & 0x1
            # 移至下一结点(下标)，优先选择最高位值不同的
            if self.node_edge[cur_index][highest_bit ^ 1] > 0:
                cur_index = self.node_edge[cur_index][highest_bit ^ 1]
            else:
                cur_index = self.node_edge[cur_index][highest_bit]
        # 最后返回结点值
        return self.node_val[cur_index]


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


def main():
    # Trie
    print('\nTrie Tree:')
    # 用于构造 Trie 的单词表 (不提前给出字符表)
    word_list = ["math", "mathematics", "physics", "philosophy", "cosmology", "serendipity"]
    # 用于搜索的单词列表
    search_list = ["math", "cosmo", "serendipity"]

    # 创建 Trie
    string_trie = StringTrie(word_list=word_list)

    # 删除单词
    print(string_trie.trie_delete("mathematics"))  # True
    print(string_trie.trie_delete("cosmo"))  # False

    # 进行搜索匹配
    start = time.process_time()
    ans_list = []
    for word in search_list:
        ans_list.append(string_trie.trie_search(word))
    end = time.process_time()

    # 查看结果 [True, False, True]
    print(ans_list)
    # 计算运行时间
    print('Trie_search: Running Time: %.5f ms' % ((end - start) * 1000))

    # 01-Trie
    print('\n01-Trie:')
    # 用于构造 01-Trie 的(正整数)数字表
    number_list = [0b10001, 0b1010, 0b101, 0b110, 0b10101]
    # 用于求异或最大值的数字列表
    query_list = [0b10110, 0b101]

    # 创建 01-Trie
    trie_01 = Trie01(number_list)

    # 进行异或求值
    start = time.process_time()
    ans_list = []
    for query_number in query_list:
        ans_list.append(trie_01.trie_01_xor_max(query_number))
    end = time.process_time()

    # 查看结果 [10: 0b01010, 17: 0b10001]
    print(ans_list)
    # 计算运行时间
    print('Trie_search: Running Time: %.5f ms' % ((end - start) * 1000))

    # Suffix Trie
    print('\nSuffix Trie:')
    # 用于构造后缀树的字符串
    suffix_str = "banana"
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
    print('Trie_search: Running Time: %.5f ms' % ((end - start) * 1000))

    # 进行子串出现次数检测
    start = time.process_time()
    ans_list = []
    for query_str in count_list:
        ans_list.append(suffix_tree.count_repetition(query_str))
    end = time.process_time()

    # 查看结果 [0, 1, 2, 2, 3, 1, 0]
    print(ans_list)
    # 计算运行时间
    print('Trie_search: Running Time: %.5f ms' % ((end - start) * 1000))

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
    print('Trie_search: Running Time: %.5f ms' % ((end - start) * 1000))

    # 进行子串出现次数检测
    start = time.process_time()
    ans_list = []
    for query_str in count_list:
        ans_list.append(g_suffix_tree.g_count_repetition(query_str))
    end = time.process_time()

    # 查看结果 [1, 1, 3, 4, 6, 1, 0]
    print(ans_list)
    # 计算运行时间
    print('Trie_search: Running Time: %.5f ms' % ((end - start) * 1000))

    # 求构建后缀树的所有字符串的最长公共子串
    print(g_suffix_tree.longest_substring())  # "an"

    # 求某个字符串的最长回文子串
    # 方法：以此字符串和其反转字符串 构建广义后缀树，然后寻找最长公共子串
    pal_str = "banana"
    print(g_suffix_tree.longest_palindrome(pal_str))  # "anana"


if __name__ == "__main__":
    sys.exit(main())
