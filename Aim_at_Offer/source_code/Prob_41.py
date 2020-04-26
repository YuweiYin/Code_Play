#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
序号：41
题目：和为 S 的连续正数序列

题目描述：
小明很喜欢数学, 有一天他在做数学作业时, 要求计算出 9~16 的和,
他马上就写出了正确答案是 100。但是他并不满足于此,
他在想究竟有多少种连续的正数序列的和为 100(至少包括两个数)。
没多久, 他就得到另一组连续正数和为 100 的序列: 18, 19, 20, 21, 22。
现在把问题交给你, 你能不能也很快的找出所有和为 S 的连续正数序列?
Good Luck!

输出描述：
输出所有和为S的连续正数序列。
序列内按照从小至大的顺序，序列间按照开始数字从小到大的顺序

时间限制：1秒 空间限制：32768K
本题知识点：知识迁移能力
"""

import sys
import time
import copy


class Solution:
    @staticmethod
    def find_continuous_sequence(t_sum):
        if t_sum <= 2:
            return []

        if t_sum == 3:
            return [[1, 2]]

        answer = []  # 最终答案
        seq = []     # 当前序列
        # seq_sum = 0  # 当前序列的值总和
        end = int(t_sum / 2 + 1)  # 最多找到 1/2 值加 1 的位置就够了

        # 方法一：O(n^2)蛮力计算
        # i = 1
        # while i <= end:
        #     seq = []
        #     seq_sum = 0

        #     # 从当前 i 的位置一个个往后加起来
        #     j = i
        #     while j <= end:
        #         seq.append(j)
        #         seq_sum += j

        #         # 恰好达到了目标值 t_sum，记录序列并退出内循环
        #         if seq_sum == t_sum:
        #             answer.append(seq)
        #             break
        #         # 超过了目标值，直接退出内循环
        #         elif seq_sum > t_sum:
        #             break
        #         # 还未达到目标值，继续下一轮内循环
        #         else:
        #             j += 1

        #     i += 1

        # return answer

        # 方法二：滑动窗口
        small = 1  # 区间下限
        big = 2    # 区间上限

        seq.append(1)
        seq.append(2)
        seq_sum = 3
        while small < end:
            # print(small, big, seq_sum)

            # 当前结果相比目标值，小则 big 后移，大则 small 后移
            if seq_sum < t_sum:
                big += 1
                seq_sum += big
                seq.append(big)

            elif seq_sum > t_sum:
                small += 1
                pop = seq.pop(0)
                seq_sum -= pop

            # 当前结果跟目标值相同
            else:
                # print(seq)
                # 注意要深复制后加入 answer，
                # 不能仅是 answer.append(seq)
                answer.append(copy.deepcopy(seq))

                small += 1
                pop = seq.pop(0)
                seq_sum -= pop

        return answer


def main():
    # t_sum = 10
    t_sum = 100
    # t_sum = 300

    start = time.process_time()
    answer = Solution.find_continuous_sequence(t_sum)
    end = time.process_time()

    if answer is not None:
        print(answer)
    else:
        print('Answer is None.')

    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
