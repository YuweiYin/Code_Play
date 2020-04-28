//
//  main.cpp
//  Prob1078_Subsets
//
//  Created by 阴昱为 on 2019/8/3.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//78. Subsets
//
//Given a set of distinct integers, nums, return all possible subsets (the power set).
//Note: The solution set must not contain duplicate subsets.
//
//给定一组不含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。
//说明：解集不能包含重复的子集。
//
//Example:
//    Input: nums = [1,2,3]
//    Output:
//    [
//     [3],
//     [1],
//     [2],
//     [1,2,3],
//     [1,3],
//     [2,3],
//     [1,2],
//     []
//    ]


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
private:
    vector<vector<int>> result = {};
    
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一。回溯法。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 99.81% 的用户
    // 内存消耗 : 9.1 MB , 在所有 C++ 提交中击败了 63.29% 的用户
    // Runtime: 4 ms, faster than 97.90% of C++ online submissions for Subsets.
    // Memory Usage: 9.2 MB, less than 74.47% of C++ online submissions for Subsets.
    vector<vector<int>> solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return {{}};
        }
        
        int len = (int)nums.size();
        
        // 特殊情况
        if (len == 1) {
            return {{}, nums};
        }
        
        this->result.push_back({});
        for (int i = 1; i < len; i++) {
            vector<int> cur_vec = {};
            backtrack(nums, i, cur_vec, 0);
        }
        this->result.push_back(nums);
        
        return this->result;
    }
    
    // 类似于 LeetCode 77 Combinations
    void backtrack (vector<int>& nums, int k, vector<int>& cur_vec, int start) {
        if (cur_vec.size() == k) {
            this->result.push_back(cur_vec);
            return;
        }
        
        for (int i = start; i < nums.size(); i++) {
            cur_vec.push_back(nums[i]);
            
            backtrack(nums, k, cur_vec, i + 1);
            
            cur_vec.pop_back();
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {1, 2, 3}; // 预期结果 [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->subsets(nums);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < ans.size(); i++) {
            for (int j = 0; j < ans[i].size(); j++) {
                cout << ans[i][j] << ", ";
            }
            cout << "End." << endl;
        }
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
