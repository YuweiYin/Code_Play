#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : string-alg.py
@Author  : YuweiYin
@Date    : 2020-05-12
=================================================="""

import sys
import time

"""
字符串 String

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 32
MIT 6.006 Introduction to Algorithms, Fall 2011
    9. Table Doubling, Karp-Rabin - https://www.youtube.com/watch?v=BRO7mVIFt08
"""


# 字符串匹配
class StringMatcher:
    def __init__(self, document="", pattern=""):

        self.document = document  # 长文本
        self.pattern = pattern    # 待匹配的模式串

    # 根据参数 alg_type 选择不同的字符串匹配算法（单次匹配）
    # 如果找到了，返回起始下标；如果找不到，返回 -1
    def do_match(self, alg_type=0):
        if alg_type == 0:
            return self._naive_string_matcher()
        elif alg_type == 1:
            return self._rabin_karp_matcher()
        elif alg_type == 2:
            return self._knuth_morris_pratt_matcher()
        else:
            print('do_match: The Parameter alg_type is NOT valid! alg_type=', alg_type)
            return -1

    # 朴素的字符串匹配方法
    # 时间复杂度：O(m(n-m+1))，其中 n = doc_len, m = ptn_len
    def _naive_string_matcher(self):
        doc_len = len(self.document)
        ptn_len = len(self.pattern)
        for start_index in range(doc_len - ptn_len):
            if self.pattern == self.document[start_index: start_index + ptn_len]:
                return start_index
        return -1

    def _rabin_karp_matcher(self):
        pass

    def _knuth_morris_pratt_matcher(self):
        pass


def main():
    # 长文本 doc 和模式串 ptn
    doc = "YuweiYin - Data Structure and Algorithm."
    ptn = "and"

    # 创建字符串匹配类对象
    string_matcher = StringMatcher(doc, ptn)

    # 进行匹配
    start = time.process_time()
    ans = string_matcher.do_match(alg_type=0)
    end = time.process_time()

    # 查看结果
    if ans >= 0:
        print('找到了模式串，其在文档中的起始下标为:', ans)
    else:
        print('无法找到模式串:\n', ptn)

    # 计算运行时间
    print('do_match: Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
