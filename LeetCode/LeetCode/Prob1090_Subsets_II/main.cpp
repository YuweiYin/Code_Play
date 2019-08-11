//
//  main.cpp
//  Prob1090_Subsets_II
//
//  Created by 阴昱为 on 2019/8/8.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//90. Subsets II
//
//Given a collection of integers that might contain duplicates, nums, return all possible subsets (the power set).
//Note: The solution set must not contain duplicate subsets.
//
//给定一个可能包含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。
//说明：解集不能包含重复的子集。
//
//Example:
//    Input: [1,2,2]
//    Output:
//    [
//      [2],
//      [1],
//      [1,2,2],
//      [2,2],
//      [1,2],
//      []
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
    map<vector<int>, bool> result = {};
    
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // TODO 方法一。回溯法。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 91.17% 的用户
    // 内存消耗 : 9.4 MB , 在所有 C++ 提交中击败了 55.34% 的用户
    // Runtime: 8 ms, faster than 84.60% of C++ online submissions for Subsets II.
    // Memory Usage: 9.5 MB, less than 50.00% of C++ online submissions for Subsets II.
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
        
        this->result.insert({{}, true});
        for (int i = 1; i < len; i++) {
            vector<int> cur_vec = {};
            backtrack(nums, i, cur_vec, 0);
        }
        this->result.insert({nums, true});
        
        vector<vector<int>> res = {};
        for (auto ite = this->result.begin(); ite != this->result.end(); ite++) {
            res.push_back(ite->first);
        }
        
        return res;
    }
    
    // 类似于 LeetCode 77 Combinations
    void backtrack (vector<int>& nums, int k, vector<int>& cur_vec, int start) {
        if (cur_vec.size() == k) {
            // 先排序，再加入 result
            sort(cur_vec.begin(), cur_vec.end());
            this->displayList(cur_vec);
            if (this->result.find(cur_vec) == this->result.end() ||
                !this->result[cur_vec]) {
                this->result.insert({cur_vec, true});
            }
            return;
        }
        
        for (int i = start; i < nums.size(); i++) {
            cur_vec.push_back(nums[i]);
            
            backtrack(nums, k, cur_vec, i + 1);
            
            cur_vec.pop_back();
        }
    }
    
    void displayList (vector<int>& vec) {
        if (vec.empty()) {
            cout << "Vector is empty." << endl;
        } else {
            for (int i = 0; i < vec.size(); i++) {
                cout << vec[i] << ", ";
            }
            cout << "End." << endl;
        }
    }
    
    // 方法二。位操作去重。时间复杂度 O()，空间复杂度 O(1)。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 91.17% 的用户
    // 内存消耗 : 9.4 MB , 在所有 C++ 提交中击败了 55.34% 的用户
    // Runtime: 8 ms, faster than 84.30% of C++ online submissions for Subsets II.
    // Memory Usage: 9.3 MB, less than 72.73% of C++ online submissions for Subsets II.
    vector<vector<int>> solution2 (vector<int>& nums) {
        sort(nums.begin(), nums.end());
        
        vector<vector<int>> res = {};
        int len = (int)nums.size();
        int subset_num = 1 << len;
        
        for(int i = 0; i < subset_num; i++) {
            vector<int> list = {};
            bool illegal = false;
            for (int j = 0; j < len; j++) {
                if ((i >> j & 1) == 1) {
                    // 若当前位是 1
                    if (j > 0 && nums[j] == nums[j - 1] && (i >> (j - 1) & 1) == 0) {
                        // 若当前是重复数字，并且前一位是 0，则跳过这种情况
                        illegal = true;
                        break;
                    } else {
                        list.push_back(nums[j]);
                    }
                }
            }
            
            if (!illegal) {
                res.push_back(list);
            }
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
    // 预期结果 [[], [1], [2], [1,2], [2,2], [1,2,2]]
//    vector<int> nums = {1, 2, 2};
    
    // 预期结果 [[],[1],[1,4],[1,4,4],[1,4,4,4],[1,4,4,4,4],[4],[4,4],[4,4,4],[4,4,4,4]]
//    vector<int> nums = {4, 4, 4, 1, 4};
    
    // 预期结果 [[],[0],[0,1],[0,1,4],[0,4],[1],[1,4],[4]]
    vector<int> nums = {4, 1, 0};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->subsetsWithDup(nums);
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
