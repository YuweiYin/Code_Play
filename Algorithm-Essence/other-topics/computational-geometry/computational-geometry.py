#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""=================================================
@Project : algorithm/other-topics/computational-geometry
@File    : computational-geometry.py
@Author  : YuweiYin
@Date    : 2020-06-13
=================================================="""

import sys
import time

"""
- 计算几何学 Computational Geometry
    - (欧几里得空间)点和线段的构造
    - 给定两条线段，判断二者是否相交
    - 给定线段集合，判断其中是否存在相交线段
    - 给定点集，寻找该点集的凸包 convex hull
        - (可利用凸包求出该点集的最远点对)
    - 给定点集，寻找最近点对

参考资料：
Introduction to Algorithm (aka CLRS) Third Edition - Chapter 33
"""


# (欧几里得空间)点结构体, 单点也可视作为向量 p_0 -> p 其中 p_0 表示坐标系原点
class Point:
    def __init__(self, vec, key, val=None, dim=2):
        self.vec = vec  # 坐标(coordinate): dim 长度的列表
        self.dim = dim  # 维度，默认维度为 2-平面几何
        self.key = key  # 关键字
        self.val = val  # 值对象

    # 类序列化输出方法
    def __str__(self):
        return 'key:' + str(self.key) + '\tval:' + str(self.val) + \
               '\tdim:' + str(self.dim) + '\tvec:' + str(self.vec)


# (欧几里得空间)线段结构体
class Segment:
    def __init__(self, from_point, to_point, key, val=None, is_directed=False):
        self.from_point = from_point    # 线段的起点
        self.to_point = to_point        # 线段的终点
        self.is_directed = is_directed  # True 表示此线段是有向线段，否则为无向线段
        self.key = key  # 关键字
        self.val = val  # 值对象

    # 类序列化输出方法
    def __str__(self):
        return 'key:' + str(self.key) + '\tval:' + str(self.val) + '\tis_directed:' + str(self.is_directed) + \
               '\nfrom:' + str(self.from_point) + '\nto:' + str(self.to_point)


# 线段端点结构体
class Endpoint:
    def __init__(self, key, point, seg, dim=2):
        self.key = key  # 关键字
        self.point = point  # 此端点对应的点 Point 结构体
        self.seg = seg  # 此端点所属的线段 Segment 结构体
        self.dim = dim  # 维度，默认维度为 2-平面几何

    # 类序列化输出方法
    def __str__(self):
        return 'key:' + str(self.key) + '\tdim:' + str(self.dim) + \
               '\npoint:' + str(self.point) + '\nseg:' + str(self.seg)


# (欧几里得空间)计算几何学算法
class ComputationalGeometry:
    def __init__(self, dim=2):
        self.dim = dim  # 当前处理的欧氏空间维度，默认为 2-平面几何

    # 对于两个向量，逐元素地操作 (例如：加减乘除等)
    # func 须是 lambda 表达式。默认为加法
    @staticmethod
    def vector_operation_by_ele(vec_1, vec_2, func=lambda x, y: x + y):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        res_vec = []
        for i in range(len(vec_1)):
            res_vec.append(func(vec_1[i], vec_2[i]))
        return res_vec

    # 计算两向量(列表)的内积/点积
    @staticmethod
    def inner_product(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        dim = len(vec_1)
        # 对应位置相乘 再求和
        res = 0
        for i in range(dim):
            res += vec_1[i] * vec_2[i]
        return res

    # 计算两向量(列表)的叉积
    # 这里只考虑维度为 2 或者 3 的情况
    @staticmethod
    def cross_product(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        dim = len(vec_1)
        if dim == 2:
            # 对二维向量 a = <a_0, a_1> 和 b = <b_0, b_1> 而言，返回(可正可负可零的)数值
            # a x b = |a|·|b|·sin<a, b> 或者 a x b = det{{a_0, a_1}, {b_0, b_1}} 行列式值
            # 如果该数值为正，则表示两向量夹角(不考虑周期)属于开区间 (0, \pi)
            # 如果该数值为负，则表示两向量夹角(不考虑周期)属于开区间 (\pi, 2 \pi)
            # 如果该数值为零，则表示两向量夹角(不考虑周期)要么是 0 要么是 \pi，故两向量共线
            return vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]
        elif dim == 3:
            # 对三维向量 a = <a_0, a_1, a_2> 和 b = <b_0, b_1, b_2> 而言，返回三维向量
            # a x b = det{{i, j, k}, {a_0, a_1, a_2}, {b_0, b_1, b_2}} 行列式值
            # 上式中的 i, j, k 分别为 x, y, z 轴方向的单位向量
            return [vec_1[1] * vec_2[2] - vec_1[2] * vec_2[1],
                    vec_1[2] * vec_2[0] - vec_1[0] * vec_2[2],
                    vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]]
        else:
            print('cross_product: 维度不为 2 或者 3')
            return None

    # (二维欧氏空间中)给定线段 Segment 结构体 seg，以及 x 坐标，获得该点的 y 坐标
    # 如果 x 坐标越出 seg 范围，则返回 None
    @staticmethod
    def segment_x2y(seg, x):
        # 先根据 Segment 结构体获取其两个端点的 Point 结构体
        assert isinstance(seg, Segment)
        p_1, p_2 = seg.from_point, seg.to_point
        assert isinstance(p_1, Point) and isinstance(p_2, Point)
        # 确定 x 坐标是否越界
        if min(p_1.vec[0], p_2.vec[0]) <= x <= max(p_1.vec[0], p_2.vec[0]):
            # 若线段垂直于 x 轴，则返回其低端点的 y 值
            if p_1.vec[0] == p_2.vec[0]:
                return min(p_1.vec[1], p_2.vec[1])
            # 否则根据平面几何公式计算 y 值
            else:
                slope = (p_2.vec[1] - p_1.vec[1]) / (p_2.vec[0] - p_1.vec[0])  # 斜率
                return slope * (x - p_1.vec[0]) + p_1.vec[1]
        else:
            return None

    # 给定两条线段，判断二者是否相交
    # 时间复杂度：O(1)
    def segments_intersect(self, seg_1, seg_2):
        if isinstance(seg_1, Segment) and isinstance(seg_2, Segment):
            # 获取两线段的四端点
            p_1, p_2, p_3, p_4 = seg_1.from_point, seg_1.to_point, seg_2.from_point, seg_2.to_point
            assert isinstance(p_1, Point) and isinstance(p_2, Point)
            assert isinstance(p_3, Point) and isinstance(p_4, Point)
            # 判断转向
            d_1 = self.direction(p_3, p_4, p_1)
            d_2 = self.direction(p_3, p_4, p_2)
            d_3 = self.direction(p_1, p_2, p_3)
            d_4 = self.direction(p_1, p_2, p_4)
            # 根据转向判断线段是否相交
            # 如果 d_1 与 d_2 异号，表示从向量 p3p4 出发去往 p1 和 p2 是不同的转向，说明 p1 与 p2 分居线段 p3p4 的两侧
            # 同理，如果 d_3 与 d_4 异号，说明 p3 与 p4 分居线段 p1p2 的两侧
            # 上述两点同时满足的话，两线段必相交
            if (d_1 < 0 < d_2 or d_1 > 0 > d_2) and (d_3 < 0 < d_4 or d_3 > 0 > d_4):
                return True
            # 如果 d_1 == 0，表示 p1 与线段 p3p4 共线
            # 此时判断 p1 是否落在线段 p3p4 内，若是，则两线段至少有交点 p1。下同
            elif d_1 == 0 and self.on_segment(p_3, p_4, p_1):
                return True
            elif d_2 == 0 and self.on_segment(p_3, p_4, p_2):
                return True
            elif d_3 == 0 and self.on_segment(p_1, p_2, p_3):
                return True
            elif d_4 == 0 and self.on_segment(p_1, p_2, p_4):
                return True
            # 其它情况下，两线段不相交
            else:
                return False
        else:
            print('输入的线段参数不合法')
            return False

    # 在二维空间中，对于首尾相接的两条有向线段 p0p1 和 p1p2
    # 以 p0p1 的方向看过去，判断 p1p2 是向左 还是向右 还是不转向
    # 只需计算 (p2 - p0) 和 (p1 - p0) 的叉积
    # 如果结果为正值，表示向量 p0p2 在 p0p1 的顺时针方法，故在 p1 处需右转
    # 如果结果为负值，表示向量 p0p2 在 p0p1 的逆时针方法，故在 p1 处需左转
    # 如果结果为零，表示向量 p0p2 与 p0p1 共线，故在 p1 处不变方向 (或者反转 180 度)
    # 时间复杂度：O(1)
    def direction(self, p_0, p_1, p_2):
        assert isinstance(p_0, Point) and isinstance(p_1, Point) and isinstance(p_2, Point)
        assert p_0.dim == p_1.dim == p_2.dim == 2  # 仅考虑二维欧氏空间
        vec_02 = self.vector_operation_by_ele(p_2.vec, p_0.vec, func=lambda x, y: x - y)
        vec_01 = self.vector_operation_by_ele(p_1.vec, p_0.vec, func=lambda x, y: x - y)
        return self.cross_product(vec_02, vec_01)

    # 假定点 p2 已经与线段 p0p1 共线
    # 判断点 p2 是否位于线段 p0p1 上 (包含线段的端点)
    # 时间复杂度：O(1)
    @staticmethod
    def on_segment(p_0, p_1, p_2):
        assert isinstance(p_0, Point) and isinstance(p_1, Point) and isinstance(p_2, Point)
        assert p_0.dim == p_1.dim == p_2.dim == 2  # 仅考虑二维欧氏空间
        # 仅需进行区间判断
        if min(p_0.vec[0], p_1.vec[0]) <= p_2.vec[0] <= max(p_0.vec[0], p_1.vec[0]) and \
                min(p_0.vec[1], p_1.vec[1]) <= p_2.vec[1] <= max(p_0.vec[1], p_1.vec[1]):
            return True
        else:
            return False

    # 给定线段集合 seg_list，确定其中是否存在相交线段
    # 时间复杂度：O(n log n)
    def any_segments_intersect(self, seg_list):
        # 1. 初始化完全前序(扩展红黑树的动态集合) T 为空
        seg_rbt = SegmentRedBlackTree()

        # 2. 将 2n 个线段端点 由左到右排序，若多个点 x 坐标值相同，则优先取 y 值低的，从而确定事件点的调度次序
        # 	 排序方式：以 (x, e, y) 作为多级关键字 进行排序，其中 x 和 y 为通常对坐标，而 e = 0 表示左端点、e = 1 表示右端点
        #    如果某线段是竖直(垂直于时间轴)的，则将其底部端点当作左端点、顶部端点当作右端点即可
        endpoint_list = []  # 先封装这 2n 个端点为 Endpoint 结构体，再进行排序。关键字 key 为元组 (x, e, y)
        for seg in seg_list:
            # 先根据 Segment 结构体获取其两个端点的 Point 结构体
            assert isinstance(seg, Segment)
            # 根据 (x, e, y) 多级关键字 顺序，将左端点设置为 seg.from_point、右端点设置为 seg.to_point
            # 方便调用 self.direction、利用叉积来判断线段的次序
            if seg.from_point.vec[0] > seg.to_point.vec[0]:
                temp = seg.from_point
                seg.from_point = seg.to_point
                seg.to_point = temp
            # 若两端点的 x 坐标相同，表示此线段与 x (时间)轴垂直，则考虑 y 坐标
            # 若两端点的 x、y 坐标均相同，则表示此线段退化成了一个点，则任取其一作为左端点均可
            elif seg.from_point.vec[0] == seg.to_point.vec[0]:
                # 优先取 y 坐标较小的端点
                if seg.from_point.vec[1] > seg.to_point.vec[1]:
                    temp = seg.from_point
                    seg.from_point = seg.to_point
                    seg.to_point = temp
            # 封装端点结构体
            p_1, p_2 = seg.from_point, seg.to_point
            ep_1 = Endpoint(key=(p_1.vec[0], 0, p_1.vec[1]), point=p_1, seg=seg)
            ep_2 = Endpoint(key=(p_2.vec[0], 1, p_2.vec[1]), point=p_2, seg=seg)
            # 将当前线段的两端点封装好后，加入 endpoint_list 列表
            endpoint_list.append(ep_1)
            endpoint_list.append(ep_2)

        self.sort_endpoints(endpoint_list)

        # 3. 在 for 循环中，每一次迭代都处理一个(端点)事件点 ep
        for ep in endpoint_list:
            assert isinstance(ep, Endpoint)
            assert isinstance(ep.key, tuple) and len(ep.key) == 3
            # 如果事件点 p 是某线段 s 的左端点，那么第 5 行将 s 添加到完全前序 T 中
            #   如果 s 与(由经过 p 的扫除线所定义的)完全前序中的(与之连续的)两条连续线段 中的任一条相交，
            #   则返回 True，表示存在相交的线段。
            #   如果 p 位于另一条线段 s' 上，则出现边界情况。此时，仅需要将 s 和 s' 连续地放入 T 中
            if ep.key[1] == 0:
                # 将当前(线段)端点插入(红黑树)完全前序 T 中
                seg_rbt.rb_insert(insert_ep=ep)
                # 获取当前端点对应线段的 TreeNode 树结点
                assert ep.seg in seg_rbt.seg2node
                cur_node = seg_rbt.seg2node[ep.seg]
                assert isinstance(cur_node, TreeNode)
                # 如果前驱结点存在，判断两线段是否相交
                above_node = seg_rbt.above(cur_node)
                if isinstance(above_node, TreeNode) and isinstance(above_node.seg, Segment):
                    above_seg = above_node.seg
                    if self.segments_intersect(ep.seg, above_seg):
                        print('Type-1:')
                        print('插入端点', ep.point.key, '时，线段', ep.seg.key, '与其上方的线段', above_seg.key, '相交')
                        return True
                # 如果后继结点存在，判断两线段是否相交
                below_node = seg_rbt.below(cur_node)
                if isinstance(below_node, TreeNode) and isinstance(below_node.seg, Segment):
                    below_seg = below_node.seg
                    if self.segments_intersect(ep.seg, below_seg):
                        print('Type-2:')
                        print('插入端点', ep.point.key, '时，线段', ep.seg.key, '与其下方的线段', below_seg.key, '相交')
                        return True
            # 如果事件点 p 是某线段 s 的右端点，那么会将 s 从完全前序 T 中删除
            #   考虑经过 p 的扫除线所定义的完全前序，如果 s 旁边(ABOVE 或者 BELOW)的线段有相交，则返回 True
            #   如果这些线段不相交，则第 11 行就将 s 从完全前序 T 中删除
            #   当 s 被删除后，s 旁边的线段就会在完全前序中变为连续(即相邻)
            if ep.key[1] == 1:
                # 获取当前端点对应线段的 TreeNode 树结点
                assert ep.seg in seg_rbt.seg2node
                cur_node = seg_rbt.seg2node[ep.seg]
                assert isinstance(cur_node, TreeNode)
                # 如果前驱结点和后继结点均存在，且前驱和后继对应的线段相交，则返回 True
                above_node = seg_rbt.above(cur_node)
                below_node = seg_rbt.below(cur_node)
                if isinstance(above_node, TreeNode) and isinstance(above_node.seg, Segment) and \
                        isinstance(below_node, TreeNode) and isinstance(below_node.seg, Segment):
                    above_seg = above_node.seg
                    below_seg = below_node.seg
                    if self.segments_intersect(above_seg, below_seg):
                        print('Type-3:')
                        print('删除端点', ep.point.key, '时，线段', above_seg.key, '与其下方的线段', below_seg.key, '相交')
                        return True
                # 将当前(线段)端点从(红黑树)完全前序 T 中删除
                seg_rbt.rb_delete(seg_rbt.bst, delete_ep=ep)

        # 4. 最后，如果在处理完全部 2n 个事件点后没发现存在线段相交，则返回 False
        return False

    # 对端点集合进行二路归并排序
    def sort_endpoints(self, endpoint_list):
        self._merge_sort(endpoint_list, 0, len(endpoint_list) - 1)

    # 归并排序
    def _merge_sort(self, endpoint_list, l, r):
        # 当待排序数组的左下标等于右下标时为基本情况：
        # 该数组只有一个元素。这自然是已排好序的，无需处理
        if l < r:
            m = int((l + r) >> 1)  # 二路归并
            self._merge_sort(endpoint_list, l, m)
            self._merge_sort(endpoint_list, m + 1, r)
            self._merge(endpoint_list, l, m, r)

    # 合并
    # 该过程假设子数组 endpoint_list[l..m] 和 endpoint_list[m+1..r] 都已排好序
    # 合并上述两个子数组为一个排好序的较大数组 seg_list[l..r]
    # 参数范围 l <= m < r
    @staticmethod
    def _merge(endpoint_list, l, m, r):
        len_sub1 = m - l + 1  # 左子数组的长度
        len_sub2 = r - m      # 右子数组的长度

        # 设置左辅助数组的前 len_sub1 项值为左子数组的值
        aux_left = endpoint_list[l: l + len_sub1]

        # 设置右辅助数组的前 len_sub2 项值为右子数组的值
        aux_right = endpoint_list[m + 1: m + 1 + len_sub2]

        # 升序排序(默认)，辅助数组末尾放置哨兵 inf 正无穷
        inf = 0x3f3f3f3f  # 哨兵数字 inf，用于升序排序。需要比 seg_list 中的所有坐标值都大
        inf_endpoint = Endpoint(key=(inf, inf, inf), point=None, seg=None)
        aux_left.append(inf_endpoint)
        aux_right.append(inf_endpoint)

        # 两个有序数组的合并
        i = 0
        j = 0
        for k in range(l, r + 1):
            # 获取当前端点
            left_ep = aux_left[i]
            right_ep = aux_right[j]
            assert isinstance(left_ep, Endpoint) and isinstance(right_ep, Endpoint)
            assert isinstance(left_ep.key, tuple) and len(left_ep.key) == 3
            assert isinstance(right_ep.key, tuple) and len(right_ep.key) == 3
            # 先按 x 坐标升序排序
            if left_ep.key[0] < right_ep.key[0]:
                endpoint_list[k] = left_ep
                i += 1
            elif left_ep.key[0] > right_ep.key[0]:
                endpoint_list[k] = right_ep
                j += 1
            # 如果 x 坐标相等，则先考虑端点是左端点还是右端点 (让左端点在前面)
            else:
                if left_ep.key[1] < right_ep.key[1]:
                    endpoint_list[k] = left_ep
                    i += 1
                elif left_ep.key[1] > right_ep.key[1]:
                    endpoint_list[k] = right_ep
                    j += 1
                # 如果同是左端点、或同是右端点，那么再考虑 y 坐标，让 y 坐标小的在前面
                else:
                    if left_ep.key[2] <= right_ep.key[2]:
                        endpoint_list[k] = left_ep
                        i += 1
                    else:
                        endpoint_list[k] = right_ep
                        j += 1


# 红黑树的树结点
class TreeNode:
    def __init__(self, seg, color=True):
        self.seg = seg       # 线段 Segment 结构体，根据叉积判断次序
        self.color = color   # 结点的颜色，True 代表红色(默认)，False 代表黑色
        self.left = None     # 左孩子指针
        self.right = None    # 右孩子指针
        self.parent = None   # 父结点指针


# 用于扫除线过程中维护线段高低序的 红黑树 Red-Black Tree
# 将基于关键字 key 的比较替换为基于叉积的比较
class SegmentRedBlackTree:
    # 构造 红黑树 Red-Black Tree
    # 时间复杂度 O(n log n)
    def __init__(self):
        self.bst = TreeNode(seg=None, color=False)  # 二叉搜索树结构，树根。初始设置任意属性的 TreeNode
        self.is_bst_empty = True  # 标志着当前 BST 是否为空
        self.seg2node = dict({})  # Segment 对象到 TreeNode 的映射

        self.nil = TreeNode(seg=None, color=False)  # 黑色的哨兵结点
        self.nil.parent = self.nil   # 哨兵的父结点仍为自己
        self.nil.left = self.nil     # 哨兵的左孩子仍为自己
        self.nil.right = self.nil    # 哨兵的右孩子仍为自己

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

            # 返回替代了 node 的结点 node_y
            return node_y
        else:
            return None

    # 对于两个向量，逐元素地操作 (例如：加减乘除等)
    # func 须是 lambda 表达式。默认为加法
    @staticmethod
    def vector_operation_by_ele(vec_1, vec_2, func=lambda x, y: x + y):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        res_vec = []
        for i in range(len(vec_1)):
            res_vec.append(func(vec_1[i], vec_2[i]))
        return res_vec

    # 计算两向量(列表)的内积/点积
    @staticmethod
    def inner_product(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        dim = len(vec_1)
        # 对应位置相乘 再求和
        res = 0
        for i in range(dim):
            res += vec_1[i] * vec_2[i]
        return res

    # 计算两向量(列表)的叉积
    # 这里只考虑维度为 2 或者 3 的情况
    @staticmethod
    def cross_product(vec_1, vec_2):
        assert isinstance(vec_1, list) and isinstance(vec_2, list) and len(vec_1) == len(vec_2)
        dim = len(vec_1)
        if dim == 2:
            # 对二维向量 a = <a_0, a_1> 和 b = <b_0, b_1> 而言，返回(可正可负可零的)数值
            # a x b = |a|·|b|·sin<a, b> 或者 a x b = det{{a_0, a_1}, {b_0, b_1}} 行列式值
            # 如果该数值为正，则表示两向量夹角(不考虑周期)属于开区间 (0, \pi)
            # 如果该数值为负，则表示两向量夹角(不考虑周期)属于开区间 (\pi, 2 \pi)
            # 如果该数值为零，则表示两向量夹角(不考虑周期)要么是 0 要么是 \pi，故两向量共线
            return vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]
        elif dim == 3:
            # 对三维向量 a = <a_0, a_1, a_2> 和 b = <b_0, b_1, b_2> 而言，返回三维向量
            # a x b = det{{i, j, k}, {a_0, a_1, a_2}, {b_0, b_1, b_2}} 行列式值
            # 上式中的 i, j, k 分别为 x, y, z 轴方向的单位向量
            return [vec_1[1] * vec_2[2] - vec_1[2] * vec_2[1],
                    vec_1[2] * vec_2[0] - vec_1[0] * vec_2[2],
                    vec_1[0] * vec_2[1] - vec_1[1] * vec_2[0]]
        else:
            print('cross_product: 维度不为 2 或者 3')
            return None

    # 在二维空间中，对于首尾相接的两条有向线段 p0p1 和 p1p2
    # 以 p0p1 的方向看过去，判断 p1p2 是向左 还是向右 还是不转向
    # 只需计算 (p2 - p0) 和 (p1 - p0) 的叉积
    # 如果结果为正值，表示向量 p0p2 在 p0p1 的顺时针方法，故在 p1 处需右转
    # 如果结果为负值，表示向量 p0p2 在 p0p1 的逆时针方法，故在 p1 处需左转
    # 如果结果为零，表示向量 p0p2 与 p0p1 共线，故在 p1 处不变方向 (或者反转 180 度)
    # 时间复杂度：O(1)
    def direction(self, p_0, p_1, p_2):
        assert isinstance(p_0, Point) and isinstance(p_1, Point) and isinstance(p_2, Point)
        assert p_0.dim == p_1.dim == p_2.dim == 2  # 仅考虑二维欧氏空间
        vec_02 = self.vector_operation_by_ele(p_2.vec, p_0.vec, func=lambda x, y: x - y)
        vec_01 = self.vector_operation_by_ele(p_1.vec, p_0.vec, func=lambda x, y: x - y)
        return self.cross_product(vec_02, vec_01)

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
    def _create_new_node(self, new_seg, color=True):
        new_node = TreeNode(new_seg, color=color)
        new_node.left = self.nil
        new_node.right = self.nil
        self.seg2node[new_seg] = new_node  # 记录映射关系
        return new_node

    # 辅助函数：清除某个结点的所有指针域
    @staticmethod
    def _clear_node_link(node):
        if isinstance(node, TreeNode):
            node.parent = None
            node.left = None
            node.right = None

    # 根据 Endpoint 端点对象增加结点 (可以根据端点对象找出其所在的 Segment 线段对象)
    # 增加后（每次都增加叶结点），调用 rb_insert_fixup 维护红黑性质
    # 刚插入新结点时，仅可能违反第四条红黑性质：每个红色结点的子结点都只能是黑色的。
    # 而调整过程中，可能会违反其它性质，但都会一一修复
    # 时间复杂度 O(log n) 与树高有关
    def rb_insert(self, insert_ep):
        assert isinstance(insert_ep, Endpoint)
        insert_seg = insert_ep.seg
        assert isinstance(insert_seg, Segment)
        if self.is_bst_empty:
            # 如果当前 BST 为空，则直接设置 self.bst 结点，完成插入
            new_node = self._create_new_node(insert_seg)
            new_node.parent = self.nil
            self.bst = new_node
            self.is_bst_empty = False
        else:
            ptr = self.bst           # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索插入位置
            ptr_p = self.bst.parent  # ptr_p 记录 ptr 的父亲
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                ptr_p = ptr
                assert isinstance(ptr.seg, Segment)
                p_1, p_2 = ptr.seg.from_point, ptr.seg.to_point
                assert isinstance(p_1, Point) and isinstance(p_2, Point)
                # 根据顶点转向决定 往左还是往右
                d = self.direction(p_1, p_2, insert_ep.point)
                if d <= 0:
                    ptr = ptr.left
                else:
                    ptr = ptr.right

            # 找到了插入位置，设置新结点属性：红色、左孩子和右孩子均为哨兵 nil、父结点为 ptr_p
            new_node = self._create_new_node(insert_seg, True)

            # 根据顶点转向决定 该插入到左边还是右边
            assert isinstance(ptr_p.seg, Segment)
            p_1, p_2 = ptr_p.seg.from_point, ptr_p.seg.to_point
            assert isinstance(p_1, Point) and isinstance(p_2, Point)
            d = self.direction(p_1, p_2, insert_ep.point)
            if d <= 0:
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

    # 根据 Endpoint 端点对象删除结点 (可以根据端点对象找出其所在的 Segment 线段对象)
    # 删除黑色结点时，可能违反红黑性质，需要调用 rb_delete_fixup 维护红黑性质
    # 时间复杂度 O(log n) 与树高有关
    def rb_delete(self, root, delete_ep):
        assert isinstance(delete_ep, Endpoint)
        delete_seg = delete_ep.seg
        assert isinstance(delete_seg, Segment)
        if self.is_bst_empty:
            print('提示：红黑树为空，无法继续删除。')
        else:
            ptr = root               # 用 ptr 指针从 root 结点（一般设为 self.bst）开始向下搜索删除位置
            while isinstance(ptr, TreeNode) and ptr != self.nil:
                assert isinstance(ptr.seg, Segment)
                if delete_seg == ptr.seg:
                    break  # 定位到了目标删除结点
                p_1, p_2 = ptr.seg.from_point, ptr.seg.to_point
                assert isinstance(p_1, Point) and isinstance(p_2, Point)
                # 根据顶点转向决定 往左还是往右
                d = self.direction(p_1, p_2, delete_ep.point)
                if d <= 0:
                    ptr = ptr.left
                else:
                    ptr = ptr.right

            # 若没找到目标结点
            assert isinstance(ptr, TreeNode)
            if ptr == self.nil:
                print('提示：删除时，找不到目标元素')
            else:
                assert ptr.seg in self.seg2node
                self.seg2node.pop(ptr.seg)  # 删除映射关系
                # 调整树结构
                if ptr == self.bst and ptr.seg == delete_seg and \
                        (not isinstance(ptr.left, TreeNode) or ptr.left == self.nil) and \
                        (not isinstance(ptr.right, TreeNode) or ptr.right == self.nil):
                    # 当前 BST 仅有一个根结点 ptr，且欲删除根结点，会导致树空
                    self.bst = None
                    self.is_bst_empty = True
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
                        y = self.below(ptr)     # y 为 ptr 的后继，y 的左孩子为 nil
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
                    # 最后，如果"真正"删除的结点颜色为黑色，则破坏了红黑性质，需要进行维护
                    if not y_original_color:
                        self._rb_delete_fixup(x)  # 删除后维护红黑性质

    # 找到一棵以 root 为根的 BST/RBT 中的最上方结点（一路左转）
    # 时间复杂度 O(log n) 与树高有关
    def highest_bst(self, root):
        if isinstance(root, TreeNode) and root != self.nil:
            while isinstance(root.left, TreeNode) and root.left != self.nil:
                root = root.left
            return root
        else:
            return None

    # 找到一棵以 root 为根的 BST/RBT 中的最下方结点（一路右转）
    # 时间复杂度 O(log n) 与树高有关
    def lowest_bst(self, root):
        if isinstance(root, TreeNode) and root != self.nil:
            while isinstance(root.right, TreeNode) and root.right != self.nil:
                root = root.right
            return root
        else:
            return None

    # 找到在 BST 中 node 结点的前驱结点
    # 如果 node 的左孩子存在，则 node 的前驱就是其左子树中的最大值
    # 如果 node 的左孩子不存在，则 node 的前驱是其某个祖先结点 a，满足此时 a.right == node
    # 时间复杂度 O(log n) 与树高有关
    def above(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            if isinstance(node.left, TreeNode) and node.left != self.nil:
                return self.lowest_bst(node.left)
            else:
                while node.parent != self.nil:
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
    def below(self, node):
        if isinstance(node, TreeNode) and node != self.nil:
            if isinstance(node.right, TreeNode) and node.right != self.nil:
                return self.highest_bst(node.right)
            else:
                while node.parent != self.nil:
                    if node.parent.left == node:
                        return node.parent
                    else:
                        node = node.parent
                return None
        else:
            return None


def main():
    cg = ComputationalGeometry()

    # 给定两条线段，判断二者是否相交
    print('\n给定两条线段，判断二者是否相交:')
    p_1 = Point(vec=[1, 1], key='p_1', val=100)
    p_2 = Point(vec=[5, 5], key='p_2', val=200)
    p_3 = Point(vec=[2, 6], key='p_3', val=300)
    p_4 = Point(vec=[4, 2], key='p_4', val=400)
    seg_1 = Segment(from_point=p_1, to_point=p_2, key='seg_1', val=111)
    seg_2 = Segment(from_point=p_3, to_point=p_4, key='seg_2', val=222)

    start = time.process_time()
    res_1 = cg.segments_intersect(seg_1, seg_2)
    end = time.process_time()

    # 输出结果: True
    if isinstance(res_1, bool) and res_1:
        print('Yes! 两线段相交')
    else:
        print('No! 两线段不相交')
    print('Running Time: %.5f ms' % ((end - start) * 1000))

    # 给定线段集合，确定其中是否存在相交线段
    print('\n给定两条线段，判断二者是否相交:')
    # 仿照《CLRS》Chapter 33 的图 33-5
    p_a_1 = Point(vec=[0, 5], key='a_1', val=100)
    p_a_2 = Point(vec=[4, 4], key='a_2', val=101)
    p_b_1 = Point(vec=[1, 1], key='b_1', val=200)
    p_b_2 = Point(vec=[11, 5], key='b_2', val=201)
    p_c_1 = Point(vec=[2, 3], key='c_1', val=300)
    p_c_2 = Point(vec=[6, 4], key='c_2', val=301)
    p_d_1 = Point(vec=[3, 5], key='d_1', val=400)
    p_d_2 = Point(vec=[11, 3], key='d_2', val=401)
    p_e_1 = Point(vec=[5, 6], key='e_1', val=500)
    p_e_2 = Point(vec=[11, 4], key='e_2', val=501)
    p_f_1 = Point(vec=[7, 3], key='f_1', val=600)
    p_f_2 = Point(vec=[10, 2], key='f_2', val=601)
    seg_a = Segment(from_point=p_a_1, to_point=p_a_2, key='seg_a', val=111)
    seg_b = Segment(from_point=p_b_1, to_point=p_b_2, key='seg_b', val=222)
    seg_c = Segment(from_point=p_c_1, to_point=p_c_2, key='seg_c', val=333)
    seg_d = Segment(from_point=p_d_1, to_point=p_d_2, key='seg_d', val=444)
    seg_e = Segment(from_point=p_e_1, to_point=p_e_2, key='seg_e', val=555)
    seg_f = Segment(from_point=p_f_1, to_point=p_f_2, key='seg_f', val=666)
    seg_list = [seg_a, seg_b, seg_c, seg_d, seg_e, seg_f]

    start = time.process_time()
    res_2 = cg.any_segments_intersect(seg_list)
    end = time.process_time()

    # 输出结果: True
    if isinstance(res_2, bool) and res_2:
        print('Yes! 线段集合中存在两线段相交')
    else:
        print('No! 线段集合中不存在两线段相交')
    print('Running Time: %.5f ms' % ((end - start) * 1000))


if __name__ == "__main__":
    sys.exit(main())
