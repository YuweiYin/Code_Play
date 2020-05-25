#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : order-statistic-tree.py
@Author  : YuweiYin
@Date    : 2020-05-24
=================================================="""

# import gc
import sys
import time

"""
顺序统计树 (Order Statistic Tree, OST)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 14
"""


class TreeNode:
    def __init__(self, key=0, val=0, color=True):
        self.key = key       # 键，按键构造 BST/RBT 树，并进行搜索/增添/删除
        self.val = val       # 值，树结点存储的值，可以为任意对象
        self.color = color   # 结点的颜色，True 代表红色(默认)，False 代表黑色
        self.left = None     # 左孩子指针
        self.right = None    # 右孩子指针
        self.parent = None   # 父结点指针
        '''上面是红黑树原本的所需的树结点属性'''
        '''下面是顺序统计树扩张红黑树功能所需的属性'''
        self.size = 1        # 以本结点为根的子树 (包括本结点) 的 (内)结点数，即这棵子树的大小/总结点数
        # rank = x.left.size + 1 就是本结点的秩 (第 rank 小顺序统计量)
        # 红黑树/顺序统计树的哨兵 self.nil 的 size 设置为 0


class OrderStatisticTree:
    # 构造 顺序统计树 (Order Statistic Tree, OST)
    # 时间复杂度 O(n log n)
    def __init__(self, kv_array):
        self.bst = TreeNode(color=False)  # 二叉搜索树结构，树根。初始设置任意属性的 TreeNode
        self.is_bst_empty = True          # 标志着当前 BST 是否为空
        self.sorted_key_list = []

        self.nil = TreeNode(color=False)  # 黑色的哨兵结点
        self.nil.parent = self.nil   # 哨兵的父结点仍为自己
        self.nil.left = self.nil     # 哨兵的左孩子仍为自己
        self.nil.right = self.nil    # 哨兵的右孩子仍为自己
        self.nil.size = 0            # 哨兵的 size 设置为 0

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 TreeNode 并插入 BST
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.rb_insert(kv[0], kv[1])
            # 中序遍历，获取 sorted_key_list 升序数组/列表
            self.update_sorted_key_list()

    '''下面是顺序统计树的扩张功能函数'''

    # 查找具有给定秩 target_rank 的元素 (target_rank >= 1)
    # 时间复杂度 O(log n)
    def os_select(self, target_rank):
        if isinstance(target_rank, int) and target_rank >= 1 and isinstance(self.bst, TreeNode):
            return self._os_select(self.bst, target_rank)
        else:
            # target_rank 取值范围不合法，或者树为空树，找不到目标结点
            return None

    # 从以结点 root 为根的子树中 查找具有给定秩 target_rank 的元素
    def _os_select(self, root, target_rank):
        # 断言当前结点 root 及其两个孩子都是树结点 (根据红黑树性质)
        assert isinstance(root, TreeNode) and isinstance(root.left, TreeNode) and isinstance(root.right, TreeNode)
        # 如果当前 root 已经移动到了哨兵结点，则找不到目标秩的结点
        if root == self.nil:
            return None
        # 计算以 root 为根的子树中结点 root 的秩 cur_rank
        # root.left.size 是对以 root 为根的子树进行中序遍历后排在 root 之前的结点个数
        cur_rank = root.left.size + 1
        # 如果目标顺序统计量序号 target_rank 等于 cur_rank，
        # 则结点 root 就是第 target_rank 小的元素，返回 root
        if target_rank == cur_rank:
            return root
        # 如果 target_rank < cur_rank，
        # 那么第 target_rank 小元素在 root 的左子树中，因此对 root.left 进行递归调用
        elif target_rank < cur_rank:
            return self._os_select(root.left, target_rank)
        # 如果 target_rank > cur_rank，
        # 那么第 target_rank 小元素在 root 的右子树中，因此对 root.right 进行递归调用
        else:
            # 注意 root 的秩为 cur_rank，表示已经有 cur_rank 个元素比 root.right 小了，
            # 所以在右子树中找第 target_rank - cur_rank 小的元素
            return self._os_select(root.right, target_rank - cur_rank)

    # 根据输入的 node 确定此元素的秩
    # 给定指向顺序统计树 OST 中结点 node 的指针
    # 返回对 OST 中序遍历对应的线性序中 node 的位置
    # 时间复杂度 O(log n)
    def os_rank_by_node(self, node):
        if isinstance(node, TreeNode):
            # node 的秩是中序遍历次序排在 node 之前的结点数再加上 1 (代表 node 自身)
            # rank 为以结点 y 为根的子树中 node.key 的秩
            rank = node.left.size + 1
            # 如果还未到 OST 树根，则继续往上搜索
            ptr = node
            while ptr != self.bst:
                assert isinstance(ptr.parent, TreeNode)
                # 如果 ptr 所指结点是其父结点的右孩子，
                # 那么它的父结点和 以左兄弟为根的子树的所有结点都排在 ptr 前
                # 所以它的秩需要加上左兄弟的秩 + 1 (代表父结点)
                if ptr == ptr.parent.right:
                    assert isinstance(ptr.parent.left, TreeNode)
                    rank += ptr.parent.left.size + 1  # 加上左兄弟的秩 + 1 (代表父结点)
                    ptr = ptr.parent  # 指针上移
            return rank
        else:
            # 异常输入，返回 -1 秩
            return -1

    # # 根据 key 值搜索结点，然后确定此结点的秩
    # # 如果搜索到了，则返回结点 TreeNode，如果搜索不到，则返回 None
    # def os_rank_by_key(self, search_key):
    #     if isinstance(self.bst, TreeNode):
    #         ptr = self.bst
    #         while isinstance(ptr, TreeNode):
    #             if search_key == ptr.key:
    #                 # 找到了目标结点，返回此 TreeNode
    #                 return ptr
    #             elif search_key < ptr.key:
    #                 # 如果新结点 key 值小于当前结点，则应该往左走
    #                 ptr = ptr.left
    #             else:
    #                 # 如果新结点 key 值大于当前结点，则应该往右走
    #                 ptr = ptr.right
    #         # 如果出了循环、到了这一步，表示找不到
    #         return None
    #     else:
    #         # BST 树为空树，找不到目标结点
    #         return None

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

            # 维护顺序统计树的属性 size
            # 对某一个结点进行 size 维护的总时间复杂度为 O(log n)，不增加渐近量级
            node_y.size = node_x.size
            node_x.size = node_x.left.size + node_x.right.size + 1

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

            # 维护顺序统计树的属性 size
            # 对某一个结点进行 size 维护的总时间复杂度为 O(log n)，不增加渐近量级
            node_y.size = node_x.size
            node_x.size = node_x.left.size + node_x.right.size + 1

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
    def _create_new_node(self, new_key, new_val, color=True):
        new_node = TreeNode(new_key, new_val, color=color)
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

    # 根据 key 值增加结点
    # 增加后（每次都增加叶结点），调用 rb_insert_fixup 维护红黑性质
    # 刚插入新结点时，仅可能违反第四条红黑性质：每个红色结点的子结点都只能是黑色的。
    # 而调整过程中，可能会违反其它性质，但都会一一修复
    # 时间复杂度 O(log n) 与树高有关
    def rb_insert(self, insert_key, insert_val):
        if self.is_bst_empty:
            # 如果当前 BST 为空，则直接设置 self.bst 结点，完成插入
            new_node = self._create_new_node(insert_key, insert_val)
            new_node.parent = self.nil
            self.bst = new_node
            self.is_bst_empty = False
        else:
            ptr = self.bst           # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索插入位置
            ptr_p = self.bst.parent  # ptr_p 记录 ptr 的父亲
            # 插入过程中维护顺序统计树的 size 属性
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                ptr_p = ptr
                ptr.size += 1        # 插入路径中的结点 size 均加 1
                if insert_key <= ptr.key:
                    ptr = ptr.left
                else:
                    ptr = ptr.right

            # 找到了插入位置，设置新结点属性：红色、左孩子和右孩子均为哨兵 nil、父结点为 ptr_p
            new_node = self._create_new_node(insert_key, insert_val, True)

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

    # 根据 key 值删除结点
    # 删除黑色结点时，可能违反红黑性质，需要调用 rb_delete_fixup 维护红黑性质
    # 时间复杂度 O(log n) 与树高有关
    def rb_delete(self, root, delete_key):
        if self.is_bst_empty:
            print('提示：红黑树为空，无法继续删除。')
        else:
            ptr = root               # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索删除位置
            ptr_p = root.parent      # ptr_p 记录 ptr 的父亲
            # 删除过程中维护顺序统计树的 size 属性
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                ptr_p = ptr          # 跟踪父结点
                ptr.size -= 1        # 删除路径中的结点 size 均减 1
                if delete_key == ptr.key:
                    break  # 定位到了目标删除结点
                elif delete_key < ptr.key:
                    ptr = ptr.left   # 小则往左
                else:
                    ptr = ptr.right  # 大则往右

            assert isinstance(ptr, TreeNode)
            # 若搜索到叶，表示没找到目标结点
            if ptr == self.nil:
                # 此时需要把删除路径中的结点 size 均加 1 (恢复成原本的 size)
                ptr = ptr_p
                while isinstance(ptr, TreeNode) and ptr != self.nil:
                    ptr.size += 1
                    ptr = ptr.parent
                print('提示：删除时，找不到 key 为', delete_key, '的元素')
            else:
                if ptr == self.bst and ptr.key == delete_key and \
                        (not isinstance(ptr.left, TreeNode) or ptr.left == self.nil) and \
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
                                    self._left_rotate(ptr.parent)
                                # 1.1.2. 如果 bro 是左孩子
                                # 则此时只需要把 bro 染黑、bro 的右孩子染红，然后把 bro 父结点右旋，就维护好红黑性质了
                                else:
                                    bro.color = False
                                    bro.right.color = True
                                    self._right_rotate(ptr.parent)

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
                                        self._left_rotate(ptr.parent)
                                    # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                    # 则此时把 bro 的左孩子染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                    elif bro.left != self.nil:
                                        assert bro.left.color is True
                                        bro.left.color = False
                                        self._right_rotate(bro)
                                        self._left_rotate(ptr.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，原本的"黑高"为 2 定然无法维持
                                        # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                        bro.color = True
                                        self._rb_delete_fixup(ptr.parent)

                                # 1.1.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                                else:
                                    # 如果 bro 的左孩子存在(必为红)
                                    # 则此时只需要把 bro 的左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                    if bro.left != self.nil:
                                        assert bro.left.color is True
                                        bro.left.color = False
                                        self._right_rotate(bro)
                                    # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                    # 则此时把 bro 的右孩子染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                    elif bro.right != self.nil:
                                        assert bro.right.color is True
                                        bro.right.color = False
                                        self._left_rotate(bro)
                                        self._right_rotate(ptr.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，而原本"黑高"为 2，定然无法维持
                                        # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                        bro.color = True
                                        self._rb_delete_fixup(ptr.parent)

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
                                    ptr.parent.color = False
                                    self._left_rotate(ptr.parent)
                                # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                # 则此时把 bro 的父结点染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                elif bro.left != self.nil:
                                    assert bro.left.color is True
                                    ptr.parent.color = False
                                    self._right_rotate(bro)
                                    self._left_rotate(ptr.parent)
                                else:
                                    # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                    # 此时将 bro 染红、父结点染黑即可
                                    bro.color = True
                                    ptr.parent.color = False

                            # 2.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                            else:
                                # 如果 bro 的左孩子存在(必为红)
                                # 则此时把 bro 染红、bro 父结点和 bro 左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                if bro.left != self.nil:
                                    bro.color = True
                                    assert bro.left.color is True
                                    bro.left.color = False
                                    ptr.parent.color = False
                                    self._right_rotate(ptr.parent)
                                # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                # 则此时把 bro 的父结点染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                elif bro.right != self.nil:
                                    assert bro.right.color is True
                                    ptr.parent.color = False
                                    self._left_rotate(bro)
                                    self._right_rotate(ptr.parent)
                                else:
                                    # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                    # 此时将 bro 染红、父结点染黑即可
                                    bro.color = True
                                    ptr.parent.color = False
                        return
                    # 如果进入下面的分支，ptr 不为叶
                    elif ptr.left == self.nil:
                        # 如果欲删除结点 ptr 的左孩子为空，且右孩子不为空，则将 ptr 替换为其右孩子
                        x = ptr.right
                        self._rb_transplant(ptr, ptr.right)
                    elif ptr.right == self.nil:
                        # 如果欲删除结点 ptr 的右孩子为空，且左孩子不为空，则将 ptr 替换为其左孩子
                        x = ptr.left
                        self._rb_transplant(ptr, ptr.left)
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
                                y.size = y.left.size + y.right.size + 1  # 更新 y 的 size
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
                                        self._left_rotate(ptr.parent)
                                    # 1.1.2. 如果 bro 是左孩子
                                    # 则此时只需要把 bro 染黑、bro 的右孩子染红，然后把 bro 父结点右旋，就维护好红黑性质了
                                    else:
                                        bro.color = False
                                        bro.right.color = True
                                        self._right_rotate(ptr.parent)

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
                                            self._left_rotate(ptr.parent)
                                        # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                        # 则此时把 bro 的左孩子染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                        elif bro.left != self.nil:
                                            assert bro.left.color is True
                                            bro.left.color = False
                                            self._right_rotate(bro)
                                            self._left_rotate(ptr.parent)
                                        else:
                                            # 如果 bro 的左右孩子都不存在，原本的"黑高"为 2 定然无法维持
                                            # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                            bro.color = True
                                            self._rb_delete_fixup(y.parent)

                                    # 1.1.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                                    else:
                                        # 如果 bro 的左孩子存在(必为红)
                                        # 则此时只需要把 bro 的左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                        if bro.left != self.nil:
                                            assert bro.left.color is True
                                            bro.left.color = False
                                            self._right_rotate(ptr.parent)
                                        # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                        # 则此时把 bro 的右孩子染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                        elif bro.right != self.nil:
                                            assert bro.right.color is True
                                            bro.right.color = False
                                            self._left_rotate(bro)
                                            self._right_rotate(ptr.parent)
                                        else:
                                            # 如果 bro 的左右孩子都不存在，而原本"黑高"为 2，定然无法维持
                                            # 此时将 bro 染红，然后从父结点("双黑")开始 fixup
                                            bro.color = True
                                            self._rb_delete_fixup(y.parent)

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
                                        y.parent.color = False
                                        self._left_rotate(ptr.parent)
                                    # 如果 bro 的右孩子不存在，但左孩子存在(必为红)
                                    # 则此时把 bro 的父结点染黑，然后先 bro 右旋、再原父结点左旋，就维护好红黑性质了
                                    elif bro.left != self.nil:
                                        assert bro.left.color is True
                                        y.parent.color = False
                                        self._right_rotate(bro)
                                        self._left_rotate(ptr.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                        # 此时将 bro 染红、父结点染黑即可
                                        bro.color = True
                                        y.parent.color = False

                                # 2.2. 如果 bro 是左孩子，检查 bro 的孩子情况
                                else:
                                    # 如果 bro 的左孩子存在(必为红)
                                    # 则此时把 bro 染红、bro 父结点和 bro 左孩子染黑，然后把 bro 父结点右旋，就维护好红黑性质了
                                    if bro.left != self.nil:
                                        bro.color = True
                                        assert bro.left.color is True
                                        bro.left.color = False
                                        y.parent.color = False
                                        self._right_rotate(ptr.parent)
                                    # 如果 bro 的左孩子不存在，但右孩子存在(必为红)
                                    # 则此时把 bro 的父结点染黑，然后先 bro 左旋、再原父结点右旋，就维护好红黑性质了
                                    elif bro.right != self.nil:
                                        assert bro.right.color is True
                                        y.parent.color = False
                                        self._left_rotate(bro)
                                        self._right_rotate(ptr.parent)
                                    else:
                                        # 如果 bro 的左右孩子都不存在，原本"黑高"为 1，只通过染色就可以维持
                                        # 此时将 bro 染红、父结点染黑即可
                                        bro.color = True
                                        y.parent.color = False

                            # TODO 把 ptr 替换为其后继结点 y，并修改链接关系和 color (不修改 y 的 key、value)
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
                            y.size = y.left.size + y.right.size + 1  # 更新 y 的 size
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
                        y.size = y.left.size + y.right.size + 1  # 更新 y 的 size
                    # 最后，如果"真正"删除的结点颜色为黑色，则破坏了红黑性质，需要进行维护
                    if not y_original_color:
                        self._rb_delete_fixup(x)  # 删除后维护红黑性质

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
        [1, 10], [2, 20], [3, 30], [7, 70], [6, 60],
        [8, 80], [9, 90], [4, 40], [5, 50]
    ]

    # kv_array = [[i, 100 * i] for i in range(1000)]
    # kv_array = [[i, 100 * i] for i in reversed(range(1000))]

    # 像这种 key 基本有序地插入，如果是普通的 BST，那么树结构会退化地很严重，大幅影响效率
    start = time.process_time()
    ost = OrderStatisticTree(kv_array)
    end = time.process_time()
    print('建立 Red-Black Tree 耗时: %.5f ms' % ((end - start) * 1000))

    # 输出升序排序的结果
    print(ost.get_sorted_key_list())  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 搜索值
    search_key = 4
    start = time.process_time()
    ans = ost.search(search_key)
    end = time.process_time()

    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 顺序统计量：查找具有给定秩 target_rank 的元素 (target_rank >= 1)
    for target_rank in range(11):
        res_node = ost.os_select(target_rank)
        if isinstance(res_node, TreeNode):
            print(target_rank, '->\t', res_node.key, res_node.val)
        else:
            print('No target_rank:', target_rank)

    # 检查某二叉树是否为 BST
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(5)
    print(ost.check_bst(root))  # True

    root.left.left = TreeNode(10)
    print(ost.check_bst(root))  # False

    # 删除结点
    ost.rb_delete(ost.bst, 17)  # 找不到

    # 结点 9 没有左右孩子，直接删除，然后调整其所有祖先结点的平衡性
    # 删除后结点 8 的高度减为 1，因此结点 7 不平衡了，需要调整
    ost.rb_delete(ost.bst, 9)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [1, 2, 3, 4, 5, 6, 7, 8]
    # 此处可通过断点调试查看树结构，ost.bst 为树根

    ost.rb_delete(ost.bst, 3)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [1, 2, 4, 5, 6, 7, 8]

    ost.rb_delete(ost.bst, 7)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [1, 2, 4, 5, 6, 8]

    ost.rb_delete(ost.bst, 8)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [1, 2, 4, 5, 6]

    ost.rb_delete(ost.bst, 2)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [1, 4, 5, 6]

    ost.rb_delete(ost.bst, 1)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [4, 5, 6]

    ost.rb_delete(ost.bst, 4)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [5, 6]

    # 测试再删不存在的关键字
    ost.rb_delete(ost.bst, 3)  # 找不到
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [5, 6]

    # 测试查找不存在的关键字
    search_key = 4
    ans = ost.search(search_key)  # 找不到
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')

    # 删空
    ost.rb_delete(ost.bst, 5)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [6]

    ost.rb_delete(ost.bst, 6)
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # []

    # 删空后再删
    ost.rb_delete(ost.bst, 3)  # 找不到
    ost.update_sorted_key_list()
    print(ost.get_sorted_key_list())  # [5, 6]

    # 删空后测试查找
    search_key = 4
    ans = ost.search(search_key)  # 找不到
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')

    # 重新动态增加（降序测试）
    for key in reversed(range(1, 10)):
        val = key * 100
        ost.rb_insert(key, val)
        ost.update_sorted_key_list()
        print(ost.get_sorted_key_list())

    # 再次测试查找
    search_key = 4
    ans = ost.search(search_key)
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')


if __name__ == "__main__":
    sys.exit(main())
