# -*- coding:utf-8 -*-

'''
序号：63
题目：数据流中的中位数

题目描述：
如何得到一个数据流中的中位数？如果从数据流中读出奇数个数值，
那么中位数就是所有数值排序之后位于中间的数值。
如果从数据流中读出偶数个数值，那么中位数就是所有数值排序之后中间两个数的平均值。
我们使用Insert()方法读取数据流，使用GetMedian()方法获取当前读取数据的中位数。

时间限制：1秒 空间限制：32768K
本题知识点：树
'''
import sys
import getopt
from heapq import *


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.heaps = [], []

    def Insert(self, num):
        # write code here
        # large 大根堆：保存大的半数的数据
        # small 小根堆：保存小的半数的数据
        # 插入一个数据的时间复杂度为 O(log(n))

        # 构造小根堆时，取元素的负值来构造
        # heappush(heap, data)，将 data 放入大根堆中
        # heapposh(heap)，弹出 heap 中的最小值
        # heappushpop(heap, data)，将 data 放入大根堆中，再弹出堆 heap 的最小值
        small, large = self.heaps

        # 将 num 放入大根堆，并弹出大根堆的最小值，
        # 取反（取反之后就变成小根堆中最小的数了，但绝对值是最大的），放入小根堆 small
        heappush(small, -heappushpop(large, num))

        # 保证大根堆的数据量不低于小根堆
        if len(large) < len(small):
            # 弹出 small 中最小的值，取反，即最大的值，放入 large
            heappush(large, -heappop(small))

        # print self.heaps

    # 由于题目问题，这道题 Python 版本的 GetMedian 函数必须要第二个参数
    def GetMedian(self, whatever):
        # write code here
        # 获取中位数的时间复杂度为 O(1)
        small, large = self.heaps

        # 大根堆数据更多，中位数为大根堆的最小值
        if len(large) > len(small):
            return float(large[0])
        # 否则大根堆小根堆的数据量相当（这是构造时约束的结果）
        else:
            return (large[0] - small[0]) / 2.0


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

    solution.Insert(1)
    solution.Insert(3)
    solution.Insert(2)
    solution.Insert(7)
    solution.Insert(5)
    solution.Insert(6)
    solution.Insert(9)

    answer = solution.GetMedian(None)

    if answer is not None:
        print answer
    else:
        print 'No Answer'



if __name__ == "__main__":
    sys.exit(main())
