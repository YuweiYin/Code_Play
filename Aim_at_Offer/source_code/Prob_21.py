#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：21
题目：栈的压入、弹出序列

题目描述：
输入两个整数序列，第一个序列表示栈的压入顺序，
请判断第二个序列是否可能为该栈的弹出顺序。
假设压入栈的所有数字均不相等。
例如序列 1,2,3,4,5 是某栈的压入顺序，
序列 4,5,3,2,1 是该压栈序列对应的一个弹出序列，
但 4,3,5,1,2 就不可能是该压栈序列的弹出序列。
（注意：这两个序列的长度是相等的）

时间限制：1秒 空间限制：32768K
本题知识点：栈，举例让抽象具体化
"""

import sys
import time


class Solution:
    @staticmethod
    def is_pop_order(push_v, pop_v):
        # 思路 1：分析序列组成
        # pop 出 4 之后，1 2 3 一定在栈底
        # 所以弹出序列 3、2、1 的相对顺序就不会变
        # 3 2 1 之间或许有别的弹出点，但终归相对顺序不会变

        # 思路 2：判断是否符合正确的弹出顺序
        # 从 push_v 一个个分析，如果当前弹出了 4，
        # 那么下一个弹出的只能是 4 之后的元素，或者是 3，
        # 如果弹出了 3 之前的，比如 2 和 1，那就错了。
        # 可惜由于时间复杂度原因，没通过在线测试

        # if len(push_v) <= 0 or len(pop_v) <= 0 or len(push_v) != len(pop_v):
        #     return False

        # if len(push_v) == 1 and len(pop_v) == 1 and push_v[0] == pop_v[0]:
        #     return True

        # flag = False
        # loc = push_v.index(pop_v[0])
        # if loc >= 1:
        #     if push_v[loc - 1] == pop_v[1]:
        #         flag = True
        #         del push_v[loc]
        #         del pop_v[0]
        #         # print(push_v, pop_v)
        #         return self.IsPopOrder(push_v, pop_v)

        # i = loc + 1
        # while i <= len(push_v) - 1:
        #     if push_v[i] == pop_v[1]:
        #         flag = True
        #         del push_v[loc]
        #         del pop_v[0]
        #         # print(push_v, pop_v)
        #         return self.IsPopOrder(push_v, pop_v)

        # # 如果没有相等的，说明 pop_v 此时弹出了不该弹出的点，否则正常
        # if flag:
        #     return True
        # else:
        #     return False

        # 思路 3：模拟压栈、弹出过程
        # 用辅助栈，遍历压栈顺序，先将第一个元素放入栈中，即 1，
        # 然后判断栈顶元素是不是出栈顺序的第一个元素，即 4，
        # 若不相等，则继续压栈，直到相等以后开始出栈，
        # 出栈一个元素，则将出栈顺序向后移动一位，直到不相等，
        # 这样循环等压栈顺序遍历完成，
        # 如果最后辅助栈还不为空，说明弹出序列不是该栈的弹出顺序。

        stack = []

        while pop_v:
            if stack and stack[-1] == pop_v[0]:
                # 如果此时辅助栈不空，且辅助栈顶元素等于弹出序列首元素
                # 则将这两个元素均弹出
                stack.pop()
                pop_v.pop(0)
            elif push_v:
                # 如果此时压栈序列不空，则压入一个元素到辅助栈
                stack.append(push_v.pop(0))
            else:
                # 压栈序列已经空了，但是辅助栈要么不空，
                # 要么其栈顶元素无法与弹出序列首元素匹配
                return False

        return True


def main():
    push_v = [1, 2, 3, 4, 5]
    pop_v1 = [4, 5, 3, 2, 1]
    pop_v2 = [4, 3, 5, 1, 2]

    start = time.process_time()
    res1 = Solution.is_pop_order(push_v, pop_v1)
    res2 = Solution.is_pop_order(push_v, pop_v2)
    end = time.process_time()

    print(res1)
    print(res2)
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
