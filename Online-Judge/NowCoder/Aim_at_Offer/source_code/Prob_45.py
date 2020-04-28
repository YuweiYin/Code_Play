#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：45
题目：扑克牌顺子

题目描述：
LL 今天心情特别好,因为他去买了一副扑克牌,
发现里面居然有 2 个大王,2 个小王(一副牌原本是 54 张^_^)...
他随机从中抽出了 5 张牌, 想测测自己的手气, 看看能不能抽到顺子,
如果抽到的话, 他决定去买体育彩票, 嘿嘿！！
“红心 A, 黑桃 3, 小王, 大王, 方片 5”, “Oh My God!”不是顺子.....
LL 不高兴了, 他想了想, 决定大/小 王可以看成任何数字,
并且 A 看作 1, J 为 11, Q 为 12, K 为 13。
上面的 5 张牌就可以变成 “1,2,3,4,5” (大小王分别看作 2 和 4),
“So Lucky!”。LL 决定去买体育彩票啦。
现在, 要求你使用这幅牌模拟上面的过程, 然后告诉我们 LL 的运气如何，
如果牌能组成顺子就输出 true，否则就输出 false。
为了方便起见, 你可以认为大小王是 0。

时间限制：1秒 空间限制：32768K
本题知识点：字符串，抽象建模能力
"""

import sys
import time


class Solution:
    @staticmethod
    def is_continuous(numbers):
        if numbers is None or len(numbers) <= 4:
            return False

        # 先排序列表
        num_sort = sorted(numbers, reverse=False)

        # 统计大小王的数量，大小王是可以被看作任何点数的牌（癞子）
        king_sum = 0
        i = 0
        while i < len(num_sort):
            if num_sort[i] == 0:
                king_sum += 1
            else:
                break
            i += 1

        # 跳过大小王，开始遍历，检查是否是顺子
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


def main():
    # numbers = [9, 11, 8, 10, 12]  # True
    # numbers = [0, 9, 11, 8, 12]  # True
    # numbers = [1, 9, 11, 8, 12]  # False
    numbers = [1, 3, 0, 5, 0]  # True

    start = time.process_time()
    answer = Solution.is_continuous(numbers)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
