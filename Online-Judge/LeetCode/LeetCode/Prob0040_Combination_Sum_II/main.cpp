//
//  main.cpp
//  Prob1040_Combination_Sum_II
//
//  Created by 阴昱为 on 2019/7/6.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//40. Combination Sum II
//
//Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sums to target.
//Each number in candidates may only be used once in the combination.
//
//Note:
//    All numbers (including target) will be positive integers.
//    The solution set must not contain duplicate combinations.
//
//给定一个数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。
//candidates 中的每个数字在每个组合中只能使用一次。
//
//说明：
//    所有数字（包括目标数）都是正整数。
//    解集不能包含重复的组合。
//
//Example 1:
//    Input: candidates = [10,1,2,7,6,1,5], target = 8,
//    A solution set is:
//    [
//      [1, 7],
//      [1, 2, 5],
//      [2, 6],
//      [1, 1, 6]
//    ]
//
//Example 2:
//    Input: candidates = [2,5,2,1,2], target = 5,
//    A solution set is:
//    [
//      [1,2,2],
//      [5]
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
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        return this->solution1(candidates, target);
    }
    
private:
    // 方法一：回溯法。时间复杂度 O()，空间复杂度 O()
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 99.10% 的用户
    // 内存消耗 : 9 MB , 在所有 C++ 提交中击败了 92.11% 的用户
    // Runtime: 8 ms, faster than 90.72% of C++ online submissions for Combination Sum II.
    // Memory Usage: 9.1 MB, less than 63.38% of C++ online submissions for Combination Sum II.
    vector<vector<int>> solution1 (vector<int>& candidates, int target) {
        // 边界情况
        if (candidates.empty()) {
            return {};
        }
        
        // 从小到大排序
        sort(candidates.begin(), candidates.end());
        
        vector<vector<int>> res = {};
        vector<int> cur_res = {};
        
        this->backtrack(res, candidates, target, 0, 0, cur_res);
        
        return res;
    }
    
    void backtrack (vector<vector<int>>& res, vector<int>& candidates, int& target, int cur_cand_index,
                    int cur_sum, vector<int>& cur_res) {
        // Error
        if (cur_sum > target) {
            return;
        }
        
        // Hit
        if (cur_sum == target) {
            // 还是可能有重复值，此时需要检测重复
            if (find(res.begin(), res.end(), cur_res) == res.end()) {
                res.emplace_back(cur_res);
            }
            return;
        }
        
        // 从 cur_cand_index 开始，避免回头取数，造成重复可能
        for (int i = cur_cand_index; i < (int)candidates.size(); i++) {
            if (cur_sum + candidates[i] <= target) {
                cur_res.push_back(candidates[i]);
                // 注意此处让下一轮的 cur_cand_index 为 i+1 ，即不能重复取值
                this->backtrack(res, candidates, target, i + 1, cur_sum + candidates[i], cur_res);
                cur_res.pop_back();
            } else {
                // 因为 candidates 为升序，所以如果 cur_sum 加上当前元素都超过 target 了
                // 那么之后的元素更不可能使总和为 target
                break;
            }
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果 [1, 7], [1, 2, 5], [2, 6], [1, 1, 6]
//    vector<int> candidates = {10, 1, 2, 7, 6, 1, 5};
//    int target = 8;
    
    // 预期结果 [1,2,2], [5]
    vector<int> candidates = {2, 5, 2, 1, 2};
    int target = 5;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->combinationSum2(candidates, target);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            for (int j = 0; j < (int)ans[i].size(); j++) {
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
