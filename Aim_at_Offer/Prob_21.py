# -*- coding:utf-8 -*-

'''
序号：21
题目：栈的压入、弹出序列

题目描述：
输入两个整数序列，第一个序列表示栈的压入顺序，
请判断第二个序列是否可能为该栈的弹出顺序。
假设压入栈的所有数字均不相等。
例如序列1,2,3,4,5是某栈的压入顺序，
序列4,5,3,2,1是该压栈序列对应的一个弹出序列，
但4,3,5,1,2就不可能是该压栈序列的弹出序列。
（注意：这两个序列的长度是相等的）

时间限制：1秒 空间限制：32768K
本题知识点：栈，举例让抽象具体化
'''
import sys
import getopt


class Solution:
    def IsPopOrder(self, pushV, popV):
        # write code here
        # 思路1：分析序列组成
        # pop 出 4 之后，1 2 3 一定在栈底
        # 所以弹出序列 3、2、1 的相对顺序就不会变
        # 3 2 1 之间或许有别的弹出点，但终归相对顺序不会变

        # 思路2：判断是否符合正确的弹出顺序
        # 从 pushV 一个个分析，如果当前弹出了 4，
        # 那么下一个弹出的只能是 4 之后的元素，或者是 3，
        # 如果弹出了 3 之前的，比如 2 和 1，那就错了。
        # 可惜由于时间复杂度原因，没通过在线测试

        # if len(pushV) <= 0 or len(popV) <= 0 or len(pushV) != len(popV):
        #     return False

        # if len(pushV) == 1 and len(popV) == 1 and pushV[0] == popV[0]:
        #     return True

        # flag = False
        # loc = pushV.index(popV[0])
        # if loc >= 1:
        #     if pushV[loc - 1] == popV[1]:
        #         flag = True
        #         del pushV[loc]
        #         del popV[0]
        #         # print pushV, popV
        #         return self.IsPopOrder(pushV, popV)

        # i = loc + 1
        # while i <= len(pushV) - 1:
        #     if pushV[i] == popV[1]:
        #         flag = True
        #         del pushV[loc]
        #         del popV[0]
        #         # print pushV, popV
        #         return self.IsPopOrder(pushV, popV)

        # # 如果没有相等的，说明 popV 此时弹出了不该弹出的点，否则正常
        # if flag:
        #     return True
        # else:
        #     return False

        # 思路3：模拟压栈、弹出过程
        # 用辅助栈，遍历压栈顺序，先将第一个元素放入栈中，即 1，
        # 然后判断栈顶元素是不是出栈顺序的第一个元素，即 4，
        # 若不相等，则继续压栈，直到相等以后开始出栈，
        # 出栈一个元素，则将出栈顺序向后移动一位，直到不相等，
        # 这样循环等压栈顺序遍历完成，
        # 如果最后辅助栈还不为空，说明弹出序列不是该栈的弹出顺序。

        stack = []

        while popV:
            if stack and stack[-1] == popV[0]:
                # 如果此时辅助栈不空，且辅助栈顶元素等于弹出序列首元素
                # 则将这两个元素均弹出
                stack.pop()
                popV.pop(0)
            elif pushV:
                # 如果此时压栈序列不空，则压入一个元素到辅助栈
                stack.append(pushV.pop(0))
            else:
                # 压栈序列已经空了，但是辅助栈要么不空，
                # 要么其栈顶元素无法与弹出序列首元素匹配
                return False

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

    pushV = [1, 2, 3, 4, 5]
    popV1 = [4, 5, 3, 2, 1]
    popV2 = [4, 3, 5, 1, 2]

    print solution.IsPopOrder(pushV, popV1)
    print solution.IsPopOrder(pushV, popV2)


if __name__ == "__main__":
    sys.exit(main())

