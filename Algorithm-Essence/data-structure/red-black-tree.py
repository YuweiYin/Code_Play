#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : red-black-tree.py
@Author  : YuweiYin
@Date    : 2020-05-06
=================================================="""

# import gc
import sys
import time

"""
红黑树 (Red-Black Tree, RBT)

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 13
"""


class TreeNode:
    def __init__(self, key=0, val=0, color=True):
        self.key = key       # 键，按键构造 BST/RBT 树，并进行搜索/增添/删除
        self.val = val       # 值，树结点存储的值，可以为任意对象
        self.color = color   # 结点的颜色，True 代表红色(默认)，False 代表黑色
        self.left = None     # 左孩子指针
        self.right = None    # 右孩子指针
        self.parent = None   # 父结点指针


class RedBlackTree:
    # 构造 红黑树 Red-Black Tree
    # 时间复杂度 O(n log n)
    def __init__(self, kv_array):
        self.bst = TreeNode(color=False)  # 二叉搜索树结构，树根。初始设置任意属性的 TreeNode
        self.is_bst_empty = True          # 标志着当前 BST 是否为空
        self.sorted_key_list = []

        self.nil = TreeNode(color=False)  # 黑色的哨兵结点
        self.nil.parent = self.nil   # 哨兵的父结点仍为自己
        self.nil.left = self.nil     # 哨兵的左孩子仍为自己
        self.nil.right = self.nil    # 哨兵的右孩子仍为自己

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 TreeNode 并插入 BST
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.rb_insert(kv[0], kv[1])
            # 中序遍历，获取 sorted_key_list 升序数组/列表
            self.update_sorted_key_list()

    # 中序遍历，将 BST 结点的 key 值（升序排列）存储于 sorted_key_list
    # 时间复杂度 O(n)
    def inorder_traversal(self, root):
        if isinstance(root, TreeNode) and root != self.nil:
            self.inorder_traversal(root.left)
            self.sorted_key_list.append(root.key)
            self.inorder_traversal(root.right)

    # 调用中序遍历，更新 sorted_key_list
    def update_sorted_key_list(self):
        self.sorted_key_list = []
        self.inorder_traversal(self.bst)

    # 获得 sorted_key_list
    def get_sorted_key_list(self):
        return self.sorted_key_list

    # 辅助操作：左旋。返回替代了 node 的新结点
    # 时间复杂度 O(1)
    def left_rotate(self, node_x):
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

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 辅助操作：右旋。返回替代了 node 的新结点
    # 时间复杂度 O(1)
    def right_rotate(self, node_x):
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

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 根据 key 值搜索结点
    # 如果搜索到了，则返回结点 TreeNode，如果搜索不到，则返回 None
    def search(self, search_key):
        if isinstance(self.bst, TreeNode):
            ptr = self.bst
            while isinstance(ptr, TreeNode):
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
    def rb_insert_fixup(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            # 当前结点 node 为新插入的结点，是红色的
            while isinstance(node.parent, TreeNode) and node.parent.color:
                if not isinstance(node.parent.parent, TreeNode):
                    # node 的爷爷结点为非树结点，红黑树不应如此
                    print('rb_insert_fixup: Error Path 0')
                elif node.parent.parent == self.nil:
                    # node 的爷爷结点为 nil 结点，而且父结点存在
                    # 这表示父结点为树根，且根是红色。只需要把根改为黑色即可
                    if node.parent == self.bst:
                        self.bst.color = False
                    else:
                        print('rb_insert_fixup: Error Path 0')
                else:
                    # node 的爷爷结点为树结点，且非 nil
                    if node.parent == node.parent.parent.left:
                        # 如果 node 的父结点是 node 爷爷结点的左孩子
                        if isinstance(node.parent.parent, TreeNode):
                            uncle = node.parent.parent.right
                            if isinstance(uncle, TreeNode) and uncle.color:
                                # case 1: 父结点为红色、父结点是爷爷结点的左孩子、叔叔结点也为红色
                                # 这种情况可以直接处理掉
                                node.parent.color = False  # 置父结点的颜色为黑色
                                uncle.color = False        # 置叔叔结点的颜色为黑色
                                node.parent.parent.color = True  # 置爷爷结点颜色为红色
                                node = node.parent.parent  # node 上移至其爷爷结点
                            else:
                                # 此时：父结点为红色、父结点是爷爷结点的左孩子、叔叔结点不存在或者为黑色
                                if node == node.parent.right:
                                    # case 2: 父结点为红色、父结点是爷爷结点的左孩子、
                                    # 叔叔结点不存在或者为黑色、当前结点是父结点的右孩子
                                    # 这种情况先转换成 case 3，然后再处理掉
                                    node = node.parent      # node 上移至其父（旋转后会降下来）
                                    self.left_rotate(node)  # 左旋，"拉直" 呈 LL 型
                                # case 3: 父结点为红色、父结点是爷爷结点的左孩子、
                                # 叔叔结点不存在或者为黑色、当前结点是父结点的左孩子
                                node.parent.color = False              # 修改父结点为黑色
                                node.parent.parent.color = True        # 修改爷爷结点为红色
                                self.right_rotate(node.parent.parent)  # 右旋爷爷结点
                        else:
                            # node 的爷爷结点为非树结点，红黑树不应如此
                            print('rb_insert_fixup: Error Path 1')
                    else:
                        # 如果 node 的父结点是 node 爷爷结点的右孩子（与前述操作呈镜像处理，减少注释）
                        if isinstance(node.parent.parent, TreeNode):
                            uncle = node.parent.parent.left
                            if isinstance(uncle, TreeNode) and uncle.color:
                                # case 1': 父结点为红色、父结点是爷爷结点的右孩子、叔叔结点也为红色
                                # 这种情况可以直接处理掉
                                node.parent.color = False  # 置父结点的颜色为黑色
                                uncle.color = False        # 置叔叔结点的颜色为黑色
                                node.parent.parent.color = True  # 置爷爷结点颜色为红色
                                node = node.parent.parent  # node 上移至其爷爷结点
                            else:
                                # 此时：父结点为红色、父结点是爷爷结点的右孩子、叔叔结点不存在或者为黑色
                                if node == node.parent.left:
                                    # case 2': 父结点为红色、父结点是爷爷结点的右孩子、
                                    # 叔叔结点不存在或者为黑色、当前结点是父结点的左孩子
                                    # 这种情况先转换成 case 3，然后再处理掉
                                    node = node.parent      # node 上移至其父（旋转后会降下来）
                                    self.right_rotate(node)  # 右旋，"拉直" 呈 RR 型
                                # case 3': 父结点为红色、父结点是爷爷结点的右孩子、
                                # 叔叔结点不存在或者为黑色、当前结点是父结点的右孩子
                                node.parent.color = False             # 修改父结点为黑色
                                node.parent.parent.color = True       # 修改爷爷结点为红色
                                self.left_rotate(node.parent.parent)  # 左旋爷爷结点
                        else:
                            # node 的爷爷结点为非树结点，红黑树不应如此
                            print('rb_insert_fixup: Error Path 2')

            # while 循环结束、处理完毕，如果此时树根存在，则置为黑色
            if isinstance(self.bst, TreeNode) and self.bst != self.nil:
                self.bst.color = False

    # 辅助操作：新建树结点
    def create_new_node(self, new_key, new_val, color=True):
        new_node = TreeNode(new_key, new_val, color=color)
        new_node.left = self.nil
        new_node.right = self.nil
        return new_node

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def clear_node_link(node):
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
            new_node = self.create_new_node(insert_key, insert_val)
            new_node.parent = self.nil
            self.bst = new_node
            self.is_bst_empty = False
        else:
            ptr = self.bst           # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索插入位置
            ptr_p = self.bst.parent  # ptr_p 记录 ptr 的父亲
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                ptr_p = ptr
                if insert_key <= ptr.key:
                    ptr = ptr.left
                else:
                    ptr = ptr.right

            # 找到了插入位置，设置新结点属性：红色、左孩子和右孩子均为哨兵 nil、父结点为 ptr_p
            new_node = self.create_new_node(insert_key, insert_val, True)

            # 根据 key 决定该插入到左边还是右边
            if new_node.key <= ptr_p.key:
                ptr_p.left = new_node
            else:
                ptr_p.right = new_node
            new_node.parent = ptr_p

            self.rb_insert_fixup(new_node)  # 插入后维护红黑性质

    # 辅助操作：将结点 u 替换为结点 v（用于删除时的红黑性质保持）
    # 时间复杂度 O(log n) 与树高有关
    def rb_transplant(self, u, v):
        if isinstance(u, TreeNode) and isinstance(v, TreeNode):
            if u == self.bst or u.parent == self.nil:
                self.bst = v
            else:
                if isinstance(u.parent, TreeNode):
                    # 根据 u 是其父结点的左孩子还是右孩子，更换指针
                    if u == u.parent.left:
                        u.parent.left = v
                    else:
                        u.parent.right = v
                else:
                    # u 的父结点为非树结点，红黑树不应如此
                    print('rb_transplant: Error Path')
        else:
            pass
        # 无条件执行：让 v 的 parent 指针指向 u 的父结点
        v.parent = u.parent

    # 辅助操作：删除之后，逐级向上进行红黑性质维护
    # 时间复杂度 O(log n) 与树高有关
    # 当删除结点 node 时，让其后继 s 替换 node。在结点被移除或者在树中移动之前，必须先记录 s 的颜色
    # 根据当前结点的父结点、兄弟结点、兄弟结点的孩子结点的颜色，分 4 种情况，用旋转操作来调整平衡
    def rb_delete_fixup(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            # 当前结点 node 为真正需要被删除的结点，其祖先中有黑色结点被删除(替换)了
            while node != self.bst and not node.color:
                if not isinstance(node.parent, TreeNode):
                    # 父结点不是树结点，红黑树不应如此
                    print('rb_delete_fixup: Error Path 0')
                elif node.parent == self.nil:
                    # 父结点是 nil，表示当前 node 为树根，只需要把根改为黑色即可
                    if node == self.bst:
                        self.bst.color = False
                    else:
                        print('rb_insert_fixup: Error Path 0+')
                elif node == node.parent.left:
                    # 如果 node 是其父结点的左孩子
                    if isinstance(node.parent, TreeNode):
                        # 记录 bro 为 node 父结点的右孩子，即 node 的兄弟结点
                        bro = node.parent.right
                        if isinstance(bro, TreeNode):
                            if bro.color:
                                # case 1: node 是其父结点的左孩子、其兄弟结点 bro 为红色
                                bro.color = False  # 让 bro 的颜色改为黑色
                                node.parent.color = True
                                self.left_rotate(node.parent)
                                bro = node.parent.right  # 确保 bro 还是 node 的兄弟结点
                            if isinstance(bro.left, TreeNode) and isinstance(bro.right, TreeNode):
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
                                        bro.left.color = False   # 修改 bro 左孩子为黑色
                                        bro.color = True         # 修改 bro 为红色（一红挂两黑）
                                        self.right_rotate(bro)   # 右旋 bro
                                        bro = node.parent.right  # 确保 bro 还是 node 的兄弟结点
                                        # case 3 之后，保证 bro 为黑色、bro 的右孩子为红色
                                    # case 4: 此时 node 是其父结点的左孩子，且兄弟结点 bro 一定为黑色
                                    # bro 的右孩子为红色，左孩子颜色为黑色
                                    bro.color = node.parent.color
                                    node.parent.color = False
                                    bro.right.color = False
                                    self.left_rotate(node.parent)
                                    node = self.bst
                            else:
                                # bro 结点的孩子为非树结点，红黑树不应如此
                                print('rb_delete_fixup: Error Path 1')
                        else:
                            # node 的兄弟结点为非树结点，红黑树不应如此
                            print('rb_delete_fixup: Error Path 2')
                    else:
                        # node 的父结点为非树结点，红黑树不应如此
                        print('rb_delete_fixup: Error Path 3')

                else:
                    # 如果 node 是其父结点的右孩子
                    if isinstance(node.parent, TreeNode):
                        # 记录 bro 为 node 父结点的左孩子，即 node 的兄弟结点
                        bro = node.parent.left
                        if isinstance(bro, TreeNode):
                            if bro.color:
                                # case 1': node 是其父结点的右孩子、其兄弟结点 bro 为红色
                                bro.color = False  # 让 bro 的颜色改为黑色
                                node.parent.color = True
                                self.right_rotate(node.parent)
                                bro = node.parent.left  # 确保 bro 还是 node 的兄弟结点
                            if isinstance(bro.left, TreeNode) and isinstance(bro.right, TreeNode):
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
                                        bro.color = True         # 修改 bro 为红色（一红挂两黑）
                                        self.left_rotate(bro)    # 左旋 bro
                                        bro = node.parent.left   # 确保 bro 还是 node 的兄弟结点
                                        # case 3' 之后，保证 bro 为黑色、bro 的左孩子为红色
                                    # case 4': 此时 node 是其父结点的右孩子，且兄弟结点 bro 一定为黑色
                                    # bro 的左孩子为红色，右孩子颜色为黑色
                                    bro.color = node.parent.color
                                    node.parent.color = False
                                    bro.left.color = False
                                    self.right_rotate(node.parent)
                                    node = self.bst
                            else:
                                # bro 结点的孩子为非树结点，红黑树不应如此
                                print('rb_delete_fixup: Error Path 1+')
                        else:
                            # node 的兄弟结点为非树结点，红黑树不应如此
                            print('rb_delete_fixup: Error Path 2+')
                    else:
                        # node 的父结点为非树结点，红黑树不应如此
                        print('rb_delete_fixup: Error Path 3+')

            # 最终将 node 的颜色置为黑色
            node.color = False

    # 根据 key 值删除结点
    # 删除黑色结点时，可能违反红黑性质，需要调用 rb_delete_fixup 维护红黑性质
    # 时间复杂度 O(log n) 与树高有关
    def rb_delete(self, root, delete_key):
        if self.is_bst_empty:
            print('提示：红黑树为空，无法继续删除。')
        else:
            ptr = root           # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索插入位置
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                if delete_key == ptr.key:
                    break            # 定位到了目标删除结点
                elif delete_key < ptr.key:
                    ptr = ptr.left   # 小则往左
                else:
                    ptr = ptr.right  # 大则往右

            # 若没找到目标结点
            if not isinstance(ptr, TreeNode) or ptr == self.nil:
                print('提示：删除时，找不到 key 为', delete_key, '的元素')

            else:
                if ptr == self.bst and ptr.key == delete_key and \
                        (not isinstance(ptr.left, TreeNode) or ptr.left == self.nil) and \
                        (not isinstance(ptr.right, TreeNode) or ptr.right == self.nil):
                    # 当前 BST 仅有一个根结点 ptr，且欲删除根结点，会导致树空
                    self.is_bst_empty = True
                    self.sorted_key_list = []
                else:
                    # 正常删除结点 ptr，不会导致树变为空
                    # 这里的 y 主要用于记录 ptr 的后继，而 x 记录真正被删除的结点
                    y = ptr
                    y_original_color = y.color  # 记录 y 原始的颜色，用于最后判断是否需要维护红黑性质

                    if ptr.left == self.nil:
                        # 如果欲删除结点 ptr 的左孩子为空，则将 ptr 替换为其右孩子
                        x = ptr.right
                        self.rb_transplant(ptr, ptr.right)
                    elif ptr.right == self.nil:
                        # 如果欲删除结点 ptr 的右孩子为空，则将 ptr 替换为其左孩子
                        x = ptr.left
                        self.rb_transplant(ptr, ptr.left)
                    else:
                        # 欲删除结点 ptr 的左右孩子均不为空，则将 ptr 替换为其后继
                        y = self.successor(ptr)     # y 为 ptr 的后继，y 的左孩子为 nil
                        y_original_color = y.color  # (修改)记录 y 原始的颜色
                        x = y.right
                        if y.parent == ptr:
                            # 如果 ptr 的后继 y 就是 ptr 的直接右孩子
                            if isinstance(x, TreeNode):
                                x.parent = y
                            else:
                                # ptr 的后继 y 的右孩子为非树结点，红黑树不应如此
                                print('rb_delete: Error Path 1')
                        else:
                            # 如果 ptr 的后继 y 不是 ptr 的直接右孩子
                            # 让 y 被其右孩子替换（因为之后 y 要用于替换 ptr）
                            # 所以真正需要被删除的结点就是 y.right，也就是 x
                            if isinstance(y.right, TreeNode):
                                self.rb_transplant(y, y.right)
                                y.right = ptr.right
                                y.right.parent = y
                            else:
                                # ptr 的后继 y 的右孩子为非树结点，红黑树不应如此
                                print('rb_delete: Error Path 2')

                        # 现在把 ptr 替换为其后继结点 y，并修改链接关系和 color（不修改 key、value）
                        self.rb_transplant(ptr, y)
                        y.left = ptr.left
                        y.left.parent = y
                        y.color = ptr.color  # y 继承 ptr 的颜色
                    # 最后，如果"真正"删除的结点颜色为黑色，则破坏了红黑性质，需要进行维护
                    if not y_original_color:
                        self.rb_delete_fixup(x)  # 删除后维护红黑性质

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
        [1, 10], [2, 20], [3, 30], [7, 70],
        [8, 80], [9, 90], [4, 40]
    ]

    # kv_array = [[i, 100 * i] for i in range(1000)]
    # kv_array = [[i, 100 * i] for i in reversed(range(1000))]

    # 像这种 key 基本有序地插入，如果是普通的 BST，那么树结构会退化地很严重，大幅影响效率
    start = time.process_time()
    rbt = RedBlackTree(kv_array)
    end = time.process_time()
    print('建立 Red-Black Tree 耗时: %.5f ms' % ((end - start) * 1000))

    # 输出升序排序的结果
    print(rbt.get_sorted_key_list())  # [1, 2, 3, 4, 7, 8, 9]

    # 搜索值
    search_key = 4
    start = time.process_time()
    ans = rbt.search(search_key)
    end = time.process_time()

    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')

    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 检查某二叉树是否为 BST
    root = TreeNode(3)
    root.left = TreeNode(1)
    root.right = TreeNode(5)
    print(rbt.check_bst(root))  # True

    root.left.left = TreeNode(10)
    print(rbt.check_bst(root))  # False

    # 删除结点
    rbt.rb_delete(rbt.bst, 17)  # 找不到

    # 结点 9 没有左右孩子，直接删除，然后调整其所有祖先结点的平衡性
    # 删除后结点 8 的高度减为 1，因此结点 7 不平衡了，需要调整
    rbt.rb_delete(rbt.bst, 9)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # [1, 2, 3, 4, 7, 8]
    # 此处可通过断点调试查看树结构，rbt.bst 为树根

    rbt.rb_delete(rbt.bst, 3)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # [1, 2, 4, 7, 8]

    rbt.rb_delete(rbt.bst, 7)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # [1, 2, 4, 8]

    rbt.rb_delete(rbt.bst, 8)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # [1, 2, 4]

    rbt.rb_delete(rbt.bst, 2)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # [1, 4]

    rbt.rb_delete(rbt.bst, 1)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # [4]

    rbt.rb_delete(rbt.bst, 4)
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # []

    # 删空之后测试再删
    rbt.rb_delete(rbt.bst, 3)  # 提示 BST 为空
    rbt.update_sorted_key_list()
    print(rbt.get_sorted_key_list())  # []

    # 删空之后测试查找
    search_key = 4
    ans = rbt.search(search_key)  # 找不到
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')

    # 重新动态增加（降序测试）
    for key in reversed(range(1, 10)):
        val = key * 100
        rbt.rb_insert(key, val)
        rbt.update_sorted_key_list()
        print(rbt.get_sorted_key_list())

    # 再次测试查找
    search_key = 4
    ans = rbt.search(search_key)
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key 为', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key 为', search_key, '的元素')


if __name__ == "__main__":
    sys.exit(main())
