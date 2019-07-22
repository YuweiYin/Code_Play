//
//  main.cpp
//  Prob1049_Group_Anagrams
//
//  Created by 阴昱为 on 2019/7/22.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//49. Group Anagrams
//
//Given an array of strings, group anagrams together.
//
//给定一个字符串数组，将字母异位词组合在一起。字母异位词指字母相同，但排列不同的字符串。
//
//Example:
//    Input: ["eat", "tea", "tan", "ate", "nat", "bat"],
//    Output:
//    [
//     ["ate","eat","tea"],
//     ["nat","tan"],
//     ["bat"]
//    ]
//
//Note:
//    All inputs will be in lowercase.
//    The order of your output does not matter.
//
//说明：
//    所有输入均为小写字母。
//    不考虑答案输出的顺序。


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
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        return this->solution1(strs);
    }
    
private:
    // 方法一：。时间复杂度 O(N * M lg M)，空间复杂度 O(N * M)。
    // N = strs.size  M 是 strs 中最长字符的长度
    // 执行用时 : 124 ms , 在所有 C++ 提交中击败了 24.23% 的用户
    // 内存消耗 : 19.7 MB , 在所有 C++ 提交中击败了 48.56% 的用户
    // Runtime: 52 ms, faster than 39.89% of C++ online submissions for Group Anagrams.
    // Memory Usage: 19.8 MB, less than 49.64% of C++ online submissions for Group Anagrams.
    vector<vector<string>> solution1 (vector<string>& strs) {
        // 边界情况
        if (strs.empty()) {
            return {};
        }
        
        vector<vector<string>> res = {};
        map<string, vector<string>> strs_map = {};
        string str_sorted = "";
        
        int len = (int)strs.size();
        for (int i = 0; i < len; i++) {
            str_sorted = strs[i];
            sort(str_sorted.begin(), str_sorted.end());
            
            if (strs_map.find(str_sorted) == strs_map.end()) {
                strs_map.insert({str_sorted, {strs[i]}});
            } else {
                strs_map[str_sorted].push_back(strs[i]);
            }
        }
        
        for (auto ite = strs_map.begin(); ite != strs_map.end(); ite++) {
            res.push_back(ite->second);
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
    // 预期结果
    //[
    //  ["ate","eat","tea"],
    //  ["nat","tan"],
    //  ["bat"]
    //]
    vector<string> strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<string>> ans = solution->groupAnagrams(strs);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < ans.size(); i++) {
            for (int j = 0; j < ans[i].size(); j++) {
                cout << ans[i][j] << ", ";
            }
            cout << endl;
        }
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
