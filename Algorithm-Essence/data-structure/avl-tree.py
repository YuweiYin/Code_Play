#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : avl-tree.py
@Author  : YuweiYin
=================================================="""

# import gc
import sys
import time

"""
AVL 树 (Adelson-Velsky-Landis Tree)
平衡二叉搜索树 (Balanced Binary Search Tree)

参考资料：
https://www.youtube.com/watch?v=FNeL18KsWPc
"""


class TreeNode:
    def __init__(self, key=0, val=0):
        self.key = key       # 键，按键构造 BST/AVL 树，并进行搜索/增添/删除
        self.val = val       # 值，树结点存储的值，可以为任意对象
        self.height = 1      # 初始时树高为 1
        self.left = None     # 左孩子指针
        self.right = None    # 右孩子指针
        self.parent = None   # 父结点指针


class AvlTree:
    # 构造 AVL 树（平衡的二叉搜索树）
    # 时间复杂度 O(n log n)
    def __init__(self, kv_array):
        self.bst = None  # 二叉搜索树结构，树根
        self.sorted_key_list = []

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 TreeNode 并插入 BST
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.insert(kv[0], kv[1])
            # 中序遍历，获取 sorted_key_list 升序数组/列表
            self.update_sorted_key_list()

    # 中序遍历，将 BST 结点的 key 值（升序排列）存储于 sorted_key_list
    # 时间复杂度 O(n)
    def inorder_traversal(self, root):
        if isinstance(root, TreeNode):
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

    # 辅助操作：平衡性检测、平衡因子计算
    # 时间复杂度 O(1)
    # 判断 node 结点是否平衡，返回左子树高度减去右子树高度
    # 即计算其左右子树的平衡因子 (Balanced Factor) 差距
    # 如果差距不大于 1，则平衡，否则不平衡，需要通过旋转操作来调整至平衡。
    @staticmethod
    def balanced_factor(node):
        if isinstance(node, TreeNode):
            left_height = 0 if not isinstance(node.left, TreeNode) else node.left.height
            right_height = 0 if not isinstance(node.right, TreeNode) else node.right.height
            return left_height - right_height
        else:
            # 空结点平衡
            return 0

    # 辅助操作：递归计算 node 结点的高度
    # 时间复杂度 O(log n) 与树高有关
    def tree_height(self, node):
        if isinstance(node, TreeNode):
            return max(self.tree_height(node.left), self.tree_height(node.right)) + 1
        else:
            return 0

    # 辅助操作：左旋
    # 时间复杂度 O(1)
    # 返回替代了 node 的新结点
    @staticmethod
    def left_rotate(node_x):
        # 对 x 进行左旋，即让 x 的右孩子 y (x.right) 成为 x 的父结点，且 x 等于 y.left。
        # 而 y 结点原本的左孩子变为新 x 的右孩子
        if isinstance(node_x, TreeNode) and isinstance(node_x.right, TreeNode):
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

            # 仅需调整 x 和 y 的高度，由于此时 x 是 y 的左孩子，故先调整 x 的高度
            x_left_h = 0 if not isinstance(node_x.left, TreeNode) else node_x.left.height
            x_right_h = 0 if not isinstance(node_x.right, TreeNode) else node_x.right.height
            node_x.height = max(x_left_h, x_right_h) + 1

            # 有了 x 的高度，再调整 y 的高度
            y_right_h = 0 if not isinstance(node_y.right, TreeNode) else node_y.right.height
            node_y.height = max(node_x.height, y_right_h) + 1

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 辅助操作：右旋
    # 时间复杂度 O(1)
    # 返回替代了 node 的新结点
    @staticmethod
    def right_rotate(node_x):
        # 对 x 进行右旋，即让 x 的左孩子 y (x.left) 成为 x 的父结点，且 x 等于 y.right。
        # 而 y 结点原本的右孩子变为新 x 的左孩子
        if isinstance(node_x, TreeNode) and isinstance(node_x.left, TreeNode):
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

            # 仅需调整 x 和 y 的高度，由于此时 x 是 y 的右孩子，故先调整 x 的高度
            x_left_h = 0 if not isinstance(node_x.left, TreeNode) else node_x.left.height
            x_right_h = 0 if not isinstance(node_x.right, TreeNode) else node_x.right.height
            node_x.height = max(x_left_h, x_right_h) + 1

            # 有了 x 的高度，再调整 y 的高度
            y_left_h = 0 if not isinstance(node_y.left, TreeNode) else node_y.left.height
            node_y.height = max(node_x.height, y_left_h) + 1

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

    # 辅助操作：逐级向上进行 height 修改，以及平衡性调整
    # 两种情况下会调用：1. 插入结点后；2. "确实地"删除结点后。
    # 时间复杂度 O(log n) 与树高有关
    # 逐层向上调整，根据平衡因子 分四种情况，用旋转操作来调整平衡
    def maintain_balance(self, node):
        if isinstance(node, TreeNode):
            # 首先计算当前结点的新高度
            left_height = 0 if not isinstance(node.left, TreeNode) else node.left.height
            right_height = 0 if not isinstance(node.right, TreeNode) else node.right.height
            node.height = max(left_height, right_height) + 1

            # 然后判断当前结点是否平衡
            # bf = self.balanced_factor(node)
            bf = left_height - right_height
            if abs(bf) <= 1:
                # 如果当前结点平衡，则观察其父结点是否需要调整
                self.maintain_balance(node.parent)
            elif bf == 2:
                # 如果当前结点的左子树过高
                if isinstance(node.left, TreeNode):
                    left_bf = self.balanced_factor(node.left)
                    if left_bf == 1:
                        # case 1：左左结构 - node 的平衡因子 bf=2 且其左孩子的平衡因子 bf=1
                        # 把 node 右旋一次即可
                        _node = self.right_rotate(node)
                        if node == self.bst:
                            # 如果 node 是 BST 树根，那么需要更换树根
                            self.bst = _node
                        else:
                            if isinstance(_node, TreeNode):
                                self.maintain_balance(_node.parent)
                    elif left_bf == -1:
                        # case 2：左右结构 - node 的平衡因子 bf=2 且其左孩子的平衡因子 bf=-1
                        # 先把 node 的左孩子左旋一次，整体成为左左结构，再把 node 右旋一次即可
                        self.left_rotate(node.left)
                        _node = self.right_rotate(node)
                        if node == self.bst:
                            # 如果 node 是 BST 树根，那么需要更换树根
                            self.bst = _node
                        else:
                            if isinstance(_node, TreeNode):
                                self.maintain_balance(_node.parent)
                    else:
                        print('maintain_balance Error Path! node.left balanced factor:', left_bf)
                else:
                    print('maintain_balance Error Path! node.left is NOT a TreeNode. balanced_factor:', bf)

            elif bf == -2:
                # 如果当前结点的右子树过高
                if isinstance(node.right, TreeNode):
                    right_bf = self.balanced_factor(node.right)
                    if right_bf == 1:
                        # case 3：右左结构 - node 的平衡因子 bf=-2 且其左孩子的平衡因子 bf=1
                        # 先把 node 的右孩子右旋一次，整体成为右右结构，再把 node 左旋一次即可
                        self.right_rotate(node.right)
                        _node = self.left_rotate(node)
                        if node == self.bst:
                            # 如果 node 是 BST 树根，那么需要更换树根
                            self.bst = _node
                        else:
                            if isinstance(_node, TreeNode):
                                self.maintain_balance(_node.parent)
                    elif right_bf == -1:
                        # case 4：右右结构 - node 的平衡因子 bf=-2 且其左孩子的平衡因子 bf=-1
                        # 把 node 左旋一次即可
                        _node = self.left_rotate(node)
                        if node == self.bst:
                            # 如果 node 是 BST 树根，那么需要更换树根
                            self.bst = _node
                        else:
                            if isinstance(_node, TreeNode):
                                self.maintain_balance(_node.parent)
                    else:
                        print('maintain_balance Error Path! node.right balanced factor:', right_bf)
                else:
                    print('maintain_balance Error Path! node.right is NOT a TreeNode. balanced_factor:', bf)

            else:
                # abs(bf) > 2，这是不该出现的情况，因为原本是平衡的，而一次插入不会将高度提升 2
                print('maintain_balance Error Path! balanced_factor:', bf)
        else:
            # 当前结点 node 不是树结点，结束
            pass

    # 辅助操作：新建树结点
    @staticmethod
    def create_new_node(new_key, new_val):
        new_node = TreeNode(new_key, new_val)
        return new_node

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def clear_node_link(node):
        if isinstance(node, TreeNode):
            node.parent = None
            node.left = None
            node.right = None

    # 根据 key 值增加结点
    # 增加后（每次都增加叶结点），逐层向上移动，修改结点的 height 属性
    # 并判断每个结点是否平衡，若不平衡则旋转调整树结构
    # 时间复杂度 O(log n) 与树高有关
    # 插入成功返回 True；否则返回 False
    def insert(self, insert_key, insert_val):
        if isinstance(self.bst, TreeNode):
            ptr = self.bst
            while isinstance(ptr, TreeNode):
                if insert_key <= ptr.key:
                    # 如果新结点 key 值小于等于当前结点，则应该往左走
                    if isinstance(ptr.left, TreeNode):
                        # 如果当前结点左孩子不为空，则往左搜索插入位置
                        ptr = ptr.left
                    else:
                        # 如果当前结点左孩子为空，表示这就是该插入的位置
                        new_node = self.create_new_node(insert_key, insert_val)
                        new_node.parent = ptr
                        ptr.left = new_node
                        self.maintain_balance(ptr)  # 调整平衡
                        return True
                else:
                    # 如果新结点 key 值大于当前结点，则应该往右走
                    if isinstance(ptr.right, TreeNode):
                        # 如果当前结点右孩子不为空，则往左搜索插入位置
                        ptr = ptr.right
                    else:
                        # 如果当前结点右孩子为空，表示这就是该插入的位置
                        new_node = self.create_new_node(insert_key, insert_val)
                        new_node.parent = ptr
                        ptr.right = new_node
                        self.maintain_balance(ptr)  # 调整平衡
                        return True
            # 如果出了循环、到了这一步，表示插入失败
            return False
        else:
            # BST 树为空树，直接创建根结点，无需调整平衡
            self.bst = self.create_new_node(insert_key, insert_val)
            return True

    # 根据 key 值删除结点
    # 有父结点指针，便于删除操作
    # 删除成功则返回被删除结点，否则返回 None
    def delete(self, delete_key):
        if not isinstance(self.bst, TreeNode):
            # BST 树为空树，找不到目标结点
            print('当前树为空，没有 key 为', delete_key, '的元素')
        else:
            self._delete(self.bst, delete_key)

    # 实际执行的删除函数，可能递归
    def _delete(self, cur_root, delete_key):
        ptr = cur_root
        while isinstance(ptr, TreeNode):
            if delete_key < ptr.key:
                # 如果新结点 key 值小于当前结点，则应该往左走
                ptr = ptr.left
            elif delete_key > ptr.key:
                # 如果新结点 key 值大于当前结点，则应该往右走
                ptr = ptr.right
            else:
                # 找到了目标结点，根据左右孩子的情况，执行不同的删除操作
                if isinstance(ptr.left, TreeNode) and isinstance(ptr.right, TreeNode):
                    # 左右孩子均有，则用后继替换当前结点，并于右子树中删除此结点(递归)
                    # 在此情况下不会进行真正的删除，而是仅是替换。另外三种情况才会删除并返回被删结点
                    # 在真正删除后，需要逐级向上调整结点高度的平衡
                    successor_node = self.successor(ptr)
                    ptr.key = successor_node.key
                    ptr.val = successor_node.val
                    self._delete(ptr.right, successor_node.key)
                elif isinstance(ptr.left, TreeNode):
                    # 仅有左孩子
                    if isinstance(ptr.parent, TreeNode):
                        # 如果被删结点有父结点，则将父结点与被删结点的左孩子相关联
                        ptr.left.parent = ptr.parent
                        if ptr == ptr.parent.left:
                            ptr.parent.left = ptr.left
                        elif ptr == ptr.parent.right:
                            ptr.parent.right = ptr.left
                        else:
                            # 异常：被删结点既不是其父结点的左孩子，亦非右孩子
                            print('_delete: Error Path 1')
                            return None
                        self.maintain_balance(ptr.parent)  # 调整平衡
                    else:
                        # 如果被删结点没有父结点，表示删除的是树根 self.bst
                        if ptr == self.bst:
                            self.bst = ptr.left
                            self.bst.parent = None
                        else:
                            # 异常：被删结点本应是树根
                            print('_delete: Error Path 2')
                            return None
                    # 删除完毕后，清除被删结点的指针域，并返回该结点
                    self.clear_node_link(ptr)
                    return ptr
                elif isinstance(ptr.right, TreeNode):
                    # 仅有右孩子
                    if isinstance(ptr.parent, TreeNode):
                        # 如果被删结点有父结点，则将父结点与被删结点的右孩子相关联
                        ptr.right.parent = ptr.parent
                        if ptr == ptr.parent.left:
                            ptr.parent.left = ptr.right
                        elif ptr == ptr.parent.right:
                            ptr.parent.right = ptr.right
                        else:
                            # 异常：被删结点既不是其父结点的左孩子，亦非右孩子
                            print('_delete: Error Path 3')
                            return None
                        self.maintain_balance(ptr.parent)  # 调整平衡
                    else:
                        # 如果被删结点没有父结点，表示删除的是树根 self.bst
                        if ptr == self.bst:
                            self.bst = ptr.right
                            self.bst.parent = None
                        else:
                            # 异常：被删结点本应是树根
                            print('_delete: Error Path 5')
                            return None
                    # 删除完毕后，清除被删结点的指针域，并返回该结点
                    self.clear_node_link(ptr)
                    return ptr
                else:
                    # 没有孩子，检查是否为根
                    if ptr == self.bst:
                        self.bst = None
                    else:
                        # 删除此叶结点
                        if ptr == ptr.parent.left:
                            ptr.parent.left = None
                        elif ptr == ptr.parent.right:
                            ptr.parent.right = None
                        else:
                            # 异常：被删结点既不是其父结点的左孩子，亦非右孩子
                            print('_delete: Error Path 6')
                            return None
                        self.maintain_balance(ptr.parent)  # 调整平衡
                    # 删除完毕后，清除被删结点的指针域，并返回该结点
                    self.clear_node_link(ptr)
                    return ptr
        # 如果出了循环、到了这一步，表示找不到
        return None

    # 找到一棵以 root 为根的 BST/AVL 中的最小值结点（一路向左）
    # 时间复杂度 O(log n) 与树高有关
    @staticmethod
    def min_bst(root):
        if isinstance(root, TreeNode):
            while isinstance(root.left, TreeNode):
                root = root.left
            return root
        else:
            return None

    # 找到一棵以 root 为根的 BST/AVL 中的最大值结点（一路向右）
    # 时间复杂度 O(log n) 与树高有关
    @staticmethod
    def max_bst(root):
        if isinstance(root, TreeNode):
            while isinstance(root.right, TreeNode):
                root = root.right
            return root
        else:
            return None

    # 找到在 BST 中 node 结点的前驱结点
    # 如果 node 的左孩子存在，则 node 的前驱就是其左子树中的最大值
    # 如果 node 的左孩子不存在，则 node 的前驱是其某个祖先结点 a，满足此时 a.right == node
    # 时间复杂度 O(log n) 与树高有关
    def predecessor(self, node):
        if isinstance(node, TreeNode):
            if isinstance(node.left, TreeNode):
                return self.max_bst(node.left)
            else:
                while node != self.bst:
                    if node.parent.right == node:
                        return node.parent
                    else:
                        node = node.parent
                return None
        else:
            return None

    # 找到在 BST 中 node 结点的后继结点
    # 如果 node 的右孩子存在，则 node 的后继就是其右子树中的最小值
    # 如果 node 的右孩子不存在，则 node 的前驱是其某个祖先结点 a，满足此时 a.left == node
    # 时间复杂度 O(log n) 与树高有关
    def successor(self, node):
        if isinstance(node, TreeNode):
            if isinstance(node.right, TreeNode):
                return self.min_bst(node.right)
            else:
                while node != self.bst:
                    if node.parent.left == node:
                        return node.parent
                    else:
                        node = node.parent
                return None
        else:
            return None

    # 检查一棵以 root 为根的二叉树是否为 BST
    def check_bst(self, root):
        if root is None:
            # 当前结点为 None，空树也算作是 BST
            return True
        elif not isinstance(root, TreeNode):
            # 不是 TreeNode 结点，不是 BST
            return False
        else:
            # 左/右孩子为空时，左/右孩子满足 BST 条件
            left_bst = True  # 左孩子是否满足 BST 条件
            right_bst = True  # 右孩子是否满足 BST 条件

            if isinstance(root.left, TreeNode):
                # 如果当前结点的左孩子不为空，检查该左孩子的值
                if root.left.key <= root.key:
                    # 如果左孩子的值小于等于当前结点的值，表示满足 BST 条件，继续往左观察
                    left_bst = self.check_bst(root.left)
                else:
                    # 如果左孩子的值大于当前结点的值，表示不满足 BST 条件
                    return False

            if isinstance(root.right, TreeNode):
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
    # 以插入的方式，构建 BST/AVL
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    kv_array = [
        [1, 100], [2, 200], [3, 300], [7, 700],
        [8, 800], [9, 900], [4, 400]
    ]
    # 像这种 key 基本有序地插入，如果是普通的 BST，那么树结构会退化地很严重，大幅影响效率
    avl = AvlTree(kv_array)

    # 输出升序排序的结果
    print(avl.get_sorted_key_list())  # [1, 2, 3, 4, 7, 8, 9]

    # 搜索值
    search_key = 4
    start = time.process_time()
    ans = avl.search(search_key)
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
    print(avl.check_bst(root))  # True

    root.left.left = TreeNode(10)
    print(avl.check_bst(root))  # False

    # 删除结点
    avl.delete(17)  # 找不到

    # 结点 9 没有左右孩子，直接删除，然后调整其所有祖先结点的平衡性
    # 删除后结点 8 的高度减为 1，因此结点 7 不平衡了，需要调整
    avl.delete(9)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # [1, 2, 3, 4, 7, 8]
    # 此处可通过断点调试查看树结构，avl.bst 为树根

    avl.delete(3)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # [1, 2, 4, 7, 8]

    avl.delete(7)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # [1, 2, 4, 8]

    avl.delete(8)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # [1, 2, 4]

    avl.delete(2)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # [1, 4]

    avl.delete(4)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # [1]

    avl.delete(1)
    avl.update_sorted_key_list()
    print(avl.get_sorted_key_list())  # []

    avl.delete(9)  # 找不到


if __name__ == "__main__":
    sys.exit(main())
