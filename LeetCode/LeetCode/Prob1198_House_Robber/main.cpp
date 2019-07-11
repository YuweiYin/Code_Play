//
//  main.cpp
//  Prob1198_House_Robber
//
//  Created by 阴昱为 on 2019/7/11.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//198. House Robber
//
//You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security system connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
//Given a list of non-negative integers representing the amount of money of each house, determine the maximum amount of money you can rob tonight without alerting the police.
//
//你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
//给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，能够偷窃到的最高金额。
//
//Example 1:
//    Input: [1,2,3,1]
//    Output: 4
//    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
//    Total amount you can rob = 1 + 3 = 4.
//
//Example 2:
//    Input: [2,7,9,3,1]
//    Output: 12
//    Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
//    Total amount you can rob = 2 + 9 + 1 = 12.


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
private:
    vector<int> dp = {};
    
public:
    int rob(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // 方法一：自顶向下，带备忘录的动态规划。时间复杂度 O(N)，空间复杂度 O(N)。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 85.68% 的用户
    // 内存消耗 : 8.5 MB , 在所有 C++ 提交中击败了 83.57% 的用户
    // Runtime: 4 ms, faster than 70.33% of C++ online submissions for House Robber.
    // Memory Usage: 8.6 MB, less than 21.91% of C++ online submissions for House Robber.
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
        vector<int> memo(len, -1);
        
        // len-1..len-1 只有一个结果为 nums[len-1]
        memo[len - 1] = nums[len - 1];
        
        this->dp = memo;
        
        return this->dpTree(nums, 0, len);
    }
    
    // 自顶向下，带备忘录的动态规划
    // dp[i] = max( nums[i] + dp[i+2], nums[i+1] + dp[i+3] )
    int dpTree (vector<int>& nums, int i, int len) {
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
            if (this->dp[i + 2] < 0) {
                // 若 dp 表当前没有值，先把运算结果给 dp 表
                this->dp[i + 2] = this->dpTree(nums, i + 2, len);
            }
            // 然后再累加结果
            choice_1 += this->dp[i + 2];
        }
        
        int choice_2 = 0;
        if (i + 1 <= len - 1) {
            // 先看 i + 1 是否越界，如果越界，则 choice_2 也不存在，置为 0
            choice_2 = nums[i + 1];
            
            if (i + 3 <= len - 1) {
                if (this->dp[i + 3] < 0) {
                    this->dp[i + 3] = this->dpTree(nums, i + 3, len);
                }
                choice_2 += this->dp[i + 3];
            }
        }
        
        // 返回两种选择中的较大值
        return max(choice_1, choice_2);
    }
    
    // 方法二：迭代、精简版动态规划。时间复杂度 O(N)，空间复杂度 O(1)。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 85.68% 的用户
    // 内存消耗 : 8.4 MB , 在所有 C++ 提交中击败了 92.57% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for House Robber.
    // Memory Usage: 8.6 MB, less than 28.11% of C++ online submissions for House Robber.
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
        int pre_max = 0; // 前一个最大值（存储它是因为不能选连续的房间）
        int cur_max = 0; // 当前最大值
        
        for (int i = 0; i < nums.size(); i++) {
            int temp = cur_max;
            
            // 在选择本房间 pre_max + nums[i] 或者不选本房间 cur_max 中挑较大值
            cur_max = max(pre_max + nums[i], cur_max);
            pre_max = temp;
        }
        
        return cur_max;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {1, 2, 3, 1}; // 预期结果 4
    vector<int> nums = {2, 7, 9, 3, 1}; // 预期结果 12
    
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
