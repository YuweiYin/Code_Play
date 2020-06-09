#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/other-topics/polynomial-fft
@File    : fast-fourier-transform.py
@Author  : YuweiYin
@Date    : 2020-06-08
=================================================="""

import sys
import time
import math

"""
- 多项式与快速傅立叶变换 Polynomial & FFT
    - 离散傅立叶变换 (Discrete Fourier Transform, DFT)
    - 快速傅立叶变换 (Fast Fourier Transform, FFT)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 30
"""


class FastFourierTransform:
    def __init__(self):
        # 根据输入，计算一些常用的数值，避免重复计算耗时
        self.w_n = 1          # 主 n 次单位复数根

    # 辅助函数：向量(列表) 乘 标量(常数) - (标量广播后)逐元素相乘
    @staticmethod
    def multi_vector_scalar(vector, scalar):
        assert isinstance(vector, list)
        for i in range(len(vector)):
            vector[i] *= scalar
        return vector

    # 辅助函数：向量(列表) 加 标量(常数) - (标量广播后)逐元素相加
    @staticmethod
    def plus_vector_scalar(vector, scalar):
        assert isinstance(vector, list)
        for i in range(len(vector)):
            vector[i] += scalar
        return vector

    # 辅助函数：向量(列表) 减 标量(常数) - (标量广播后)逐元素相减
    @staticmethod
    def minus_vector_scalar(vector, scalar):
        assert isinstance(vector, list)
        for i in range(len(vector)):
            vector[i] -= scalar
        return vector

    # 辅助函数：行向量(列表) 乘 列向量(列表) - 内积运算
    @staticmethod
    def dot_multi_vector(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        res_scalar = 0
        for i in range(len(vec_1)):
            res_scalar += vec_1[i] * vec_2[i]
        return res_scalar

    # 辅助函数：向量(列表) 加 向量(列表) - (同规模的向量)逐元素相加
    @staticmethod
    def plus_vector_vector(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        res_scalar = [vec_1[i] + vec_2[i] for i in range(vec_1)]
        return res_scalar

    # 辅助函数：向量(列表) 减 向量(列表) - (同规模的向量)逐元素相减
    @staticmethod
    def minus_vector_vector(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        res_scalar = [vec_1[i] - vec_2[i] for i in range(vec_1)]
        return res_scalar

    # 用 DFT & FFT 计算两个多项式的乘积
    # bound_n 是多项式 poly_a 和 poly_b 的次数界，这里默认为 2 的幂次
    # 时间复杂度：\Theta(n log n)
    def do_fft_polynomial_multiply(self, poly_a, poly_b, bound_n):
        assert isinstance(poly_a, list) and isinstance(poly_b, list)
        # 设置新的次数界 new_bound_n
        new_bound_n = bound_n << 1
        # 将两个多项式的长度均填充到 new_bound_n
        for _ in range(new_bound_n - len(poly_a)):
            poly_a.append(0)
        for _ in range(new_bound_n - len(poly_b)):
            poly_b.append(0)
        # 设置主 new_bound_n 次单位复数根 (用于 DFT 过程)
        # TODO 复数的指数运算
        self.w_n = math.pow(math.e, 2 * math.pi * 1j / new_bound_n)

        # 调用 DFT 过程，进行取值操作，将系数向量转为点值向量 \Theta(n log n)
        y_a = self.recursive_dft(poly_a)
        y_b = self.recursive_dft(poly_b)

        # 在点值形式下，进行多项式乘法(逐点相乘) \Theta(n)
        assert isinstance(y_a, list) and isinstance(y_b, list) and len(y_a) == len(y_b) == new_bound_n
        multi_poly = [y_a[i] * y_b[i] for i in range(new_bound_n)]

        # 调用逆 DFT 过程，进行插值操作，将点值向量转为系数向量 \Theta(n log n)
        res_poly = self.recursive_reverse_dft(multi_poly)
        return res_poly

    # 递归的 离散傅立叶变换 DFT 过程
    # 进行取值操作，将系数向量转为点值向量
    # 时间复杂度：\Theta(n log n)
    def recursive_dft(self, poly):
        return self._recursive_dft(poly)

    def _recursive_dft(self, poly):
        assert isinstance(poly, list)
        # 1. 获取当前递归的子问题规模 n
        n = len(poly)
        half_n = n >> 1

        # 2. 处理基本情况，一个元素的 DFT 就是该元素自身，因为此时 y_0 = a_0 * w_1^{0} = a_0 * 1 = a_0
        if n <= 0:
            print('recursive_fft: length of Polynomial a <= 0!')
            return [0]
        elif n == 1:
            return poly

        # 3. 设置初始 w 值为 1
        w = 1

        # 4. 定义以偶数下标元素组成的多项式的系数向量 a^{0}，下标为奇数时是 a^{1}
        a_0 = poly[0::2]
        a_1 = poly[1::2]

        # 5. 递归计算子问题 $ DFT_{n/2} $
        y_0 = self._recursive_dft(a_0)
        y_1 = self._recursive_dft(a_1)
        assert isinstance(y_0, list) and isinstance(y_1, list) and len(y_0) == len(y_1) == half_n

        # 6. 在 for 循环中，综合了递归 $ DFT_{n/2} $ 的计算结果
        y = [0 for _ in range(n)]
        for k in range(half_n):
            temp = y_1[k] * w
            y[k] = y_0[k] + temp
            y[k + half_n] = y_0[k] - temp
            w *= self.w_n

        # 7. 最后，返回计算结果 y，即输入的多项式系数向量 a 的 DFT 向量
        return y

    # 递归的 逆离散傅立叶变换 DFT^{-1} 过程
    # 进行插值操作，将点值向量转为系数向量
    # 时间复杂度：\Theta(n log n)
    def recursive_reverse_dft(self, poly):
        return self._recursive_reverse_dft(poly)

    def _recursive_reverse_dft(self, poly):
        assert isinstance(poly, list)
        # 1. 获取当前递归的子问题规模 n
        n = len(poly)
        half_n = n >> 1

        # 2. 处理基本情况，一个元素的 DFT^{-1} 就是该元素自身，因为此时 y_0 = a_0 * w_1^{0}^{-1} = a_0 * 1 = a_0
        if n <= 0:
            print('recursive_fft: length of Polynomial a <= 0!')
            return [0]
        elif n == 1:
            return poly

        # 3. 设置初始 w 值为 1
        w = 1

        # 4. 定义以偶数下标元素组成的多项式的系数向量 a^{0}，下标为奇数时是 a^{1}
        a_0 = poly[0::2]
        a_1 = poly[1::2]

        # 5. 递归计算子问题 $ DFT_{n/2}^{-1} $
        y_0 = self._recursive_reverse_dft(a_0)
        y_1 = self._recursive_reverse_dft(a_1)
        assert isinstance(y_0, list) and isinstance(y_1, list) and len(y_0) == len(y_1) == half_n

        # 6. 在 for 循环中，综合了递归 $ DFT_{n/2}^{-1} $ 的计算结果
        y = [0 for _ in range(n)]
        for k in range(half_n):
            temp = y_1[k] * w
            y[k] = (y_0[k] + temp) / n
            y[k + half_n] = (y_0[k] - temp) / n
            w /= self.w_n

        # 7. 最后，返回计算结果 y，即输入的多项式点值向量对应的系数向量
        return y


def main():
    fft = FastFourierTransform()

    # DFT & FFT 求解 两个多项式的乘积
    print('\nDFT & FFT:')
    # 用于单纯形算法的线性规划标准型，同《CLRS》Chapter 30 中的第一个多项式乘法例子
    # A(x) = 6 * x^3 + 7 * x^2 - 10 * x + 9
    # B(x) = -2 * x^3 + 4 * x - 5
    # C(x) = -12 * x^6 - 14 * x^5 + 44 * x^4 - 20 x^3 - 75 x^2 + 86 x - 45
    poly_a = [6, 7, -10, 9]
    poly_b = [-2, 0, 4, -5]
    bound_n = 4  # 这里多项式 a 和 b 的次数界均为 4，另外，这里需要次数界为 2 的自然数幂次
    start = time.process_time()
    res_poly = fft.do_fft_polynomial_multiply(poly_a, poly_b, bound_n)
    end = time.process_time()

    # 输出结果
    # [-12, -14, 44, -20, -75, 86, -45]
    if isinstance(res_poly, list):
        print('\nres_poly:')
        print(res_poly)
    else:
        print('DFT & FFT 算法无结果')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
