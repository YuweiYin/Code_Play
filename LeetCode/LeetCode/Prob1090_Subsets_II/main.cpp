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
//     [2],
//     [1],
//     [1,2,2],
//     [2,2],
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
    map<vector<int>, bool> result = {};
    
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // TODO 方法一。回溯法。时间复杂度 O()，空间复杂度 O()。
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
    
    /*
    // TODO 方法二。哈希、统计数字频次去重。时间复杂度 O()，空间复杂度 O()。
    vector<vector<int>> solution2 (vector<int>& nums) {
        // 不用去重也不用排序的思路：
        // 先统计每个数字的频次，
        // 之后再根据每个数字的频次来组合，如 [1，2，2，3，3，3]
        // 得到字典｛1:1,2:2,3:3｝之后，
        // 直接按个数组合就能得到结果也能避免重合。即 0 个数字的子集为 1 种，1 个数字的子集为 3 种，
        // 2 个数字的子集... 6 个数字的子集就能得到所有结果
        
        map<int, int> dict = {};
        int index = 0;
        for (; index < nums.size(); index++) {
            if (dict.find(index) == dict.end()) {
                dict.insert({index, 0});
            } else {
                dict[index] ++;
            }
        }
        
        vector<vector<int>> res = {{}};
        index = 0;
        for (auto ite = dict.begin(); ite != dict.end(); ite++, index++) {
            vector<vector<int>> temp = copy(dict.begin(), dict.end());
            for () {
                
            }
        }
        for i, v in dic.items():
            temp = res.copy()
            for j in res:
                temp.extend(j+[i]*(k+1) for k in range(v))
            res = temp
        return res;
    }
    */
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
