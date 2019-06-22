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
        
        return calculateArea(heights, 0, (int)heights.size() - 1);
    }
    
    int calculateArea(vector<int> heights, int left, int right) {
        if (left > right) {
            return 0;
        }
        
        // 从 left 到 right，找到最矮柱对应的下标
        int min_index = left;
        for (int i = left; i <= right; i++) {
            if (heights[min_index] > heights[i]) {
                min_index = i;
            }
        }
        
        // 返回三种情况的最大值
        return max(heights[min_index] * (right - left + 1), // 情况一：以最矮柱的高度为矩形的高，以整个区间长为矩形的宽
                   max(calculateArea(heights, left, min_index - 1), // 情况二：左侧递归
                       calculateArea(heights, min_index + 1, right) // 情况三：右侧递归
                       )
                   );
    }
    
    
    // 方法二。栈模拟。
    // 时间复杂度 O(N)，空间复杂度 O(N)
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 91.23% 的用户
    // 内存消耗 : 10 MB , 在所有 C++ 提交中击败了 76.91% 的用户
    // Runtime: 16 ms, faster than 67.45% of C++ online submissions for Largest Rectangle in Histogram.
    // Memory Usage: 10.1 MB, less than 86.71% of C++ online submissions for Largest Rectangle in Histogram.
    int solution2 (vector<int>& heights) {
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
    vector<int> heights = {2, 1, 5, 6, 2, 3}; // 预期结果 10
    
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
