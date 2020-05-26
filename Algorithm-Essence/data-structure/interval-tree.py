#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : interval-tree.py
@Author  : YuweiYin
@Date    : 2020-05-24
=================================================="""

# import gc
import sys
import time

"""
区间树 (Interval Tree)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 14
"""


class TreeNode:
    def __init__(self, inter_low, inter_high, val=0, color=True):
        self.key = inter_low  # 键，区间树的关键字 key 即为区间的低端点
        self.val = val        # 值，树结点存储的值，可以为任意对象
        self.color = color    # 结点的颜色，True 代表红色(默认)，False 代表黑色
        self.left = None      # 左孩子指针
        self.right = None     # 右孩子指针
        self.parent = None    # 父结点指针
        '''上面是红黑树原本的所需的树结点属性'''
        '''下面是顺序统计树扩张红黑树功能所需的属性'''
        self.inter = (inter_low, inter_high)  # interval 区间属性 (这里默认为闭区间)
        self.max_end = inter_high             # 以本结点为根的子树的 所有区间端点的最大值


class IntervalTree:
    # 构造 区间树 (Interval Tree)
    # 时间复杂度 O(n log n)
    def __init__(self, node_array):
        neg_inf = -0x3f3f3f3f  # 负无穷，设置为哨兵的区间值
        self.bst = None            # 二叉搜索树结构 self.bst 树根
        self.is_bst_empty = True   # 标志着当前 BST 是否为空
        self.sorted_key_list = []  # 已排好序的关键字列表

        self.nil = TreeNode(neg_inf, neg_inf, color=False)  # 黑色的哨兵结点
        self.nil.parent = self.nil   # 哨兵的父结点仍为自己
        self.nil.left = self.nil     # 哨兵的左孩子仍为自己
        self.nil.right = self.nil    # 哨兵的右孩子仍为自己

        # if isinstance(kv_array, list) and len(kv_array) > 0:
        #     for kv in kv_array:
        #         # 对区间树来说，构造数组中的 k 即为 区间的低高端点 (inter_low, inter_high)
        #         assert isinstance(kv, list) and len(kv) == 2
        #         assert isinstance(kv[0], tuple) and len(kv[0]) == 2
        #         assert kv[0][0] <= kv[0][1]  # 低端点 <= 高端点
        #         self.rb_insert(kv[0], kv[1])
        #     # 中序遍历，获取 sorted_key_list 升序数组/列表
        #     self.update_sorted_key_list()

        # 按结点对象列表插入
        if isinstance(node_array, list) and len(node_array) > 0:
            for interval_node in node_array:
                self.interval_insert(interval_node)
            # 中序遍历，获取 sorted_key_list 升序数组/列表
            self.update_sorted_key_list()

    '''下面是顺序统计树的扩张功能函数'''

    # 查询区间树中是否存在与闭区间 target_interval 有重叠的区间
    def interval_search(self, target_interval):
        if isinstance(self.bst, TreeNode) and \
                isinstance(target_interval, tuple) and len(target_interval) == 2:
            ptr = self.bst
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                # 如果 ptr 结点的区间与目标区间 target_interval 有重叠，则返回 ptr
                # 有重叠：inter1.low <= inter2.high 并且 inter2.low <= inter1.high
                if ptr.inter[0] <= target_interval[1] and target_interval[0] <= ptr.inter[1]:
                    return ptr
                # 如果无重叠，则往左或往右 继续搜索
                else:
                    assert isinstance(ptr.left, TreeNode)
                    # 如果左孩子存在 (不是哨兵)，且左子树的区间端点最大值超过 目标区间的低端点，
                    # 表示左侧有与目标区间重合的区间结点，则往左继续搜索
                    # 注意到：由于区间是连续的，所以此时不可能与右子树中的任何区间重叠了
                    if ptr.left != self.nil and ptr.left.max_end >= target_interval[0]:
                        ptr = ptr.left
                    # 否则，左孩子不存在 (是哨兵)，或者左子树的区间端点最大值不及 目标区间的低端点，
                    # 表示左侧的结点已经不可能与目标区间有重合了，则往右继续搜索
                    else:
                        ptr = ptr.right
            # 如果出了循环、到了这一步，表示找不到
            return None
        else:
            # BST 树为空树，找不到目标结点
            return None

    # 根据 TreeNode 精确匹配结点，用于删除结点时检查某结点是否存在于树中
    # 如果搜索到了，则返回 True，如果搜索不到，则返回 False
    def exact_search(self, target_node):
        if isinstance(self.bst, TreeNode) and isinstance(target_node, TreeNode):
            ptr = self.bst
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                if target_node == ptr:
                    # 找到了目标结点，返回此 TreeNode
                    return True
                elif target_node.key < ptr.key:
                    # 如果新结点 key 值小于当前结点，则应该往左走
                    ptr = ptr.left
                else:
                    # 如果新结点 key 值大于当前结点，则应该往右走
                    ptr = ptr.right
            # 如果出了循环、到了这一步，表示找不到
            return False
        else:
            # 找不到目标结点
            return False

    '''下面是红黑树原本的代码 + 维护新性质所需的额外操作'''

    # 中序遍历，将 BST 结点的 key 值（升序排列）存储于 sorted_key_list
    # 时间复杂度 O(n)
    def _inorder_traversal(self, root):
        if isinstance(root, TreeNode) and root != self.nil:
            self._inorder_traversal(root.left)
            self.sorted_key_list.append(root.key)
            self._inorder_traversal(root.right)

    # 调用中序遍历，更新 sorted_key_list
    def update_sorted_key_list(self):
        self.sorted_key_list = []
        self._inorder_traversal(self.bst)

    # 获得 sorted_key_list
    def get_sorted_key_list(self):
        return self.sorted_key_list

    # 辅助操作：左旋。返回替代了 node 的新结点
    # 时间复杂度 O(1)
    def _left_rotate(self, node_x):
        # 对 x 进行左旋，即让 x 的右孩子 y (x.right) 成为 x 的父结点，且 x 等于 y.left。
        # 而 y 结点原本的左孩子变为新 x 的右孩子
        if isinstance(node_x, TreeNode) and isinstance(node_x.right, TreeNode):
            # 如果 x 是 BST 树根，那么树根要更换
            if node_x == self.bst:
                self.bst = node_x.right

            # 调整树结构
            node_y = node_x.right
            node_y.parent = node_x.parent  # 设置 node_y 的父结点（互相关联）
            if isinstance(node_x.parent, TreeNode):
                if node_x == node_x.parent.left:
                    node_x.parent.left = node_y
                else:
                    node_x.parent.right = node_y

            node_x.right = node_y.left  # y 结点原本的左孩子变为新 x 的右孩子
            if isinstance(node_y.left, TreeNode):
                node_y.left.parent = node_x

            node_y.left = node_x
            node_x.parent = node_y

            # 维护区间树的属性 max_end (注意先更新此时的子结点 node_x, 后更新 node_y)
            # 对某一个结点进行 max_end 维护的总时间复杂度为 O(log n)，不增加渐近量级
            assert isinstance(node_x.left, TreeNode) and isinstance(node_x.right, TreeNode)
            assert isinstance(node_y.left, TreeNode) and isinstance(node_y.right, TreeNode)
            node_x.max_end = max(max(node_x.left.max_end, node_x.right.max_end), node_x.inter[1])
            node_y.max_end = max(max(node_y.left.max_end, node_y.right.max_end), node_y.inter[1])

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 辅助操作：右旋。返回替代了 node 的新结点
    # 时间复杂度 O(1)
    def _right_rotate(self, node_x):
        # 对 x 进行右旋，即让 x 的左孩子 y (x.left) 成为 x 的父结点，且 x 等于 y.right。
        # 而 y 结点原本的右孩子变为新 x 的左孩子
        if isinstance(node_x, TreeNode) and isinstance(node_x.left, TreeNode):
            # 如果 x 是 BST 树根，那么树根要更换
            if node_x == self.bst:
                self.bst = node_x.left

            # 调整树结构
            node_y = node_x.left
            node_y.parent = node_x.parent  # 设置 node_y 的父结点（互相关联）
            if isinstance(node_x.parent, TreeNode):
                if node_x == node_x.parent.left:
                    node_x.parent.left = node_y
                else:
                    node_x.parent.right = node_y

            node_x.left = node_y.right  # y 结点原本的右孩子变为新 x 的左孩子
            if isinstance(node_y.right, TreeNode):
                node_y.right.parent = node_x

            node_y.right = node_x
            node_x.parent = node_y

            # 维护区间树的属性 max_end (注意先更新此时的子结点 node_x, 后更新 node_y)
            # 对某一个结点进行 max_end 维护的总时间复杂度为 O(log n)，不增加渐近量级
            assert isinstance(node_x.left, TreeNode) and isinstance(node_x.right, TreeNode)
            assert isinstance(node_y.left, TreeNode) and isinstance(node_y.right, TreeNode)
            node_x.max_end = max(max(node_x.left.max_end, node_x.right.max_end), node_x.inter[1])
            node_y.max_end = max(max(node_y.left.max_end, node_y.right.max_end), node_y.inter[1])

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 根据 key 值搜索结点
    # 如果搜索到了，则返回结点 TreeNode，如果搜索不到，则返回 None
    def search(self, search_key):
        if isinstance(self.bst, TreeNode):
            ptr = self.bst
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                if search_key == ptr.key:
                    # 找到了目标结点，返回此 TreeNode
                    return ptr
                elif search_key < ptr.key:
                    # 如果新结点 key 值小于当前结点，则应该往左走
                    ptr = ptr.left
                else:
                    # 如果新结点 key 值大于当前结点，则应该往右走
                    ptr = ptr.right
            # 如果出了循环、到了这一步，表示找不到
            return None
        else:
            # BST 树为空树，找不到目标结点
            return None

    # 辅助操作：插入之后，逐级向上进行红黑性质维护
    # 时间复杂度 O(log n) 与树高有关
    # 根据当前结点的父结点、爷爷结点、叔叔结点的颜色，分 3 种情况，用旋转操作来调整平衡
    def _rb_insert_fixup(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            # 当前结点 node 为新插入的结点，是红色的
            while isinstance(node.parent, TreeNode) and node.parent.color:
                # node 的爷爷结点必为树结点 (红黑树性质)
                assert isinstance(node.parent.parent, TreeNode)
                if node.parent.parent == self.nil:
                    # node 的爷爷结点为 nil 结点，而且父结点存在
                    # 这表示父结点为树根，且根是红色。只需要把根改为黑色即可
                    assert node.parent == self.bst
                    self.bst.color = False
                else:
                    # node 的爷爷结点为树结点，且非 nil
                    if node.parent == node.parent.parent.left:
                        # 如果 node 的父结点是 node 爷爷结点的左孩子
                        uncle = node.parent.parent.right
                        if isinstance(uncle, TreeNode) and uncle.color:
                            # case 1: 父结点为红色、父结点是爷爷结点的左孩子、叔叔结点也为红色
                            # 这种情况可以直接处理掉
                            node.parent.color = False  # 置父结点的颜色为黑色
                            uncle.color = False  # 置叔叔结点的颜色为黑色
                            node.parent.parent.color = True  # 置爷爷结点颜色为红色
                            node = node.parent.parent  # node 上移至其爷爷结点
                        else:
                            # 此时：父结点为红色、父结点是爷爷结点的左孩子、叔叔结点不存在或者为黑色
                            if node == node.parent.right:
                                # case 2: 父结点为红色、父结点是爷爷结点的左孩子、
                                # 叔叔结点不存在或者为黑色、当前结点是父结点的右孩子
                                # 这种情况先转换成 case 3，然后再处理掉
                                node = node.parent  # node 上移至其父（旋转后会降下来）
                                self._left_rotate(node)  # 左旋，"拉直" 呈 LL 型
                            # case 3: 父结点为红色、父结点是爷爷结点的左孩子、
                            # 叔叔结点不存在或者为黑色、当前结点是父结点的左孩子
                            node.parent.color = False  # 修改父结点为黑色
                            node.parent.parent.color = True  # 修改爷爷结点为红色
                            self._right_rotate(node.parent.parent)  # 右旋爷爷结点
                    else:
                        # 如果 node 的父结点是 node 爷爷结点的右孩子（与前述操作呈镜像处理，减少注释）
                        uncle = node.parent.parent.left
                        if isinstance(uncle, TreeNode) and uncle.color:
                            # case 1': 父结点为红色、父结点是爷爷结点的右孩子、叔叔结点也为红色
                            # 这种情况可以直接处理掉
                            node.parent.color = False  # 置父结点的颜色为黑色
                            uncle.color = False  # 置叔叔结点的颜色为黑色
                            node.parent.parent.color = True  # 置爷爷结点颜色为红色
                            node = node.parent.parent  # node 上移至其爷爷结点
                        else:
                            # 此时：父结点为红色、父结点是爷爷结点的右孩子、叔叔结点不存在或者为黑色
                            if node == node.parent.left:
                                # case 2': 父结点为红色、父结点是爷爷结点的右孩子、
                                # 叔叔结点不存在或者为黑色、当前结点是父结点的左孩子
                                # 这种情况先转换成 case 3，然后再处理掉
                                node = node.parent  # node 上移至其父（旋转后会降下来）
                                self._right_rotate(node)  # 右旋，"拉直" 呈 RR 型
                            # case 3': 父结点为红色、父结点是爷爷结点的右孩子、
                            # 叔叔结点不存在或者为黑色、当前结点是父结点的右孩子
                            node.parent.color = False  # 修改父结点为黑色
                            node.parent.parent.color = True  # 修改爷爷结点为红色
                            self._left_rotate(node.parent.parent)  # 左旋爷爷结点

            # while 循环结束、处理完毕，如果此时树根存在，则置为黑色
            if isinstance(self.bst, TreeNode) and self.bst != self.nil:
                self.bst.color = False

    # 辅助操作：新建树结点
    def _create_new_node(self, new_interval, new_val, color=True):
        assert isinstance(new_interval, tuple) and len(new_interval) == 2
        assert new_interval[0] <= new_interval[1]
        new_node = TreeNode(new_interval[0], new_interval[1], val=new_val, color=color)
        new_node.left = self.nil
        new_node.right = self.nil
        return new_node

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def _clear_node_link(node):
        if isinstance(node, TreeNode):
            node.parent = None
            node.left = None
            node.right = None

    # 根据 TreeNode 对象增加结点
    # 增加后（每次都增加叶结点），调用 rb_insert_fixup 维护红黑性质
    # 时间复杂度 O(log n) 与树高有关
    def interval_insert(self, insert_node):
        assert isinstance(insert_node, TreeNode)
        insert_interval = insert_node.inter
        assert isinstance(insert_interval, tuple) and len(insert_interval) == 2
        assert insert_interval[0] <= insert_interval[1]
        insert_node.left = self.nil
        insert_node.right = self.nil
        insert_node.color = True
        if self.is_bst_empty:
            # 如果当前 BST 为空，则直接设置 self.bst 结点，完成插入
            insert_node.parent = self.nil
            insert_node.color = False
            self.bst = insert_node
            self.is_bst_empty = False
        else:
            ptr = self.bst  # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索插入位置
            ptr_p = self.bst.parent  # ptr_p 记录 ptr 的父亲
            # 插入过程中维护区间树的 max_end 属性
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                ptr_p = ptr
                # ptr 会是新结点的祖先结点，所以根据高端点 决定是否需要更新本结点的 max_end
                if insert_interval[1] > ptr.max_end:
                    ptr.max_end = insert_interval[1]
                # 根据低端点 (即 key) 来决定往左还是往右插入
                if insert_interval[0] <= ptr.key:
                    ptr = ptr.left
                else:
                    ptr = ptr.right

            # 根据 key 决定该插入到左边还是右边
            if insert_node.key <= ptr_p.key:
                ptr_p.left = insert_node
            else:
                ptr_p.right = insert_node
            insert_node.parent = ptr_p

            self._rb_insert_fixup(insert_node)  # 插入后维护红黑性质

    # 根据 key 值增加结点
    # 增加后（每次都增加叶结点），调用 rb_insert_fixup 维护红黑性质
    # 刚插入新结点时，仅可能违反第四条红黑性质：每个红色结点的子结点都只能是黑色的。
    # 而调整过程中，可能会违反其它性质，但都会一一修复
    # 时间复杂度 O(log n) 与树高有关
    def rb_insert(self, insert_interval, insert_val):
        assert isinstance(insert_interval, tuple) and len(insert_interval) == 2
        assert insert_interval[0] <= insert_interval[1]
        if self.is_bst_empty:
            # 如果当前 BST 为空，则直接设置 self.bst 结点，完成插入
            new_node = self._create_new_node(insert_interval, insert_val)
            new_node.parent = self.nil
            self.bst = new_node
            self.is_bst_empty = False
        else:
            ptr = self.bst           # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索插入位置
            ptr_p = self.bst.parent  # ptr_p 记录 ptr 的父亲
            # 插入过程中维护区间树的 max_end 属性
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                ptr_p = ptr
                # ptr 会是新结点的祖先结点，所以根据高端点 决定是否需要更新本结点的 max_end
                if insert_interval[1] > ptr.max_end:
                    ptr.max_end = insert_interval[1]
                # 根据低端点 (即 key) 来决定往左还是往右插入
                if insert_interval[0] <= ptr.key:
                    ptr = ptr.left
                else:
                    ptr = ptr.right

            # 找到了插入位置，设置新结点属性：红色、左孩子和右孩子均为哨兵 nil、父结点为 ptr_p
            new_node = self._create_new_node(insert_interval, insert_val, True)

            # 根据 key 决定该插入到左边还是右边
            if new_node.key <= ptr_p.key:
                ptr_p.left = new_node
            else:
                ptr_p.right = new_node
            new_node.parent = ptr_p

            self._rb_insert_fixup(new_node)  # 插入后维护红黑性质

    # 辅助操作：将结点 u 替换为结点 v（用于删除时的红黑性质保持）
    # 时间复杂度 O(1)
    def _rb_transplant(self, u, v):
        if isinstance(u, TreeNode) and isinstance(v, TreeNode):
            if u == self.bst or u.parent == self.nil:
                self.bst = v
            else:
                # u 的父结点必为树结点 (红黑树性质)
                assert isinstance(u.parent, TreeNode)
                # 根据 u 是其父结点的左孩子还是右孩子，更换指针
                if u == u.parent.left:
                    u.parent.left = v
                else:
                    u.parent.right = v
        # 无条件执行：让 v 的 parent 指针指向 u 的父结点
        v.parent = u.parent

    # 辅助操作：删除之后，逐级向上进行红黑性质维护
    # 时间复杂度 O(log n) 与树高有关
    # 当删除结点 node 时，让其后继 s 替换 node。在结点被移除或者在树中移动之前，必须先记录 s 的颜色
    # 根据当前结点的父结点、兄弟结点、兄弟结点的孩子结点的颜色，分 4 种情况，用旋转操作来调整平衡
    def _rb_delete_fixup(self, node):
        # if isinstance(node, TreeNode) and node != self.nil:
        if isinstance(node, TreeNode) and node != self.bst:
            # 当前结点 node 为真正需要被删除的结点，其祖先中有黑色结点被删除(替换)了
            while node != self.bst and not node.color:
                # node 的父结点必为树结点 (红黑树性质)
                assert isinstance(node.parent, TreeNode)
                if node.parent == self.nil:
                    # 父结点是 nil，表示当前 node 为树根，只需要把根改为黑色即可
                    assert node == self.bst
                    self.bst.color = False
                elif node == node.parent.left:
                    # 如果 node 是其父结点的左孩子
                    # node 的父结点必为树结点 (红黑树性质)
                    assert isinstance(node.parent, TreeNode)
                    # 记录 bro 为 node 父结点的右孩子，即 node 的兄弟结点
                    bro = node.parent.right
                    # node 的兄弟结点必为树结点 (红黑树性质)
                    assert isinstance(bro, TreeNode)
                    if bro.color:
                        # case 1: node 是其父结点的左孩子、其兄弟结点 bro 为红色
                        bro.color = False  # 让 bro 的颜色改为黑色
                        node.parent.color = True
                        self._left_rotate(node.parent)
                        bro = node.parent.right  # 确保 bro 还是 node 的兄弟结点
                    # bro 结点的孩子必为树结点 (红黑树性质)
                    assert isinstance(bro.left, TreeNode) and isinstance(bro.right, TreeNode)
                    if not bro.left.color and not bro.right.color:
                        # case 2: 此时兄弟结点 bro 一定为黑色，如果原本不是黑色，会经过 case 1 变为黑色
                        # 此时 bro 孩子均为黑色，让 bro 变为 红色
                        bro.color = True
                        node = node.parent  # node 上移
                    else:
                        # 此时 bro 的孩子不全为黑色
                        if not bro.right.color:
                            # case 3: 此时 node 是其父结点的左孩子，且兄弟结点 bro 一定为黑色
                            # bro 的左孩子为红色，右孩子为黑色
                            bro.left.color = False  # 修改 bro 左孩子为黑色
                            bro.color = True  # 修改 bro 为红色（一红挂两黑）
                            self._right_rotate(bro)  # 右旋 bro
                            bro = node.parent.right  # 确保 bro 还是 node 的兄弟结点
                            # case 3 之后，保证 bro 为黑色、bro 的右孩子为红色
                        # case 4: 此时 node 是其父结点的左孩子，且兄弟结点 bro 一定为黑色
                        # bro 的右孩子为红色，左孩子颜色为黑色
                        bro.color = node.parent.color
                        node.parent.color = False
                        bro.right.color = False
                        self._left_rotate(node.parent)
                        node = self.bst

                else:
                    # 如果 node 是其父结点的右孩子
                    # node 的父结点必为树结点 (红黑树性质)
                    assert isinstance(node.parent, TreeNode)
                    # 记录 bro 为 node 父结点的左孩子，即 node 的兄弟结点
                    bro = node.parent.left
                    # node 的兄弟结点必为树结点 (红黑树性质)
                    assert isinstance(bro, TreeNode)
                    if bro.color:
                        # case 1': node 是其父结点的右孩子、其兄弟结点 bro 为红色
                        bro.color = False  # 让 bro 的颜色改为黑色
                        node.parent.color = True
                        self._right_rotate(node.parent)
                        bro = node.parent.left  # 确保 bro 还是 node 的兄弟结点
                    # bro 结点的孩子必为树结点 (红黑树性质)
                    assert isinstance(bro.left, TreeNode) and isinstance(bro.right, TreeNode)
                    if not bro.left.color and not bro.right.color:
                        # case 2': 此时兄弟结点 bro 一定为黑色，如果原本不是黑色，会经过 case 1' 变为黑色
                        # 此时 bro 孩子均为黑色，让 bro 变为 红色
                        bro.color = True
                        node = node.parent  # node 上移
                    else:
                        # 此时 bro 的孩子不全为黑色
                        if not bro.left.color:
                            # case 3': 此时 node 是其父结点的右孩子，且兄弟结点 bro 一定为黑色
                            # bro 的左孩子为黑色，右孩子为红色
                            bro.right.color = False  # 修改 bro 右孩子为黑色
                            bro.color = True  # 修改 bro 为红色（一红挂两黑）
                            self._left_rotate(bro)  # 左旋 bro
                            bro = node.parent.left  # 确保 bro 还是 node 的兄弟结点
                            # case 3' 之后，保证 bro 为黑色、bro 的左孩子为红色
                        # case 4': 此时 node 是其父结点的右孩子，且兄弟结点 bro 一定为黑色
                        # bro 的左孩子为红色，右孩子颜色为黑色
                        bro.color = node.parent.color
                        node.parent.color = False
                        bro.left.color = False
                        self._right_rotate(node.parent)
                        node = self.bst

            # 最终将 node 的颜色置为黑色
            node.color = False

    # 删除某结点后，逐级向上维护 max_end 属性
    # 时间复杂度 O(log n) 与树高有关
    def _interval_delete_fix_max(self, node):
        ptr = node
        while isinstance(ptr, TreeNode) and ptr != self.nil:
            assert isinstance(ptr.left, TreeNode) and isinstance(ptr.right, TreeNode)
            ptr.max_end = max(max(ptr.left.max_end, ptr.right.max_end), ptr.inter[1])
            ptr = ptr.parent

    # 删除结点：输入的是被删结点 (TreeNode 类型)
    # 删除黑色结点时，可能违反红黑性质，需要调用 rb_delete_fixup 维护红黑性质
    # 时间复杂度 O(log n) 与树高有关
    def interval_delete(self, delete_node):
        if not isinstance(delete_node, TreeNode):
            # 输入的 delete_node 不合法
            print('delete_node invalid!')
            print(delete_node)
            return
        if self.is_bst_empty:
            print('提示：红黑树为空，无法继续删除。')
        else:
            assert isinstance(self.bst, TreeNode)
            # 通过 exact_search 精确查找树中有没有 delete_node 结点
            if self.exact_search(delete_node):
                ptr = delete_node
                if ptr == self.bst and (not isinstance(ptr.left, TreeNode) or ptr.left == self.nil) and \
                        (not isinstance(ptr.right, TreeNode) or ptr.right == self.nil):
                    # 当前 BST 仅有一个根结点 ptr，且欲删除根结点，会导致树空
                    self.bst = None
                    self.is_bst_empty = True
                    self.sorted_key_list = []
                else:
                    # 正常删除结点 ptr，不会导致树变为空
                    # 这里的 y 主要用于记录 ptr 的后继，而 x 是覆盖了"真正被删除的结点"的结点
                    # 如果 x 覆盖了一个黑色的结点，那么在最后 需要从 x 开始向上调整红黑性质
                    y = ptr
                    y_original_color = y.color  # 记录 y 原始的颜色，用于最后判断是否需要维护红黑性质

                    if ptr.left == self.nil and ptr.right == self.nil:
                        # 如果欲删除结点 ptr 的左右孩子均为空，则为叶，没有孩子可以覆盖 ptr
                        # 先让 ptr 父结点的相应孩子指针指向 self.nil
                        assert isinstance(ptr.parent, TreeNode)
                        if ptr == ptr.parent.left:
                            ptr.parent.left = self.nil
                            bro = ptr.parent.right
                        else:
                            ptr.parent.right = self.nil
                            bro = ptr.parent.left

                        # 如果欲删除的叶结点 ptr 为红色，那么红黑性质不会被破坏
                        if ptr.color:
                            # 逐级向上修改 max_end
                            self._interval_delete_fix_max(ptr.parent)
                            return
                        # 如果欲删除的叶结点 ptr 为黑色，那么红黑性质会被破坏，其父结点的左侧"黑高"低于右侧"黑高"
                        # 因为原本红黑性质是满足的，所以此时 (删除 ptr 前) 只有如下这几种可能：
                        # 1. ptr 为黑、ptr 的父结点为黑
                        if not ptr.parent.color:
                            assert bro != self.nil  # 兄弟必存在，否则原本就不符合红黑性质了
                            # 1.1. ptr 为黑、ptr 的父结点为黑、ptr 的兄弟结点为红
                            # 那么 bro 必有两个黑孩子，而且 bro 的黑孩子必为叶
                            if bro.color:
                                assert bro.left != self.nil and bro.right != self.nil
                                assert (not bro.left.color) and (not bro.right.color)
                                # 1.1.1. 如果 bro 是右孩子
                                # 则此时只需要把 bro 染黑、bro 的左孩子染红，然后把 bro 父结点左旋，就维护好红黑性质了
                                if bro == ptr.parent.right:
                                    bro.color = False
                                    bro.left.color = True
                                    self._left_rotate(bro.parent)
                                # 1.1.2. 如果 bro 是左孩子
                                # 则此时只需要把 bro 染黑、bro 的右孩子染红，然后把 bro 父结点右旋，就维护好红黑性质了
                                else:
                                    bro.color = False
                                    bro.right.color = True
                                    self._right_rotate(bro.parent)

                            # 1.2. ptr 为黑、ptr 的父结点为黑、ptr 的兄弟结点为黑
                            # 那么 bro 若有孩子，必为红孩子，而且 bro 的红孩子必为叶
                            else:
                                # 1.1.1. 如果 bro 是右孩子，检查 bro 的孩子情况
                                if bro == ptr.parent.right:
                                    # 如果 bro 的右孩子存在(必为红)
                                    # 则此时只需要把 bro 的右孩子染黑，然后把 bro 父结点左旋，就维护好红黑性质了
                                    if bro.right != self.nil:
                                        assert bro.right.color is True
                                        bro.right.color = False
                                        self._left_rotate(bro.parent)
                                    # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                    # 则此时把 bro 的左孩子染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                    elif bro.left != self.nil:
                                        assert bro.left.color is True
                                        bro.left.color = False
                                        new_bro = self._right_rotate(bro)
                                        self._left_rotate(new_bro.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，原本的"黑高"为 2 定然无法维持
                                        # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                        bro.color = True
                                        self._rb_delete_fixup(bro.parent)

                                # 1.1.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                                else:
                                    # 如果 bro 的左孩子存在(必为红)
                                    # 则此时只需要把 bro 的左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                    if bro.left != self.nil:
                                        assert bro.left.color is True
                                        bro.left.color = False
                                        self._right_rotate(bro.parent)
                                    # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                    # 则此时把 bro 的右孩子染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                    elif bro.right != self.nil:
                                        assert bro.right.color is True
                                        bro.right.color = False
                                        new_bro = self._left_rotate(bro)
                                        self._right_rotate(new_bro.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，而原本"黑高"为 2，定然无法维持
                                        # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                        bro.color = True
                                        self._rb_delete_fixup(bro.parent)

                        # 2. ptr 为黑、ptr 的父结点为红
                        else:
                            # 此时兄弟必存在，且为黑，否则原本就不符合红黑性质了
                            assert bro != self.nil and (not bro.color)
                            # 类似 1.2. 处理
                            # 2.1. 如果 bro 是右孩子，检查 bro 的孩子情况
                            if bro == ptr.parent.right:
                                # 如果 bro 的右孩子存在(必为红)
                                # 则此时把 bro 染红、bro 父结点和 bro 右孩子染黑，然后把 bro 父结点左旋，就维护好红黑性质了
                                if bro.right != self.nil:
                                    bro.color = True
                                    assert bro.right.color is True
                                    bro.right.color = False
                                    bro.parent.color = False
                                    self._left_rotate(bro.parent)
                                # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                # 则此时把 bro 的父结点染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                elif bro.left != self.nil:
                                    assert bro.left.color is True
                                    bro.parent.color = False
                                    new_bro = self._right_rotate(bro)
                                    self._left_rotate(new_bro.parent)
                                else:
                                    # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                    # 此时将 bro 染红、父结点染黑即可
                                    bro.color = True
                                    bro.parent.color = False

                            # 2.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                            else:
                                # 如果 bro 的左孩子存在(必为红)
                                # 则此时把 bro 染红、bro 父结点和 bro 左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                if bro.left != self.nil:
                                    bro.color = True
                                    assert bro.left.color is True
                                    bro.left.color = False
                                    bro.parent.color = False
                                    self._right_rotate(bro.parent)
                                # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                # 则此时把 bro 的父结点染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                elif bro.right != self.nil:
                                    assert bro.right.color is True
                                    bro.parent.color = False
                                    self._left_rotate(bro)
                                    self._right_rotate(bro.parent)
                                else:
                                    # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                    # 此时将 bro 染红、父结点染黑即可
                                    bro.color = True
                                    bro.parent.color = False
                        # 逐级向上修改 max_end
                        self._interval_delete_fix_max(ptr.parent)
                        return
                    # 如果进入下面的分支，ptr 不为叶
                    elif ptr.left == self.nil:
                        # 如果欲删除结点 ptr 的左孩子为空，且右孩子不为空，则将 ptr 替换为其右孩子
                        x = ptr.right
                        self._rb_transplant(ptr, ptr.right)
                        # 逐级向上修改 max_end
                        self._interval_delete_fix_max(ptr.parent)
                    elif ptr.right == self.nil:
                        # 如果欲删除结点 ptr 的右孩子为空，且左孩子不为空，则将 ptr 替换为其左孩子
                        x = ptr.left
                        self._rb_transplant(ptr, ptr.left)
                        # 逐级向上修改 max_end
                        self._interval_delete_fix_max(ptr.parent)
                    else:
                        # 欲删除结点 ptr 的左右孩子均不为空，则将 ptr 替换为其后继
                        y = self.successor(ptr)     # y 为 ptr 的后继，y 的左孩子为 nil
                        assert isinstance(y, TreeNode) and y.left == self.nil
                        y_original_color = y.color  # (修改)记录 y 原始的颜色
                        x = y.right  # 后继结点 y 必无左孩子，让其右孩子 x 替换 y

                        if x == self.nil:
                            # 如果 x 是哨兵 nil，意味着 y 是叶，类似前面 ptr 为叶的处理方式
                            assert isinstance(y.parent, TreeNode)
                            # 如果欲删除结点 y 的左右孩子均为空，则为叶，没有孩子可以覆盖 y
                            # 先让 y 父结点的相应孩子指针指向 self.nil
                            assert isinstance(y.parent, TreeNode)
                            if y == y.parent.left:
                                y.parent.left = self.nil
                                bro = y.parent.right
                            else:
                                y.parent.right = self.nil
                                bro = y.parent.left

                            # 如果欲删除的叶结点 y 为红色，那么红黑性质不会被破坏
                            if y.color:
                                # 把 ptr 替换为其后继结点 y，并修改链接关系和 color (不修改 y 的 key、value)
                                if ptr == self.bst or ptr.parent == self.nil:
                                    self.bst = y
                                else:
                                    # 根据 u 是其父结点的左孩子还是右孩子，更换指针
                                    if ptr == ptr.parent.left:
                                        ptr.parent.left = y
                                    else:
                                        ptr.parent.right = y
                                # 让 y 的 parent 指针指向 ptr 的父结点
                                y.parent = ptr.parent
                                y.left = ptr.left
                                y.left.parent = y
                                y.right = ptr.right
                                y.right.parent = y
                                y.color = ptr.color  # y 继承 ptr 的颜色
                                # 逐级向上修改 max_end
                                self._interval_delete_fix_max(y)
                                return
                            # 如果欲删除的叶结点 y 为黑色，那么红黑性质会被破坏，其父结点的左侧"黑高"低于右侧"黑高"
                            # 因为原本红黑性质是满足的，所以此时 (删除 y 前) 只有如下这几种可能：
                            # 1. y 为黑、y 的父结点为黑
                            if not y.parent.color:
                                assert bro != self.nil  # 兄弟必存在，否则原本就不符合红黑性质了
                                # 1.1. y 为黑、y 的父结点为黑、y 的兄弟结点为红
                                # 那么 bro 必有两个黑孩子，而且 bro 的黑孩子必为叶
                                if bro.color:
                                    assert bro.left != self.nil and bro.right != self.nil
                                    assert (not bro.left.color) and (not bro.right.color)
                                    # 1.1.1. 如果 bro 是右孩子
                                    # 则此时只需要把 bro 染黑、bro 的左孩子染红，然后把 bro 父结点左旋，就维护好红黑性质了
                                    if bro == y.parent.right:
                                        bro.color = False
                                        bro.left.color = True
                                        self._left_rotate(bro.parent)
                                    # 1.1.2. 如果 bro 是左孩子
                                    # 则此时只需要把 bro 染黑、bro 的右孩子染红，然后把 bro 父结点右旋，就维护好红黑性质了
                                    else:
                                        bro.color = False
                                        bro.right.color = True
                                        self._right_rotate(bro.parent)

                                # 1.2. y 为黑、y 的父结点为黑、y 的兄弟结点为黑
                                # 那么 bro 若有孩子，必为红孩子，而且 bro 的红孩子必为叶
                                else:
                                    # 1.1.1. 如果 bro 是右孩子，检查 bro 的孩子情况
                                    if bro == y.parent.right:
                                        # 如果 bro 的右孩子存在(必为红)
                                        # 则此时只需要把 bro 的右孩子染黑，然后把 bro 父结点左旋，就维护好红黑性质了
                                        if bro.right != self.nil:
                                            assert bro.right.color is True
                                            bro.right.color = False
                                            self._left_rotate(bro.parent)
                                        # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                        # 则此时把 bro 的左孩子染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                        elif bro.left != self.nil:
                                            assert bro.left.color is True
                                            bro.left.color = False
                                            new_bro = self._right_rotate(bro)
                                            self._left_rotate(new_bro.parent)
                                        else:
                                            # 如果 bro 的左右孩子都不存在，原本的"黑高"为 2 定然无法维持
                                            # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                            bro.color = True
                                            self._rb_delete_fixup(bro.parent)

                                    # 1.1.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                                    else:
                                        # 如果 bro 的左孩子存在(必为红)
                                        # 则此时只需要把 bro 的左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                        if bro.left != self.nil:
                                            assert bro.left.color is True
                                            bro.left.color = False
                                            self._right_rotate(bro.parent)
                                        # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                        # 则此时把 bro 的右孩子染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                        elif bro.right != self.nil:
                                            assert bro.right.color is True
                                            bro.right.color = False
                                            new_bro = self._left_rotate(bro)
                                            self._right_rotate(new_bro.parent)
                                        else:
                                            # 如果 bro 的左右孩子都不存在，而原本"黑高"为 2，定然无法维持
                                            # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                            bro.color = True
                                            self._rb_delete_fixup(bro.parent)

                            # 2. y 为黑、y 的父结点为红
                            else:
                                # 此时兄弟必存在，且为黑，否则原本就不符合红黑性质了
                                assert bro != self.nil and (not bro.color)
                                # 类似 1.2. 处理
                                # 2.1. 如果 bro 是右孩子，检查 bro 的孩子情况
                                if bro == y.parent.right:
                                    # 如果 bro 的右孩子存在(必为红)
                                    # 则此时把 bro 染红、bro 父结点和 bro 右孩子染黑，然后把 bro 父结点左旋，就维护好红黑性质了
                                    if bro.right != self.nil:
                                        bro.color = True
                                        assert bro.right.color is True
                                        bro.right.color = False
                                        bro.parent.color = False
                                        self._left_rotate(bro.parent)
                                    # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                    # 则此时把 bro 的父结点染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                    elif bro.left != self.nil:
                                        assert bro.left.color is True
                                        bro.parent.color = False
                                        new_bro = self._right_rotate(bro)
                                        self._left_rotate(new_bro.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                        # 此时将 bro 染红、父结点染黑即可
                                        bro.color = True
                                        bro.parent.color = False

                                # 2.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                                else:
                                    # 如果 bro 的左孩子存在(必为红)
                                    # 则此时把 bro 染红、bro 父结点和 bro 左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                    if bro.left != self.nil:
                                        bro.color = True
                                        assert bro.left.color is True
                                        bro.left.color = False
                                        bro.parent.color = False
                                        self._right_rotate(bro.parent)
                                    # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                    # 则此时把 bro 的父结点染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                    elif bro.right != self.nil:
                                        assert bro.right.color is True
                                        y.parent.color = False
                                        new_bro = self._left_rotate(bro)
                                        self._right_rotate(new_bro.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                        # 此时将 bro 染红、父结点染黑即可
                                        bro.color = True
                                        bro.parent.color = False

                            # 把 ptr 替换为其后继结点 y，并修改链接关系和 color (不修改 y 的 key、value)
                            if ptr == self.bst or ptr.parent == self.nil:
                                self.bst = y
                            else:
                                # 根据 u 是其父结点的左孩子还是右孩子，更换指针
                                if ptr == ptr.parent.left:
                                    ptr.parent.left = y
                                else:
                                    ptr.parent.right = y
                            # 让 y 的 parent 指针指向 ptr 的父结点
                            y.parent = ptr.parent
                            y.left = ptr.left
                            y.left.parent = y
                            y.right = ptr.right
                            y.right.parent = y
                            y.color = ptr.color  # y 继承 ptr 的颜色
                            # 逐级向上修改 max_end
                            self._interval_delete_fix_max(y)
                            return
                        # 此时后继 y 一定有右孩子，x 不可能为 self.nil
                        if y.parent == ptr:
                            # 如果 ptr 的后继 y 就是 ptr 的直接右孩子
                            assert isinstance(x, TreeNode) and x != self.nil
                            x.parent = y
                        else:
                            # 如果 ptr 的后继 y 不是 ptr 的直接右孩子
                            # 让 y 被其右孩子替换（因为之后 y 要用于替换 ptr）
                            # 所以替换了 y 的结点就是 y.right，也即 x
                            assert isinstance(y.right, TreeNode) and y.right != self.nil
                            self._rb_transplant(y, y.right)
                            y.right = ptr.right
                            y.right.parent = y

                        # 现在把 ptr 替换为其后继结点 y，并修改链接关系和 color (不修改 y 的 key、value)
                        self._rb_transplant(ptr, y)
                        y.left = ptr.left
                        y.left.parent = y
                        y.right = ptr.right
                        y.right.parent = y
                        y.color = ptr.color  # y 继承 ptr 的颜色
                        # 逐级向上修改 max_end
                        self._interval_delete_fix_max(x)
                    # 最后，如果"真正"删除的结点颜色为黑色，则破坏了红黑性质，需要进行维护
                    if not y_original_color:
                        self._rb_delete_fixup(x)  # 删除后维护红黑性质
            else:
                # 找不到目标结点
                print('找不到目标结点，删除失败')
                print(delete_node.inter)

    # 找到一棵以 root 为根的 BST/RBT 中的最小值结点（一路向左）
    # 时间复杂度 O(log n) 与树高有关
    def min_bst(self, root):
        if isinstance(root, TreeNode) and root != self.nil:
            while isinstance(root.left, TreeNode) and root.left != self.nil:
                root = root.left
            return root
        else:
            return None

    # 找到一棵以 root 为根的 BST/RBT 中的最大值结点（一路向右）
    # 时间复杂度 O(log n) 与树高有关
    def max_bst(self, root):
        if isinstance(root, TreeNode) and root != self.nil:
            while isinstance(root.right, TreeNode) and root.right != self.nil:
                root = root.right
            return root
        else:
            return None

    # 找到在 BST 中 node 结点的前驱结点，即：其左子树中的最大值
    # 时间复杂度 O(log n) 与树高有关
    def predecessor(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            return self.max_bst(node.left)
        else:
            return None

    # 找到在 BST 中 node 结点的后继结点，即：其右子树中的最小值
    # 时间复杂度 O(log n) 与树高有关
    def successor(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            return self.min_bst(node.right)
        else:
            return None

    # 检查一棵以 root 为根的二叉树是否为 BST
    def check_bst(self, root):
        if not isinstance(root, TreeNode):
            # 当前结点非树结点，不合法
            return False
        elif root == self.nil:
            # 当前结点为哨兵，空树也算作是 BST
            return True
        else:
            # 左/右孩子为空时，左/右孩子满足 BST 条件
            left_bst = True   # 左孩子是否满足 BST 条件
            right_bst = True  # 右孩子是否满足 BST 条件

            if root.left is not None:
                # 如果当前结点的左孩子不为空，检查该左孩子的值
                if root.left.key <= root.key:
                    # 如果左孩子的值小于等于当前结点的值，表示满足 BST 条件，继续往左观察
                    left_bst = self.check_bst(root.left)
                else:
                    # 如果左孩子的值大于当前结点的值，表示不满足 BST 条件
                    return False

            if root.right is not None:
                # 如果当前结点的右孩子不为空，检查该右孩子的值
                if root.right.key > root.key:
                    # 如果右孩子的值大于当前结点的值，表示满足 BST 条件，继续往右观察
                    right_bst = self.check_bst(root.right)
                else:
                    # 如果右孩子的值小于等于当前结点的值，表示不满足 BST 条件
                    return False

            # 左右孩子都满足条件，才返回 True
            return left_bst and right_bst


def main():
    # 以插入的方式，构建 BST/RBT
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    kv_array = [
        [(16, 21), 100], [(8, 9), 200], [(25, 30), 300], [(5, 8), 400],
        [(15, 23), 500], [(17, 19), 600], [(26, 26), 700], [(0, 3), 800],
        [(6, 10), 900], [(19, 20), 1000]
    ]

    # kv_array = [[(i, i << 1), 100 * i] for i in range(1000)]
    # kv_array = [[(i, i << 1), 100 * i] for i in reversed(range(1000))]

    node_array = []
    for kv in kv_array:
        node_array.append(TreeNode(kv[0][0], kv[0][1], val=kv[1]))

    # 像这种 key 基本有序地插入，如果是普通的 BST，那么树结构会退化地很严重，大幅影响效率
    start = time.process_time()
    # inter_tree = IntervalTree(kv_array)
    inter_tree = IntervalTree(node_array)
    end = time.process_time()
    print('建立 Red-Black Tree 耗时: %.5f ms' % ((end - start) * 1000))

    # 输出升序排序的结果
    print(inter_tree.get_sorted_key_list())  # [0, 5, 6, 8, 15, 16, 17, 19, 25, 26]

    # 区间搜索
    search_interval = (6, 7)
    start = time.process_time()
    ans = inter_tree.interval_search(search_interval)
    end = time.process_time()

    if ans is not None and isinstance(ans, TreeNode):
        print('找到了与 interval', search_interval, '有重叠的区间', ans.inter, '，其值为:', ans.val)
    else:
        print('找不到与 interval', search_interval, '有重叠的区间')

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 删除结点
    inter_tree.interval_delete(TreeNode(100, 200))  # 找不到

    delete_nodes = node_array
    for delete_node in delete_nodes:
        inter_tree.interval_delete(delete_node)
        inter_tree.update_sorted_key_list()
        print(inter_tree.get_sorted_key_list())

    # 删空之后测试再删
    inter_tree.interval_delete(TreeNode(10, 20))  # 提示 BST 为空
    inter_tree.update_sorted_key_list()
    print(inter_tree.get_sorted_key_list())

    # 删空之后测试查找
    search_interval = (6, 7)
    ans = inter_tree.interval_search(search_interval)  # 找不到
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了与 interval', search_interval, '有重叠的区间', ans.inter, '，其值为:', ans.val)
    else:
        print('找不到与 interval', search_interval, '有重叠的区间')

    # 重新动态增加
    for node in reversed(node_array):
        inter_tree.interval_insert(node)
        inter_tree.update_sorted_key_list()
        print(inter_tree.get_sorted_key_list())

    # 再次测试区间搜索
    search_interval = (6, 7)
    ans = inter_tree.interval_search(search_interval)
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了与 interval', search_interval, '有重叠的区间', ans.inter, '，其值为:', ans.val)
    else:
        print('找不到与 interval', search_interval, '有重叠的区间')


if __name__ == "__main__":
    sys.exit(main())
