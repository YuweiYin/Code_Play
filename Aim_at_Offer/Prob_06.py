# -*- coding:utf-8 -*-

'''
序号：06
题目：旋转数组的最小数字

题目描述：
把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。
输入一个非减排序的数组的一个旋转，输出旋转数组的最小元素。
例如数组{3,4,5,1,2}为{1,2,3,4,5}的一个旋转，该数组的最小值为1。
NOTE：给出的所有元素都大于0，若数组大小为0，请返回0。

时间限制：3秒 空间限制：32768K
本题知识点：查找
'''
import sys
import getopt


class Solution:
    def minNumberInRotateArray(self, rotateArray):
        # write code here
        if len(rotateArray) <= 0:
            return 0
        elif len(rotateArray) == 1:
            return rotateArray[0]
        else:
            # 由于原数组时非减排序，那么旋转数组就是两段非减序列
            # 只要查找到单调性突变的位置就好了
            for i in range(len(rotateArray) - 1):
                if rotateArray[i] > rotateArray[i+1]:
                    return min(rotateArray[0], rotateArray[i+1])

            return rotateArray[0]


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
    # rotateArray = [3, 4, 5, 1, 2]
    rotateArray = [5]
    print solution.minNumberInRotateArray(rotateArray)


if __name__ == "__main__":
    sys.exit(main())

