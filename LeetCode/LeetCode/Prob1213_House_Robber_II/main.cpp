//
//  main.cpp
//  Prob1213_House_Robber_II
//
//  Created by 阴昱为 on 2019/7/11.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//213. House Robber II
//
//You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have security system connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
//Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.
//
//你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都围成一圈，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
//给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，能够偷窃到的最高金额。
//
//Example 1:
//    Input: [2,3,2]
//    Output: 3
//    Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2),
//    because they are adjacent houses.
//
//Example 2:
//    Input: [1,2,3,1]
//    Output: 4
//    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
//    Total amount you can rob = 1 + 3 = 4.


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
    int rob(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // 方法一：自顶向下，带备忘录的动态规划。时间复杂度 O(N)，空间复杂度 O(N)。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 87.25% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 73.26% 的用户
    // Runtime: 4 ms, faster than 72.78% of C++ online submissions for House Robber II.
    // Memory Usage: 8.6 MB, less than 53.75% of C++ online submissions for House Robber II.
    int solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            return nums[0];
        }
        
        // memo[i] 表示从 i..len-1 的最优值
        vector<int> dp(len - 1, -1);
        vector<int> dp2(len, -1);
        
        // len-1..len-1 只有一个结果为 nums[len-1]
        dp[len - 2] = nums[len - 2];
        dp2[len - 1] = nums[len - 1];
        
        // 区分选不选第一个元素，选了它就不能选第二个元素和最后一个元素
        int choose_first = nums[0] + this->dpTree(nums, 2, len - 1, dp);
        int not_choose_first = this->dpTree(nums, 1, len, dp2);
        
        return max(choose_first, not_choose_first);
    }
    
    // 自顶向下，带备忘录的动态规划
    // dp[i] = max( nums[i] + dp[i+2], nums[i+1] + dp[i+3] )
    int dpTree (vector<int>& nums, int i, int len, vector<int>& dp) {
        // 先看 i 是否越界
        if (i >= len) {
            return 0;
        }
        
        if (i == len - 1) {
            return nums[i]; // len-1..len-1 只有一个结果为 nums[len-1]
        }
        
        int choice_1 = nums[i];
        if (i + 2 <= len - 1) {
            // 若下标不越界，则需要查看 dp 表的值
            if (dp[i + 2] < 0) {
                // 若 dp 表当前没有值，先把运算结果给 dp 表
                dp[i + 2] = this->dpTree(nums, i + 2, len, dp);
            }
            // 然后再累加结果
            choice_1 += dp[i + 2];
        }
        
        int choice_2 = 0;
        if (i + 1 <= len - 1) {
            // 先看 i + 1 是否越界，如果越界，则 choice_2 也不存在，置为 0
            choice_2 = nums[i + 1];
            
            if (i + 3 <= len - 1) {
                if (dp[i + 3] < 0) {
                    dp[i + 3] = this->dpTree(nums, i + 3, len, dp);
                }
                choice_2 += dp[i + 3];
            }
        }
        
        // 返回两种选择中的较大值
        return max(choice_1, choice_2);
    }
    
    // 方法二：迭代、精简版动态规划。时间复杂度 O(N)，空间复杂度 O(1)。
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 73.26% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for House Robber II.
    // Memory Usage: 8.6 MB, less than 50.00% of C++ online submissions for House Robber II.
    int solution2 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            return nums[0];
        }
        
        // 不用 dp 表，直接用两个值来记录最大值的变化情况
        int pre_max_1 = 0; // 前一个最大值（存储它是因为不能选连续的房间）
        int cur_max_1 = 0; // 当前最大值
        
        for (int i = 0; i < len - 1; i++) { // 0..len-2
            int temp = cur_max_1;
            
            // 在选择本房间 pre_max + nums[i] 或者不选本房间 cur_max 中挑较大值
            cur_max_1 = max(pre_max_1 + nums[i], cur_max_1);
            pre_max_1 = temp;
        }
        
        int pre_max_2 = 0;
        int cur_max_2 = 0;
        
        for (int i = 1; i < len; i++) { // 1..len-1
            int temp = cur_max_2;
            cur_max_2 = max(pre_max_2 + nums[i], cur_max_2);
            pre_max_2 = temp;
        }
        
        // 返回两种选择的最大值
        return max(cur_max_1, cur_max_2);
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {2, 3, 2}; // 预期结果 3
//    vector<int> nums = {1, 2, 3, 1}; // 预期结果 4
    vector<int> nums = {6, 6, 4, 8, 4, 3, 3, 10}; // 预期结果 27
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->rob(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
