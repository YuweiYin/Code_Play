#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/sort
@File    : median-order-statistic.py
@Author  : YuweiYin
@Date    : 2020-05-24
=================================================="""

import sys
import time
import random

"""
中位数和顺序统计量 (Median & Order Statistic)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 9
"""


# 元素结构体 key-value 键值对
class Element:
    def __init__(self, key, val=None):
        self.key = key  # (必备) 键 key。按 key 排序，因此 key 必须具有全序关系（常为整数）
        self.val = val  # (可选) 值 value。可为任意对象


# 中位数和顺序统计量
class MedianOrderStatistic:
    def __init__(self, ele_list):
        assert isinstance(ele_list, list)
        for ele in ele_list:
            assert isinstance(ele, Element)
        self.ele_list = ele_list

    # 获取输入数组
    def get_ele_list(self):
        return self.ele_list

    # 获取输入数组中 key 的列表
    def get_key_list(self):
        if isinstance(self.ele_list, list) and len(self.ele_list) > 0:
            key_list = []
            for ele in self.ele_list:
                assert isinstance(ele, Element)
                key_list.append(ele.key)
            return key_list
        else:
            return None

    # 获取输入数组中 val 的列表
    def get_val_list(self):
        if isinstance(self.ele_list, list) and len(self.ele_list) > 0:
            val_list = []
            for ele in self.ele_list:
                assert isinstance(ele, Element)
                val_list.append(ele.val)
            return val_list
        else:
            return None

    # 辅助函数：交换 self.ele_list 中下标 i 和下标 j 的两个元素
    # 参数范围 0 <= i,j < ele_len
    def _exchange(self, i, j):
        if i != j:
            ele_len = len(self.ele_list)
            if 0 <= i < ele_len and 0 <= j < ele_len:
                temp = self.ele_list[i]
                self.ele_list[i] = self.ele_list[j]
                self.ele_list[j] = temp
            else:
                # 数组越界
                print('_exchange: Error Path. i=', i, '\tj=', j)
        else:
            # 下标相同，无需处理
            pass

    # 求集合 (数组) 最小值
    # 时间复杂度：\Theta(n)
    # 需 n-1 次比较
    def minimum(self):
        assert isinstance(self.ele_list, list)
        ele_len = len(self.ele_list)
        if ele_len <= 0:
            # 数组为空，返回 None
            return None
        elif ele_len == 1:
            # 数组仅有一个元素，返回此唯一元素
            return self.ele_list[0]
        else:
            # 数组不止一个元素，先记录 min 为首元素
            min_ele = self.ele_list[0]
            # 然后遍历其余元素，与 min 比较
            for i in range(1, ele_len):
                # 若当前元素比 min 更小，则更新 min
                if self.ele_list[i].key < min_ele.key:
                    min_ele = self.ele_list[i]
            return min_ele

    # 求集合 (数组) 最大值
    # 时间复杂度：\Theta(n)
    # 需 n-1 次比较
    def maximum(self):
        assert isinstance(self.ele_list, list)
        ele_len = len(self.ele_list)
        if ele_len <= 0:
            # 数组为空，返回 None
            return None
        elif ele_len == 1:
            # 数组仅有一个元素，返回此唯一元素
            return self.ele_list[0]
        else:
            # 数组不止一个元素，先记录 max 为首元素
            max_ele = self.ele_list[0]
            # 然后遍历其余元素，与 max 比较
            for i in range(1, ele_len):
                # 若当前元素比 max 更大，则更新 max
                if self.ele_list[i].key > max_ele.key:
                    max_ele = self.ele_list[i]
            return max_ele

    # 同时求集合 (数组) 最小值和最大值
    # 时间复杂度：\Theta(n)
    # 需 3 \floor(n/2) 次比较，优于分别调用 minimum 和 maximum 的总共 2(n-1) 次比较
    def min_max(self):
        assert isinstance(self.ele_list, list)
        ele_len = len(self.ele_list)
        if ele_len <= 0:
            # 数组为空，返回 None
            return None, None
        elif ele_len == 1:
            # 数组仅有一个元素，返回此唯一元素
            return self.ele_list[0], self.ele_list[0]
        else:
            # 数组不止一个元素，根据列表长度的奇偶性做处理
            if ele_len & 0x1:
                # 集合的秩为奇数，初始化 min 和 max 均为首元素
                min_ele = max_ele = self.ele_list[0]
                start_index = 1  # 之后从下标 1 开始处理剩余元素
            else:
                # 集合的秩为偶数，先进行初始比较，取较小者作为 min、较大者作为 max
                if self.ele_list[0] < self.ele_list[1]:
                    min_ele = self.ele_list[0]
                    max_ele = self.ele_list[1]
                else:
                    min_ele = self.ele_list[1]
                    max_ele = self.ele_list[0]
                start_index = 2  # 之后从下标 2 开始处理剩余元素
            # 然后遍历其余元素，成对地处理
            half = (ele_len - start_index) >> 1  # 剩余元素数目的一半
            for i in range(start_index, start_index + half):
                # 先让两个元素进行比较，得到较小者和较大者
                if self.ele_list[i].key < self.ele_list[i + half].key:
                    # 若较小者比 min 更小，则更新 min
                    if self.ele_list[i].key < min_ele.key:
                        min_ele = self.ele_list[i]
                    # 若较大者比 max 更大，则更新 max
                    if self.ele_list[i + half].key > max_ele.key:
                        max_ele = self.ele_list[i + half]
                else:
                    # 若较小者比 min 更小，则更新 min
                    if self.ele_list[i + half].key < min_ele.key:
                        min_ele = self.ele_list[i + half]
                    # 若较大者比 max 更大，则更新 max
                    if self.ele_list[i].key > max_ele.key:
                        max_ele = self.ele_list[i]
            return min_ele, max_ele

    # (顺序统计量)选择算法
    # 求集合 (数组) 中第 i 小的元素 (1 <= i <= ele_len)
    def order_statistic_select(self, i):
        assert isinstance(self.ele_list, list)
        ele_len = len(self.ele_list)
        if ele_len == 0 or i <= 0 or i > ele_len:
            return None
        elif ele_len == 1:
            return self.ele_list[0]
        else:
            # return self._quick_select(0, ele_len - 1, i)
            return self._linear_select(self.ele_list[:], 0, ele_len - 1, i)

    # 快速(顺序统计量)选择算法
    # 利用类似随机化快速排序的方法
    # 期望时间复杂度：\Theta(n)
    # 最坏时间复杂度：\Theta(n^2) 不过由于做了随机化处理，几乎不会出现最坏情况
    # 注意：由于快排的不稳定性，如果集合中有相同 key 的元素，则此算法求顺序统计量也是不稳定的
    # 每次从数组 A 中选取主元 p(pivot) 下标，
    # 默认升序排列，如下操作：
    # 让 A[lo..p-1] 中的每个元素都小于等于 A[p]
    # 让 A[p+1..hi] 中的每个元素都大于等于 A[p]
    def _quick_select(self, lo, hi, target_order):
        # 当待排序数组的左下标等于右下标时为基本情况：
        # 该数组只有一个元素，返回之
        assert 0 <= lo <= hi < len(self.ele_list)
        if lo == hi:
            return self.ele_list[lo]
        # p = self._partition(lo, hi)             # 固定选择选取主元、划分区间
        # p = self._randomized_partition(lo, hi)  # 随机选取主元
        # p = self._mid_three_partition(lo, hi)   # 三数取中法
        p = self._mid_three_randomized_partition(lo, hi)  # 随机三数取中法
        assert p >= 0
        left_len = p - lo + 1  # 划分出的左子数组的长度，包括主元 p 在内，这些元素都小于等于主元 p 所代表的元素
        # 如果 left_len 恰等于 i，则找到了目标顺序统计量
        if target_order == left_len:
            return self.ele_list[p]
        # 如果 left_len 大于 i，表示应该在左子数组中寻找目标顺序统计量
        elif target_order < left_len:
            return self._quick_select(lo, p - 1, target_order)  # 在左子数组中递归
        # 如果 left_len 小于 i，表示应该在右子数组中寻找目标顺序统计量
        # 注意搜寻目标 i 要变成相对的"第 i 小"，即右子数组中的第 i - left_len 小
        else:
            return self._quick_select(p + 1, hi, target_order - left_len)  # 在右子数组中递归

    # 基于快速排序 + 良好划分的(顺序统计量)选择算法
    # 期望时间复杂度：\Theta(n)
    # 最坏时间复杂度：\Theta(n)
    def _linear_select(self, ele_list, lo, hi, target_order):
        # 当待排序数组的左下标等于右下标时为基本情况：
        # 该数组只有一个元素，返回之
        ele_len = len(ele_list)
        assert 0 <= lo <= hi < ele_len
        if lo == hi:
            return ele_list[lo]
        # 1. 将输入数组的 n 个元素划分为 `\floor(n/5)` 组，每组有 5 个元素
        # 且至多只有一组由剩下的 n mod 5 个元素组成。
        n = hi - lo + 1
        group_size = 5
        rest_group_size = n % group_size  # 剩余组的长度
        full_group_num = int(n / group_size)  # 长度为 group_size 的组数目

        # 2. 对各个长度为 group_size 的分组进行插入排序
        # 获取这 `\ceil(n/5)` 组中每一组的(下)中位数
        groups_median = []  # 存储每一组的中位数，以便递归寻找其中的中位数
        median_ele2index = dict({})  # 把 groups_median 的中位数下标转为 ele_list 的元素下标
        start_index = lo
        end_index = start_index + group_size
        # 先处理长度为 group_size 的组
        for full_group_index in range(full_group_num):
            # 先进行插入排序
            self._insertion_sort(ele_list, start_index, end_index)
            # 再取其(下)中位数
            mid_index = start_index + ((group_size - 1) >> 1)
            groups_median.append(ele_list[mid_index])
            median_ele2index[ele_list[mid_index]] = mid_index
            # 修改起始终止下标
            start_index += group_size
            end_index += group_size

        # 如果剩余组不为空，则还需处理剩余组
        if rest_group_size > 0:
            # 先进行插入排序
            start_index = lo + full_group_num * group_size
            self._insertion_sort(ele_list, start_index, hi)
            # 再取其(下)中位数
            mid_index = start_index + ((rest_group_size - 1) >> 1)
            groups_median.append(ele_list[mid_index])
            median_ele2index[ele_list[mid_index]] = mid_index

        # 3. 对第 2 步中找出的 `\ceil(n/5)` 个中位数，
        # 递归调用 linear_select 以找出这 `\ceil(n/5)` 个元素的中位数 x
        # （如果 `\ceil(n/5)` 是偶数，则取 x 为下中位数）。
        median_order = len(groups_median) >> 1
        median_ele = self._linear_select(groups_median, 0, len(groups_median) - 1, median_order)
        assert isinstance(median_ele, Element) and median_ele in median_ele2index
        # 把 groups_median 的中位数下标转为 ele_list 的元素下标
        median_index = median_ele2index[median_ele]

        # 4. 利用修改过的 partition 划分子过程，以中位数 x 为主元对输入数组进行划分。
        # 让 k 比“划分低区”中的元素数目多 1，因此 x 是第 k 小的元素，并且有 n - k 个元素在划分高区。
        p = self._partition_with_pivot(ele_list, lo, hi, median_index)
        assert p >= 0

        # 5. 根据 i 和 k 的大小关系来处理：
        # 	- 如果 i == k，则返回 x
        # 	- 如果 i < k，则在划分低区递归调用 linear_select 来找出其中第 i 小的元素
        # 	- 如果 i > k，则在划分高区递归调用 linear_select 来找出其中第 i - k 小的元素
        left_len = p - lo + 1  # 划分出的左子数组的长度，包括主元 p 在内，这些元素都小于等于主元 p 所代表的元素
        # 如果 left_len 恰等于 i，则找到了目标顺序统计量
        if target_order == left_len:
            return self.ele_list[p]
        # 如果 left_len 大于 i，表示应该在左子数组中寻找目标顺序统计量
        elif target_order < left_len:
            return self._linear_select(ele_list, lo, p - 1, target_order)  # 在左子数组中递归
        # 如果 left_len 小于 i，表示应该在右子数组中寻找目标顺序统计量
        # 注意搜寻目标 i 要变成相对的"第 i 小"，即右子数组中的第 i - left_len 小
        else:
            return self._linear_select(ele_list, p + 1, hi, target_order - left_len)  # 在右子数组中递归

    # 插入排序
    # 对数组 self.ele_list 的半闭半开区间 [lo, hi) 进行排序
    @staticmethod
    def _insertion_sort(ele_list, lo, hi):
        ele_len = len(ele_list)
        assert 0 <= lo < ele_len and lo <= hi <= ele_len
        if lo == hi:
            return
        if lo + 1 == hi:
            # 仅有两个元素，若反序则逆之
            if ele_list[lo].key > ele_list[hi].key:
                temp = ele_list[lo]
                ele_list[lo] = ele_list[hi]
                ele_list[hi] = temp
        else:
            for j in range(lo + 1, hi):
                cur_ele = ele_list[j]  # 当前循环的处理元素
                assert isinstance(cur_ele, Element)
                # 记录 cur_ele 的 key 和 val 值，因为之后可能会被其它元素覆盖掉
                cur_key = cur_ele.key
                cur_val = cur_ele.val
                # 将 ele_list[j] 插入到已排好序的列表 ele_list[0..j-1] 中
                i = j - 1
                while i >= 0 and ele_list[i].key > cur_key:  # key 升序排序(默认)
                    # 右移 i 号元素：把 i 号元素的 key 和 val 都赋值给 i+1 号元素
                    ele_list[i + 1].key = ele_list[i].key
                    ele_list[i + 1].val = ele_list[i].val
                    i -= 1  # 继续往左寻找插入位置
                # 此时 i 号元素不满足 while 循环条件，即表示 i+1 号即为该插入的位置
                # 于是将之前记录好的 cur_key 和 cur_val 赋值给 i+1 号元素，完成插入
                ele_list[i + 1].key = cur_key
                ele_list[i + 1].val = cur_val

    # 从数组 A 中选取主元下标 p、划分区间
    # 使得位于下标 p 之前的元素值都小于等于 A[p]，之后的都大于等于 A[p]
    # 若为降序排列，则反之。
    # 简单的快排主元选取，可以总是选取 A[hi] 即最右元素作为主元，
    def _partition(self, lo, hi):
        assert 0 <= lo < hi < len(self.ele_list)
        assert isinstance(self.ele_list[hi], Element)
        p_key = self.ele_list[hi].key
        # 做法：快慢双指针。
        # i 为慢指针，只有在某个比 p_key 小的元素被换到数组前半部分后，才会增长
        # j 为快指针，逐个往后判断当前元素的 key 是否小于等于 p_key
        i = lo - 1
        for j in range(lo, hi):  # j = lo..hi-1
            assert isinstance(self.ele_list[j], Element)
            if self.ele_list[j].key <= p_key:
                i += 1
                self._exchange(i, j)
        self._exchange(i + 1, hi)
        return i + 1  # 返回主元元素最终的下标位置，即为划分子区间的下标

    # 从数组 A 中选取主元下标 p、划分区间
    def _partition_with_pivot(self, ele_list, lo, hi, pivot):
        assert 0 <= lo < hi < len(ele_list) and lo <= pivot <= hi
        if hi - lo > 1:
            # 把主元交换到 index=hi
            temp = ele_list[pivot]
            ele_list[pivot] = ele_list[hi]
            ele_list[hi] = temp
        # 与 _partition 函数同样的做法：快慢双指针
        p_key = self.ele_list[hi].key
        i = lo - 1
        for j in range(lo, hi):  # j = lo..hi-1
            assert isinstance(self.ele_list[j], Element)
            if self.ele_list[j].key <= p_key:
                i += 1
                self._exchange(i, j)
        self._exchange(i + 1, hi)
        return i + 1  # 返回主元元素最终的下标位置，即为划分子区间的下标

    # _partition 中选取主元缺乏随机性，如果数组本就有序，或几乎有序，则很影响快排效率
    # 几乎有序的场景也不少，比如往一个有序的数组中新插入某个值，再重新排序
    # 常有两种改进方式：1. 根据随机数，随机选取主元。2. 三数取中划分。
    def _randomized_partition(self, lo, hi):
        assert 0 <= lo < hi < len(self.ele_list)
        if hi - lo > 1:  # hi - lo > 1 表示当前子数组元素有至少 3 个元素
            p_index = self._get_random_int(lo, hi)
            self._exchange(p_index, hi)  # 把主元交换到 index=hi 即可
        return self._partition(lo, hi)  # 调用原本的 partition 函数

    # (常用)三数取中划分：若当前数组区间的元素不少于 3，
    # 取最左、中间、最右这三个元素的 key 中位数者作为主元
    def _mid_three_partition(self, lo, hi):
        assert 0 <= lo < hi < len(self.ele_list)
        if hi - lo > 3:  # r - lo > 3 表示当前子数组元素有至少 5 个元素
            mid_index = int((lo + hi) >> 1)
            p_index = self._get_mid_key_index(lo, mid_index, hi)
            self._exchange(p_index, hi)  # 把主元交换到 index=hi 即可
        return self._partition(lo, hi)  # 调用原本的 partition 函数

    # 随机三数取中划分：若当前数组区间的元素不少于 3，
    # 则先从中随机选出 3 个元素，再取其中位数作为主元
    def _mid_three_randomized_partition(self, lo, hi):
        assert 0 <= lo < hi < len(self.ele_list)
        if hi - lo > 3:  # hi - lo > 3 表示当前子数组元素有至少 5 个元素
            p_index1 = self._get_random_int(lo, hi)
            p_index2 = self._get_random_int(lo, hi)
            p_index3 = self._get_random_int(lo, hi)
            p_index = self._get_mid_key_index(p_index1, p_index2, p_index3)
            self._exchange(p_index, hi)  # 把主元交换到 index=hi 即可
        return self._partition(lo, hi)  # 调用原本的 partition 函数

    # 辅助函数：获取闭区间 [lo, hi] 范围内的一个随机整数
    # 注意：调用前要确保 lo <= hi
    @staticmethod
    def _get_random_int(lo, hi):
        time_int = int(time.time())
        random.seed(time_int)  # 每次根据当前时间更换随机数种子
        return random.randint(lo, hi)

    # 辅助函数：三数取中
    # 输入三个下标。根据这三个下标对应元素的 key 值，取中位数者的下标返回。
    # 注意：调用前要确保 0 <= a,b,c < len(self.ele_list)
    def _get_mid_key_index(self, index1, index2, index3):
        assert isinstance(self.ele_list[index1], Element) and \
               isinstance(self.ele_list[index2], Element) and isinstance(self.ele_list[index3], Element)
        key1 = self.ele_list[index1].key
        key2 = self.ele_list[index2].key
        key3 = self.ele_list[index3].key
        if key1 <= key2:
            if key2 <= key3:
                return index2
            elif key1 <= key3:
                return index3
            else:
                return index1
        else:
            # 此时 key2 < key1
            if key1 <= key3:
                return index1
            elif key2 <= key3:
                return index3
            else:
                return index2


def main():
    # 键值对列表
    kv_list = [
        [3, 300], [1, 100], [2, 200], [8, 800],
        [7, 700], [9, 900], [4, 400]
    ]

    # Element 元素列表(待排序)
    ele_list = []
    if isinstance(kv_list, list) and len(kv_list) > 0:
        for kv in kv_list:
            if isinstance(kv, list) and len(kv) == 2:
                ele_list.append(Element(kv[0], kv[1]))

    mos = MedianOrderStatistic(ele_list)
    print(mos.get_key_list())  # [3, 1, 2, 8, 7, 9, 3]

    # 获取最值
    print('\n获取最值:')
    _min = mos.minimum()  # 获取最小值 1
    _max = mos.maximum()  # 获取最大值 9
    _min_, _max_ = mos.min_max()  # 同时获取最小值 1 和最大值 9

    if isinstance(_min, Element):
        print('min: ', _min.key, _min.val)
    if isinstance(_max, Element):
        print('max: ', _max.key, _max.val)
    if isinstance(_min_, Element) and isinstance(_max_, Element):
        print('min_max: ', _min_.key, _min_.val, '\t', _max_.key, _max_.val)

    # 顺序统计量 选择问题
    print('\n顺序统计量:')
    start = time.process_time()
    os_1 = mos.order_statistic_select(1)
    end = time.process_time()

    if isinstance(os_1, Element):
        print('os_1: ', os_1.key, os_1.key)

    print('order_statistic_select: Running Time: %.5f ms' % ((end - start) * 1000))

    for i in range(-1, 10):
        os = mos.order_statistic_select(i)
        if isinstance(os, Element):
            print('os: ', os.key, os.val)
        else:
            print('No Order Statistic:', i)


if __name__ == "__main__":
    sys.exit(main())
