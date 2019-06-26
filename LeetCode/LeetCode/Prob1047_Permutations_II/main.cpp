//
//  main.cpp
//  Prob1047_Permutations_II
//
//  Created by 阴昱为 on 2019/6/26.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//47. Permutations II
//
//Given a collection of numbers that might contain duplicates, return all possible unique permutations.
//
//给定一个可包含重复数字的序列，返回所有不重复的全排列。
//
//Example:
//    Input: [1,1,2]
//    Output:
//    [
//      [1,1,2],
//      [1,2,1],
//      [2,1,1]
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
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：回溯法。时间复杂度 O(N!)，空间复杂度 O(N)
    // Runtime: 28 ms, faster than 46.55% of C++ online submissions for Permutations II.
    // Memory Usage: 10.4 MB, less than 50.79% of C++ online submissions for Permutations II.
    vector<vector<int>> solution1 (vector<int>& nums) {
        if (nums.empty() || nums.size() <= 1) {
            return {nums};
        }
        
        // 先排序，方便找到重复元素，剪枝
        sort(nums.begin(), nums.end());
        int n_len = (int)nums.size();
        
        // 记录某数字是否已经被选择过
        vector<bool> selected = vector<bool>(n_len, false);
        vector<int> cur_num = {};
        
        this->backtrack(nums, n_len, 0, cur_num, selected);
        
        return this->res;
    }
    
    // 回溯法
    void backtrack (vector<int>& nums, int n_len, int depth, vector<int>& cur_num, vector<bool>& selected) {
        if (depth >= n_len) {
            this->res.push_back(cur_num);
            return;
        }
        
        for (int i = 0; i < n_len; i++) {
            // 当前数字未使用过，则选择它
            if (!selected[i]) {
                // 如果当前数字和前一个数相等，并且前一个数已经使用过了，那么不选它(两个相同分支只进一个)
                if (i > 0 && nums[i] == nums[i - 1] && selected[i - 1]) {
                    continue;
                }
                
                // 前进，把 i 元素加进来
                // this->mySwap(nums[i], nums[cur_len]);
                cur_num.push_back(nums[i]);
                selected[i] = true;
                
                // 深度向下执行，长度加一
                this->backtrack(nums, n_len, depth + 1, cur_num, selected);
                
                // 回溯，弹出 i 元素
                // this->mySwap(nums[i], nums[cur_len]);
                cur_num.erase(cur_num.end() - 1);
                selected[i] = false;
            }
        }
    }
    
    // 交换元素值
//    void mySwap (int& a, int& b) {
//        if (a != b) {
//            a = a ^ b;
//            b = a ^ b;
//            a = a ^ b;
//        }
//    }
    
    // 方法二：库函数。
    // Runtime: 24 ms, faster than 82.07% of C++ online submissions for Permutations II.
    // Memory Usage: 10.1 MB, less than 65.42% of C++ online submissions for Permutations II.
    vector<vector<int>> solution2 (vector<int>& nums) {
        sort(nums.begin(), nums.end());
        
        this->res.push_back(nums);
        
        while (next_permutation(nums.begin(), nums.end())) {
            this->res.push_back(nums);
        }
        
        return this->res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 [1,1,2], [1,2,1], [2,1,1]
    vector<int> nums = {1, 1, 2};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans =solution->permuteUnique(nums);
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
