//
//  main.cpp
//  Prob1084_Largest_Rectangle_in_Histogram
//
//  Created by 阴昱为 on 2019/6/22.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1084. Largest Rectangle in Histogram
//
//Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.
//
//给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。
//求在该柱状图中，能够勾勒出来的矩形的最大面积。
//
//     H
//    HH
//    HH
//    HH H
//  H HHHH
//  HHHHHH
//
//Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].
//The largest rectangle is shown in the shaded area, which has area = 10 unit.
//
//Example:
//    Input: [2,1,5,6,2,3]
//    Output: 10


// 设置系统栈深度
#pragma comment(linker, "/STACK:1024000000,1024000000")

// 引入头文件
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>

#include <math.h>
#include <time.h>

#include <algorithm>
#include <string>
#include <vector>
#include <list>
#include <stack>
#include <queue>
#include <map>
#include <set>
#include <bitset>

#include <unordered_set>
#include <unordered_map>

// 使用 std 标准命名空间
using namespace std;

// 类型命名
//typedef __int64_t ll;
//#define ll __int64_t
//#define ll long long

// 全局常量
//#define PI acos(-1.0)
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


// 线段树。如：
//          1~10
//         /    \
//      1~5      6~10
//     /   \     /   \
//   1~3   4~5  6~8   9~10
//   / \   / \  / \   /  \
//  1~2 3  4 5 6~7 8  9  10
//  / \        / \
// 1   2      6   7
// 如果每个结点存储最小值。那么每个叶节点有各自独有的最小值，
// 而中间结点的最小值是左右孩子的最小值中的较小值
class SegTreeNode {
public:
    int start;
    int end;
    int min; // 区间内 heights 最小值的坐标
    SegTreeNode *left;
    SegTreeNode *right;
    
public:
    SegTreeNode(int start, int end) {
        this->start = start;
        this->end = end;
        left = right = NULL;
    }
};


class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        return this->solution2(heights);
    }
    
private:
    // 方法一，分治法。
    // 时间复杂度 O(N^2)，平均 O(lg N)，空间复杂度 O(N)
    // 通过 94/96 个测试用例，在第 95 个测试用例处，MLE 超出内存限制
    // 分治法进一步优化：
    // 如果是最坏情况(数组本身是升序或者降序的)，分治法退化到 O(N^2)，
    // 原因是每次我们都需要在一个很大的 O(N) 级别的数组里顺序找最小值。
    // 可以用线段树代替遍历来找到区间最小值，查找复杂度就变成了O(lg N)。
    int solution1 (vector<int>& heights) {
        if (heights.empty()) {
            return 0;
        }
        
        return calculateMaxArea(heights, 0, (int)heights.size() - 1);
    }
    
    int calculateMaxArea(vector<int> heights, int start, int end) {
        if (start > end) {
            return 0;
        }
        
        if (start == end) {
            return heights[start];
        }
        
        // 从 start 到 end，找到最矮柱对应的下标
        int min_index = start;
        for (int i = start; i <= end; i++) {
            if (heights[min_index] > heights[i]) {
                min_index = i;
            }
        }
        
        // 返回三种情况的最大值
        return max(heights[min_index] * (end - start + 1), // 情况一：以最矮柱的高度为矩形的高，以整个区间长为矩形的宽
                   max(calculateMaxArea(heights, start, min_index - 1), // 情况二：左侧递归找最大值
                       calculateMaxArea(heights, min_index + 1, end))); // 情况三：右侧递归找最大值
    }
    
    // 方法二。优化的分治法，用线段树搜索区间最小值。
    // 时间复杂度 O(N lg N)，空间复杂度 O(N)
    int solution2 (vector<int>& heights) {
        if (heights.empty()) {
            return 0;
        }
        
        // 递归建立线段树
        SegTreeNode *root = buildSegmentTree(heights, 0, (int)heights.size() - 1);
        
        // 分治递归计算最大面积
        return calculateMax(heights, root, 0, (int)heights.size() - 1);
    }
    
    // 分治递归计算最大面积
    int calculateMax(vector<int>& heights, SegTreeNode* root, int start, int end) {
        if (start > end) {
            return 0;
        }
        
        if (start == end) {
            return heights[start];
        }
        
        // 利用线段树，以 O(lg N) 时间效率找到最矮柱对应的下标
        int min_index = query(root, heights, start, end);

        return max(heights[min_index] * (end - start + 1), // 情况一：以最矮柱的高度为矩形的高，以整个区间长为矩形的宽
                   max(calculateMax(heights, root, start, min_index - 1), // 情况二：左侧递归找最大值
                       calculateMax(heights, root, min_index + 1, end))); // 情况三：右侧递归找最大值
    }
    
    // 递归建立线段树
    SegTreeNode* buildSegmentTree(vector<int>& heights, int start, int end) {
        if (start > end) {
            return NULL;
        }
        
        SegTreeNode *root = new SegTreeNode(start, end);
        
        if (start == end) {
            // 区间起点等于终点，表示这个是叶子结点，可以直接赋最值
            root->min = start;
            
            return root;
        } else {
            int mid = (start + end) / 2; // 找到中点，二分区间
            root->left = buildSegmentTree(heights, start, mid); // 递归构建左子树
            root->right = buildSegmentTree(heights, mid + 1, end); // 递归构建右子树
            
            // 这个是中间结点，它的高度最小值等于左右子树的高度最小值中的较小值，所在的坐标
            root->min = heights[root->left->min] < heights[root->right->min] ? root->left->min : root->right->min;
            
            return root;
        }
    }
    
    // 线段树查询最小值。找区间 [start, end] 内 heights 元素的最小值坐标
    int query(SegTreeNode *root, vector<int>& heights, int start, int end) {
        // 到空结点，或者目标区间 [start, end] 和当前结点区间完全没有交集，则返回 -1
        if (root == NULL || end < root->start || start > root->end) {
            return -1; // -1 是约定值
        }
        
        // 如果目标区间 [start, end] 完全包含当前结点的区间，返回结点的最小值
        if (start <= root->start && end >= root->end) {
            return root->min;
        }
        
        // 否则表示目标区间 [start, end] 和当前结点的区间有交集，并且差集不为空
        // 还没定位准确。解释：参考定义 class SegTreeNode 时举的线段树例子，
        // 如果查找 heights 的 [2, 5] 中的最小高度值的坐标，那么从根结点 1~10 开始
        // [2, 5] 与 [1, 10] 有交集，但 [2, 5] 没有把 [1, 10] 完全包住，所以找左右子树
        // 在右子树 [6, 10] 里，[2, 5] 与它毫无交集，所以直接返回 -1，本结点返回其左子树最值
        // 在左子树 [1, 5] 里，[2, 5] 没有把 [1, 5] 完全包住，所以继续往下找左右子树
        // 在右子树 [4, 5] 里，[2, 5] 把 [4, 5] 完全包住了，所以返回其最小值 r1
        // 在左子树 [1, 3] 里，[2, 5] 没有把 [1, 5] 完全包住，所以继续往下找左右子树
        // 在右子树 [3, 3] 里，[2, 5] 把 [3, 3] 完全包住了，所以返回其最小值 r2
        // 在左子树 [1, 2] 里，[2, 5] 没有把 [1, 2] 完全包住，所以继续往下找左右子树
        // 在右子树 [2, 2] 里，[2, 5] 把 [2, 2] 完全包住了，所以返回其最小值 r3
        // 在左子树 [1, 1] 里，[2, 5] 与它毫无交集，所以直接返回 -1，本结点返回其右子树最值
        // 所以最终结果为 min(min(r3, r2), r1)
        
        // 分别以目标区间 [start, end] 去找左右子树的最小值坐标
        int left_min = query(root->left, heights, start, end);
        int right_min = query(root->right, heights, start, end);
        
        if (left_min == -1) {
            return right_min;
        }
        
        if (right_min == -1) {
            return left_min;
        }
        
        // 返回二者中的较小值的坐标
        return heights[left_min] < heights[right_min] ? left_min : right_min;
    }
    
    
    // 方法三。栈模拟。
    // 时间复杂度 O(N)，空间复杂度 O(N)
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 91.23% 的用户
    // 内存消耗 : 10 MB , 在所有 C++ 提交中击败了 76.91% 的用户
    // Runtime: 12 ms, faster than 94.36% of C++ online submissions for Largest Rectangle in Histogram.
    // Memory Usage: 10.2 MB, less than 79.24% of C++ online submissions for Largest Rectangle in Histogram.
    int solution3 (vector<int>& heights) {
        if(heights.empty()) {
            return 0;
        }
        
        int res = 0;
        
        stack<int> sk = {};
        sk.push(-1); // 规定的栈底元素
        int h_len = (int)heights.size();
        int cur_height = 0;
        
        // 不断压栈，保持升序，如果出现降序，则一个个处理、弹出比新元素大的栈顶元素
        for (int i = 0; i < h_len; i++) {
            // 如果未到栈底，并且新加入的元素相比栈顶是较小数
            while (sk.top() != -1 && heights[sk.top()] >= heights[i]) {
                // 此时让比 heights[i] 大的元素一个个出栈，并计算所能形成的矩形面积
                cur_height = heights[sk.top()]; // 以出栈元素的高作为形成矩形的高
                sk.pop();
                
                // 以 i 到出栈元素的距离作为形成矩形的宽
                res = max(res, cur_height * (i - sk.top() - 1));
            }
            
            // 压入新元素 heights[i]，此时从栈底到栈顶保持升序
            sk.push(i);
        }
        
        // 最后的情况，做相似处理
        while (sk.top() != -1) {
            cur_height = heights[sk.top()];
            sk.pop();
            res = max(res, cur_height * (h_len - sk.top() - 1));
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> heights = {2, 1, 5, 6, 2, 3}; // 预期结果 10
    vector<int> heights = {3, 6, 5, 7, 4, 8, 1, 0}; // 预期结果 20
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->largestRectangleArea(heights);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
