//
//  main.cpp
//  Prob1077_Combinations
//
//  Created by 阴昱为 on 2019/8/3.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//77. Combinations
//
//Given two integers n and k, return all possible combinations of k numbers out of 1 ... n.
//
//给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。
//
//Example:
//    Input: n = 4, k = 2
//    Output:
//    [
//     [2,4],
//     [3,4],
//     [2,3],
//     [1,2],
//     [1,3],
//     [1,4],
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
    vector<vector<int>> combine(int n, int k) {
        return this->solution1(n, k);
    }
    
private:
    // 方法一。回溯法。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 128 ms , 在所有 C++ 提交中击败了 71.57% 的用户
    // 内存消耗 : 12.7 MB , 在所有 C++ 提交中击败了 49.82% 的用户
    // Runtime: 88 ms, faster than 49.28% of C++ online submissions for Combinations.
    // Memory Usage: 12.8 MB, less than 40.19% of C++ online submissions for Combinations.
    vector<vector<int>> solution1 (int n, int k) {
        // 边界情况
        if (n <= 0 || k <= 0 || n < k) {
            return {};
        }
        
        // 特殊情况
        if (n == k) {
            this->result.push_back({});
            for (int i = 1; i <= n; i++) {
                this->result[0].push_back(i);
            }
            return this->result;
        }
        
        if (k == 1) {
            for (int i = 1; i <= n; i++) {
                this->result.push_back({i});
            }
            return this->result;
        }
        
        vector<int> cur_vec;
        
        backtrack(n, k, cur_vec, 1);
        
        return this->result;
    }
    
    void backtrack (int n, int k, vector<int>& cur_vec, int start) {
        if (cur_vec.size() == k) {
            this->result.push_back(cur_vec);
            return;
        }
        
        for (int i = start; i < n + 1; i++) {
            cur_vec.push_back(i);
            
            backtrack(n, k, cur_vec, i + 1);
            
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
//    int n = 4, k = 2; // 预期结果 [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
//    int n = 3, k = 3; // 预期结果 [[1,2,3]]
    int n = 4, k = 3; // 预期结果 [[1,2,3], [1,2,4], [1,3,4], [2,3,4]]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->combine(n, k);
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
