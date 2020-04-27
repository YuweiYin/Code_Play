//
//  main.cpp
//  Prob1044_Wildcard_Matching
//
//  Created by 阴昱为 on 2019/7/20.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//44. Wildcard Matching
//
//Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*'.
//'?' Matches any single character.
//'*' Matches any sequence of characters (including the empty sequence).
//The matching should cover the entire input string (not partial).
//
//Note:
//    s could be empty and contains only lowercase letters a-z.
//    p could be empty and contains only lowercase letters a-z, and characters like ? or *.
//
//给定一个字符串 (s) 和一个字符模式 (p) ，实现一个支持 '?' 和 '*' 的通配符匹配。
//'?' 可以匹配任何单个字符。
//'*' 可以匹配任意字符串（包括空字符串）。
//两个字符串完全匹配才算匹配成功。
//
//说明:
//    s 可能为空，且只包含从 a-z 的小写字母。
//    p 可能为空，且只包含从 a-z 的小写字母，以及字符 ? 和 *。
//
//Example 1:
//    Input:
//    s = "aa"
//    p = "a"
//    Output: false
//    Explanation: "a" does not match the entire string "aa".
//
//Example 2:
//    Input:
//    s = "aa"
//    p = "*"
//    Output: true
//    Explanation: '*' matches any sequence.
//
//Example 3:
//    Input:
//    s = "cb"
//    p = "?a"
//    Output: false
//    Explanation: '?' matches 'c', but the second letter is 'a', which does not match 'b'.
//
//Example 4:
//    Input:
//    s = "adceb"
//    p = "*a*b"
//    Output: true
//    Explanation: The first '*' matches the empty sequence, while the second '*' matches the substring "dce".
//
//Example 5:
//    Input:
//    s = "acdcb"
//    p = "a*c?b"
//    Output: false


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


#include <regex>


class Solution {
public:
    bool isMatch(string s, string p) {
        return this->solution2(s, p);
    }
    
private:
    // 方法一：regex 正则匹配。时间复杂度 O()，空间复杂度 O()。
    bool solution1 (string& s, string& p) {
        // 边界情况
        if (s.empty() || p.empty()) {
            return false;
        }
        
        if (s == p) {
            return true;
        }
        
        bool res = true;
        
        // 正则匹配 TODO p 不是合法模式串
        regex pattern(p, regex::icase);
        smatch result;
        
        if(regex_match(s, result, pattern)) {
            cout << result[0] << endl;
            cout << result[1] << endl;
        }
        
        return res;
    }
    
    // 方法二：暴力法，直接匹配。时间复杂度 O(N)，空间复杂度 O(1)。N = s.size
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 92.12% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 93.93% 的用户
    // Runtime: 4 ms, faster than 99.05% of C++ online submissions for Wildcard Matching.
    // Memory Usage: 8.6 MB, less than 96.98% of C++ online submissions for Wildcard Matching.
    bool solution2 (string& s, string& p) {
        int j = 0, s_len = (int)s.size(), p_len = (int)p.size();
        
        for (int star = 0, i = 0, last = 0; i < s_len; ) {
            // i 指示 s 位置，j 指示 p 位置
            if (j < p_len && (s[i] == p[j] || p[j] == '?')) {
                // j 不越界，并且 s[i] 与 p[j] 相匹配，或者 p[j] 为 '?' 可以任意匹配单字符
                i ++; // 往后看 s 串
                j ++; // 往后看 p 串
            } else if (j < p_len && p[j] == '*') {
                // j 不越界，并且 p[j] 为 '*' 可以任意匹配多字符
                last = i; // i 不变，继续用 '*' 匹配，但把 i 值记录到 last 变量中
                star = ++j; // 记录 p 中 '*' 下一个字符的位置到 star 变量中，往后看 p 串(先把 '*' 看作匹配 "")
            } else if (star != 0) {
                // 出现不匹配，如果此时 star 不为 0，就表示可以用 p 中前一个 '*' 匹配来弥补
                i = ++last; // 匹配上 s[i]，往后看 s 串
                j = star; // j 在 star 位置，即 p 中前一个 '*' 的下个字符(每次只用 '*' 匹配来弥补一个字符，不"贪心")
            } else {
                // 出现不匹配，p 中也没有 '*' 匹配来弥补，直接返回 false，匹配失败
                return false;
            }
        }
        
        // s 匹配结束了，p 还剩字符，必须要全是 '*' 才行
        for(; j < p_len && p[j] == '*'; j++);
        
        return j == p_len;
    }
    
    // C++ Regex
    void testRegex () {
        // 第一种存储方式
        // match_results<string::const_iterator> result;
        // 第二种存储方式
        smatch result;
        
        // 设置字符串数据
        string str = "1995 is my birth year 1995";
        
        // 正则表达式
        string regex_str = "\\d{4}";
        regex pattern1(regex_str, regex::icase);
        
        // 迭代器声明
        string::const_iterator iter = str.begin();
        string::const_iterator iterEnd = str.end();
        string temp;
        
        // 正则查找
        while (std::regex_search(iter, iterEnd, result, pattern1)) {
            temp = result[0];
            cout << temp << endl;
            iter = result[0].second; // 更新搜索起始位置
        }
        
        // 正则匹配
        string regex_str2 = "(\\d{4}).*";
        regex pattern2(regex_str2, regex::icase);
        
        if(regex_match(str, result, pattern2)) {
            cout << result[0] << endl;
            cout << result[1] << endl;
        }
        
        // 正则替换
        regex reg1("\\d{4}");
        string t = "1989";
        str = regex_replace(str, reg1, t); // trim_left
        cout << str << endl;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string s = "adceb", p = "*a*b"; // 预期结果 true
    string s = "acdcb", p = "a*c?b"; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isMatch(s, p);
    if (ans) {
        cout << s << " Match " << p << endl;
    } else {
        cout << s << " Do NOT Match " << p << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
