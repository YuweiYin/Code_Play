//
//  main.cpp
//  Prob1042_Trapping_Rain_Water
//
//  Created by 阴昱为 on 2019/7/7.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//42. Trapping Rain Water
//
//Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.
//
//给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
//y ^
//3 |              H
//2 |      H w w w H H w H
//1 |  H w H H w H H H H H H
//0 -0-1-0-2-1-0-1-3-2-1-2-1->x
//
// 图中 H 表示每单位柱子，w 表示能放在柱子中的每单位雨水
//
//Example:
//    Input: [0,1,0,2,1,0,1,3,2,1,2,1]
//    Output: 6


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
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    int trap(vector<int>& height) {
        // 边界情况
        if (height.empty() || height.size() <= 1) {
            return 0;
        }
        
        return this->solution4(height);
    }
    
private:
    // 方法一：暴力法。时间复杂度 O(N^2)，空间复杂度 O(1)
    // 执行用时 : 388 ms , 在所有 C++ 提交中击败了 5.13% 的用户
    // 内存消耗 : 9.1 MB , 在所有 C++ 提交中击败了 82.06% 的用户
    // Runtime: 212 ms, faster than 5.06% of C++ online submissions for Trapping Rain Water.
    // Memory Usage: 9.1 MB, less than 44.83% of C++ online submissions for Trapping Rain Water.
    int solution1 (vector<int>& height) {
        int res = 0;
        int len = (int)height.size();
        
        for (int i = 1; i < len - 1; i++) {
            int max_left = 0, max_right = 0;
            
            // 找左边部分最高的峰值
            for (int j = i; j >= 0; j--) {
                if (height[j] > max_left) {
                    max_left = height[j];
                }
            }
            
            // 找右边部分最高的峰值
            for (int j = i; j < len; j++) {
                if (height[j] > max_right) {
                    max_right = height[j];
                }
            }
            
            // 每次加上 x 方向长度为 1 的矩形面积，高度为左右最高高度的较小值 - 自己的高度
            res += min(max_left, max_right) - height[i];
        }
        
        return res;
    }
    
    // 方法二：动态规划。时间复杂度 O(N)，空间复杂度 O(N)
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 90.52% 的用户
    // 内存消耗 : 9.2 MB , 在所有 C++ 提交中击败了 77.81% 的用户
    // Runtime: 4 ms, faster than 97.81% of C++ online submissions for Trapping Rain Water.
    // Memory Usage: 9.2 MB, less than 24.71% of C++ online submissions for Trapping Rain Water.
    int solution2 (vector<int>& height) {
        // 用 DP 表保存暴力法中每次查找的左右最高高度
        int res = 0;
        int len = (int)height.size();
        
        vector<int> left_max(len);
        left_max[0] = height[0];
        // 从左到右 DP，记录每个点左侧的柱子最高高度
        for (int i = 1; i < len; i++) {
            left_max[i] = max(height[i], left_max[i - 1]);
        }
        
        vector<int> right_max(len);
        right_max[len - 1] = height[len - 1];
        // 从右到左 DP，记录每个点右侧的柱子最高高度
        for (int i = len - 2; i >= 0; i--) {
            right_max[i] = max(height[i], right_max[i + 1]);
        }
        
        // 与暴力法相同的方式，计算每个点能存储的雨水量
        for (int i = 1; i < len - 1; i++) {
            res += min(left_max[i], right_max[i]) - height[i];
        }
        
        return res;
    }
    
    // 方法三：栈。时间复杂度 O(N)，空间复杂度 O(N)
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 90.52% 的用户
    // 内存消耗 : 9.3 MB , 在所有 C++ 提交中击败了 73.35% 的用户
    // Runtime: 8 ms, faster than 74.61% of C++ online submissions for Trapping Rain Water.
    // Memory Usage: 9.4 MB, less than 9.33% of C++ online submissions for Trapping Rain Water.
    int solution3 (vector<int>& height) {
        // 可以不用像方法 2 那样存储最大高度，而是用栈来跟踪可能储水的最长的条形块。使用栈就可以在一次遍历内完成计算。
        // 在遍历数组时维护一个栈。如果当前的条形块小于或等于栈顶的条形块，将条形块的索引入栈，
        // 意思是当前的条形块被栈中的前一个条形块界定。如果发现一个条形块长于栈顶，
        // 可以确定栈顶的条形块被当前条形块和栈的前一个条形块界定，因此可以弹出栈顶元素并且累加答案到 res 。
        int res = 0;
        int len = (int)height.size();
        
        stack<int> sk; // 使用栈来存储条形块的索引下标
        
        int index = 0;
        while (index < len) {
            // 如果栈不空，且遇到了更高的柱子，执行内部 while 循环
            // 思路：越靠近的栈顶的元素都比越靠近栈底的前一个元素矮，所以如果后来出现比它高的元素
            // 那么它们仨就形成了一个凹槽，可以装水
            while (!sk.empty() && height[index] > height[sk.top()]) {
                // 先把之前的栈顶元素取出来
                int top = sk.top();
                sk.pop();
                
                if (sk.empty()) {
                    break;
                }
                
                // 计算这个区间的矩形面积
                int distance = index - sk.top() - 1; // 底边长度
                int bounded_height = min(height[index], height[sk.top()]) - height[top]; // 高度
                res += distance * bounded_height;
            }
            
            // 栈为空，或者当前是较矮的柱子，则继续压栈
            sk.push(index++);
        }
        
        return res;
    }
    
    // 方法四：对撞指针。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 98.96% 的用户
    // 内存消耗 : 8.9 MB , 在所有 C++ 提交中击败了 98.09% 的用户
    // Runtime: 4 ms, faster than 97.81% of C++ online submissions for Trapping Rain Water.
    // Memory Usage: 8.9 MB, less than 88.41% of C++ online submissions for Trapping Rain Water.
    int solution4 (vector<int>& height) {
        // 和方法 2 相比，不从左和从右分开计算，想办法一次完成遍历。
        // 从动态编程方法的示意图中注意到，只要 right_max[i]>left_max[i] （元素 0 到元素 6），
        // 积水高度将由 left_max 决定，类似地 left_max[i]>right_max[i]（元素 8 到元素 11）。
        // 所以可以认为如果一端有更高的条形块（例如右端），积水的高度依赖于当前方向的高度（从左到右）。
        // 当发现另一侧（右侧）的条形块高度不是最高的，则开始从相反的方向遍历（从右到左）。
        // 必须在遍历时维护 left_max 和 right_max ，但是现在可以使用两个指针交替进行，实现 1 次遍历即可完成。
        int res = 0;
        
        int left = 0, right = (int)height.size() - 1;
        int left_max = 0, right_max = 0;
        
        while (left < right) {
            if (height[left] < height[right]) {
                // 左柱高度小于右柱高度
                if (height[left] >= left_max) {
                    // 更新左侧最高柱值 left_max
                    left_max = height[left];
                } else {
                    // 左柱高度小于 left_max，同时又已知左柱高度小于右柱高度
                    // 所以该点是在凹槽之中，于是加上该点的矩形面积
                    res += left_max - height[left];
                }
                left ++;
            } else {
                // 同理，对称处理。
                if (height[right] >= right_max) {
                    right_max = height[right];
                } else {
                    res += right_max - height[right];
                }
                right --;
            }
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
    vector<int> height = {0,1,0,2,1,0,1,3,2,1,2,1}; // 预期结果 6
//    vector<int> height = {3,1,2,1,3,2,0,1}; // 预期结果 6
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->trap(height);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
