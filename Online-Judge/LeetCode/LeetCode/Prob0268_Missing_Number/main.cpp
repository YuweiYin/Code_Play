//
//  main.cpp
//  Prob1268_Missing_Number
//
//  Created by 阴昱为 on 2019/7/6.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//268. Missing Number
//
//Given an array containing n distinct numbers taken from 0, 1, 2, ..., n, find the one that is missing from the array.
//
//给定一个包含 0, 1, 2, ..., n 中 n 个数的序列，找出 0 .. n 中没有出现在序列中的那个数。
//
//Example 1:
//    Input: [3,0,1]
//    Output: 2
//
//Example 2:
//    Input: [9,6,4,2,3,5,7,0,1]
//    Output: 8
//
//Note:
//    Your algorithm should run in linear runtime complexity.
//    Could you implement it using only constant extra space complexity?
//说明:
//    你的算法应具有线性时间复杂度。你能否仅使用额外常数空间来实现?


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
    // 其他方法：
    // 排序后顺序查找，Time O(N lgN), Space O(1)
    // 哈希表存储后顺序查找，Time O(N), Space O(N)
    int missingNumber(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // 方法一：异或XOR位运算。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 28 ms , 在所有 C++ 提交中击败了 82.35% 的用户
    // 内存消耗 : 9.8 MB , 在所有 C++ 提交中击败了 42.03% 的用户
    // Runtime: 24 ms, faster than 86.33% of C++ online submissions for Missing Number.
    // Memory Usage: 9.9 MB, less than 31.31% of C++ online submissions for Missing Number.
    int solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        int res = len;
        
        // 思路：假设 nums = {3,1,0} 不计顺序，缺失值为 2
        // 如果要检查是否 0~N 是否在 nums 中出现，那么就让 0~N 彼此异或、然后与 nums 中的各个元素异或
        // 二元运算异或运算在整数域满足交换律和结合律，相等的数异或结果为 0，而任何数与 0 按位异或都等于自身
        // 设 res 初值为 len = 3（即 0~N 中的 N），因为数组下标只有 0~N-1 ，所以弥补一个 N
        // 异或运算 3 ^ (0^3) ^ (1^1) ^ (2^0) = (0^0) ^ (1^1) ^ 2 ^ (3^3) = 0 ^ 0 ^ 2 ^ 0 = 2
        for (int i = 0; i < len; i++) {
            res ^= i ^ nums[i];
        }
        
        return res;
    }
    
    // 方法二：等差数列公式。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 20 ms , 在所有 C++ 提交中击败了 98.34% 的用户
    // 内存消耗 : 9.8 MB , 在所有 C++ 提交中击败了 50.13% 的用户
    // Runtime: 20 ms, faster than 97.49% of C++ online submissions for Missing Number.
    // Memory Usage: 9.7 MB, less than 81.19% of C++ online submissions for Missing Number.
    int solution2 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        // 0 + 1 + 2 + .. + len
        int expected_sum = (len * (len + 1)) >> 1;
        int actually_sum = 0;
        
        for (int i = 0; i < len; i++) {
            actually_sum += nums[i];
        }
        
        return expected_sum - actually_sum;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {3, 0, 1}; // 预期结果 2
    vector<int> nums = {9, 6, 4, 2, 3, 5, 7, 0, 1}; // 预期结果 8
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->missingNumber(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
