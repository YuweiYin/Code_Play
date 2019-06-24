//
//  main.cpp
//  Prob1028_Implement_strStr_function
//
//  Created by 阴昱为 on 2019/6/24.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//28. Implement strStr()
//
//Implement strStr().
//Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.
//
//实现 strStr() 函数。
//给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。
//
//Example 1:
//    Input: haystack = "hello", needle = "ll"
//    Output: 2
//
//Example 2:
//    Input: haystack = "aaaaa", needle = "bba"
//    Output: -1
//
//Clarification:
//    What should we return when needle is an empty string? This is a great question to ask during an interview.
//    For the purpose of this problem, we will return 0 when needle is an empty string. This is consistent to C's strstr() and Java's indexOf().
//
//说明:
//    当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。
//    对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。


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
    int strStr(string haystack, string needle) {
        return this->solution2(haystack, needle);
    }
private:
    // 方法一：从左到右暴力匹配。时间复杂度 O(NM)，空间复杂度 O(1)
    // N 是匹配串 haystack 的长度，M 是模式串 needle 的长度
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 9.1 MB , 在所有 C++ 提交中击败了 82.45% 的用户
    // Runtime: 4 ms, faster than 95.80% of C++ online submissions for Implement strStr().
    // Memory Usage: 9.1 MB, less than 62.80% of C++ online submissions for Implement strStr().
    int solution1 (string haystack, string needle) {
        // 边界情况
        if (needle.empty()) {
            return 0;
        }
        
        if (haystack.empty()) {
            return -1;
        }
        
        int h_len = (int)haystack.size();
        int n_len = (int)needle.size();
        
        if (h_len < n_len) {
            return -1;
        }
        
        for (int i = 0; i < h_len; i++) {
            // 如果剩余的字符串长度不足以匹配模式串，直接返回 -1 不匹配
            if (h_len - i < n_len) {
                return -1;
            }
            
            bool match_flag = true; // 匹配成功标志
            
            if (haystack[i] == needle[0]) {
                // 往后逐个对比匹配
                for (int j = 1; j < n_len; j++) {
                    if (haystack[i + j] != needle[j]) {
                        match_flag = false;
                        break;
                    }
                }
                
                if (match_flag) {
                    return i; // 如果匹配成功，返回结果
                }
            }
        }
        
        // 之前没有返回，表示前面都匹配失败了
        return -1;
    }
    
    // 方法二：KMP 算法。时间复杂度 O(N+M)，空间复杂度 O(1)
    // N 是匹配串 haystack 的长度，M 是模式串 needle 的长度
    // KMP 核心思想：如果模式串有"重复结构"，当出现不匹配时，
    // 不必直接让匹配串从下一个开始、模式串从头开始。而是找到一个恰当的重新开始匹配的位置。
    int solution2 (string haystack, string needle) {
        // 边界情况
        if (needle.empty()) {
            return 0;
        }
        
        if (haystack.empty()) {
            return -1;
        }
        
        int h_len = (int)haystack.size();
        int n_len = (int)needle.size();
        
        if (h_len < n_len) {
            return -1;
        }
        
        // 建表。时间复杂度 O(M)，空间复杂度 O(M)
        // 如果模式串的 k 位置不匹配了，那么下一次匹配时应当从 kmp_table[k-1] 下标匹配
        // 并且下一次开始匹配前，匹配串应向右移动 k 步
        vector<int> kmp_table = vector<int>(n_len, 0);
        
        for (int i = 1; i < n_len; i++) {
            if (needle[i] == needle[kmp_table[i - 1]]) {
                kmp_table[i] = kmp_table[i - 1] + 1;
            }
        }
        
        // 匹配。时间复杂度 O(N)，空间复杂度 O(1)
        int match_start = 0; // 匹配串的初始匹配位置
        int pattern_start = 0; // 模式串的初始匹配位置
        while (match_start < h_len) {
            // 如果剩余的字符串长度不足以匹配模式串，直接返回 -1 不匹配
            if (h_len - match_start < n_len) {
                return -1;
            }
            
            bool match_flag = true; // 匹配成功标志
            
            // 往后逐个对比匹配
            for (int j = 0; j < n_len; j++) {
                if (haystack[match_start + j] != needle[pattern_start + j]) {
                    // 出现不匹配时，计算重新开始匹配的位置
                    if (pattern_start > 0) {
                        pattern_start = kmp_table[pattern_start + j - 1];
                        match_start += pattern_start;
                    } else {
                        // 如果模式串头都不能和当前的原串字符匹配，那么只需右移一次 match_start
                        match_start ++;
                    }
                    
                    match_flag = false;
                    break;
                }
            }
            
            if (match_flag) {
                return match_start; // 如果匹配成功，返回结果
            }
        }
        
        // 之前没有返回，表示前面都匹配失败了
        return -1;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    string haystack = "hello", needle = "ll"; // 预期结果 2
//    string haystack = "aaaaa", needle = "bba"; // 预期结果 -1
//    string haystack = "abcde", needle = ""; // 预期结果 0
//    string haystack = "aaabcdaabcaab", needle = "aabcaa"; // 预期结果 6
    string haystack = "dgmabdgmxdgmabdgmz", needle = "dgmabdgmz"; // 预期结果 9
//    string haystack = "aaaabacaaaaabaa", needle = "aaaabaa"; // 预期结果 8
//    string haystack = "mississippi", needle = "issip"; // 预期结果 4
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->strStr(haystack, needle);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
