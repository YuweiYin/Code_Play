# -*- coding:utf-8 -*-

'''
序号：24
题目：二叉树中和为某一值的路径

题目描述：
输入一颗二叉树的跟节点和一个整数，
打印出二叉树中结点值的和为输入整数的所有路径。
路径定义为从树的根结点开始往下一直到叶结点所经过的结点形成一条路径。
(注意: 在返回值的list中，数组长度大的数组靠前)

时间限制：1秒 空间限制：32768K
本题知识点：树，举例让抽象具体化
'''
import sys
import getopt


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.path_list_all = []
        self.path_list_current = []
        # self.path_len = 0

    # 返回二维列表，内部每个列表表示找到的路径
    def FindPath(self, root, expectNumber):
        # write code here
        # 思路：深度优先搜索
        # 剪枝条件：当前路径结点值总和超过了 expectNumber

        # 当为空时结束
        if not root:
            return self.path_list_all

        self.path_list_current.append(root.val)

        # 若是满足条件则符合
        if root.left is None and root.right is None and root.val == expectNumber:
            value_path = []
            for i in self.path_list_current:
                value_path.append(i)
            # 保证在返回值的 list 中，数组长度大的数组靠前
            # 如果原本 path_list_all 为空，则直接把 value_path 加进去
            if len(self.path_list_all) <= 0:
                self.path_list_all.append(value_path)
            else:
                # 遍历 path_list_all，如果 value_path 值比当前元素值大，那就插入到当前元素前
                flag = True
                for i in range(len(self.path_list_all)):
                    if len(value_path) > len(self.path_list_all[i]):
                        self.path_list_all.insert(i, value_path)
                        flag = False

                # 如果 value_path 比 path_list_all，里的所有元素都小，则插入到最后
                if flag:
                    self.path_list_all.append(value_path)

        # 若左子树不为空，且值小于目标值，则递归遍历下一层
        if root.val <= expectNumber and root.left is not None:
            self.FindPath(root.left, expectNumber - root.val)

        # 若右子树不为空，且值小于目标值，则递归遍历下一层
        if root.val <= expectNumber and root.right is not None:
            self.FindPath(root.right, expectNumber - root.val)

        # 若都不符合，则回溯退到父节点，弹出子节点（避免重复出现）
        self.path_list_current.pop()
        return self.path_list_all

        '''
        # 主根节点为空
        if root is None:
            return []

        # 把当前结点加入当前路径里
        self.path_list_current.append(root)
        self.path_len += root.val
        print 'self.path_len = ', self.path_len

        if self.path_len >= expectNumber:
            # 若当前路径累积值已达到预期值
            if self.path_len == expectNumber and root.left is None and root.right is None:
                # 若当前节点是叶节点，表示已经找到一条路径了
                for i in range(len(self.path_list_current)):
                    print self.path_list_current[i].val
                self.path_list_all.append(self.path_list_current)
            
            # 无论找没找到路径，都不用继续往下搜索了，所以回溯并删除节点
            self.path_list_current.pop()
            self.path_len -= root.val
            print 'self.path_len = ', self.path_len
            # 删除当前节点，回溯退到父节点，在父节点继续递归执行任务
            if len(self.path_list_current) >= 1:
                father = self.path_list_current[len(self.path_list_current) - 1]
                if father.left == root:
                    father.left = None
                elif father.right == root:
                    father.right = None
                else:
                    # 不应出现的情况
                    father.left = None
                    father.right = None

                print '往回走'
                print root.val, ' -> ', father.val
                print 'father.left: ', father.left
                print 'father.right: ', father.right
                # self.FindPath(father, expectNumber)
            else:
                # 不应出现的情况
                pass

        else:
            # 还没达到目标数值，继续往下搜索
            # print root.left
            # print root.right
            len_list = len(self.path_list_current)
            if root.left is not None:
                print '向左走', self.path_list_current[len_list - 1]
                self.FindPath(self.path_list_current[len_list - 1].left, expectNumber)
            if root.right is not None:
                print '向右走', self.path_list_current[len_list - 1]
                self.FindPath(self.path_list_current[len_list - 1].right, expectNumber)

        # return None
        '''


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    # Main Logic Part

    solution = Solution()

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(1)
    root.left.left = TreeNode(3)
    root.left.right = TreeNode(4)
    root.right.right = TreeNode(2)
    root.right.right.left = TreeNode(2)

    expectNumber = 6

    print solution.FindPath(root, expectNumber)


if __name__ == "__main__":
    sys.exit(main())

