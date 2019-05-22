# -*- coding:utf-8 -*-

'''
序号：23
题目：二叉搜索树的后序遍历序列

题目描述：
输入一个整数数组，判断该数组是不是某二叉搜索树的后序遍历的结果。
如果是则输出Yes,否则输出No。假设输入的数组的任意两个数字都互不相同。

时间限制：1秒 空间限制：32768K
本题知识点：树，举例让抽象具体化
'''
import sys
import getopt


class Solution:
    def VerifySquenceOfBST(self, sequence):
        # write code here
        # 思路：
        # 二叉搜索树的特点：根节点的左子树节点值都小于根，
        # 根节点的右子树节点值都大于根
        # 后序遍历序列特点：序列最后一个节点就是当前子树的根
        # 由上面两个规律可以还原构造出 BST
        # 如果成功构造则 True，否则 False

        if len(sequence) <= 0:
            return False

        left_seq = []
        right_seq = []

        left_answer = True
        right_answer = True

        # 找到根节点，分割左右子树序列
        root = sequence[len(sequence) - 1]
        flag = True
        for i in range(len(sequence) - 1):
            # flag 为真表示正在分割左子树序列
            if flag:
                # 把比根节点小的值存入 left_seq
                if sequence[i] < root:
                    left_seq.append(sequence[i])
                # 如果出现比根节点大的值，则开始分割右子树
                else:
                    right_seq.append(sequence[i])
                    flag = False
            # flag 为假表示正在分割右子树序列
            else:
                # 如果在右子树序列里面存在比根小的值，则序列不符合 BST
                if sequence[i] < root:
                    return False
                else:
                    right_seq.append(sequence[i])

        # print left_seq
        # print right_seq

        # 递归判断左右子树序列
        if len(left_seq) > 0:
            left_answer = self.VerifySquenceOfBST(left_seq)
        if len(right_seq) > 0:
            right_answer = self.VerifySquenceOfBST(right_seq)

        # 左右子树都判断为真，才能确认为真
        return left_answer and right_answer


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

    '''
    Tree1 
         4
       /   \
      2     7
       \   / \
        3 5   9
    '''

    sequence1 = [3, 2, 5, 9, 7, 4] # True
    sequence2 = [3, 2, 9, 5, 7, 4] # False

    print solution.VerifySquenceOfBST(sequence1)
    print solution.VerifySquenceOfBST(sequence2)


if __name__ == "__main__":
    sys.exit(main())

