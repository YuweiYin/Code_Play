//
//  main.cpp
//  Prob1217_Contains_Duplicate
//
//  Created by 阴昱为 on 2019/9/4.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//217. Contains Duplicate
//
//Given an array of integers, find if the array contains any duplicates.
//Your function should return true if any value appears at least twice in the array, and it should return false if every element is distinct.
//
//给定一个整数数组，判断是否存在重复元素。
//如果任何值在数组中出现至少两次，函数返回 true。如果数组中每个元素都不相同，则返回 false。
//
//Example 1:
//    Input: [1,2,3,1]
//    Output: true
//
//Example 2:
//    Input: [1,2,3,4]
//    Output: false
//
//Example 3:
//    Input: [1,1,1,3,3,4,3,2,4,2]
//    Output: true


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
    bool containsDuplicate(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // 方法一：集合检重法。时间复杂度 O(N)，空间复杂度 O(N)。N = nums.size
    // 执行用时 : 108 ms , 在所有 C++ 提交中击败了 8.77% 的用户
    // 内存消耗 : 16.4 MB , 在所有 C++ 提交中击败了 37.93% 的用户
    // Runtime: 56 ms, faster than 18.39% of C++ online submissions for Contains Duplicate.
    // Memory Usage: 16.5 MB, less than 71.43% of C++ online submissions for Contains Duplicate.
    bool solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return false;
        }
        
        int len = (int)nums.size();
        
        if (len <= 1) {
            return false;
        }
        
        set<int> unique_set = {};
        
        for (int i = 0; i < len; i++) {
            if (unique_set.find(nums[i]) == unique_set.end()) {
                unique_set.insert(nums[i]);
            } else {
                return true;
            }
        }
        
        return false;
    }
    
    // 方法二：哈希检重法。时间复杂度 O(N)，空间复杂度 O(N)。N = nums.size
    // 执行用时 : 120 ms , 在所有 C++ 提交中击败了 6.06% 的用户
    // 内存消耗 : 16.4 MB , 在所有 C++ 提交中击败了 37.93% 的用户
    // Runtime: 52 ms, faster than 25.91% of C++ online submissions for Contains Duplicate.
    // Memory Usage: 16.6 MB, less than 62.64% of C++ online submissions for Contains Duplicate.
    bool solution2 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return false;
        }
        
        int len = (int)nums.size();
        
        if (len <= 1) {
            return false;
        }
        
        map<int, bool> unique_hash = {};
        
        for (int i = 0; i < len; i++) {
            if (unique_hash.find(nums[i]) == unique_hash.end()) {
                unique_hash.insert({nums[i], true});
            } else {
                return true;
            }
        }
        
        return false;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {1, 2, 3, 1}; // 预期结果 true
//    vector<int> nums = {1, 2, 3, 4}; // 预期结果 false
    vector<int> nums = {1, 1, 1, 3, 3, 4, 3, 2, 4, 2}; // 预期结果 true
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->containsDuplicate(nums);
    if (ans) {
        cout << "Contains duplicate number." << endl;
    } else {
        cout << "Do NOT contain duplicate number." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
