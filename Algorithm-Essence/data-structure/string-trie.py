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
"""


# Trie 字典树的树结点
class TrieNode:
    def __init__(self, char, is_word=False):
        self.char = char          # 当前结点存储的字符 (在本实现中此属性可不使用)
        self.is_word = is_word    # True 则表示当前字符可以是某个单词的结尾
        self.children = dict({})  # 孩子结点(指针)字典，dict[char] 表示 char 字符映射到的孩子结点


# Trie 字典树
class StringTrie:
    # 初始时，字符表 vocab 可以为空，可以根据输入的单词表 word_list 来更新字符表
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


def main():
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


if __name__ == "__main__":
    sys.exit(main())
