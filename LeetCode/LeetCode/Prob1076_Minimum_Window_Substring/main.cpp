//
//  main.cpp
//  Prob1076_Minimum_Window_Substring
//
//  Created by 阴昱为 on 2019/8/3.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//76. Minimum Window Substring
//
//Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).
//
//给你一个字符串 S、一个字符串 T，请在字符串 S 里面找出：包含 T 所有字母的最小子串。
//
//Example:
//    Input: S = "ADOBECODEBANC", T = "ABC"
//    Output: "BANC"
//
//Note:
//    If there is no such window in S that covers all characters in T, return the empty string "".
//    If there is such window, you are guaranteed that there will always be only one unique minimum window in S.
//
//说明：
//    如果 S 中不存这样的子串，则返回空字符串 ""。
//    如果 S 中存在这样的子串，我们保证它是唯一的答案。


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
    string minWindow(string s, string t) {
        return this->solution1(s, t);
    }
    
private:
    // 方法一。滑动窗口。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 52 ms , 在所有 C++ 提交中击败了 37.97% 的用户
    // 内存消耗 : 9.9 MB , 在所有 C++ 提交中击败了 58.23% 的用户
    // Runtime: 36 ms, faster than 25.49% of C++ online submissions for Minimum Window Substring.
    // Memory Usage: 9.9 MB, less than 89.15% of C++ online submissions for Minimum Window Substring.
    string solution1 (string s, string t) {
        // 边界情况，矩阵为空
        if (s.empty() || t.empty()) {
            return "";
        }
        
        // 记录最短子串的开始位置和长度
        int start = 0, min_len = INT_MAX;
        int left = 0, right = 0;
        
        map<char, int> window;
        map<char, int> needs;
        
        for (char c: t) {
            needs[c] ++;
        }
        
        int match = 0; // 成功匹配单词数
        int s_len = (int)s.size();
        int needs_len = (int)needs.size();
        
        while (right < s_len) {
            char right_char = s[right]; // 当前最右字符
            if (needs.count(right_char)) {
                window[right_char] ++;
                
                if (window[right_char] == needs[right_char]) {
                    match ++; // 匹配上一个单词
                }
            }
            right ++; // 右滑
            
            // 若匹配个数符合要求
            while (match == needs_len) {
                if (right - left < min_len) {
                    // 更新最小子串的位置和长度
                    start = left;
                    min_len = right - left;
                }
                
                char left_char = s[left]; // 当前最左字符
                if (needs.count(left_char)) {
                    window[left_char] --;
                    
                    if (window[left_char] < needs[left_char]) {
                        match --; // 匹配单词数减一
                    }
                }
                
                left ++; // 左滑
            }
        }
        
        return min_len == INT_MAX ? "" : s.substr(start, min_len);
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    string S = "ADOBECODEBANC", T = "ABC"; // 预期结果 "BANC"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->minWindow(S, T);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        cout << "Answer is " << ans << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
