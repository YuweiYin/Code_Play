#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/other-topics/string-matching
@File    : string-algorithm.py
@Author  : YuweiYin
@Date    : 2020-06-11
=================================================="""

import sys
import time

"""
- 字符串匹配 String Matching
    - 朴素字符串匹配算法 Naive String Matching
    - Rabin-Karp 字符串匹配算法
    - Finite Automaton 有限自动机-字符串匹配算法
    - Knuth-Morris-Pratt - KMP 字符串匹配算法

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 32
"""


class StringMatcher:
    def __init__(self):
        pass

    # 朴素字符串匹配算法
    # 输入文本字符串 text 和模式匹配串 ptn (pattern) 以及全匹配标志 glo (global)
    # 如果 glo 为 True，则返回所有模式串出现的位置(在 text 中的下标偏移量) 列表；如果无匹配，则返回 None
    # 如果 glo 为 False，则返回模式串首次出现的(下标偏移)位置 (仅含一个元素的)列表；如果无匹配，则返回 None
    # 这里模式串不考虑正则匹配的各种符号
    # 时间复杂度：\Theta((n-m+1)m)
    @staticmethod
    def naive_string_matcher(text, ptn, glo=True):
        if isinstance(text, str) and isinstance(ptn, str) and isinstance(glo, bool):
            n = len(text)
            m = len(ptn)
            # 模式串为空串
            if m == 0:
                print('模式串为空串，可匹配文本串的任意位置')
                if glo:
                    return list(range(n))
                else:
                    return [0]
            # 文本串为空串，而模式串不为空串
            elif n == 0:
                print('文本串为空，而模式串不为空，没有可匹配的位置')
                return []
            # 文本串和模式串均不为空串
            else:
                res_s = []  # 能够匹配成功的所有偏移下标
                if glo:
                    # 全局匹配模式
                    for s in range(n - m):
                        # 以模式串 ptn 的长度 m 为滑动窗口大小，从左往右匹配
                        if ptn == text[s: s + m]:  # Python 切分子串较为方便
                            res_s.append(s)
                else:
                    # 首个匹配模式
                    for s in range(n - m):
                        # 非全局匹配，匹配成功一次就结束
                        if ptn == text[s: s + m]:
                            res_s.append(s)
                            break
                return res_s
        else:
            print('输入的参数不合法')
            return []

    # Rabin-Karp 字符串匹配算法
    # 输入数字字符串 text 和数字模式匹配串 ptn (pattern) 以及全匹配标志 glo (global)
    # base_dict 是将字符(哈希)映射到数字的字典，base = len(base_dict) 是数字的基
    # base_dict 字典中映射到的数字不重复地取自集合 {0, 1, 2, ..., base - 1}
    # prime 是一个素数，作为模数，并且 (base * mod) 的值在一个计算机字长内
    # 如果 glo 为 True，则返回所有模式串出现的位置(在 text 中的下标偏移量) 列表；如果无匹配，则返回 None
    # 如果 glo 为 False，则返回模式串首次出现的(下标偏移)位置 (仅含一个元素的)列表；如果无匹配，则返回 None
    # 这里模式串不考虑正则匹配的各种符号
    # 期望时间复杂度：O(n+m)
    # 最坏时间复杂度：\Theta((n-m+1)m) 即每次都伪命中
    def rabin_karp_matcher(self, text, ptn, prime, base_dict, glo=True):
        if isinstance(text, str) and isinstance(ptn, str) and isinstance(prime, int) and \
                isinstance(base_dict, dict) and isinstance(glo, bool):
            n = len(text)
            m = len(ptn)
            base = len(base_dict)  # 数字的基
            # 模式串为空串
            if m == 0:
                print('模式串为空串，可匹配文本串的任意位置')
                if glo:
                    return list(range(n))
                else:
                    return [0]
            # 文本串为空串，而模式串不为空串
            elif n == 0:
                print('文本串为空，而模式串不为空，没有可匹配的位置')
                return []
            # 文本串和模式串均不为空串
            else:
                res_s = []  # 能够匹配成功的所有偏移下标

                # 1. 预处理：用霍纳法则 计算模式串 ptn 以及 text 初始 m 窗口的 base 进制值
                text_num = 0
                ptn_num = 0
                for i in range(m):
                    # 如果字符不在 base_dict 字典中，则是异常字符，故报错
                    assert text[i] in base_dict and ptn[i] in base_dict
                    cur_t_num = base_dict[text[i]]
                    cur_p_num = base_dict[ptn[i]]
                    assert isinstance(cur_t_num, int) and isinstance(cur_p_num, int)
                    # 霍纳法则求 base 进制值
                    text_num = (base * text_num + cur_t_num) % prime
                    ptn_num = (base * ptn_num + cur_p_num) % prime

                # 2. 用快速幂方法 计算 h = base^{m-1} mod prime
                h = self.modular_exponentiation(base, m - 1, prime)
                assert isinstance(h, int) and h > 0

                # 3. 匹配过程：在 text 上滑动窗口
                for s in range(n - m):
                    # 如果模式串的数值取模 等于 当前的 text 窗口的数值取模，则表示伪命中
                    if ptn_num == text_num:
                        # 伪命中后，需进一步检查字符是否确实完全相同
                        if ptn == text[s: s + m]:
                            res_s.append(s)
                            if not glo:  # 首个匹配模式
                                return res_s

                    # 如果未至尾部，则右滑窗口，并更新窗口的数值取模
                    if s < n - m:
                        assert text[s] in base_dict and text[s + m] in base_dict
                        # 减去被移除的数字代表的数值 (由于是最高位，所以乘以 h)
                        temp = (base_dict[text[s]] * h) % prime
                        # 将剩余的数值乘以 base
                        temp = ((text_num - temp) * base) % prime
                        # 加上新的数字代表的数值
                        text_num = (temp + base_dict[text[s + m]]) % prime

                return res_s
        else:
            print('输入的参数不合法')
            return []

    # 元素的模取幂
    # 输入非负整数 a, b 以及正整数 n
    # 用反复平方法(快速幂)快速求解 a^b mod n
    # TODO 乘积上溢处理
    @staticmethod
    def modular_exponentiation(a, b, n):
        if isinstance(a, int) and isinstance(b, int) and isinstance(n, int) and a >= 0 and b >= 0 and n > 0:
            prod = 1  # 累乘的结果
            base = a % n  # 每次(如果要乘)累乘的量
            while b > 0:
                # 如果当前最低二进制位为 1 则累乘 base
                if b & 0x1:
                    prod = (prod * base) % n
                # 继续考虑下一个(更高的)二进制位
                b >>= 1
                # 加倍 base: a^1 -> a^2 -> a^4 -> a^8 -> ...
                base = (base * base) % n
            return prod
        else:
            print('modular_exponentiation: 输入数据不合法!')
            return None

    # 有限自动机-字符串匹配算法
    # 输入数字字符串 text 和数字模式匹配串 ptn (pattern) 以及全匹配标志 glo (global)
    # gamma 是字符表。除了空串，text 和 ptn 中所有字符均取自此字符表
    # 如果 glo 为 True，则返回所有模式串出现的位置(在 text 中的下标偏移量) 列表；如果无匹配，则返回 None
    # 如果 glo 为 False，则返回模式串首次出现的(下标偏移)位置 (仅含一个元素的)列表；如果无匹配，则返回 None
    # 这里模式串不考虑正则匹配的各种符号
    # 预处理时间复杂度：O(m |\Gamma|)
    # 匹配时间复杂度：\Theta(n)
    def finite_automaton_matcher(self, text, ptn, gamma, glo=True):
        if isinstance(text, str) and isinstance(ptn, str) and isinstance(gamma, list) and isinstance(glo, bool):
            # 预处理：计算转移函数
            delta = self.compute_transition_function(ptn, gamma)
            if not isinstance(delta, dict):
                print('计算转移函数失败')
                return []
            # 设置变量
            res_s = []  # 能够匹配成功的所有偏移下标
            n = len(text)
            m = len(ptn)
            state = 0
            # 匹配过程：逐个考察 text 的每个字符
            for i in range(n):
                if (state, text[i]) in delta:
                    # 如果能够通过转移函数 delta 进行转移，则转移状态
                    state = delta[(state, text[i])]
                    if state == m:
                        res_s.append(i - m + 1)
                        if not glo:  # 首个匹配模式
                            return res_s
                else:
                    # 否则回归初始状态
                    state = 0
            return res_s
        else:
            print('输入的参数不合法')
            return []

    # 根据模式串 ptn 和字符表 $ \Gamma $ 计算出转移函数 delta (这里用字典表达 delta)
    @staticmethod
    def compute_transition_function(ptn, gamma):
        if isinstance(ptn, str) and isinstance(gamma, list):
            m = len(ptn)      # 模式串长度
            delta = dict({})  # 状态转移函数 (state, char) -> state
            # 循环处理状态集合 {0, 1, 2, ..., m}
            for state in range(m + 1):
                # ptn 长度为 state 的前缀
                state_prefix = ptn[: state]
                # 循环处理字符表中的每个字符
                for char in gamma:
                    # 从最大可能位置开始寻找
                    k = min(m, state + 1)
                    # state_prefix 连结当前字符 char
                    state_char = state_prefix + char
                    # while 循环直到 ptn 长度为 k 的前缀 是 state_char 的后缀为止
                    while k > 0 and ptn[: k] != state_char[-k:]:
                        k -= 1
                    # 空串为所有字符串的后缀，如果 k == 0 则不记录到 delta 中 以节省空间
                    if k > 0:
                        delta[(state, char)] = k
            return delta
        else:
            print('输入的参数不合法')
            return None

    # Knuth-Morris-Pratt - KMP 字符串匹配算法
    # 输入数字字符串 text 和数字模式匹配串 ptn (pattern) 以及全匹配标志 glo (global)
    # 如果 glo 为 True，则返回所有模式串出现的位置(在 text 中的下标偏移量) 列表；如果无匹配，则返回 None
    # 如果 glo 为 False，则返回模式串首次出现的(下标偏移)位置 (仅含一个元素的)列表；如果无匹配，则返回 None
    # 这里模式串不考虑正则匹配的各种符号
    # 预处理时间复杂度：\Theta(m)
    # 匹配时间复杂度：\Theta(n)
    def knuth_morris_pratt_matcher(self, text, ptn, glo=True):
        if isinstance(text, str) and isinstance(ptn, str) and isinstance(glo, bool):
            # 预处理：计算转移函数
            prefix = self.compute_prefix_function(ptn)
            if not isinstance(prefix, list):
                print('计算前缀函数失败')
                return []
            # 设置变量
            res_s = []  # 能够匹配成功的所有偏移下标
            n = len(text)
            m = len(ptn)
            state = 0  # 模式串 ptn 中待匹配的字符下标
            # 匹配过程：从左至右 逐个考察 text 的每个字符
            for i in range(n):
                # 如果模式串 ptn 的 state 位置出现了不匹配，则查询前缀函数 回退到前一个 state
                # 如果回退之后，到了开头 (即 state == 0) 或者出现匹配，就跳出 while 循环
                while state > 0 and ptn[state] != text[i]:
                    state = prefix[state - 1]
                # 如果是出现匹配的情况，就继续往后匹配，state 加一
                if ptn[state] == text[i]:
                    state += 1
                # 如果所有的模式串字符都已被匹配，则匹配成功
                if state == m:
                    res_s.append(i - m + 1)
                    if not glo:  # 首个匹配模式
                        return res_s
                    # 匹配成功后，state 跳到尾元素的前缀
                    state = prefix[state - 1]
            return res_s
        else:
            print('输入的参数不合法')
            return []

    # 根据模式串 ptn 计算前缀函数 prefix
    # prefix[i] 表示当匹配到模式串的第 i 个位置 发现不匹配时，能够回退到的最大下标位置 (而不必总是从头重新开始)
    # prefix[q] = max{k: k < q \land P[1..k] is suffix of P[1..q]}
    # prefix[q] == k 表示 前缀子串 P[1..k] 是前缀子串 P[1..q] 的后缀，并且 k 值尽可能大
    # 因此，如果在匹配过程中，如果字符 ptn[q + 1] 与 text[i] 出现不匹配 (但 ptn[q] 是已匹配上的)
    # 那么可以回退到 prefix[q] 继续匹配，注意实际中 ptn 的下标是从 0 开始，所以 prefix[q] 正好是目标回退值，举例如下：
    # 例如 ptn = 'abaca' 的前缀函数为 [0, 0, 1, 0, 1] 在 'c' 处 (index=3) 发现与 text[i] 不匹配，
    # 那么查看 prefix[3-1] = 1，从 ptn[1] = 'b' 处继续匹配 text[i]，而跳过了 ptn[0] = 'a' 的匹配，
    # 因为如果是匹配到 'c' 才发现不匹配的，那么 'c' 前面的 'a' 是已匹配了的。
    @staticmethod
    def compute_prefix_function(ptn):
        if isinstance(ptn, str):
            m = len(ptn)  # 模式串长度
            prefix = [0 for _ in range(m)]  # 前缀函数 (一维列表)
            k = 0
            for state in range(1, m):
                # 如果在位置 k 出现了不匹配，则查询前缀函数 回退到前一个 k
                # 如果回退之后，到了开头 (即 k == 0) 或者 k 的位置出现匹配，就跳出 while 循环
                while k > 0 and ptn[k] != ptn[state]:
                    k = prefix[k]
                # 如果是位置 k 出现匹配的情况
                # 表示当模式串在 state 位置出现不匹配，则可以回退到 k+1 的位置继续进行匹配，而不是回退到 k
                if ptn[k] == ptn[state]:
                    k += 1
                # 记录模式串的 state 位置可以回退到的位置
                prefix[state] = k
            # 返回前缀函数 (一维列表)
            return prefix
        else:
            print('输入的参数不合法')
            return None


def main():
    str_matcher = StringMatcher()

    # 朴素字符串匹配算法
    print('\n朴素字符串匹配算法:')
    # 同《CLRS》Chapter 32 中的图 32-4
    text, ptn, glo = 'acaabc', 'aab', True

    start = time.process_time()
    res_1 = str_matcher.naive_string_matcher(text, ptn, glo)
    end = time.process_time()

    # 输出结果: [2]
    if res_1 is not None:
        print(res_1)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # Rabin-Karp 字符串匹配算法
    print('\nRabin-Karp 字符串匹配算法(十进制数字串):')
    # 同《CLRS》Chapter 32 中的图 32-5
    text, ptn, prime, glo = '2359023141526739921', '31415', 13, True
    # 设置 base_dict 字典将字符(哈希)映射到数字，base = len(base_dict) 是数字的基
    base_dict = dict({})
    for i in range(10):
        base_dict[str(i)] = i

    start = time.process_time()
    res_2 = str_matcher.rabin_karp_matcher(text=text, ptn=ptn, prime=prime, base_dict=base_dict, glo=glo)
    end = time.process_time()

    # 输出结果: [6]
    if res_2 is not None:
        print(res_2)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # Rabin-Karp 字符串匹配算法 - 非十进制数字
    print('\nRabin-Karp 字符串匹配算法(非十进制数字串):')
    # 同《CLRS》Chapter 32 中的图 32-4
    text, ptn, prime, glo = 'acaabc', 'aab', 13, True
    # 设置 base_dict 字典将字符(哈希)映射到数字，base = len(base_dict) 是数字的基
    base_dict = dict({})
    base_dict['a'] = 0
    base_dict['b'] = 1
    base_dict['c'] = 2

    start = time.process_time()
    res_3 = str_matcher.rabin_karp_matcher(text=text, ptn=ptn, prime=prime, base_dict=base_dict, glo=glo)
    end = time.process_time()

    # 输出结果: [2]
    if res_3 is not None:
        print(res_3)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 有限自动机-字符串匹配算法
    print('\n有限自动机-字符串匹配算法:')
    # 同《CLRS》Chapter 32 中的图 32-7
    text, ptn, gama, glo = 'abababacaba', 'ababaca', ['a', 'b', 'c'], True

    start = time.process_time()
    res_4 = str_matcher.finite_automaton_matcher(text, ptn, gama, glo)
    end = time.process_time()

    # 输出结果: [2]
    # 另外，设置端点可以查看转移函数 delta，如果是二维列表则如下 (如果是字典，则不存储转移到 0 的表项)
    # 外索引为状态 0~7，内索引为接受的输入字符 a, b, c，元素值为转移的状态
    # [[1, 0, 0],
    # [1, 2, 0],
    # [3, 0, 0],
    # [1, 4, 0],
    # [5, 0, 0],
    # [1, 4, 6],
    # [7, 0, 0],
    # [1, 2, 0]]
    if res_4 is not None:
        print(res_4)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # Knuth-Morris-Pratt - KMP 字符串匹配算法
    print('\nKnuth-Morris-Pratt - KMP 字符串匹配算法(无匹配):')
    # 同《CLRS》Chapter 32 中的图 32-10
    text, ptn, glo = 'bacbababaabcbab', 'ababaca', True

    start = time.process_time()
    res_5 = str_matcher.knuth_morris_pratt_matcher(text, ptn, glo)
    end = time.process_time()

    # 输出结果: []
    # 设置端点可以查看前缀函数 prefix
    # i:         0, 1, 2, 3, 4, 5, 6
    # P[i]:      a, b, a, b, a, c, a
    # prefix[i]: 0, 0, 1, 2, 3, 0, 1
    if res_5 is not None:
        print(res_5)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # Knuth-Morris-Pratt - KMP 字符串匹配算法
    print('\nKnuth-Morris-Pratt - KMP 字符串匹配算法(单匹配):')
    # 一个能够匹配上的例子
    text, ptn, glo = 'bacbababababacabab', 'ababaca', True

    start = time.process_time()
    res_6 = str_matcher.knuth_morris_pratt_matcher(text, ptn, glo)
    end = time.process_time()

    # 输出结果: [8]
    if res_6 is not None:
        print(res_6)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # Knuth-Morris-Pratt - KMP 字符串匹配算法
    print('\nKnuth-Morris-Pratt - KMP 字符串匹配算法(多匹配):')
    # 一个能够匹配上的例子
    text, ptn, glo = 'abcabcabcad', 'abcab', True

    start = time.process_time()
    res_7 = str_matcher.knuth_morris_pratt_matcher(text, ptn, glo)
    end = time.process_time()

    # 输出结果: [0, 3]
    # 设置端点可以查看前缀函数 prefix
    # i:         0, 1, 2, 3, 4
    # P[i]:      a, b, c, a, b
    # prefix[i]: 0, 0, 0, 1, 2
    if res_7 is not None:
        print(res_7)
    else:
        print('找不到模式串:', ptn)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
