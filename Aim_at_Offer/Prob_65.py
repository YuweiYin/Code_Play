# -*- coding:utf-8 -*-

'''
序号：65
题目：矩阵中的路径

题目描述：
请设计一个函数，用来判断在一个矩阵中是否存在一条包含某字符串所有字符的路径。
路径可以从矩阵中的任意一个格子开始，每一步可以在矩阵中向左，向右，向上，向下移动一个格子。
如果一条路径经过了矩阵中的某一个格子，则之后不能再次进入这个格子。
例如 a b c e s f c s a d e e 这样的3 X 4 矩阵中包含一条字符串"bcced"的路径，
但是矩阵中不包含"abcb"路径，因为字符串的第一个字符b占据了矩阵中的第一行第二个格子之后，
路径不能再次进入该格子。

时间限制：1秒 空间限制：32768K
本题知识点：回溯法
'''
import sys
import getopt


class Solution:
    def hasPath(self, matrix, rows, cols, path):
        # write code here
        if matrix is None or len(matrix) < (rows * cols):
            return False

        # 空路径当前能满足
        if path is None or len(path) <= 0:
            return True

        # 将原本的一维数组 matrix 转为二维矩阵 matrix_2d
        matrix_2d = [list(matrix[cols * i: cols * i + cols]) for i in range(rows)]

        # 从左上角开始，对各行各列的每个元素寻找目标路径
        for i in range(rows):
            for j in range(cols):
                # 如果找到了一条，则返回 True 表示能找到一条目标路径
                if self.FindPath(matrix_2d, i, j, path):
                    return True

        return False

    # 回溯法寻找路径
    def FindPath(self, matrix, i, j, path):
        # 先判断当前坐标所在的矩阵值，是否等于目标路径的首字符
        if matrix[i][j] == path[0]:
            # 如果目标路径只有一个字符，那么匹配到首字符就等于匹配到路径了，返回 True
            if not path[1: ]:
                return True

            # 将已经经过的矩阵元素标记为 ''
            matrix[i][j] = ''

            # 往上走
            if i > 0 and self.FindPath(matrix, i - 1, j, path[1: ]):
                return True

            # 往下走
            if i < len(matrix) - 1 and self.FindPath(matrix, i + 1, j ,path[1: ]):
                return True

            # 往左走
            if j > 0 and self.FindPath(matrix, i, j - 1, path[1: ]):
                return True

            # 往右走
            if j < len(matrix[0]) - 1 and self.FindPath(matrix, i, j + 1, path[1: ]):
                return True

            # 还原、回溯，将标记为 '' 的矩阵元素还原成原本的值，回到上一层的递归
            matrix[i][j] = path[0]

            # 目前未找到目标路径
            return False

        # 首字符都不匹配，当然未找到目标路径
        else:
            return False


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

    # matrix = [
    #     ['a', 'b', 'c', 'e'],
    #     ['s', 'f', 'c', 's'],
    #     ['a', 'd', 'e', 'e']
    # ]
    matrix = [
        'a', 'b', 'c', 'e',
        's', 'f', 'c', 's',
        'a', 'd', 'e', 'e'
    ]
    rows = 3
    cols = 4
    path = 'bcced'
    # path = 'abcb'

    answer = solution.hasPath(matrix, rows, cols, path)

    if answer is not None:
        print answer
    else:
        print 'No Answer'



if __name__ == "__main__":
    sys.exit(main())
