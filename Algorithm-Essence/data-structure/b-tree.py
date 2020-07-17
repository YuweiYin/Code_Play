#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : b-tree.py
@Author  : YuweiYin
=================================================="""

# import gc
import sys
import time
import random

"""
B-Tree

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 18
https://www.youtube.com/watch?v=TOb1tuEZ2X4
"""


class TreeNode:
    def __init__(self, key=0, val=0):
        # keys 和 vals 列表之间必须逐下标一一对应
        # 即 val_i 对象是 key_i 关键字的卫星数据
        self.keys = [key]    # 当前存储在结点中的关键字列表，关键字升序排列
        self.vals = [val]    # 当前存储在结点中的值元素列表，卫星数据，可以为任意对象
        self.kids = []       # 孩子结点指针列表
        self.parent = None   # 父结点指针
        self.is_leaf = True  # 如果此结点是叶结点，则为 True，否则为 False


class BTree:
    # 构造 B 树
    def __init__(self, kv_array, bf=2):
        self.b_root = None  # B 树的树根
        self.bf = bf  # 分支因子 Branching Factor，默认设置为 2，即 2-3-4 树
        # bf - 1 <= # of keys <= 2 * bf - 1
        # bf <= # of children <= 2 * bf
        assert isinstance(bf, int) and bf >= 2  # bf 需为正整数，且至少为 2

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 TreeNode 并插入 B-Tree
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.insert(kv[0], kv[1])

    # 从外存读取结点 node 的第 kid_index 个孩子结点
    @staticmethod
    def disk_read(node, kid_index):
        # TODO 从外存读取对象（这里代码假设整个 B 树已在主存）
        if isinstance(node, TreeNode) and kid_index < len(node.kids) and \
                isinstance(node.kids[kid_index], TreeNode):
            return True
        return False

    # 将结点 node 写到外存
    @staticmethod
    def disk_write(node):
        # TODO 将结点 node 写到外存（这里代码假设整个 B 树已在主存）
        if isinstance(node, TreeNode):
            return True
        else:
            return False

    # 辅助操作：B-Tree 结点 keys (非降序排列) 的二分搜索
    # 返回 k 在 keys 列表中的索引，如果不存在返回当前下标
    def _binary_search(self, keys, lo, hi, k):
        assert isinstance(keys, list) and isinstance(lo, int) and isinstance(hi, int)
        n_keys = len(keys)
        if n_keys == 0:
            return n_keys
        # 越界情况
        if lo < 0:
            lo = 0
        if hi >= n_keys:
            hi = n_keys - 1
        # 根据下标大小分情况处理
        if lo == hi:
            return lo if k <= keys[lo] else lo + 1
        elif lo < hi:
            mid = int((lo + hi) >> 1)
            # 目标 k 匹配 mid 位置的值，返回 mid
            if k == keys[mid]:
                return mid
            # 目标 k 小于 mid 位置的值，往左看
            elif k < keys[mid]:
                return self._binary_search(keys, lo, mid - 1, k)
            # 目标 k 大于 mid 位置的值，往右看
            else:
                return self._binary_search(keys, mid + 1, hi, k)
        else:
            # 不存在
            return lo

    # 根据 key 值搜索结点
    # 如果搜索到了，则返回结点 TreeNode 及其孩子下标 kid_index
    # 如果搜索不到，则返回 None, -1
    def search(self, search_key):
        if isinstance(self.b_root, TreeNode):
            return self._search(self.b_root, search_key)
        else:
            # 当前树为空，找不到目标结点
            return None, -1

    def _search(self, root, search_key):
        if isinstance(root, TreeNode):
            # key_index = 0  # 当前结点的关键字索引，如果找不到，就是孩子结点索引
            # 线性扫描当前结点的每个关键字，在当前结点中找出下标 kid_index，
            # 使得 search_key 搜索目标关键字 小于等于 root 的某个孩子的关键字
            # while key_index < len(root.keys) and search_key > root.keys[key_index]:
            #     key_index += 1
            key_index = self._binary_search(root.keys, 0, len(root.keys) - 1, search_key)
            # 检查是否已找到关键字
            if 0 <= key_index < len(root.keys) and search_key == root.keys[key_index]:
                return root, key_index
            # 如果找不到，判断当前结点 root 是否为叶子，如果是，则表示没有此元素
            elif root.is_leaf:
                return None, -1
            # 如果当前结点 root 是中间结点，从外存读取孩子结点
            else:
                if self.disk_read(root, key_index):
                    return self._search(root.kids[key_index], search_key)
                else:
                    # 读外存失败
                    print('_search: Path 2')
                    return None, -1
        else:
            # root 结点类型异常
            print('_search: Path 1')
            return None, -1

    # 辅助操作：新建树结点
    def create_new_node(self, new_key=0, new_val=0):
        new_node = TreeNode(new_key, new_val)
        if self.disk_write(new_node):
            return new_node
        else:
            return None

    # 根据 key 值增加结点
    # 先找到插入位置，将新结点插入已存在的叶结点上，
    # (分叉因子记为 bf)，如果是要插入到一个"满"了的叶结点，即该叶结点已有 (2 * bf - 1) 个关键字
    # 则需先将此叶结点分裂，下标为 bf 的中间 key 提升到父结点中，左右各 (bf - 1) 个 key 分裂为左右孩子
    # 而且如果提升前 父结点也是满的，那么也需要以同样的方式分裂父结点，以此类推
    # 另外，并不是等到插入时才逐级向上维护 B 树性质，而是在定位插入位置的搜索路径中，将遇到的满结点分裂开来
    # 时间复杂度 O(log n) 与树高有关
    # 插入成功返回 True；否则返回 False
    def insert(self, insert_key, insert_val):
        if isinstance(self.b_root, TreeNode):
            root = self.b_root
            # 处理树根为满的情况
            if len(root.keys) == ((self.bf << 1) - 1):
                new_root = self.create_new_node()
                new_root.is_leaf = False
                new_root.keys = []
                new_root.vals = []
                new_root.kids = [root]
                root.parent = new_root
                self.b_root = new_root
                self.split_kids(self.b_root, 0)
                return self._insert_not_full(new_root, insert_key, insert_val)
            else:
                return self._insert_not_full(root, insert_key, insert_val)
        else:
            # 当前树为空
            new_node = TreeNode(insert_key, insert_val)
            self.b_root = new_node
            return True

    # 从一个非满的子树树根 root 插入一个非满的结点
    # 插入成功返回 True；否则返回 False
    def _insert_not_full(self, root, insert_key, insert_val):
        if isinstance(root, TreeNode):
            i = self._binary_search(root.keys, 0, len(root.keys) - 1, insert_key)
            # 如果当前 root 为叶结点，则插入到此叶结点（已确保非满）
            if root.is_leaf:
                # 插入 key/val
                root.keys.insert(i, insert_key)
                root.vals.insert(i, insert_val)
                # 将有修改的 root 结点写回外存
                return self.disk_write(root)
            # 如果当前 root 不是叶结点，则寻找一个孩子结点
            else:
                # 从外存读入孩子结点
                if self.disk_read(root, i):
                    # 如果此孩子满了，则先将此孩子分裂
                    if len(root.kids[i].keys) == ((self.bf << 1) - 1):
                        self.split_kids(root, i)
                        # 分裂之后 观察提升上来的 key，决定是否调整 i 下标
                        if insert_key > root.keys[i]:
                            i += 1
                    # 递归，往当前结点 root 的第 i 个孩子中插入新 key/val
                    return self._insert_not_full(root.kids[i], insert_key, insert_val)
                else:
                    # 读外存失败
                    print('_insert_not_full: Path 2')
                    return False
        else:
            # root 结点类型异常
            print('_insert_not_full: Path 1')
            return False

    # 辅助操作：分裂结点
    # 将 node 结点的第 kid_index 个孩子分裂开来
    # 注意：此时 node 结点不应是满结点，而其第 kid_index 个孩子是满结点（有 2 * bf - 1 个 keys）
    def split_kids(self, node, kid_index):
        if isinstance(node, TreeNode) and not node.is_leaf and kid_index < len(node.kids):
            kid = node.kids[kid_index]
            if isinstance(kid, TreeNode):
                if len(node.keys) < ((self.bf << 1) - 1) and len(kid.keys) == ((self.bf << 1) - 1):
                    new_right_kid = self.create_new_node()
                    new_right_kid.keys = []
                    new_right_kid.vals = []
                    new_right_kid.is_leaf = kid.is_leaf  # 如果 kid 是叶结点，则 new_right_kid 也是叶结点
                    new_right_kid.parent = node

                    # 把 kid 的后 bf - 1 个 key/val 分给 new_right_kid
                    for i in range(self.bf - 1):
                        new_right_kid.keys.append(kid.keys[i + self.bf])
                        new_right_kid.vals.append(kid.vals[i + self.bf])
                    # 如果 kid 不是叶结点，则把其后 bf 个孩子分给 new_right_kid
                    if not kid.is_leaf:
                        for i in range(self.bf):
                            new_right_kid.kids.append(kid.kids[i + self.bf])

                    # node 结点的各列表新增一个占位元素
                    node.kids.append(TreeNode())
                    node.keys.append(0)
                    node.vals.append(0)

                    # 将 node 结点 kid_index 下标右侧的 kid 全部右移，准备把 new_right_kid 插入
                    # node 结点有 len(node.keys) + 1 个孩子
                    for i in reversed(range(kid_index + 2, len(node.keys) + 1)):
                        node.kids[i] = node.kids[i - 1]
                    # 把 new_right_kid 插入 node 结点
                    node.kids[kid_index + 1] = new_right_kid

                    # 将 node 结点从 kid_index 下标开始的 key/val 全部右移，准备把中间的 key/val 插入
                    for i in reversed(range(kid_index + 1, len(node.keys))):
                        node.keys[i] = node.keys[i - 1]
                        node.vals[i] = node.vals[i - 1]
                    # 将中间的 key/val 提升到 node 结点
                    node.keys[kid_index] = kid.keys[self.bf - 1]
                    node.vals[kid_index] = kid.vals[self.bf - 1]

                    # 修改 kid 的 key/val/kids 列表、关键字数目，作为分裂出的左孩子
                    kid.keys = kid.keys[:(self.bf - 1)]  # kid 剩余 bf - 1 个关键字
                    kid.vals = kid.vals[:(self.bf - 1)]  # kid 剩余 bf - 1 个值对象
                    kid.kids = kid.kids[:self.bf]        # kid 剩余 bf 个孩子

                    # 将有修改的三个结点写回外存
                    self.disk_write(node)
                    self.disk_write(kid)
                    self.disk_write(new_right_kid)
                else:
                    # node 或 kid 结点的 keys 列表长度异常
                    print('split_kids: Error Path 3')
            else:
                # kid 结点类型异常
                print('split_kids: Error Path 2')
        else:
            # node 结点类型异常
            print('split_kids: Error Path 1')

    # 根据 key 值删除结点
    # 如果删除成功，则返回被删的 key, val
    # 如果删除失败，则返回 None, None
    def delete(self, delete_key):
        if isinstance(self.b_root, TreeNode):
            deleted_key, deleted_val = self._delete(self.b_root, delete_key)
            # 删除之后，检查树根是否被删除成了个空结点（没有 key/val）
            if len(self.b_root.keys) == 0:
                assert len(self.b_root.keys) == len(self.b_root.vals)
                assert len(self.b_root.kids) <= 1
                # 如果只有一个 kid，则将此唯一 kid 作为新的树根
                if len(self.b_root.kids) == 1:
                    deleted_root = self.b_root
                    self.b_root = self.b_root.kids[0]
                    self.b_root.parent = None
                    del deleted_root
                # 如果没有 kid，则表示此 B 树全被删空了
                else:
                    del self.b_root
                    self.b_root = None
            return deleted_key, deleted_val
        else:
            # 当前树为空，找不到目标结点，删除失败
            return None, -1

    # 实际执行的删除函数，可能递归
    def _delete(self, root, delete_key):
        assert isinstance(root, TreeNode)
        # 约定此时结点（如果不是树根）的关键字数目不少于 bf
        if root != self.b_root:
            assert len(root.keys) >= self.bf

        # 扫描当前叶结点，判断 delete_key 是否在结点中
        # key_index = 0
        # for key in root.keys:
        #     if delete_key == key:
        #         break
        #     key_index += 1
        key_index = self._binary_search(root.keys, 0, len(root.keys) - 1, delete_key)

        # 分情况处理（实际发生的删除都是在叶结点上）
        if root.is_leaf:
            # case 1: 如果 x 是叶结点，且关键字 k 在结点 x 中，则直接从 x 中删除 k
            # if key_index < len(root.keys):
            if 0 <= key_index < len(root.keys) and root.keys[key_index] == delete_key:
                # 直接删除 delete_key
                deleted_key = root.keys.pop(key_index)
                deleted_val = root.vals.pop(key_index)
                return deleted_key, deleted_val
            else:
                # 叶结点中都找不到 delete_key，表示树中没有 delete_key，删除失败
                return None, None
        else:
            # case 2: 如果 x 是内部结点，且关键字 k 在结点 x 中
            # if key_index < len(root.keys):
            if 0 <= key_index < len(root.keys) and root.keys[key_index] == delete_key:
                # 关键字 k 左右的孩子结点分别称为 left_kid 和 right_kid
                left_kid = root.kids[key_index]
                right_kid = root.kids[key_index + 1]
                # 确认 left_kid 和 right_kid 结点属性的合法性
                assert isinstance(left_kid, TreeNode) and isinstance(right_kid, TreeNode)
                assert isinstance(left_kid.keys, list) and isinstance(right_kid.keys, list)
                l_len = len(left_kid.keys)
                r_len = len(right_kid.keys)
                assert (self.bf - 1) <= l_len <= ((self.bf << 1) - 1) and l_len == len(left_kid.vals)
                if not left_kid.is_leaf:   # 叶结点无孩子
                    assert l_len == len(left_kid.kids) - 1
                assert (self.bf - 1) <= r_len <= ((self.bf << 1) - 1) and r_len == len(right_kid.vals)
                if not right_kid.is_leaf:  # 叶结点无孩子
                    assert r_len == len(right_kid.kids) - 1

                if len(left_kid.keys) >= self.bf:
                    # case 2.1: 如果子结点 left_kid 中至少包含 bf 个关键字
                    # 则找出关键字 k 在以 left_kid 为根的子树中的 前驱 k'
                    # 在 x 中用 k' 替代 k，并在 y 中递归删除 k'

                    # 记录被替换的 key/val
                    deleted_key = root.keys[key_index]  # 记录被替换的 key
                    deleted_val = root.vals[key_index]  # 记录被替换的 val
                    assert deleted_key == delete_key

                    # 用前驱的 key/val 替换被删除的 key/val
                    predecessor_key, predecessor_val = self.predecessor(root, key_index)
                    root.keys[key_index] = predecessor_key
                    root.vals[key_index] = predecessor_val
                    # 在 left_kid 中递归删除 predecessor_key
                    self._delete(left_kid, predecessor_key)
                    return deleted_key, deleted_val  # 此时被替换的 key/val 就是目标删除的 key/val
                elif len(right_kid.keys) >= self.bf:
                    # case 2.2: 如果子结点 left_kid 中的关键字数目少于 bf，则检查子结点 right_kid
                    # 如果 right_kid 中至少包含 bf 个关键字，则找出关键字 k 在以 right_kid 为根的子树中的 后继 k''
                    # 在 x 中用 k'' 替代 k，并在 right_kid 中递归删除 k''

                    # 记录被替换的 key/val
                    deleted_key = root.keys[key_index]  # 记录被替换的 key
                    deleted_val = root.vals[key_index]  # 记录被替换的 val
                    assert deleted_key == delete_key

                    # 用后继的 key/val 替换被删除的 key/val
                    successor_key, successor_val = self.successor(root, key_index)
                    root.keys[key_index] = successor_key
                    root.vals[key_index] = successor_val
                    # 在 right_kid 中递归删除 successor_key
                    self._delete(right_kid, successor_key)
                    return deleted_key, deleted_val  # 此时被替换的 key/val 就是目标删除的 key/val
                else:
                    # case 2.3: 否则，如果 left_kid 和 right_kid 都只含有 (bf - 1) 个关键字，
                    # 则将关键字 k 和子结点 right_kid 中的所有关键字都合并进入子结点 left_kid（此时 left_kid 结点变为满结点）
                    # 然后释放子结点 right_kid，并递归地在子结点 left_kid 中删除关键字 k

                    deleted_key = root.keys.pop(key_index)  # 弹出被删除的 key
                    assert deleted_key == delete_key
                    deleted_val = root.vals.pop(key_index)  # 弹出被删除的 val
                    right_kid = root.kids.pop(key_index + 1)  # 弹出右侧孩子 right_kid
                    assert isinstance(right_kid, TreeNode)
                    # 先把目标删除的 key/val 增添到 left_kid 尾部
                    left_kid.keys.append(deleted_key)
                    left_kid.vals.append(deleted_val)
                    # 再让 left_kid 与 right_kid 列表连接
                    left_kid.keys.extend(right_kid.keys)
                    left_kid.vals.extend(right_kid.vals)
                    if len(left_kid.kids) > 0 or len(right_kid.kids) > 0:
                        left_kid.kids.extend(right_kid.kids)  # 此二者若为叶结点，则无孩子结点，所以做此判断
                    return self._delete(left_kid, delete_key)
            # case 3: 如果 x 是内部结点，且关键字 k 不在结点 x 中
            else:
                kid_index = 0
                n_keys = len(root.keys)
                if n_keys == 0:
                    # 这表明当前 x 为整个 B 树的树根，且其中没有关键字、只有一个孩子
                    assert len(root.kids) == 1
                else:
                    # 扫描当前内部结点 x，判断 delete_key 应在在 x 的哪个孩子结点中
                    # while kid_index < n_keys and root.keys[kid_index] < delete_key:
                    #     kid_index += 1
                    kid_index = self._binary_search(root.keys, 0, len(root.keys) - 1, delete_key)
                assert kid_index < len(root.kids)

                # delete_key 所在的孩子结点 kid
                kid = root.kids[kid_index]
                # 确认 kid 结点属性的合法性
                assert isinstance(kid, TreeNode) and isinstance(kid.keys, list)
                kid_len = len(kid.keys)
                assert (self.bf - 1) <= kid_len <= ((self.bf << 1) - 1) and kid_len == len(kid.vals)
                if not kid.is_leaf:  # 叶结点无孩子
                    assert kid_len == len(kid.kids) - 1

                # case 3.0: 如果 kid 结点的关键字数目不少于 bf，
                # 则于其中删除一个关键字不会导致 B 树性质破坏，因此直接递归地在 kid 中删除
                if len(kid.keys) >= self.bf:
                    return self._delete(kid, delete_key)
                # case 3.1 和 3.2: kid 结点的关键字数目为 bf - 1，则观察其左右兄弟结点
                else:
                    # delete_key 所在的孩子结点 kid 左右的兄弟结点分别称为 left_bro 和 right_bro
                    # 如果 kid 是最左孩子，则没有 left_bro；如果 kid 是最右孩子，则没有 right_bro
                    left_bro = root.kids[kid_index - 1] if kid_index > 0 else None
                    right_bro = root.kids[kid_index + 1] if kid_index < len(root.kids) - 1 else None

                    # 确认 kid、left_bro 和 right_bro 结点属性的合法性
                    if left_bro is not None:
                        assert isinstance(left_bro, TreeNode) and isinstance(left_bro.keys, list)
                        l_len = len(left_bro.keys)
                        assert (self.bf - 1) <= l_len <= ((self.bf << 1) - 1) and l_len == len(left_bro.vals)
                        assert left_bro.is_leaf == kid.is_leaf
                        if not left_bro.is_leaf:  # 叶结点无孩子
                            assert l_len == len(left_bro.kids) - 1
                    if right_bro is not None:
                        assert isinstance(right_bro, TreeNode) and isinstance(right_bro.keys, list)
                        r_len = len(right_bro.keys)
                        assert (self.bf - 1) <= r_len <= ((self.bf << 1) - 1) and r_len == len(right_bro.vals)
                        assert right_bro.is_leaf == kid.is_leaf
                        if not right_bro.is_leaf:  # 叶结点无孩子
                            assert r_len == len(right_bro.kids) - 1

                    # case 3.1: 如果 kid 只含有 (bf - 1) 个关键字，但是它的一个相邻的兄弟结点至少包含 bf 个关键字，
                    # 则将 x 中的某个关键字下降至 kid 中，再将 kid 相邻的左兄弟或右兄弟结点 bro 的一个关键字提升到 x 中，
                    # 而 bro 结点的相应孩子指针也移动到 kid 中。（此乃移花接木、李代桃僵之术也。）
                    if left_bro is not None and len(left_bro.keys) >= self.bf:
                        # 先从左兄弟（如果存在）中"借"关键字
                        borrow_key = left_bro.keys.pop()  # 借左兄弟的最右 key
                        borrow_val = left_bro.vals.pop()  # 借左兄弟的最右 val

                        # 借来的 key/val 提升到 x 中
                        substitute_key = root.keys[kid_index - 1]  # 记录 x 中被替换的 key
                        substitute_val = root.vals[kid_index - 1]  # 记录 x 中被替换的 val
                        root.keys[kid_index - 1] = borrow_key
                        root.vals[kid_index - 1] = borrow_val

                        # x 中被替换的 key/val 以及从左兄弟借来的孩子 一起加入到 kid
                        kid.keys.insert(0, substitute_key)
                        kid.vals.insert(0, substitute_val)
                        if not kid.is_leaf:
                            borrow_kid = left_bro.kids.pop()  # 借左兄弟的最右孩子
                            kid.kids.insert(0, borrow_kid)

                        # 递归地从 kid 中删除目标关键字
                        return self._delete(kid, delete_key)
                    elif right_bro is not None and len(right_bro.keys) >= self.bf:
                        # 左兄弟不存在或者关键字数量不足，则从右兄弟（如果存在）中"借"关键字
                        borrow_key = right_bro.keys.pop(0)  # 借右兄弟的最左 key
                        borrow_val = right_bro.vals.pop(0)  # 借右兄弟的最左 val

                        # 借来的 key/val 提升到 x 中
                        substitute_key = root.keys[kid_index]  # 记录 x 中被替换的 key
                        substitute_val = root.vals[kid_index]  # 记录 x 中被替换的 val
                        root.keys[kid_index] = borrow_key
                        root.vals[kid_index] = borrow_val

                        # x 中被替换的 key/val 以及从右兄弟借来的孩子 一起加入到 kid
                        kid.keys.append(substitute_key)
                        kid.vals.append(substitute_val)
                        if not kid.is_leaf:
                            borrow_kid = right_bro.kids.pop(0)  # 借右兄弟的最左孩子
                            kid.kids.append(borrow_kid)

                        # 递归地从 kid 中删除目标关键字
                        return self._delete(kid, delete_key)
                    # case 3.2: 如果 kid 和其所有相邻兄弟结点都只包含 (bf - 1) 个关键字
                    # （表示 kid 没法从兄弟结点“借”关键字来维持 B 树性质），则将 kid 与其某一个兄弟结点合并。
                    # 此后在 kid 中递归地删除目标关键字 k。
                    else:
                        if left_bro is not None:
                            # 如果左兄弟存在，则和左兄弟合并
                            down_key = root.keys.pop(kid_index - 1)  # 从 x 中下降的 key
                            down_val = root.vals.pop(kid_index - 1)  # 从 x 中下降的 val
                            left_bro = root.kids.pop(kid_index - 1)  # 弹出左兄弟结点

                            # 进行合并
                            kid.keys.insert(0, down_key)
                            kid.vals.insert(0, down_val)
                            kid.keys = left_bro.keys + kid.keys
                            kid.vals = left_bro.vals + kid.vals
                            if not kid.is_leaf:
                                kid.kids = left_bro.kids + kid.kids

                            # 递归地从 kid 中删除目标关键字
                            return self._delete(kid, delete_key)
                        elif right_bro is not None:
                            # 如果左兄弟不存在但右兄弟存在，则和右兄弟合并
                            down_key = root.keys.pop(kid_index)  # 从 x 中下降的 key
                            down_val = root.vals.pop(kid_index)  # 从 x 中下降的 val
                            right_bro = root.kids.pop(kid_index + 1)  # 弹出右兄弟结点

                            # 进行合并
                            kid.keys.append(down_key)
                            kid.vals.append(down_val)
                            kid.keys.extend(right_bro.keys)
                            kid.vals.extend(right_bro.vals)
                            if not kid.is_leaf:
                                kid.kids.extend(right_bro.kids)

                            # 递归地从 kid 中删除目标关键字
                            return self._delete(kid, delete_key)
                        else:
                            # 左右兄弟都不存在，则这只表明一种情况：
                            # 当前 root 是树根，且只有一个孩子，关键字数量不超过 1
                            assert root == self.b_root and len(root.kids) == 1
                            assert len(root.keys) == len(root.vals) <= 1
                            assert kid_index == 0
                            # 如果有一个关键字，则将此树根关键字下降到其唯一孩子处
                            # （树高度缩减的工作会在结束 delete 函数中处理）
                            if len(root.keys) == len(root.vals) == 1:
                                down_key = root.keys.pop(0)  # 从 x 中下降的 key
                                down_val = root.vals.pop(0)  # 从 x 中下降的 val
                                assert len(kid.keys) > 0
                                # 根据唯一孩子中的 key 相对于 root 中唯一 key 的大小来决定插入位置 (首部 or 尾部)
                                if down_key <= kid.keys[0]:
                                    kid.keys.insert(0, down_key)
                                    kid.vals.insert(0, down_val)
                                else:
                                    kid.keys.append(down_key)
                                    kid.vals.append(down_val)
                            # 此时保证 root 不含关键字，直接删除之，并修改根结点指针
                            deleted_root = self.b_root
                            self.b_root = kid
                            kid.parent = None
                            del deleted_root
                            # 递归地从 kid 中删除目标关键字
                            return self._delete(kid, delete_key)

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def clear_node_link(node):
        if isinstance(node, TreeNode):
            node.parent = None
            node.keys = []
            node.vals = []
            node.kids = []

    # 找到一棵以 root 为根的 B-Tree 中的最小值结点（一路向左）
    # 返回目标结点的 key/val
    # 时间复杂度 O(log n) 与树高有关
    @staticmethod
    def min_bst(root):
        assert isinstance(root, TreeNode)
        ptr = root
        # 一路向左找到最左叶结点
        while not ptr.is_leaf:
            assert isinstance(ptr.kids, list) and len(ptr.kids) > 0
            ptr = ptr.kids[0]
        # 如果此叶结点合法，则返回最左元素的 key/val
        assert isinstance(ptr, TreeNode) and isinstance(ptr.keys, list) and len(ptr.keys) > 0
        assert isinstance(ptr.vals, list) and len(ptr.vals) > 0 and (len(ptr.keys) == len(ptr.vals))
        return ptr.keys[0], ptr.vals[0]  # 返回目标 key/val

    # 找到一棵以 root 为根的 B-Tree 中的最大值结点（一路向右）
    # 返回目标结点的 key/val
    # 时间复杂度 O(log n) 与树高有关
    @staticmethod
    def max_bst(root):
        assert isinstance(root, TreeNode)
        ptr = root
        # 一路向右找到最右叶结点
        while not ptr.is_leaf:
            assert isinstance(ptr.kids, list) and len(ptr.kids) > 0
            ptr = ptr.kids[len(ptr.kids) - 1]
        # 如果此叶结点合法，则返回最右元素的 key/val
        assert isinstance(ptr, TreeNode) and isinstance(ptr.keys, list) and len(ptr.keys) > 0
        assert isinstance(ptr.vals, list) and len(ptr.vals) > 0 and (len(ptr.keys) == len(ptr.vals))
        return ptr.keys[len(ptr.keys) - 1], ptr.vals[len(ptr.vals) - 1]  # 返回目标 key/val

    # 找到在 B-Tree 中结点 node 的关键字 key_index 的前驱结点
    # 如果 node 的左孩子存在，则 node 的前驱就是其左子树中的最大值
    # TODO 如果 node 的左孩子不存在，则 node 的前驱是其某个祖先结点 a，满足此时 a.right == node
    # 返回目标结点的 key/val
    # 时间复杂度 O(log n) 与树高有关
    def predecessor(self, node, key_index):
        assert isinstance(node, TreeNode) and len(node.keys) == len(node.vals)
        assert key_index < len(node.keys) and (len(node.kids) == len(node.keys) + 1)
        return self.max_bst(node.kids[key_index])

    # 找到在 B-Tree 中结点 node 的关键字 key_index 的后继结点
    # 如果 node 的右孩子存在，则 node 的后继就是其右子树中的最小值
    # TODO 如果 node 的右孩子不存在，则 node 的前驱是其某个祖先结点 a，满足此时 a.left == node
    # 返回目标结点的 key/val
    # 时间复杂度 O(log n) 与树高有关
    def successor(self, node, key_index):
        assert isinstance(node, TreeNode) and len(node.keys) == len(node.vals)
        assert key_index < len(node.keys) and (len(node.kids) == len(node.keys) + 1)
        return self.min_bst(node.kids[key_index + 1])


# 随机打乱数组
class ShuffleArray:
    def __init__(self, array):
        self.array = array

    def do_shuffle(self):
        if isinstance(self.array, list) and len(self.array) > 1:
            # 从最高的 index 开始降到 1，每次生成 0～index-1 的随机数，与 index=index 的元素交换
            for i in reversed(range(1, len(self.array))):
                self._exchange(i, self._get_random_int(i - 1))
        else:
            print('The so-called array is NOT a list!')

    # 按下标生成随机数
    def _get_random_int(self, index):
        random.seed(id(self.array[index]))  # 以对象的唯一标识符 id 作为随机数种子
        return random.randint(0, index)     # 生成 0～index 的整型随机数

    # 按下标交换 self.array 中的两个元素
    def _exchange(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp


def main():
    # 以插入的方式，构建 B-Tree
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    # kv_array = [
    #     [1, 100], [2, 200], [3, 300], [7, 700],
    #     [8, 800], [9, 900], [4, 400]
    # ]
    kv_array = [[i, 100 * i] for i in range(1, 21)]

    # 以插入的方式建立 B-Tree
    # key 有序地插入可能会导致 B-Tree 高度过高，很多结点可能仅存储了一个关键字
    # 但是如果有删除操作，则会调整树结构、压低树高、提升结点利用率
    b_tree = BTree(kv_array, bf=2)  # 分支因子 bf=2 为默认值，此时为 2-3-4 树。bf 不能小于 2

    # 搜索值
    search_key = 4
    start = time.process_time()
    res_node, key_index = b_tree.search(search_key)
    end = time.process_time()

    if res_node is not None and isinstance(res_node, TreeNode) and \
            key_index < len(res_node.keys):
        print('搜索: 找到了 key 为', res_node.keys[key_index], '的元素，其值为:', res_node.vals[key_index])
    else:
        print('搜索: 找不到 key 为', search_key, '的元素')

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 删除结点，通过 debug 模式观察树结构的正确变化
    delete_key = 27
    del_key, del_val = b_tree.delete(delete_key)  # 找不到, case 3.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 20
    del_key, del_val = b_tree.delete(delete_key)  # case 1
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 18
    del_key, del_val = b_tree.delete(delete_key)  # case 2.3
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 15
    del_key, del_val = b_tree.delete(delete_key)  # case 2.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 13
    del_key, del_val = b_tree.delete(delete_key)  # case 3.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 19
    del_key, del_val = b_tree.delete(delete_key)  # case 3.2 & case 2.1
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 7
    del_key, del_val = b_tree.delete(delete_key)  # case 3.1 & case 3.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    delete_key = 4
    del_key, del_val = b_tree.delete(delete_key)  # case 2.3 & case 2.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    # 删成空树，通过 debug 模式观察树结构的正确变化
    b_tree.delete(5)
    b_tree.delete(12)
    b_tree.delete(6)
    b_tree.delete(3)
    b_tree.delete(1)
    b_tree.delete(10)
    b_tree.delete(2)
    b_tree.delete(9)
    b_tree.delete(11)
    b_tree.delete(14)
    b_tree.delete(8)
    b_tree.delete(17)
    b_tree.delete(16)

    # 再删则找不到
    delete_key = 4
    del_key, del_val = b_tree.delete(delete_key)  # case 2.3 & case 2.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)

    # 随机打乱 kv_array 后再重新建立 B-Tree
    # print(kv_array)
    shuffler = ShuffleArray(kv_array)
    shuffler.do_shuffle()
    # print(shuffler.array)
    kv_array = shuffler.array

    if isinstance(kv_array, list) and len(kv_array) > 0:
        for kv in kv_array:
            if isinstance(kv, list) and len(kv) == 2:
                b_tree.insert(kv[0], kv[1])

    # 搜索值
    search_key = 4
    res_node, key_index = b_tree.search(search_key)
    if res_node is not None and isinstance(res_node, TreeNode) and \
            key_index < len(res_node.keys):
        print('搜索: 找到了 key 为', res_node.keys[key_index], '的元素，其值为:', res_node.vals[key_index])
    else:
        print('搜索: 找不到 key 为', search_key, '的元素')

    delete_key = 4
    del_key, del_val = b_tree.delete(delete_key)  # case 2.3 & case 2.2
    if del_key is not None:
        print('删除成功:', del_key, del_val)
    else:
        print('删除: 找不到 delete_key=', delete_key)


if __name__ == "__main__":
    sys.exit(main())
