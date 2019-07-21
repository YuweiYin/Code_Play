//
//  main.cpp
//  Prob1055_Jump_Game
//
//  Created by 阴昱为 on 2019/7/21.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//55. Jump Game
//
//Given an array of non-negative integers, you are initially positioned at the first index of the array.
//Each element in the array represents your maximum jump length at that position.
//Determine if you are able to reach the last index.
//
//给定一个非负整数数组，你最初位于数组的第一个位置。
//数组中的每个元素代表你在该位置可以跳跃的最大长度。
//判断你是否能够到达最后一个位置。
//
//Example 1:
//    Input: [2,3,1,1,4]
//    Output: true
//    Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
//
//Example 2:
//    Input: [3,2,1,0,4]
//    Output: false
//    Explanation: You will always arrive at index 3 no matter what. Its maximum
//    jump length is 0, which makes it impossible to reach the last index.


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    bool canJump(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // 方法一：贪心选择。时间复杂度 O(N^2)，空间复杂度 O(1)。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 90.01% 的用户
    // 内存消耗 : 9.9 MB , 在所有 C++ 提交中击败了 73.75% 的用户
    // Runtime: 12 ms, faster than 76.62% of C++ online submissions for Jump Game.
    // Memory Usage: 9.8 MB, less than 81.66% of C++ online submissions for Jump Game.
    bool solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return false;
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            return true;
        }
        
        bool res = true;
        
        int cur_index = 0, best_choice = 0;
        int farthest_index = nums[0];
        if (farthest_index >= len - 1) {
            return true;
        }
        
        while (farthest_index < len - 1) {
            best_choice = farthest_index;
            
            // 贪心选择综合效果最远的点
            for (int i = farthest_index; i >= cur_index; i--) {
                if (i + nums[i] >= len - 1) {
                    return true;
                }
                
                if (i + nums[i] > best_choice) {
                    best_choice = i + nums[i];
                }
            }
            
            // cout << "best_choice = " << best_choice << endl;
            
            if (best_choice <= farthest_index) {
                // 最佳跳跃都不能使得前进，则不可能达到目的地
                return false;
            } else {
                farthest_index = best_choice;
                cur_index ++; // 至少向前要跳一步
            }
        }
        
        return res;
    }
    
    // 方法二：动态规划。时间复杂度 O(N)，空间复杂度 O(1)。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 90.01% 的用户
    // 内存消耗 : 9.7 MB , 在所有 C++ 提交中击败了 94.39% 的用户
    // Runtime: 8 ms, faster than 97.42% of C++ online submissions for Jump Game.
    // Memory Usage: 10 MB, less than 33.31% of C++ online submissions for Jump Game.
    bool solution2 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return false;
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            return true;
        }
        
        // 从后向前看
        int aim_index = len - 1;
        for (int i = len - 1; i >= 0; i--) {
            if (i + nums[i] >= aim_index) {
                // 若从某点 i 能到达目标，则更改目标为：到达 i
                aim_index = i;
            }
        }
        
        return aim_index == 0;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {2, 3, 1, 1, 4}; // 预期结果 true
//    vector<int> nums = {3, 2, 1, 0, 4}; // 预期结果 false
    vector<int> nums = {2, 3, 1, 1, 4, 2, 3, 1, 1, 4, 2, 3, 1, 1, 4}; // 预期结果 true
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->canJump(nums);
    if (ans) {
        cout << "Can jump to end."<< endl;
    } else {
        cout << "Can NOT jump to end."<< endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
