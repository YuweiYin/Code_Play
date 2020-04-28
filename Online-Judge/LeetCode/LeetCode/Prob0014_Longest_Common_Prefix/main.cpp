//
//  main.cpp
//  Prob1014_Longest_Common_Prefix
//
//  Created by 阴昱为 on 2019/6/8.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//14. Longest Common Prefix
//
//Write a function to find the longest common prefix string amongst an array of strings.
//If there is no common prefix, return an empty string "".
//
//编写一个函数来查找字符串数组中的最长公共前缀。
//如果不存在公共前缀，返回空字符串 ""。
//
//Example 1:
//    Input: ["flower","flow","flight"]
//    Output: "fl"
//
//Example 2:
//    Input: ["dog","racecar","car"]
//    Output: ""
//    Explanation: There is no common prefix among the input strings.
//
//Note:
//    All given inputs are in lowercase letters a-z.


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
public:
    string longestCommonPrefix(vector<string>& strs) {
        return this->solution1(strs);
    }
    
private:
    // 方法一：简单直接
    string solution1 (vector<string>& strs) {
        // 字符串列表为空，则直接返回 ""
        if (strs.empty()) {
            return "";
        }
        
        string res = "";
        
        // 先对字符串列表的各个元素排序，保证短的字符串在前
        sort(strs.begin(), strs.end(), myVectorComp);
        // 获取最短串作为基准，因为最长前缀至多就是它
        string shortest_str = strs[0];
        
        // 最短字符串为空，则直接返回 ""
        if (shortest_str.empty()) {
            return "";
        }
        
        // 对于最短字符串的每一位字符
        for (int i = 0; i < (int)shortest_str.size(); i++) {
            char cur = shortest_str[i]; // 当前位的字符
            
            // 看是否与其它字符串的该位字符相匹配
            for (int j = 1; j < (int)strs.size(); j++) {
                // 若不匹配，则终止循环，返回结果
                if (strs[j][i] != cur) {
                    return res;
                }
            }
            
            res += cur;
        }
        
        return res;
    }
    
    // 自定义排序函数
    static bool myVectorComp (const string &a, const string &b) {
        if (a.size() == b.size()) {
            // 如果长度相等，则返回字符值小的字符串
            return a < b;
        } else {
            // 否则返回长度更短的字符串
            return a.size() < b.size();
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    vector<string> strs = {"flower","flow","flight"};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->longestCommonPrefix(strs) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
