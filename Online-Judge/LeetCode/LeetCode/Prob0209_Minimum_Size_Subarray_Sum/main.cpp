//
//  main.cpp
//  Prob1209_Minimum_Size_Subarray_Sum
//
//  Created by 阴昱为 on 2019/8/4.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//209. Minimum Size Subarray Sum
//
//Given an array of n positive integers and a positive integer s, find the minimal length of a contiguous subarray of which the sum ≥ s. If there isn't one, return 0 instead.
//
//给定一个含有 n 个正整数的数组和一个正整数 s ，找出该数组中满足其和 ≥ s 的长度最小的连续子数组。如果不存在符合条件的连续子数组，返回 0。
//
//Example:
//    Input: s = 7, nums = [2,3,1,2,4,3]
//    Output: 2
//    Explanation: the subarray [4,3] has the minimal length under the problem constraint.
//
//Follow up:
//    If you have figured out the O(n) solution, try coding another solution of which the time complexity is O(n log n).
//
//进阶:
//    如果你已经完成了O(n) 时间复杂度的解法, 请尝试 O(n log n) 时间复杂度的解法。


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
    int minSubArrayLen(int s, vector<int>& nums) {
        return this->solution1(s, nums);
    }
    
private:
    // 方法一。滑动窗口。时间复杂度 O(N lg N)，空间复杂度 O(1)。
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 98.95% 的用户
    // 内存消耗 : 9.7 MB , 在所有 C++ 提交中击败了 99.40% 的用户
    // Runtime: 12 ms, faster than 69.87% of C++ online submissions for Minimum Size Subarray Sum.
    // Memory Usage: 9.8 MB, less than 100.00% of C++ online submissions for Minimum Size Subarray Sum.
    int solution1 (int s, vector<int>& nums) {
        // 边界情况，矩阵为空
        if (s < 0 || nums.empty()) {
            return 0;
        }
        
        int ans = INT_MAX;
        int i = 0; // 滑窗的右边框
        int sum = 0; // 窗口间的和
        int begin = 0; // 滑窗的左边框
        
        while (i < nums.size()) {
            // 滑窗的右边框不能超出界限
            if (sum + nums[i] < s) {
                // 若滑窗之间的和小于s，右边框右移，sum增大
                sum += nums[i];
                i ++;
            } else {
                // 若滑窗之间的和大于等于s，左边框右移，sum减小
                if (i - begin < ans) {
                    // 若当前符合条件的连续子数组比ans内记录的长度更小，则更新ans值
                    ans = i - begin + 1;
                }
                
                sum = sum - nums[begin];
                begin ++;
            }
        }
        
        return ans == INT_MAX ? 0 : ans;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int s = 7;
    vector<int> nums = {2,3,1,2,4,3}; // 预期结果 2
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->minSubArrayLen(s, nums);
    if (ans <= 0) {
        cout << "Answer is empty." << endl;
    } else {
        cout << "Answer is " << ans << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
