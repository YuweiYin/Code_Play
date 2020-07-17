#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/other-topics/number-theoretic-algorithm
@File    : number-theory.py
@Author  : YuweiYin
=================================================="""

import sys
import time
import random

"""
- 数论算法 Number-Theoretic Algorithm
    - 欧几里得算法 Euclidean Algorithm
    - 扩展的欧几里得算法 Extended Euclidean Algorithm
    - 求解模线性方程 Modular Linear Equation Solving
    - 中国剩余定理 Chinese Remainder Theorem
    - 元素的模取幂 Modular Exponentiation
    - (伪)素数测试 Fermat Pseudo Prime Test
    - Miller-Rabin 随机性素数测试方法
    - 整数的(素)因子分解 - Pollard-Rho 启发式算法

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 31
"""


class NumberTheoreticAlgorithm:
    def __init__(self):
        pass

    # (递归的)欧几里得算法 - 求最大公约数
    # 返回最大公约数 gcd(a, b)
    # 如果 gcd(a, b) == 1，则表示 a 与 b 互素
    # 时间复杂度：O(log b)
    # 最坏情况：a 和 b 是相邻的斐波那契数。此时，如果较大数是第 k 个斐波那契数，那么将递归 k 次
    def recursive_euclid(self, a, b):
        # return a if b == 0 else self.recursive_euclid(b, a % b)
        if b == 0:
            return a
        else:
            return self.recursive_euclid(b, a % b)

    # (迭代的)欧几里得算法 - 求最大公约数
    # 时间复杂度：O(log b)
    @staticmethod
    def iterative_euclid(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    # (递归的)扩展欧几里得算法 - 求最大公约数 & (模)乘法逆元
    # 时间复杂度：O(log b)
    # 返回 (d, x, y) 满足 gcd(a, b) = d = ax + by
    # 因此如果最终 d == 1，那么在 mod b 或 mod y 的情况下，a 与 x 互为(模)乘法逆元
    # 同理如果最终 d == 1，那么在 mod a 或 mod x 的情况下，b 与 y 互为(模)乘法逆元
    # 然而如果最终 d >= 1，那么在 mod b 或 mod y 的情况下，a/d 与 x 互为(模)乘法逆元
    # 同理如果最终 d >= 1，那么在 mod a 或 mod x 的情况下，b/d 与 y 互为(模)乘法逆元
    def recursive_extended_euclid(self, a, b):
        if b == 0:
            return a, 1, 0
        else:
            d, x, y = self.recursive_extended_euclid(b, a % b)
            return d, y, x - y * int(a / b)

    # 求解模方程 ax = b (mod n) 输出其所有解
    # 输入 a 和 n 为任意正整数，b 为任意整数
    def modular_linear_equation_solver(self, a, b, n):
        if isinstance(a, int) and isinstance(b, int) and isinstance(n, int) and a > 0 and b > 0:
            d, x, y = self.recursive_extended_euclid(a, n)
            if b % d == 0:
                res_x = [0 for _ in range(d)]
                x_0 = res_x[0] = (x * (b / d)) % n
                n_d = n / d
                for i in range(1, d):
                    res_x[i] = (x_0 + i * n_d) % n
                return res_x
            else:
                print('No solutions')
                return None
        else:
            print('modular_linear_equation_solver: 输入数据的范围不合法!')
            return None

    # 中国剩余定理，求解未知数 x，它满足 x = a_i mod n_i
    def chinese_remainder_theorem(self, vector_a, vector_n):
        if isinstance(vector_a, list) and isinstance(vector_n, list) and len(vector_a) == len(vector_n) > 0:
            # 确保 n_i 之间两两互素
            vec_len = len(vector_a)
            for i in range(vec_len - 1):
                if self.iterative_euclid(vector_n[i], vector_n[i + 1]) != 1:
                    print('chinese_remainder_theorem: 输入的 n_i 之间并不两两互素!')
                    return None

            # 定义 n = \prod n_i
            # TODO 乘积上溢处理
            n = 1
            for i in range(len(vector_n)):
                n *= vector_n[i]

            # 求解 m_i = n / n_i
            vector_m = [n / vector_n[i] for i in range(vec_len)]

            # 求解 m_i^{-1} mod n_i
            # 《CLRS》定理 31.6 保证 m_i 与 n_i 互素
            # 《CLRS》推论 31.26 保证 m_i^{-1} mod n_i 存在
            vector_m_rev = []
            for i in range(vec_len):
                d, x, y = self.recursive_extended_euclid(vector_m[i], vector_n[i])
                assert d == 1
                vector_m_rev.append(x % vector_n[i])  # 此时 x 即为 m_i 在 mod n_i 下的乘法逆元 m_i^{-1}

            # 定义 c_i = m_i * (m_i^{-1} mod n_i)
            vector_c = [vector_m[i] * vector_m_rev[i] for i in range(vec_len)]

            # 结果 res_x = (\sum_{i} (a_i * c_i)) mod n
            res_x = 0
            for i in range(vec_len):
                res_x += (vector_a[i] * vector_c[i]) % n
            return res_x % n
        else:
            print('chinese_remainder_theorem: 输入数据不合法!')
            return None

    # 元素的模取幂
    # 输入非负整数 a, b 以及正整数 n
    # 用反复平方法(快速幂)快速求解 a^b mod n
    # TODO 乘积上溢处理
    @staticmethod
    def modular_exponentiation(a, b, n):
        if isinstance(a, int) and isinstance(b, int) and isinstance(n, int) and a >= 0 and b >= 0 and n > 0:
            prod = 1      # 累乘的结果
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

    # (伪)素数测试 - 在大多数情况下运行还不错，但会被攻击者针对性地设计输入合数 n，但检测结果为素数
    # 基于费马(小)定理: 如果 p 是素数，则 a^{p-1} = 1 (mod p) 对所有 a \in Z_{p}^{*} 都成立
    # 输入整数 n
    # 返回 True 表示 n 为素数，返回 False 表示 n 为合数
    # 检测到合数，一定不会判断错；检测到素数，有可能判断错 (这种数被称为 Carmicheal 数)
    # (伪)素数测试 的出错率 依赖于 n 的大小，n 越大 出错率越小
    # 如果 n 是一个随机选取的 512 位数，那么出错概率不到 1e-20；如果是 1024 位数，则出错率不到 1e-42
    def fermat_pseudo_prime_test(self, n):
        if n == 2:
            # 2 是素数
            return True
        elif n < 2 or not (n & 0x1):
            # 除了 2 自身以外，2 的倍数是合数 (小于 2 的数不是素数，不考虑它们)
            return False
        else:
            if self.modular_exponentiation(2, n - 1, n) % n != 1:
                # 检测结果：n 一定是合数
                return False
            else:
                # 检测结果：n 很可能是素数
                return True

    # Miller-Rabin 随机性素数测试方法 - 比(伪)素数测试更优
    # 输入整数 n，以及检测循环次数 s (s 越大，检测出错的概率就越小)
    # 返回 True 表示 n 为素数，返回 False 表示 n 为合数
    # 检测到合数，一定不会判断错；检测到素数，有可能判断错
    # Miller-Rabin 的出错率不依赖于 n 的大小，而是与 s 有关，至多为 2^{-s}
    def miller_rabin_prime_test(self, n, s):
        if n == 2:
            # 2 是素数
            return True
        elif n < 2 or not (n & 0x1):
            # 除了 2 自身以外，2 的倍数是合数 (小于 2 的数不是素数，不考虑它们)
            return False
        else:
            # 循环 s 次，检查 n 是否为合数
            for i in range(s):
                # 随机选取整数 a (范围是 1 <= a <= n-1) 作为检测合数的证据因子
                a = random.randint(1, n - 1)
                # 调用子过程 witness 检测 n 是否为合数
                if self.witness(a, n):
                    # 检测结果：n 一定是合数
                    return False

            # 如果 n 次检查都不为合数，则 n 很可能为素数
            return True

    # 辅助函数 - 检测 n 是否为合数
    # 这是 Miller-Rabin 随机性素数测试方法的子过程
    # 输入: 大于 2 的整数 n, 以及整数 a (范围是 1 <= a <= n-1) 作为检测合数的证据因子
    def witness(self, a, n):
        assert n >= 2
        if n == 2:
            # 2 为素数
            return False
        elif not (n & 0x1):
            # n 为大于 2 的偶数(即二进制末尾为 0)，则必为合数
            return True
        else:
            # 此时 n 为大于 2 的奇数，故 n-1 是偶数，n-1 的二进制末尾必为 0
            # 构造 u 和 t，使得 t >= 1 且 u 为奇数，并且 n - 1 = u * 2^{t}
            u = n - 1
            t = 0
            while not u & 0x1:
                # 如果 u 的二进制位末尾为 0，则右移一位 u
                u >>= 1
                t += 1
            # 计算 x_0 = a^u mod n
            x = [0 for _ in range(t + 1)]
            x[0] = self.modular_exponentiation(a, u, n) % n

            # 对结果连续平方 t 次
            for i in range(1, t + 1):
                x[i] = (x[i - 1] * x[i - 1]) % n
                # 仅当 n 为合数时，才存在以 n 为模的 1 的非平凡平方根
                if x[i] == 1 and x[i - 1] != 1 and x[i - 1] != n - 1:
                    return True

            # 如果 x^t = a^{n-1} mod n 的值不等于 1，则表示 n 为合数
            if x[t] != 1:
                return True

            # 否则(很可能)是素数
            return False

    # 整数的(素)因子分解 - Pollard-Rho 启发式算法
    # 对小于 R 的所有整数进行试除，保证完全获得小于 R^2 的任意数的因子分解
    # Pollard-Rho 启发式算法用相同的工作量，就能对小于 R^4 的任意数进行因子分解（除非运气不佳，否则可以完成）
    # 由于该过程仅仅是一种启发式方法，因此既不能保证其运行时间 也不能保证其运行成功，尽管该过程在实际应用中非常有效
    # Pollard-Rho 启发式算法的另一个优点是：空间复杂度很低
    # 输入整数 n，输出其素因子结果集合
    def pollard_rho(self, n):
        res_set = set({})  # 结果集合
        if n < 2:
            return res_set
        elif n == 2:
            return set(2)

        # 初始化 i 为 1，并把 x_1 初始化为整数加群 Z_n 中一个随机值
        i = 1
        x = [0, random.randint(0, n - 1)]  # x[0] 仅作占位
        y = x[1]
        k = 2
        # while 循环一直迭代，搜索 n 的因子
        while True:
            # 运行递归式 x_i = (x_{i-1}^2 - 1) mod n
            # 计算无穷序列 x_1, x_2, x_3, ... 中的下一个值
            x.append((x[i] * x[i] - 1) % n)
            i += 1
            # 尝试用当前 y 值和 x_i 值 来寻找 n 的素因子
            d = self.iterative_euclid(y - x[i], n)
            if d != 1 and d != n:
                # 找到了一个新的素因子，加入结果集合
                if not (d in res_set):
                    print(d)
                    res_set.add(d)
                    # 检查，如果当前集合中的素因子(的正整数次幂)的乘积恰等于 n，则结束搜索
                    temp_n = n
                    for prime in res_set:
                        # 除以当前素因子 prime 的尽可能多次幂，之后再考虑下一个素因子
                        while temp_n % prime == 0:
                            temp_n /= prime
                    # 如果最后 n 被除为 1，则表示找出了所有素因子
                    if temp_n == 1:
                        return res_set
                    else:
                        # 如果最后剩余的因子是素数，则将之加入到结果集合中，并返回 res_set
                        temp_n = int(temp_n)
                        if self.miller_rabin_prime_test(temp_n, 10):
                            print(temp_n)
                            res_set.add(temp_n)
                            return res_set
            # k 的值保持为 2 的某个幂次，k 的序列为 2, 4, 8, 16, ...
            # 当 i 达到 k 值时，将 x_i 保存在 y 中
            if i == k:
                # 本来 while 循环需要一直不停地迭代下去，但这里限制循环次数
                if k >= 0x10000000:
                    return res_set
                y = x[i]
                k <<= 1


def main():
    nta = NumberTheoreticAlgorithm()

    # 计算最大公约数
    print('\nGCD - (Extended) Euclidean Algorithm:')
    a, b = 99, 78  # 同《CLRS》Chapter 31 中的图 31-1

    start = time.process_time()
    res_1 = nta.recursive_euclid(a, b)
    res_2 = nta.iterative_euclid(a, b)
    res_3 = nta.recursive_extended_euclid(a, b)
    end = time.process_time()

    # 输出结果: gcd(99, 78) = 3 = -11 * 99 + 14 * 78
    print(res_1)
    print(res_2)
    print(res_3)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 求解模方程 ax = b (mod n) 输出其所有解
    print('\nModular Linear Equation Solving:')
    a, b, n = 14, 30, 100  # 同《CLRS》Chapter 31 中 31.4 节的模方程例子

    start = time.process_time()
    res_4 = nta.modular_linear_equation_solver(a, b, n)
    end = time.process_time()

    # 输出结果: [95, 45]
    if isinstance(res_4, list):
        print(res_4)
    else:
        print('此模方程无解:', a, 'x=', b, 'mod', n)
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 中国剩余定理，求解未知数 x，它满足 x = a_i mod n_i
    print('\nChinese Remainder Theorem:')
    # 同《CLRS》Chapter 31 中的图 31-3: x = 2 mod 5 并且 x = 3 mod 13
    vector_a = [2, 3]
    vector_n = [5, 13]

    start = time.process_time()
    res_5 = nta.chinese_remainder_theorem(vector_a, vector_n)
    end = time.process_time()

    # 输出结果: 42
    if res_5 is not None:
        print(int(res_5))
    else:
        print('中国剩余定理无解')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 制作同《CLRS》Chapter 31 中的图 31-3 的表格
    if isinstance(vector_n, list) and len(vector_n) == 2:
        res_table = [[0 for _ in range(vector_n[1])] for _ in range(vector_n[0])]
        for i in range(vector_n[0]):
            for j in range(vector_n[1]):
                res_table[i][j] = int(nta.chinese_remainder_theorem([i, j], vector_n))

        print('\n《CLRS》Chapter 31 图 31-3 表格:')
        # [0, 40, 15, 55, 30, 5, 45, 20, 60, 35, 10, 50, 25]
        # [26, 1, 41, 16, 56, 31, 6, 46, 21, 61, 36, 11, 51]
        # [52, 27, 2, 42, 17, 57, 32, 7, 47, 22, 62, 37, 12]
        # [13, 53, 28, 3, 43, 18, 58, 33, 8, 48, 23, 63, 38]
        # [39, 14, 54, 29, 4, 44, 19, 59, 34, 9, 49, 24, 64]
        for row in res_table:
            print(row)

    # 元素的模取幂
    # 输入非负整数 a, b 以及正整数 n
    # 用反复平方法(快速幂)快速求解 a^b mod n
    print('\nModular Exponentiation:')
    # 同《CLRS》Chapter 31 中的图 31-4: a = 7, b = 560 = <1000110000>, n = 561
    a, b, n = 7, 560, 561

    start = time.process_time()
    res_6 = nta.modular_exponentiation(a, b, n)
    end = time.process_time()

    # 输出结果: 1
    if res_6 is not None:
        print(int(res_6))
    else:
        print('元素的模取幂无解')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 素数检测
    print('\nPrime Test:')
    # 这里随机选取 10 个正整数，分别用 (伪)素数测试 和 Miller-Rabin 随机性素数测试方法 来检测素性
    # int_range = 0x3f3f3f3f
    int_range = 50
    s_1 = 10   # Miller-Rabin 循环 10 次
    s_2 = 100  # Miller-Rabin 循环 100 次
    for i in range(10):
        n = random.randint(3, int_range)
        fermat_res = nta.fermat_pseudo_prime_test(n)
        mr_res_1 = nta.miller_rabin_prime_test(n, s_1)
        mr_res_2 = nta.miller_rabin_prime_test(n, s_2)
        print('n:', n, '\tFermat:', fermat_res, '\tMiller-Rabin-10:', mr_res_1, '\tMiller-Rabin-100:', mr_res_2)

    # 整数的(素)因子分解 - Pollard-Rho 启发式算法
    print('\nPollard-Rho:')
    # 同《CLRS》Chapter 31 中的图 31-7: n = 1387 = 19 * 73
    n = 1387

    start = time.process_time()
    res_7 = nta.pollard_rho(n)
    end = time.process_time()

    # 输出结果: {73, 19}
    if isinstance(res_7, set):
        print(res_7)
    else:
        print('整数的(素)因子分解无解')
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
