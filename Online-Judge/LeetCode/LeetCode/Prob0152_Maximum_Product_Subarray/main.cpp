//
//  main.cpp
//  Prob1152_Maximum_Product_Subarray
//
//  Created by 阴昱为 on 2019/7/8.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//152. Maximum Product Subarray
//
//Given an integer array nums, find the contiguous subarray within an array (containing at least one number) which has the largest product.
//
//给定一个整数数组 nums ，找出一个序列中乘积最大的连续子序列（该序列至少包含一个数）。
//
//Example 1:
//    Input: [2,3,-2,4]
//    Output: 6
//    Explanation: [2,3] has the largest product 6.
//
//Example 2:
//    Input: [-2,0,-1]
//    Output: 0
//    Explanation: The result cannot be 2, because [-2,-1] is not a subarray.


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
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    int maxProduct(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(N)，空间复杂度 O(1), N = nums.size()
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 97.15% 的用户
    // 内存消耗 : 9.1 MB , 在所有 C++ 提交中击败了 47.92% 的用户
    // Runtime: 8 ms, faster than 46.62% of C++ online submissions for Maximum Product Subarray.
    // Memory Usage: 9 MB, less than 74.52% of C++ online submissions for Maximum Product Subarray.
    int solution1 (vector<int>& nums) {
        // 边界条件
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len <= 1) {
            return nums[0];
        }
        
        // 如果是连续正数，或者夹杂着偶数个负数，则乘得越多越好
        // 遇到 0 时，会使得 cur_max 和 cur_min 此时都变为 0，
        // 但如果之前 res 的值大于 0，就不会影响 res，等于实现了分段处理（按 0 断开数组）
        // 所以只需始终保持 cur_max 和 cur_min 分别为当前累积乘积的最大/小值即可
        int res = MIN_INT32, cur_max = 1, cur_min = 1;
        
        for(int i = 0; i < len; i++) {
            // 出现负值，乘 nums[i] 后会导致最大值和最小值异号
            // 于是交换 cur_max 和 cur_min，保持乘 nums[i] 后最大/小值还是最大/小值
            if(nums[i] < 0) {
                int temp = cur_max;
                cur_max = cur_min;
                cur_min = temp;
            }
            
            // 把当前值和累积乘积比较，取较大/小值
            cur_max = max(cur_max * nums[i], nums[i]);
            cur_min = min(cur_min * nums[i], nums[i]);
            
            res = max(res, cur_max);
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
    vector<int> nums = {2, -3, -2, -4, 0, 5, 8}; // 预期结果 40
//    vector<int> nums = {-2, 0, -1}; // 预期结果 0
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->maxProduct(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
