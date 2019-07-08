//
//  main.cpp
//  Prob1053_Maximum_Subarray
//
//  Created by 阴昱为 on 2019/7/8.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//53. Maximum Subarray
//
//Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.
//
//给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
//
//Example:
//    Input: [-2,1,-3,4,-1,2,1,-5,4],
//    Output: 6
//    Explanation: [4,-1,2,1] has the largest sum = 6.
//
//Follow up:
//    If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
//
//进阶:
//    如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的分治法求解。


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
    int maxSubArray(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(N)，空间复杂度 O(1), N = nums.size()
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 99.42% 的用户
    // 内存消耗 : 9.2 MB , 在所有 C++ 提交中击败了 83.15% 的用户
    // Runtime: 8 ms, faster than 82.00% of C++ online submissions for Maximum Subarray.
    // Memory Usage: 9.1 MB, less than 81.04% of C++ online submissions for Maximum Subarray.
    int solution1 (vector<int>& nums) {
        // 边界条件
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len <= 1) {
            return nums[0];
        }
        
        // 记录累加的增益
        // 可能出现 cur_sum 比较大，遇到了绝对值较小的负数 nums[i] 的情况
        // 此时导致于是 cur_sum 变小了，但不会影响全局最大值 res
        // 只要 cur_sum 还大于零，就表示前面累加的增益为正，可以继续加下去
        int res = nums[0], cur_sum = 0;
        
        for(int i = 0; i < len; i++) {
            // 如果 cur_sum + nums[i] 更大，表示前一步的 cur_sum 大于 0，那么要把前一步的增益累加到本步，继续累积 sum
            // 如果 nums[i] 更大，表示前一步的 cur_sum 小于 0，那么不能累加该减益效果。等于抛开前面的 sum，从当前重新开始计算
            cur_sum = max(cur_sum + nums[i], nums[i]);
            
            res = max(res, cur_sum);
        }
        
        return res;
    }
    
    // 至于分治法，可以分为三段考虑：最大子序和要么在左半边，要么在右半边，要么是穿过中间
    // 在 CLRS 3rd Edition 中也有用分治法解决此问题的案例
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果 6 解释：连续子数组 [4,-1,2,1] 的和最大，为 6
    vector<int> nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->maxSubArray(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
