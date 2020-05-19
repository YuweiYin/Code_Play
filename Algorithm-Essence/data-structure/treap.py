#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/data_structure
@File    : treap.py
@Author  : YuweiYin
@Date    : 2020-05-08
=================================================="""

# import gc
import sys
import time
import random

"""
堆树 Treap

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 13
"""


class TreeNode:
    def __init__(self, key=0, val=0, priority=0):
        self.key = key       # 键，按键构造 BST 树，并进行搜索/增添/删除
        self.val = val       # 值，树结点存储的值，可以为任意对象
        self.priority = priority   # 结点的优先级，用于构建最小堆
        self.left = None     # 左孩子指针
        self.right = None    # 右孩子指针
        self.parent = None   # 父结点指针
        self.is_left = True  # True 则表示自己是父结点的左孩子(默认)，否则为右孩子


class Treap:
    # 构造 Treap（这里利用的是最小堆，但最大堆也可以）
    # 时间复杂度 O(n)
    def __init__(self, kv_array):
        self.bst = None             # 二叉搜索树结构，树根
        self.inf = 0x3f3f3f3f       # 0..inf 是优先级的随机选择范围
        self.used_priority = set()  # 集合，存储当前已经使用过的优先级
        self.sorted_key_list = []   # 已排好序的 key 列表

        if isinstance(kv_array, list) and len(kv_array) > 0:
            # 依次将 array 中的元素作为 key 值构造 TreeNode 并插入 BST
            for kv in kv_array:
                if isinstance(kv, list) and len(kv) == 2:
                    self.treap_insert(kv[0], kv[1])
            # 中序遍历，获取 sorted_list 升序数组/列表
            self.update_sorted_list()

    # 中序遍历，将 BST 结点的 key 值（升序排列）存储于 sorted_list
    # 时间复杂度 O(n)
    def inorder_traversal(self, root):
        if root is not None and isinstance(root, TreeNode):
            self.inorder_traversal(root.left)
            self.sorted_key_list.append(root.key)
            self.inorder_traversal(root.right)

    # 调用中序遍历，更新 sorted_list
    def update_sorted_list(self):
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
                if node_x.is_left:
                    node_x.parent.left = node_y
                    node_y.is_left = True
                else:
                    node_x.parent.right = node_y
                    node_y.is_left = False

            node_x.right = node_y.left  # y 结点原本的左孩子变为新 x 的右孩子
            if isinstance(node_y.left, TreeNode):
                node_y.left.parent = node_x
                node_y.left.is_left = False

            node_y.left = node_x
            node_x.parent = node_y
            node_x.is_left = True

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
                if node_x.is_left:
                    node_x.parent.left = node_y
                    node_y.is_left = True
                else:
                    node_x.parent.right = node_y
                    node_y.is_left = False

            node_x.left = node_y.right  # y 结点原本的右孩子变为新 x 的左孩子
            if isinstance(node_y.right, TreeNode):
                node_y.right.parent = node_x
                node_y.right.is_left = True

            node_y.right = node_x
            node_x.parent = node_y
            node_x.is_left = False

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 根据 key 值搜索结点
    # 如果搜索到了，则返回结点 TreeNode，如果搜索不到，则返回 None
    def treap_search(self, search_key):
        if not isinstance(self.bst, TreeNode):
            # 如果当前 BST 为空，则找不到
            print('提示：搜索时，Treap 为空，无法找到目标元素。')
            return None
        else:
            # 否则正常搜索
            ptr = self.bst
            while isinstance(ptr, TreeNode):
                if search_key == ptr.key:
                    return ptr  # 搜索到了
                elif search_key < ptr.key:
                    if isinstance(ptr.left, TreeNode):
                        ptr = ptr.left  # 小则往左
                    else:
                        print('提示：搜索时，无法找到 key 为', search_key, '的目标元素。')
                        return None  # 左孩子为空，找不到
                else:
                    if isinstance(ptr.right, TreeNode):
                        ptr = ptr.right  # 大则往右
                    else:
                        print('提示：搜索时，无法找到 key 为', search_key, '的目标元素。')
                        return None  # 右孩子为空，找不到

    # 辅助操作：新建并返回具有随机优先级的结点
    def create_new_node(self, new_key, new_val):
        new_node = TreeNode(new_key, new_val)
        random.seed(id(new_node))  # 以新结点对象的唯一标识符 id 作为随机数种子
        priority = random.randint(1, self.inf)  # 生成整型随机数
        # 如果优先级重复，则更换随机数 TODO 思考更优的随机优先级分配方案
        while priority in self.used_priority:
            priority = random.randint(1, self.inf)  # 更换一个随机数
        self.used_priority.add(priority)  # 将选取好的不重复的优先级存储于集合中
        new_node.priority = priority
        return new_node

    # Treap 按 key 插入新结点，并给出 value
    def treap_insert(self, insert_key, insert_val):
        if not isinstance(self.bst, TreeNode):
            # 如果当前 BST 为空，创建新结点作为树根
            self.bst = self.create_new_node(insert_key, insert_val)
        else:
            # 否则正常插入，先寻找应插入位置
            ptr = self.bst
            while isinstance(ptr, TreeNode):
                if insert_key <= ptr.key:
                    if isinstance(ptr.left, TreeNode):
                        ptr = ptr.left  # 小则往左
                    else:
                        # 找到了插入位置，即 ptr.left
                        new_node = self.create_new_node(insert_key, insert_val)
                        new_node.parent = ptr
                        new_node.is_left = True
                        ptr.left = new_node
                        # 插入后逐级往上维护最小堆性质 (根据优先级)
                        self._treap_priority_fixup(ptr.left)
                        break
                else:
                    if isinstance(ptr.right, TreeNode):
                        ptr = ptr.right  # 大则往右
                    else:
                        # 找到了插入位置，即 ptr.right
                        new_node = self.create_new_node(insert_key, insert_val)
                        new_node.parent = ptr
                        new_node.is_left = False
                        ptr.right = new_node
                        # 插入后逐级往上维护最小堆性质 (根据优先级)
                        self._treap_priority_fixup(ptr.right)
                        break

    # 辅助操作：Treap 插入结点之后，逐级向上根据优先级 priority 维护最小堆性质
    # 时间复杂度 O(log n) 与树高有关
    # 根据当前结点的优先级与其父结点的优先级对比，分 2 种情况，用旋转操作来调整平衡
    def _treap_priority_fixup(self, node):
        if isinstance(node, TreeNode):
            if isinstance(node.parent, TreeNode):
                if node.priority < node.parent.priority:
                    # 当前结点的优先级比其父结点低，需要上移
                    if node.is_left:
                        # 当前结点是其父结点的左孩子，则右旋其父
                        node = self.right_rotate(node.parent)
                    else:
                        # 当前结点是其父结点的右孩子，则左旋其父
                        node = self.left_rotate(node.parent)
                    if node is not None and isinstance(node, TreeNode) and \
                            isinstance(node.parent, TreeNode):
                        # 如果当前结点的父结点存在，则递归、继续往上调整
                        self._treap_priority_fixup(node)
                    else:
                        return
                else:
                    # 当前结点的优先级不比父结点低，未破坏最小堆性质，可终止
                    return
            else:
                # 当前结点的父结点为非树结点，可终止
                return
        else:
            # 当前结点为非树结点，可终止
            return

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def clear_node_link(node):
        if isinstance(node, TreeNode):
            node.left = None
            node.right = None
            node.parent = None

    # 根据 key 值删除结点，并返回被删除的结点
    # 时间复杂度 O(log n) 与树高有关
    def treap_delete(self, delete_key):
        if not isinstance(self.bst, TreeNode):
            # 如果当前 BST 为空，则找不到目标 key，故无法删除
            # print('删除提示 1：Treap 为空，无法找到目标元素。')
            return None
        else:
            return self._treap_delete(self.bst, delete_key)

    # 实际执行的删除函数，可能递归
    def _treap_delete(self, root, delete_key):
        if root is None or not isinstance(root, TreeNode):
            # 如果当前结点为空，则找不到目标 key，故无法删除
            return None
        else:
            # 否则正常删除，先搜索目标 key 位置
            ptr = root
            while isinstance(ptr, TreeNode):
                if delete_key == ptr.key:
                    # 搜索到了目标 key，根据目标结点的孩子数目进行删除处理
                    delete_node = ptr
                    if isinstance(ptr.left, TreeNode) and isinstance(ptr.right, TreeNode):
                        # 目标结点左右孩子都有，则先用后继替换此结点，然后从右子树中删除该后继
                        # 替换时，当前结点的优先级保留
                        successor = self.successor(ptr)
                        ptr.key = successor.key
                        ptr.val = successor.val
                        # 向右递归，从右子树中删除该后继
                        if successor == ptr.right:
                            # 后继等于右孩子，表示右孩子没有 left，
                            # 那么该直接删除该右孩子，把其 right 接到本结点
                            if isinstance(ptr.right.right, TreeNode):
                                # 右孩子的 right 是树结点类型
                                ptr.right.right.parent = ptr
                                ptr.right.right.is_left = False
                                ptr.right = ptr.right.right
                            else:
                                # 右孩子既没有 left 也没有 right
                                ptr.right = None
                            # 清除 self.used_priority 中 successor 结点的优先级
                            if successor.priority in self.used_priority:
                                self.used_priority.remove(successor.priority)
                            self.clear_node_link(successor)
                            return successor
                        else:
                            self._treap_delete(ptr.right, successor.key)
                    else:
                        if isinstance(ptr.left, TreeNode):
                            # 目标结点仅有左孩子，用左孩子替换自己，最小堆性质不会改变
                            ptr.left.parent = ptr.parent
                            if isinstance(ptr.parent, TreeNode):
                                if ptr.is_left:
                                    ptr.parent.left = ptr.left
                                    ptr.left.is_left = True
                                else:
                                    ptr.parent.right = ptr.left
                                    ptr.left.is_left = False
                            else:
                                # 如果待删除结点 ptr 没有父结点，则表示为根结点，需要更换树根
                                if ptr == self.bst:
                                    self.bst = ptr.left
                                else:
                                    # 不应走此 Path
                                    print('treap_delete: Error Path1 - delete_key=', delete_key)
                        elif isinstance(ptr.right, TreeNode):
                            # 目标结点仅有右孩子，用右孩子替换自己，最小堆性质不会改变
                            ptr.right.parent = ptr.parent
                            if isinstance(ptr.parent, TreeNode):
                                if ptr.is_left:
                                    ptr.parent.left = ptr.right
                                    ptr.right.is_left = True
                                else:
                                    ptr.parent.right = ptr.right
                                    ptr.right.is_left = False
                            else:
                                # 如果待删除结点 ptr 没有父结点，则表示为根结点，需要更换树根
                                if ptr == self.bst:
                                    self.bst = ptr.right
                                else:
                                    # 不应走此 Path
                                    print('treap_delete: Error Path2 - delete_key=', delete_key)
                        else:
                            # 目标结点没有左右孩子，直接删除，最小堆性质不会改变
                            if isinstance(ptr.parent, TreeNode):
                                # 根据它是其父结点的左孩子还是右孩子，单向切断链接关系
                                if ptr.is_left:
                                    ptr.parent.left = None
                                else:
                                    ptr.parent.right = None
                            else:
                                # 此结点既没有左右孩子，父结点还为非树结点，表示删除的是树根
                                if ptr == self.bst:
                                    self.bst = None
                                else:
                                    # 不应走此 Path
                                    print('treap_delete: Error Path3 - delete_key=', delete_key)
                        # 清除 self.used_priority 中本结点的优先级
                        if delete_node.priority in self.used_priority:
                            self.used_priority.remove(delete_node.priority)
                        self.clear_node_link(delete_node)
                        return delete_node  # 返回被删除的结点
                elif delete_key < ptr.key:
                    if isinstance(ptr.left, TreeNode):
                        ptr = ptr.left  # 小则往左
                    else:
                        # print('删除提示 2：删除时，无法找到 key 为', delete_key, '的目标元素。')
                        return None  # 左孩子为空，找不到
                else:
                    if isinstance(ptr.right, TreeNode):
                        ptr = ptr.right  # 大则往右
                    else:
                        # print('删除提示 3：删除时，无法找到 key 为', delete_key, '的目标元素。')
                        return None  # 右孩子为空，找不到

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

    # 找到在 BST 中 node 结点的前驱结点，即：其左子树中的最大值
    # 时间复杂度 O(log n) 与树高有关
    def predecessor(self, node):
        if isinstance(node, TreeNode):
            return self.max_bst(node.left)
        else:
            return None

    # 找到在 BST 中 node 结点的后继结点，即：其右子树中的最小值
    # 时间复杂度 O(log n) 与树高有关
    def successor(self, node):
        if isinstance(node, TreeNode):
            return self.min_bst(node.right)
        else:
            return None

    # 检查一棵以 root 为根的二叉树是否为 BST
    def check_bst(self, root):
        if not root:
            # 空树也算作是 BST
            return True
        elif not isinstance(root, TreeNode):
            # 当前结点非空，但是非树结点，不合法
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
    # 以插入的方式，构建 BST/RBT
    # kv_array 为二维数组，内维度的数组，首元素为 key，次元素为 value，可以为任意对象
    kv_array = [
        [1, 10], [2, 20], [3, 30], [7, 70],
        [8, 80], [9, 90], [4, 40]
    ]
    # 像这种 key 基本有序地插入，如果是普通的 BST，那么树结构会退化地很严重，大幅影响效率
    treap = Treap(kv_array)

    # 输出升序排序的结果
    print(treap.get_sorted_key_list())  # [1, 2, 3, 4, 7, 8, 9]

    # 搜索值
    search_key = 4
    start = time.process_time()
    ans = treap.treap_search(search_key)
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
    print(treap.check_bst(root))  # True

    root.left.left = TreeNode(10)
    print(treap.check_bst(root))  # False

    # 删除结点，预期结果如下：
    # 找不到 key= 17  的结点
    # [1, 2, 3, 4, 7, 8]
    # [1, 2, 4, 7, 8]
    # [1, 2, 4, 8]
    # [1, 2, 4]
    # [1, 4]
    # [4]
    # []
    # 找不到 key= 3  的结点
    delete_key_list = [17, 9, 3, 7, 8, 2, 1, 4, 3]
    for delete_key in delete_key_list:
        deleted_node = treap.treap_delete(delete_key)
        if isinstance(deleted_node, TreeNode):
            # print('删除了 key=', deleted_node.key, ' val=', deleted_node.val, ' 的结点')
            # print('删除了 key=', deleted_node.key, ' 的结点')
            treap.update_sorted_list()
            print(treap.get_sorted_key_list())
        else:
            print('找不到 key=', delete_key, ' 的结点')

    # 删空之后测试查找。预期如下：
    # 提示：搜索时，Treap 为空，无法找到目标元素。
    # 找不到 key= 4 的元素
    search_key = 4
    ans = treap.treap_search(search_key)  # 找不到
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key=', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key=', search_key, '的元素')

    # 重新动态增加（降序测试）
    for key in reversed(range(1, 10)):
        val = key * 100
        treap.treap_insert(key, val)
        treap.update_sorted_list()
        print(treap.get_sorted_key_list())

    # 再次测试查找。预期如下：
    # 找到了 key= 4 的元素，其值为: 400
    search_key = 4
    ans = treap.treap_search(search_key)
    if ans is not None and isinstance(ans, TreeNode):
        print('找到了 key=', ans.key, '的元素，其值为:', ans.val)
    else:
        print('找不到 key=', search_key, '的元素')


if __name__ == "__main__":
    sys.exit(main())
