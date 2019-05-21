# -*- coding:utf-8 -*-

'''
序号：11
题目：二进制中1的个数

题目描述：
输入一个整数，输出该数二进制表示中1的个数。
其中负数用补码表示。

时间限制：1秒 空间限制：32768K
本题知识点：位运算
'''
import sys
import getopt


class Solution:
    def NumberOf1(self, n):
        # write code here
        # print '十进制数为：', n # 100 -100
        # print '转为二进制数为：\n', bin(n) # 0b1100100 -0b1100100
        # print '转为八进制数为：', oct(n) # 0144 -0144
        # print '转为十六进制数为：', hex(n) # 0x64 -0x64
        # print type(bin(n)) # str
        # print type(oct(n)) # str
        # print type(hex(n)) # str

        if n > 0:
            # 正数的原反补码相同
            return bin(n).count('1')
        elif n == 0:
            return 0
        else:
            # 负数用补码表示，而 bin 函数的结果是原码，需要转换
            # & 按位与运算符，| 按位或运算符，^ 按位异或运算符
            # ~ 按位取反运算符，<< 左移动运算符，高位丢弃，低位补零
            # >> 右移动运算符，低位丢弃，高位补零
            original_code = bin(n)[3: ]
            # print original_code
            inverse_code = ''

            for i in range(len(original_code)):
                if original_code[i] == '1':
                    inverse_code += '0'
                else:
                    inverse_code += '1'

            # 本题二进制长度为 32 位
            temp = ''
            for i in range(32 - len(inverse_code)):
                temp += '1'

            inverse_code = '0b' + temp + inverse_code
            # print inverse_code

            complement_code = bin(int(inverse_code, 2) + 1)
            # print complement_code
            return complement_code.count('1')


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
    # n = 2147483648
    # n = 2147483647
    # n = -1
    # n = -2147483647
    n = -2147483648
    print solution.NumberOf1(n)


if __name__ == "__main__":
    sys.exit(main())

