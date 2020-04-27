//
//  main.cpp
//  Prob1046_Permutations
//
//  Created by 阴昱为 on 2019/6/26.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//46. Permutations
//
//Given a collection of distinct integers, return all possible permutations.
//
//给定一个没有重复数字的序列，返回其所有可能的全排列。
//
//Example:
//    Input: [1,2,3]
//    Output:
//    [
//      [1,2,3],
//      [1,3,2],
//      [2,1,3],
//      [2,3,1],
//      [3,1,2],
//      [3,2,1]
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
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
private:
    vector<vector<int>> res = {};
    
public:
    vector<vector<int>> permute(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：回溯法。时间复杂度 O(N!)，空间复杂度 O(N)
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 99.53% 的用户
    // 内存消耗 : 9.3 MB , 在所有 C++ 提交中击败了 72.76% 的用户
    // Runtime: 12 ms, faster than 84.41% of C++ online submissions for Permutations.
    // Memory Usage: 9.5 MB, less than 40.76% of C++ online submissions for Permutations.
    vector<vector<int>> solution1 (vector<int>& nums) {
        if (nums.empty() || nums.size() <= 1) {
            return {nums};
        }
        
        int n_len = (int)nums.size();
        
        this->backtrack(nums, n_len, 0);
        
        return this->res;
    }
    
    // 回溯法
    void backtrack (vector<int>& nums, int n_len, int cur_len) {
        if (cur_len >= n_len) {
            this->res.push_back(nums);
            return;
        }
        
        for (int i = cur_len; i < n_len; i++) {
            // 前进，把未当过(当前)开头的元素放到前面来
            this->mySwap(nums[i], nums[cur_len]);
            
            // 深度向下执行，长度加一
            this->backtrack(nums, n_len, cur_len + 1);
            
            // 回溯，把交换过的元素交换回来
            this->mySwap(nums[i], nums[cur_len]);
        }
    }
    
    // 交换元素值
    void mySwap (int& a, int& b) {
        if (a != b) {
            a = a ^ b;
            b = a ^ b;
            a = a ^ b;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]
    vector<int> nums = {1, 2, 3};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans =solution->permute(nums);
    if (!ans.empty()) {
        for (int i = 0; i < (int)ans.size(); i++) {
            if (!ans[i].empty()) {
                for (int j = 0; j < (int)ans[i].size(); j++) {
                    cout << ans[i][j] << ", ";
                }
                cout << "End." << endl;
            }
        }
    } else {
        cout << "Answer is empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
