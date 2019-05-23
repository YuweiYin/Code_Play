# -*- coding:utf-8 -*-

'''
序号：40
题目：数组中只出现一次的数字

题目描述：
一个整型数组里除了两个数字之外，其他的数字都出现了两次。
请写程序找出这两个只出现一次的数字。

时间限制：1秒 空间限制：32768K
本题知识点：数组，知识迁移能力
'''
import sys
import getopt


class Solution:
    # 返回[a,b] 其中ab是出现一次的两个数字
    def FindNumsAppearOnce(self, array):
        # write code here
        answer = []

        # array 为空
        if array is None or len(array) <= 0:
            return []

        # array 长度为 1
        a_len = len(array)
        if a_len == 1:
            answer.append(array[0])
            return answer

        # array 长度为 2
        if a_len == 2:
            if array[0] != array[1]:
                return array
            else:
                return []

        # 遍历第一遍，用字典存储某个元素的出现次数
        dic = dict()
        for item in array:
            if item in dic:
                dic[item] += 1
            else:
                dic[item] = 1

        # 遍历第二遍，取出出现次数为 1 的元素
        for item in array:
            if dic[item] == 1:
                answer.append(item)

        return answer


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

    # array = [] # []
    # array = [1] # [1]
    # array = [1, 1] # []
    # array = [1, 2] # [1, 2]
    array = [1, 2, 3, 4, 3, 5, 2, 1] # [4, 5]

    answer = solution.FindNumsAppearOnce(array)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

