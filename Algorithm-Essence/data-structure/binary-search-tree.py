#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : binary-search-tree.py
@Author  : YuweiYin
@Date    : 2020-05-04
=================================================="""

# import gc
import sys
import time

"""
二叉排序/搜索树 (Binary Sort/Search Tree, BST)

参考资料：
https://www.youtube.com/watch?v=pYT9F8_LFTM
https://www.youtube.com/watch?v=COZK7NATh4k
https://www.youtube.com/watch?v=gcULXE7ViZw
https://www.youtube.com/watch?v=yEwSGhSsT0U
"""


class TreeNode:
    def __init__(self, key=0, val=0):
        self.key = key      # 键，按键构造 BST 树，并进行搜索/增添/删除
        self.val = val      # 值，树结点存储的值，可以为任意对象
        self.left = None    # 左孩子
        self.right = None   # 右孩子
        self.parent = None  # 父结点。便于删除、以及其它逐层向上的调整操作


class BinarySearchTree:
    # 构造 BST
    # 时间复杂度 O(n log n)
    def __init__(self, kv_array):
        self.bst = None
        self.sorted_key_list = []  # 存储排好序的

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 TreeNode 并插入 BST
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.insert(kv[0], kv[1])
            # 中序遍历，获取 sorted_list 升序数组/列表
            self.update_sorted_list()

    # 中序遍历，将 BST 结点的 key 值（升序排列）存储于 sorted_list
    def inorder_traversal(self, root):
        if isinstance(root, TreeNode):
            self.inorder_traversal(root.left)
            self.sorted_key_list.append(root.key)
            self.inorder_traversal(root.right)

    # 调用中序遍历，更新 sorted_key_list
    def update_sorted_list(self):
        self.sorted_key_list = []
        self.inorder_traversal(self.bst)

    # 获得 sorted_key_list
    def get_sorted_key_list(self):
        return self.sorted_key_list

    # 根据 key 值搜索结点
    # 如果搜索到了，则返回结点 TreeNode；否则返回 None
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
                        return True
            # 如果出了循环、到了这一步，表示插入失败
            return False
        else:
            # BST 树为空树
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
                    # 删除完毕后，清除被删结点的指针域，并返回该结点
                    self.clear_node_link(ptr)
                    return ptr
        # 如果出了循环、到了这一步，表示找不到
        return None

    # 找到一棵以 root 为根的 BST 中的最小值结点（一路向左）
    # 时间复杂度 O(log n) 与树高有关
    @staticmethod
    def min_bst(root):
        if isinstance(root, TreeNode):
            while isinstance(root.left, TreeNode):
                root = root.left
            return root
        else:
            return None

    # 找到一棵以 root 为根的 BST 中的最大值结点（一路向右）
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
            left_bst = True   # 左孩子是否满足 BST 条件
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
    # 以插入的方式，构建 BST
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    kv_array = [
        [15, 100], [10, 200], [20, 300], [8, 400],
        [12, 500], [17, 600], [25, 700]
    ]
    bst = BinarySearchTree(kv_array)

    # 输出升序排序的结果
    print(bst.get_sorted_key_list())  # [8, 10, 12, 15, 17, 20, 25]

    # 搜索值
    search_key = 12
    start = time.process_time()
    ans = bst.search(search_key)
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
    print(bst.check_bst(root))  # True

    root.left.left = TreeNode(10)
    print(bst.check_bst(root))  # False

    # 删除结点
    bst.delete(19)  # 找不到

    bst.delete(25)  # 25 没有左右孩子
    bst.update_sorted_list()
    print(bst.get_sorted_key_list())  # [8, 10, 12, 15, 17, 20]

    bst.delete(20)  # 20 没有左右孩子
    bst.update_sorted_list()
    print(bst.get_sorted_key_list())  # [8, 10, 12, 15, 17]

    bst.delete(15)  # 15 是 BST 的根，有左右孩子，递归删除
    bst.update_sorted_list()
    print(bst.get_sorted_key_list())  # [8, 10, 12, 17]

    bst.delete(10)  # 10 不是 BST 的根，有左右孩子，递归删除
    bst.update_sorted_list()
    print(bst.get_sorted_key_list())  # [8, 12, 17]


if __name__ == "__main__":
    sys.exit(main())
