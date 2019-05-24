# -*- coding:utf-8 -*-

'''
序号：45
题目：翻转单词顺序列

题目描述：
LL今天心情特别好,因为他去买了一副扑克牌,
发现里面居然有2个大王,2个小王(一副牌原本是54张^_^)...
他随机从中抽出了5张牌,想测测自己的手气,看看能不能抽到顺子,
如果抽到的话,他决定去买体育彩票,嘿嘿！！
“红心A,黑桃3,小王,大王,方片5”,“Oh My God!”不是顺子.....
LL不高兴了,他想了想,决定大/小 王可以看成任何数字,
并且A看作1,J为11,Q为12,K为13。
上面的5张牌就可以变成“1,2,3,4,5”(大小王分别看作2和4),
“So Lucky!”。LL决定去买体育彩票啦。
现在,要求你使用这幅牌模拟上面的过程,然后告诉我们LL的运气如何，
如果牌能组成顺子就输出true，否则就输出false。
为了方便起见,你可以认为大小王是0。

时间限制：1秒 空间限制：32768K
本题知识点：字符串，抽象建模能力
'''
import sys
import getopt


class Solution:
    def IsContinuous(self, numbers):
        # write code here
        if numbers is None or len(numbers) <= 4:
            return False

        # 先排序列表
        num_sort = sorted(numbers, reverse=False)

        # 找出大小王的数量，大小王是可以被看作任何点数的牌（癞子）
        king_sum = 0
        i = 0
        while i < len(num_sort):
            if num_sort[i] == 0:
                king_sum += 1
            else:
                break
            i += 1

        # 遍历，检查是否是顺子
        i = king_sum
        while i <= (len(num_sort) - 2):
            if num_sort[i] == num_sort[i + 1]:
                # 因为只抽五张牌，所以一旦有点数相等的牌，那就不会构成顺子
                return False

            # 计算前后两数之差超过 1 的值，超过 1 多少就要用多少张王牌去补
            difference = num_sort[i + 1] - num_sort[i] - 1

            # 如果王牌数量不足以弥补差距，则不构成顺子
            if difference > king_sum:
                return False

            # 消耗王牌数
            king_sum -= difference
            i += 1

        return True


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

    # numbers = [9, 11, 8, 10, 12] # True
    # numbers = [0, 9, 11, 8, 12] # True
    # numbers = [1, 9, 11, 8, 12] # False
    numbers = [1, 3, 0, 5, 0] # True

    answer = solution.IsContinuous(numbers)

    if answer is not None:
        print answer
    else:
        print 'No Answer'


if __name__ == "__main__":
    sys.exit(main())

