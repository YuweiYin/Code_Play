//
//  main.cpp
//  Prob1005_Longest_Palindromic_Substring
//
//  Created by 阴昱为 on 2019/5/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//


//5. Longest Palindromic Substring
//
//Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
//
//给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。
//
//Example1:
//  Input: "babad"
//  Output: "bab"
//  Note: "aba" is also a valid answer.
//
//Example2:
//  Input: "cbbd"
//  Output: "bb"


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


class Solution {
public:
    // const int MAX_LEN = 1000;
    string best_substring;
    int max_len;
    
    Solution() {
        this->best_substring = "";
        this->max_len = 0;
    }
    
    Solution(string best_substring, int max_len) {
        this->best_substring = best_substring;
        this->max_len = max_len;
    }
    
    string longestPalindrome(string s) {
        string ans = "";
        
        if (this->manacher(s) >= 0) {
            ans = this->best_substring;
        }
        
        return ans;
    }
    
    string initManacherString(string s) {
        string str = "#";
        for (int i = 0; i < s.length(); i++) {
            str += s[i];
            str += "#";
        }
        return str;
    }
    
    int manacher(string s) {
        if (s.empty()){
            return -1;
        }
        
        string manacher_string = this->initManacherString(s);
        int best_index = -1;
        int radius[manacher_string.length()];
        string substring[manacher_string.length()];
        for (int i = 0; i < manacher_string.length(); i++) {
            radius[i] = 0;
            substring[i] = "";
        }
        
        int R = -1;
        int c = -1;
        int cur_len = 0;
        
        for (int i = 0; i < manacher_string.length(); i++) {
            string cur_substring = "";
            cur_substring += manacher_string[i];
            
            radius[i] = R > i ? min(radius[2 * c - i], R - i + 1): 1;
            while(i + radius[i] < manacher_string.length() && i - radius[i] > -1) {
                if (manacher_string[i - radius[i]] == manacher_string[i + radius[i]]) {
                    char match_char = manacher_string[i - radius[i]];
                    if (match_char != '#') {
                        cur_substring = manacher_string[i - radius[i]] + cur_substring +
                            manacher_string[i - radius[i]];
                    }
                    radius[i] ++;
                } else {
                    break;
                }
            }
            
            // 记录当前的回文串到数组
            substring[i] = cur_substring;
            
            if (i + radius[i] > R) {
                R = i + radius[i] - 1;
                c = i;
            }
            
            if (radius[i] > cur_len) {
                cur_len = radius[i];
                best_index = i;
            }
        }
        
        if (best_index < 0) {
            this->best_substring = "";
        } else {
            this->best_substring = substring[best_index];
        }
        
        // cout << "this->best_substring = " << this->best_substring << endl;
        
        this->max_len = cur_len - 1;
        return this->max_len;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    string s = "babad";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->longestPalindrome(s) << endl;
    // cout << solution->manacher(s) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
