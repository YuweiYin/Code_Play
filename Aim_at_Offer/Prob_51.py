# -*- coding:utf-8 -*-

'''
序号：51
题目：构建乘积数组

题目描述：
给定一个数组A[0,1,...,n-1],请构建一个数组B[0,1,...,n-1],
其中B中的元素B[i]=A[0]*A[1]*...*A[i-1]*A[i+1]*...*A[n-1]。
不能使用除法。

时间限制：1秒 空间限制：32768K
本题知识点：数组
'''
import sys
import getopt


class Solution:
    def multiply(self, A):
        # write code here
        if A is None or len(A) <= 0:
            return []

        A_len = len(A)
        if A_len == 1:
            return A

        # 列表元素循环右移，每次右移一位，形成一个新数组
        # 最终结果列表就是：这些新数组的相应位置元素的乘积
        # 这个方法仍然是 O(n^2) 的复杂度
        # B = []
        # mul_matrix = []
        # i = 1
        # while i < A_len:
        #     mul_matrix.append(A[i: ] + A[: i])
        #     i += 1

        # # print mul_matrix

        # i = 0
        # mul_len = len(mul_matrix)
        # while i < A_len:
        #     mul = 1
        #     j = 0
        #     while j < mul_len:
        #         mul *= mul_matrix[j][i]
        #         j += 1

        #     B.append(mul)
        #     i += 1

        # return B

        # 方法二：改进效率
        # 还是看成矩阵，但是缓存每一行的两段乘积，对角线的值为 1
        # B0: 1 2 3 4 5
        # B1: 1 1 3 4 5
        # B2: 1 2 1 4 5
        # B3: 1 2 3 1 5
        # B4: 1 2 3 4 1
        # 
        B = []
        B.append(1)

        # 存储下三角的每行乘积
        # B0:          
        # B1: 1        
        # B2: 1 2      
        # B3: 1 2 3    
        # B4: 1 2 3 4  
        i = 1
        while i < A_len:
            B.append(B[i - 1] * A[i - 1])

            i += 1

        # 再乘以上三角的每行乘积
        # B0:   2 3 4 5
        # B1:     3 4 5
        # B2:       4 5
        # B3:         5
        # B4:          
        i = A_len - 2
        mul = 1
        while i >= 0:
            # 每行乘积都迭代存储在 mul 里了
            mul *= A[i + 1]
            B[i] *= mul

            i -= 1

        return B


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    # Main Logic Part

    solution = Solution()

    A = [1, 2, 3, 4, 5]

    answer = solution.multiply(A)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

