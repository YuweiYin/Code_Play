//
//  main.cpp
//  Prob1010_Regular_Expression_Matching
//
//  Created by 阴昱为 on 2019/6/6.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//10. Regular Expression Matching
//
//Given an input string (s) and a pattern (p), implement regular expression matching with support for '.' and '*'.
//  '.' Matches any single character.
//  '*' Matches zero or more of the preceding element.
//The matching should cover the entire input string (not partial).
//Note:
//  s could be empty and contains only lowercase letters a-z.
//  p could be empty and contains only lowercase letters a-z, and characters like . or *.

//给你一个字符串 s 和一个字符规律 p，请你来实现一个支持 '.' 和 '*' 的正则表达式匹配。
//  '.' 匹配任意单个字符
//  '*' 匹配零个或多个前面的那一个元素
//所谓匹配，是要涵盖 整个 字符串 s的，而不是部分字符串。
//说明:
//  s 可能为空，且只包含从 a-z 的小写字母。
//  p 可能为空，且只包含从 a-z 的小写字母，以及字符 . 和 *。
//
//Example1:
//  Input:
//  s = "aa"
//  p = "a"
//  Output: false
//  Explanation: "a" does not match the entire string "aa".
//
//Example2:
//  Input:
//  s = "aa"
//  p = "a*"
//  Output: true
//  Explanation: '*' means zero or more of the precedeng element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
//
//Example3:
//  Input:
//  s = "ab"
//  p = ".*"
//  Output: true
//  Explanation: ".*" means "zero or more (*) of any character (.)".
//
//Example4:
//  Input:
//  Input:
//  s = "aab"
//  p = "c*a*b"
//  Output: true
//  Explanation: c can be repeated 0 times, a can be repeated 1 time. Therefore it matches "aab".
//
//Example5:
//  Input:
//  s = "mississippi"
//  p = "mis*is*p*."
//  Output: false

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
    map<tuple<int, int>, bool> dp_notebook;
public:
    bool isMatch(string s, string p) {
        return this->solution4(s, p);
    }
    
    // 1：在不考虑 '*' 的情况下，非递归匹配两个串
    bool solution1 (string s, string p) {
        // 两串均空，匹配成功
        if (s.empty() && p.empty()) {
            return true;
        }
        
        int i = 0, j = 0;
        
        // i 遍历 s, j 遍历 p
        while (i < (int)s.size()) {
            if (j > (int)p.size()) {
                return false;
            }
            if (s[i] != p[j] && p[j] != '.') {
                // 当前字符不匹配，且模式串不是万能匹配符 '.'
                return false;
            }
            i ++;
            j ++;
        }
        
        return true;
    }
    
    // 2：在不考虑 '*' 的情况下，递归匹配两个串
    bool solution2 (string s, string p) {
        // 两串均空，匹配成功
        if (s.empty() && p.empty()) {
            return true;
        }
        
        // 判断首字符是否匹配
        bool first_match = (s[0] == p[0]) || (p[0] == '.');
        
        return first_match && this->solution2(s.substr(1), p.substr(1));
    }
    
    // 3：考虑 '*' 的情况下，递归匹配两个串
    bool solution3 (string s, string p) {
        // 两串均空，匹配成功
        if (s.empty() && p.empty()) {
            return true;
        }
        
        // 判断首字符是否匹配
        bool first_match = (s[0] == p[0]) || (p[0] == '.');
        
        // 如果模式串的左数第二个字符是 '*'
        if ((int)p.size() >= 2 && p[1] == '*') {
            // 假设 s 为 'bba', p 为 'b*a', 下一步要么变为 'bbb' 和 'a' 或者 'bb' 和 'b*a'
            // 一次只匹配 0 个或 1 个 b
            return this->solution3(s, p.substr(2)) ||
                (first_match && this->solution3(s.substr(1), p));
        }
        
        return first_match && this->solution3(s.substr(1), p.substr(1));
    }
    
    // 4：考虑 '*' 的情况下，递归匹配两个串。存在重叠子问题，可以用动态规划来优化
    // 重叠子问题分析：在匹配 '*' 时，有两条路径：dp[i][j+2] 和 dp[i+1][j]。最末还有条 dp[i+1, j+1] 的路径。
    // 因此从初始态 dp[0][0] 到终止态 dp[max_i][max_j] 的过程可以有三条路，必有重叠路径
    // 举例：从 dp[0][0] 到 dp[2][2]，可以->dp[1][1]->dp[2][2]，也可以->dp[0][2]->dp[1][2]->dp[2][2]
    bool solution4 (string s, string p) {
        // 两串均空，匹配成功
        if (s.empty() && p.empty()) {
            return true;
        }
        
        // 从 (0, 0) 开始匹配两串
        return this->DP(s, p, 0, 0);
    }
    
private:
    bool DP (string s, string p, int i, int j) {
        // 动态规划核心1：如果 DP 表中已有该位置的值，则不必重复计算，直接返回这个位置的值
        if (this->dp_notebook.find(make_tuple(i, j)) != dp_notebook.end()) {
            return dp_notebook[make_tuple(i, j)];
        }
        
        // 如果模式串到末尾了，判断匹配串是否也到达末尾
        if (j >= (int)p.size()) {
            return i == (int)s.size();
        }
        
        bool res = true;
        // 判断 s[i] 和 p[j] 字符是否匹配
        bool first_match = i < (int)s.size() && ((s[i] == p[j]) || (p[j] == '.'));
        
        // 如果从位置 j 开始，模式串的左数第二个字符是 '*'
        if (j <= (int)p.size() - 2 && p[j + 1] == '*') {
            // dp[i][j] ->dp[i][j+2] 或者 ->dp[i+1][j+1]
            res = this->DP(s, p, i, j + 2) ||
                (first_match && this->DP(s, p, i + 1, j));
        } else {
            // dp[i][j] ->dp[i+1][j+1]
            res = first_match && this->DP(s, p, i + 1, j + 1);
        }
        
        // 动态规划核心2：记录 DP 表项
        this->dp_notebook.insert(make_pair(make_tuple(i, j), res));
        //this->dp_notebook.insert(pair<tuple<int, int>, bool>(tuple<int, int>(i, j), res));
        
        //map<tuple<int, int>, bool>::iterator ite = this->dp_notebook.begin();
        //cout << get<0>(ite->first) << get<1>(ite->first) << ite->second << endl;
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    string s = "abbc";
    //string p = "c*a*b*c";
    //string p = "a..c";
    //string p = "a.*c";
    string p = ".*c";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->isMatch(s, p) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
