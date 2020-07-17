#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : van-emde-boas-tree.py
@Author  : YuweiYin
=================================================="""

# import gc
import sys
import time

"""
van Emde Boas Tree, vEB

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 20
"""


class TreeNode:
    def __init__(self, min_key=0x3f3f3f3f, min_val=None, max_key=0x3f3f3f3f, max_val=None, power=1):
        # 注意表示 min_key 和 max_key 为无的 inf 值可能需要根据场景变化
        # 因为有的应用（比如路由表）中全域 u 比 0x3f3f3f3f 还大，所以要重设 inf 值
        self.min_key = min_key  # 本结点存储的最小关键字 inf 表示无 min
        self.max_key = max_key  # 本结点存储的最大关键字 inf 表示无 max
        self.min_val = min_val  # 最小关键字的值对象，可以为任意对象
        self.max_val = max_val  # 最大关键字的值对象，可以为任意对象

        # 当 power=1 (也即 u=2 和 sqrt_u=1) 时，为叶结点
        # 叶结点至多含两个值 min/max，当只有一个值时，为 min
        self.power = power               # 全域大小 u = 2^power
        self.u = 1 << power              # 本结点的全域大小，为 2 的正整数 power 次幂
        self.sqrt_u = 1 << (power >> 1)  # 全域大小 u 的平方根

        # 可优化 self.cluster 为 dict 字典数据结构 (而不是 list 列表)，不存储为空的簇
        # 使得空间复杂度由 O(u) 降到 O(n log log u)。u 是整棵树的全域大小、n 是实际数据量
        self.cluster = dict({})  # 本结点的簇结点列表 (叶结点中没有子簇)
        self.summary = None      # 本结点的 summary 摘要结点 (叶结点中没有 summary 结点)
        self.is_summary = False  # 标志本结点是否为 summary 摘要结点。有些操作可能要据此区分处理


class VanEmdeBoasTree:
    # 以插入方式构造 van Emde Boas Tree
    # 时间复杂度 O(n log n)
    def __init__(self, kv_array):
        self.veb = None        # 树根结点
        self.veb_p = 16        # 全域大小 u = 2^p，这里设为 p = 16 = 2^4
        self.veb_u = 1 << self.veb_p  # 树的关键字全域大小，为 2 的正整数次 p 幂，这里设为 2^16
        self.inf = 0x3f3f3f3f  # inf 值，要比树的关键字全域更大。当结点的 min/max 关键字等于 inf 时，表示不存在

        if isinstance(kv_array, list) and len(kv_array) > 0:
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.insert(kv[0], kv[1])

    # 辅助操作：取某个关键字 key 所在的簇号
    # 当前结点的全域大小 u = 2^power，因此只需取高 (power/2) 位
    @staticmethod
    def high(key, power):
        return key >> (power >> 1)

    # 辅助操作：取某个关键字 key 所在簇的簇内偏移
    # 当前结点的全域大小 u = 2^power，因此只需取低 (power/2) 位
    @staticmethod
    def low(key, power):
        return key % (1 << (power >> 1))  # 用模运算完成
        # 将 1 左移 (power/2)+1 位，再减去 1，就得到了 (power/2) 位全 1 的掩码
        # return key & ((1 << ((power >> 1) + 1)) - 1)  # 和掩码做与运算

    # 根据 key 值判断该结点是否在 vEB 树中
    # 如果在 vEB 树中，则返回 True；否则返回 False
    # 时间复杂度 O(log log u)
    def is_member(self, key):
        if isinstance(key, int) and 0 <= key <= self.veb_u:
            if isinstance(self.veb, TreeNode):
                self._is_member(self.veb, key)
            else:
                # vEB 树为空树，找不到目标 key
                return False
        else:
            print('is_member: key invalid:', key)
            return False

    def _is_member(self, v, key):
        assert isinstance(v, TreeNode)
        assert v.power >= 0 and v.u == (1 << v.power) and v.sqrt_u == (1 << (v.power >> 1))
        # 如果比最小值还小 或者比最大值还大，则找不到
        if key < v.min_key or key > v.max_key:
            return None
        # 判断 key 是否和当前结点 v 的 min_key 或 max_key 相等
        elif key == v.min_key or key == v.max_key:
            # 若相等，则存在此元素
            return True
        # 若不相等，查看当前是否为叶结点
        elif v.power == 1:
            # 如果是叶结点，而 key 又和 min/max 都不相等，表示找不到
            return False
        # 若不相等，且是内部结点，则递归往下查找
        else:
            hi = self.high(key, v.power)
            lo = self.low(key, v.power)
            if hi in v.cluster and isinstance(v.cluster[hi], TreeNode):
                return self._is_member(v.cluster[hi], lo)
            else:
                return False

    # 根据 key 值搜索结点 (与 is_member 很类似)
    # 如果在 vEB 树中，则返回 val；否则返回 None
    # 时间复杂度 O(log log u)
    def search(self, key):
        if isinstance(key, int) and 0 <= key <= self.veb_u:
            if isinstance(self.veb, TreeNode):
                return self._search(self.veb, key)
            else:
                # vEB 树为空树，找不到目标 key
                return None
        else:
            print('search: key invalid:', key)
            return None

    def _search(self, v, key):
        assert isinstance(v, TreeNode)
        assert v.power >= 0 and v.u == (1 << v.power) and v.sqrt_u == (1 << (v.power >> 1))
        # 如果比最小值还小 或者比最大值还大，则找不到
        if key < v.min_key or key > v.max_key:
            return None
        # 判断 key 是否和当前结点 v 的 min_key 或 max_key 相等
        elif key == v.min_key:
            # 若与 min_key 相等，则返回 min_val
            return v.min_val
        elif key == v.max_key:
            # 若与 max_key 相等，则返回 max_val
            return v.max_val
        # 若均不相等，判断当前结点 v 是否为叶结点
        elif v.power == 1:
            # 如果是叶结点，而 key 又和 min/max 都不相等，表示找不到
            return None
        # 若均不相等，且是内部结点，则递归往下查找
        else:
            hi = self.high(key, v.power)
            lo = self.low(key, v.power)
            if hi in v.cluster and isinstance(v.cluster[hi], TreeNode):
                return self._search(v.cluster[hi], lo)
            else:
                return None

    # 根据 key 值查找后继结点
    # 查找成功返回该后继的 key, val；否则返回 self.inf, None
    # 时间复杂度 O(log log u)
    def successor(self, key):
        if isinstance(key, int) and 0 <= key <= self.veb_u:
            if isinstance(self.veb, TreeNode):
                return self._successor(self.veb, key)
            else:
                # vEB 树为空树
                return self.inf, None
        else:
            print('successor: key invalid:', key)
            return self.inf, None

    def _successor(self, v, key):
        if isinstance(v, TreeNode):
            assert v.power >= 0 and v.u == (1 << v.power) and v.sqrt_u == (1 << (v.power >> 1))
            # 基本情况：当 power=1 (也即 u=2 和 sqrt_u=1) 时，为叶结点，至多含两个值 min/max
            if v.power == 1:
                # 当前是叶结点，如果 key 比 min_key 小，则后继为 min
                if v.min_key != self.inf and key < v.min_key:
                    return v.min_key, v.min_val
                # 如果 key 等于 min_key 并且 max 存在，则后继为 max
                elif v.min_key != self.inf and key == v.min_key and v.max_key != self.inf and key < v.max_key:
                    return v.max_key, v.max_val
                # 否则找不到后继结点
                else:
                    return self.inf, None
            # 如果当前不是叶结点，且 key 小于当前结点的 min_key，则 min 就是其后继
            elif v.min_key != self.inf and key < v.min_key:
                return v.min_key, v.min_val
            else:
                hi = self.high(key, v.power)
                lo = self.low(key, v.power)
                # 注意：由于 Lazy Insertion 策略，当前 key 可能不会被插入 v.cluster[hi] 中
                # 如果 v.cluster[hi] 不存在，表示当前 key 是该簇中的唯一元素，所以要查 summary
                is_succ_in = False  # 标志 key 的后继是否位于 key 应在的簇 v.cluster[hi] 中
                if hi in v.cluster and isinstance(v.cluster[hi], TreeNode):
                    # 获得 key 对应簇中的最大元素
                    max_low = v.cluster[hi].max_key
                    # 根据簇内偏移 lo，如果该簇中存在大于 key 的元素，则后继就在此簇中
                    if max_low != self.inf and lo < max_low:
                        is_succ_in = True
                # 如果在簇不存在或者该簇中找不到后继，则通过查 summary 来确定后继所在的 cluster
                # 而不是顺序遍历各个 cluster 来检查，从而提高了速度
                if is_succ_in:
                    offset_key, offset_val = self._successor(v.cluster[hi], lo)
                    return (hi << (v.power >> 1)) + offset_key, offset_val
                else:
                    # 关键是找簇号 succ_key 而非值元素 succ_val
                    succ_key, succ_val = self._successor(v.summary, hi)
                    if succ_key != self.inf:
                        assert succ_key in v.cluster and isinstance(v.cluster[succ_key], TreeNode)
                        # 找到后继簇号后，从此簇中获取最小元素
                        offset_key = v.cluster[succ_key].min_key
                        return (succ_key << (v.power >> 1)) + offset_key, v.cluster[succ_key].min_val
                    else:
                        # 找不到后继簇号，没有后继
                        return self.inf, None
        else:
            return self.inf, None

    # 根据 key 值查找前驱结点
    # 查找成功返回该前驱的 key, val；否则返回 inf, None
    # 时间复杂度 O(log log u)
    def predecessor(self, key):
        if isinstance(key, int) and 0 <= key <= self.veb_u:
            if isinstance(self.veb, TreeNode):
                return self._predecessor(self.veb, key)
            else:
                # vEB 树为空树
                return self.inf, None
        else:
            print('predecessor: key invalid:', key)
            return self.inf, None

    def _predecessor(self, v, key):
        if isinstance(v, TreeNode):
            assert v.power >= 0 and v.u == (1 << v.power) and v.sqrt_u == (1 << (v.power >> 1))
            # 基本情况：当 power=1 (也即 u=2 和 sqrt_u=1) 时，为叶结点，至多含两个值 min/max
            if v.power == 1:
                # 当前是叶结点，如果 key 比 max_key 大，则前驱为 max
                if v.max_key != self.inf and key > v.max_key:
                    return v.max_key, v.max_val
                # 如果 key 等于 max_key 并且 min 存在，则前驱为 min
                elif v.max_key != self.inf and key == v.max_key and v.min_key != self.inf and key > v.min_key:
                    return v.min_key, v.min_val
                # 否则找不到后继结点
                else:
                    return self.inf, None
            # 如果当前不是叶结点，且 key 大于当前结点的 max_key，则 max 就是其前驱
            elif v.max_key != self.inf and key > v.max_key:
                return v.max_key, v.max_val
            else:
                hi = self.high(key, v.power)
                lo = self.low(key, v.power)
                # 注意：由于 Lazy Insertion 策略，当前 key 可能不会被插入 v.cluster[hi] 中
                # 如果 v.cluster[hi] 不存在，表示当前 key 是该簇中的唯一元素，所以要查 summary
                is_pred_in = False  # 标志 key 的前驱是否位于 key 应在的簇 v.cluster[hi] 中
                if hi in v.cluster and isinstance(v.cluster[hi], TreeNode):
                    # 获得 key 对应簇中的最小元素
                    min_low = v.cluster[hi].min_key
                    # 根据簇内偏移 lo，如果该簇中存在小于 key 的元素，则前驱就在此簇中
                    if min_low != self.inf and lo > min_low:
                        is_pred_in = True
                # 如果在簇不存在或者该簇中找不到前驱，则通过查 summary 来确定前驱所在的 cluster
                # 而不是顺序遍历各个 cluster 来检查，从而提高了速度
                if is_pred_in:
                    offset_key, offset_val = self._predecessor(v.cluster[hi], lo)
                    return (hi << (v.power >> 1)) + offset_key, offset_val
                else:
                    # 关键是找簇号 pred_key 而非值元素 pred_val
                    pred_key, pred_val = self._predecessor(v.summary, hi)
                    if pred_key != self.inf:
                        assert pred_key in v.cluster and isinstance(v.cluster[pred_key], TreeNode)
                        # 找到前驱簇号后，从此簇中获取最大元素
                        offset_key = v.cluster[pred_key].max_key
                        return (pred_key << (v.power >> 1)) + offset_key, v.cluster[pred_key].max_val
                    else:
                        # 找不到前驱簇号
                        if v.min_key != self.inf and key > v.min_key:
                            # 与求后继不同的附加情况：x 的前驱存在，且是 v.min，因此前驱结点就是 v.min
                            # 但此时会 pred_key 会是 self.inf
                            return v.min_key, v.min_val
                        else:
                            return self.inf, None
        else:
            return self.inf, None

    # 根据 key 值增加结点
    # 插入成功返回 True；否则返回 False
    # 时间复杂度 O(log log u)
    def insert(self, insert_key, insert_val):
        if isinstance(insert_key, int) and 0 <= insert_key <= self.veb_u:
            if isinstance(self.veb, TreeNode):
                return self._insert(self.veb, insert_key, insert_val)
            else:
                # vEB 树为 None 空树，则创建新树根
                new_root = TreeNode(power=self.veb_p)
                new_root.min_key = new_root.max_key = insert_key
                new_root.min_val = new_root.max_val = insert_val
                new_root.summary = TreeNode(power=(self.veb_p >> 1))
                new_root.summary.is_summary = True
                # hi = self.high(insert_key, new_root.summary.power)
                # lo = self.low(insert_key, new_root.summary.power)
                # new_root.summary.cluster[hi]
                self.veb = new_root
                return True
        else:
            print('insert: key invalid:', insert_key)
            return False

    # 辅助操作：将元素插入一个空的树结点中
    @staticmethod
    def _insert_empty(v, insert_key, insert_val):
        assert isinstance(v, TreeNode)
        v.min_key = v.max_key = insert_key
        v.min_val = v.max_val = insert_val

    def _insert(self, v, insert_key, insert_val):
        assert isinstance(v, TreeNode)
        # 如果当前结点 v 为空 (没有 min/max)，则调用 _insert_empty
        if v.min_key == self.inf:
            self._insert_empty(v, insert_key, insert_val)
        # 当前结点 v 不为空，某个元素 (不一定是 insert_key) 会被插入到 v 的一个簇中
        else:
            # vEB 默认不重复插入，为了支持重复的 key 插入，
            # 这里采用 OverWrite 重写覆盖机制，如果 key 相同，则新 val 覆盖旧 val
            # 如果插入的 insert_key 等于 v.min 或 v.max，则替换其值
            if insert_key == v.min_key:
                v.min_val = insert_val  # 这里不返回，而是继续往下修改所有 key 相同的 min_val
            if insert_key == v.max_key:
                v.max_val = insert_val  # 这里不返回，而是继续往下修改所有 key 相同的 max_val
            # 插入的 insert_key 比 v 的最小关键字还小，则需更换 v.min
            if insert_key < v.min_key:
                # 交换 key/val
                temp = insert_key
                insert_key = v.min_key
                v.min_key = temp

                temp = insert_val
                insert_val = v.min_val
                v.min_val = temp
            # 如果 v 不是叶结点
            if v.power > 1:
                hi = self.high(insert_key, v.power)
                lo = self.low(insert_key, v.power)
                # 若无 v.cluster[hi] 则新建一个
                if not (hi in v.cluster):
                    new_c = TreeNode(power=(v.power >> 1))
                    # 如果当前结点是 summary 摘要结点，则其 cluster 结点也都是 summary
                    if v.is_summary:
                        new_c.is_summary = True
                    v.cluster[hi] = new_c
                assert hi in v.cluster and isinstance(v.cluster[hi], TreeNode)
                # 目标插入的簇为空
                if v.cluster[hi].min_key == self.inf:
                    # 若无 summary 则新建一个
                    if not isinstance(v.summary, TreeNode):
                        new_s = TreeNode(power=(v.power >> 1))
                        new_s.is_summary = True
                        v.summary = new_s
                    # 目标簇对应的 summary 位为空，需要插入
                    self._insert(v.summary, hi, insert_val)
                    # 调用 _insert_empty 插入空簇
                    self._insert_empty(v.cluster[hi], lo, insert_val)
                # 目标插入的簇不为空
                else:
                    # 无需更新对应的 summary 位，只需递归插入即可
                    self._insert(v.cluster[hi], lo, insert_val)
            # 视情况更新当前结点 v 的 max
            if insert_key > v.max_key:
                v.max_key = insert_key
                v.max_val = insert_val
        # TODO 考虑插入操作可能的异常情况
        return True

    # 根据 key 值删除结点
    # 注意：这里的删除不会删除、释放结点，而仅是把所有 delete_key 改为 self.inf，相应的 val 改为 None
    # 删除成功则返回被删除结点的 val，否则返回 None
    # 时间复杂度 O(log log u)
    def delete(self, delete_key):
        if isinstance(delete_key, int) and 0 <= delete_key <= self.veb_u:
            if isinstance(self.veb, TreeNode):
                return self._delete(self.veb, delete_key)
            else:
                # vEB 树为空树
                print('delete: 当前 vEB 树为空，没有 key 为', delete_key, '的元素')
                return None
        else:
            print('delete: key invalid:', delete_key)
            return None

    # 实际执行的删除函数，可能递归
    def _delete(self, v, delete_key):
        assert isinstance(v, TreeNode)
        # 如果比最小值还小 或者比最大值还大，则找不到
        if delete_key < v.min_key or delete_key > v.max_key:
            return None
        # 当前结点的 min_key 等于 max_key，表示当前为仅含一个关键字的叶结点
        elif v.min_key == v.max_key:
            if delete_key == v.min_key:
                # 如果 min/max 的关键字值正是目标 delete_key，则删除之
                deleted_val = v.min_val
                v.min_key = v.max_key = self.inf
                v.min_val = v.max_val = None
                return deleted_val
            else:
                # 否则表示找不到目标 delete_key
                return None
        # 当前为叶结点，且 min_key 不等于 max_key，故 min/max 都存在
        elif v.power == 1:
            if v.min_key == delete_key and v.min_key != self.inf:
                # 删除 min_key
                deleted_val = v.min_val
                v.min_key = v.max_key
                v.min_val = v.max_val
                return deleted_val
            elif v.max_key == delete_key and v.max_key != self.inf:
                # 删除 max_key
                deleted_val = v.max_val
                v.max_key = v.min_key
                v.max_val = v.min_val
                return deleted_val
            else:
                # 没有目标删除元素
                return None
        # 当前 v 为内部结点，包含两个或两个以上的元素
        else:
            # 如果欲删除 v 的最小值，需要先用别的元素替换 v.min，再从相应簇中删去用于替换的元素
            deleted_val = None     # 实际被删除元素的 val
            is_substitute = False  # 标志 delete_key 是否被替换
            if delete_key == v.min_key:
                assert isinstance(v.summary, TreeNode)
                first_cluster = v.summary.min_key  # 获取除了 v.min 以外的最小元素所在簇号
                assert first_cluster in v.cluster and isinstance(v.cluster[first_cluster], TreeNode)

                deleted_val = v.min_val
                is_substitute = True

                # 将目标删除的 delete_key/val 置为前述最小元素
                # 注意：要用修正后的相对索引来替换 v.min_key
                delete_key = (first_cluster << (v.power >> 1)) + v.cluster[first_cluster].min_key
                delete_val = v.cluster[first_cluster].min_val
                # 然后用它替换
                v.min_key = delete_key
                v.min_val = delete_val

            # 执行删除
            hi = self.high(delete_key, v.power)
            lo = self.low(delete_key, v.power)
            # 注意：由于 Lazy Insertion 策略，当前 key 可能不会被插入 v.cluster[hi] 中
            # 如果 v.cluster[hi] 不存在，表示当前 key 是该簇中的唯一元素，所以要查 summary
            is_key_in = False  # 标志 key 是否位于 key 应在的簇 v.cluster[hi] 中
            if hi in v.cluster and isinstance(v.cluster[hi], TreeNode):
                is_key_in = True
                if is_substitute:
                    # 如果 delete_key 被替换了，则无需更新 deleted_val
                    self._delete(v.cluster[hi], lo)
                else:
                    # 如果 delete_key 未被替换，则 deleted_val 为此次调用的返回值
                    deleted_val = self._delete(v.cluster[hi], lo)

            # 删除后的处理
            # 判断删除目标元素后的簇是否为空
            if (not is_key_in) or v.cluster[hi].min_key == self.inf:
                assert isinstance(v.summary, TreeNode)
                # 如果为空，则需要把此簇号从 v.summary 中删除
                self._delete(v.summary, hi)
                # 判断删除的是 v.max
                if delete_key == v.max_key:
                    # 如果是，则获取编号最大的非空簇的簇号
                    summary_max = v.summary.max_key
                    if summary_max == self.inf:
                        # 如果所有 v 的簇都为空，则 v 中剩余的元素只有 v.min
                        v.max_key = v.min_key
                        v.max_val = v.min_val
                    else:
                        # 否则，把 summary_max 簇中的最大元素值赋值给 v.max
                        assert summary_max in v.cluster and isinstance(v.cluster[summary_max], TreeNode)
                        # 注意：要用修正后的相对索引来替换 v.max_key
                        v.max_key = (summary_max << (v.power >> 1)) + v.cluster[summary_max].max_key
                        v.max_val = v.cluster[summary_max].max_val
            # 删除目标元素后的簇不为空，此时无需更新 v.summary
            # 但如果删除的是 v.max，还要另选一个元素来更新 v.max
            elif delete_key == v.max_key:
                assert isinstance(v.cluster[hi], TreeNode)
                # 注意：要用修正后的相对索引来替换 v.max_key
                v.max_key = (hi << (v.power >> 1)) + v.cluster[hi].max_key
                v.max_val = v.cluster[hi].max_val
            # 返回实际被删除元素的 val
            return deleted_val


def main():
    # 以插入的方式，构建 vEB Tree
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    kv_array = [[key, [key, key * 100]] for key in range(1, 10)]
    veb = VanEmdeBoasTree(kv_array)

    # 搜索值
    search_key = 7
    start = time.process_time()
    ans_val = veb.search(search_key)  # [7, 700]
    end = time.process_time()

    if ans_val is not None:
        print('找到了 key 为', search_key, '的元素，其值为:', ans_val)
    else:
        print('找不到 key 为', search_key, '的元素')

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 搜索测试 Done
    print('\n搜索测试')
    print(veb.search(0))  # None
    print(veb.search(1))  # [i, i * 100]
    print(veb.search(2))
    print(veb.search(3))
    print(veb.search(4))
    print(veb.search(5))
    print(veb.search(6))
    print(veb.search(7))
    print(veb.search(8))
    print(veb.search(9))
    print(veb.search(10))  # None

    # 插入测试 (测试重写覆盖机制) Done
    # 关键字 5/6/7 的值 [5/6/7, 500/600/700] 被替换为 [5/6/7, 555/666/777]
    new_kv_array = [[key, [key, key * 111]] for key in range(5, 8)]
    for new_kv in new_kv_array:
        veb.insert(new_kv[0], new_kv[1])

    # 后继测试 Done
    print('\n后继测试')
    print(veb.successor(0))  # [i+1, (i+1) * 100] 或 [i+1, (i+1) * 111]
    print(veb.successor(1))
    print(veb.successor(2))
    print(veb.successor(3))
    print(veb.successor(4))
    print(veb.successor(5))
    print(veb.successor(6))
    print(veb.successor(7))
    print(veb.successor(8))
    print(veb.successor(9))  # inf, None
    print(veb.successor(10))  # inf, None

    # 前驱测试 Done
    print('\n前驱测试')
    print(veb.predecessor(0))  # inf, None
    print(veb.predecessor(1))  # inf, None
    print(veb.predecessor(2))  # [i-1, (i-1) * 100] 或 [i-1, (i-1) * 111]
    print(veb.predecessor(3))
    print(veb.predecessor(4))
    print(veb.predecessor(5))
    print(veb.predecessor(6))
    print(veb.predecessor(7))
    print(veb.predecessor(8))
    print(veb.predecessor(9))
    print(veb.predecessor(10))

    # 删除测试 Done
    print('\n删除测试')
    print(veb.delete(0))  # None
    print(veb.delete(1))  # [i, i * 100] 或 [i, i * 111]
    print(veb.delete(2))
    print(veb.delete(3))
    print(veb.delete(4))
    print(veb.delete(5))
    print(veb.delete(6))
    print(veb.delete(7))
    print(veb.delete(8))
    print(veb.delete(9))
    print(veb.delete(10))  # None

    # 搜索测试 (辅助上述删除测试) Done
    print('\n搜索测试')
    print(veb.search(0))  # None
    print(veb.search(1))  # [i, i * 100] 或 [i, i * 111]
    print(veb.search(2))
    print(veb.search(3))
    print(veb.search(4))
    print(veb.search(5))
    print(veb.search(6))
    print(veb.search(7))
    print(veb.search(8))
    print(veb.search(9))
    print(veb.search(10))  # None


if __name__ == "__main__":
    sys.exit(main())
