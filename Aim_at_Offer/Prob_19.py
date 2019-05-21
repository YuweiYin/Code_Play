# -*- coding:utf-8 -*-

'''
序号：19
题目：顺时针打印矩阵

题目描述：
输入一个矩阵，按照从外向里以顺时针的顺序依次打印出每一个数字，
例如，如果输入如下4 X 4矩阵：
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 
则依次打印出数字
1,2,3,4,8,12,16,15,14,13,9,5,6,7,11,10.

时间限制：1秒 空间限制：32768K
本题知识点：数组，画图让抽象形象化
'''
import sys
import getopt


class Solution:
    # matrix类型为二维列表，需要返回列表
    def printMatrix(self, matrix):
        # write code here
        # 思路：从 0 行 0 列开始，做如下循环，直至数组为空
        # 从左到右输出，并删除该行，然后从上到下、并删除该列
        # 从右到左输出，并删除该行，然后从下到上，并删除该列
        _matrix = matrix
        answer_list = []
        row_len = len(_matrix[0])
        col_len = len(_matrix)

        # direction 方向为 0 表示从左到右，1 表示从上到下
        # 2 表示从右到左，3 表示从下到上
        # row, col = 0, 0
        direction = 0
        while len(_matrix) > 0:
            if direction == 0:
                # 从左到右，遍历当前行
                row = 0 # 固定行坐标位置
                for i in range(len(_matrix[row])):
                    answer_list.append(_matrix[row][i])

                del _matrix[row] # 删除该行
                # print _matrix

            if direction == 1:
                # 从上到下，遍历当前列
                col = len(_matrix[0]) - 1 # 固定列坐标位置
                i = 0
                while i <= len(_matrix) - 1:
                    answer_list.append(_matrix[i][col])
                    del _matrix[i][col]

                    i += 1

                # print _matrix
                # 如果纵向删空了一行，则可以结束
                if len(_matrix[len(_matrix) - 1]) <= 0:
                    break

            if direction == 2:
                # 从右到左，遍历当前行
                row = len(_matrix) - 1 # 固定行坐标位置
                temp_len = len(_matrix[row])
                for i in range(temp_len):
                    answer_list.append(_matrix[row][temp_len - 1 - i])

                del _matrix[row] # 删除该行
                # print _matrix

            if direction == 3:
                # 从下到上，遍历当前列
                col = 0 # 固定列坐标位置
                i = len(_matrix) - 1
                while i >= 0:
                    answer_list.append(_matrix[i][col])
                    del _matrix[i][col]

                    i -= 1

                # print _matrix
                # 如果纵向删空了一行，则可以结束
                if len(_matrix[0]) <= 0:
                    break

            direction = (direction + 1) % 4

        return answer_list


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
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    # matrix = [
    #     [1, 2],
    #     [3, 4],
    #     [5, 6],
    #     [7, 8]
    # ]

    # matrix = [
    #     [1],
    #     [2],
    #     [3],
    #     [4],
    #     [5]
    # ]

    # matrix = [
    #     [1, 2, 3, 4, 5]
    # ]

    solution = Solution()
    answer = solution.printMatrix(matrix)

    if answer is not None:
        print answer
    else:
        print None


if __name__ == "__main__":
    sys.exit(main())

