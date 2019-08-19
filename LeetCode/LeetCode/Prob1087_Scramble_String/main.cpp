//
//  main.cpp
//  Prob1087_Scramble_String
//
//  Created by 阴昱为 on 2019/8/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//87. Scramble String
//
//Given a string s1, we may represent it as a binary tree by partitioning it to two non-empty substrings recursively.
//给定一个字符串 s1，我们可以把它递归地分割成两个非空子字符串，从而将其表示为二叉树。
//
//Below is one possible representation of s1 = "great":
//    great
//   /    \
//  gr    eat
// / \    /  \
//g   r  e   at
//          /  \
//         a    t
//To scramble the string, we may choose any non-leaf node and swap its two children.
//
//For example, if we choose the node "gr" and swap its two children, it produces a scrambled string "rgeat".
//
//     rgeat
//    /    \
//   rg    eat
//  / \    /  \
// r   g  e   at
//           /  \
//          a    t
//We say that "rgeat" is a scrambled string of "great".
//
//Similarly, if we continue to swap the children of nodes "eat" and "at", it produces a scrambled string "rgtae".
//
//     rgtae
//    /    \
//   rg    tae
//  / \    /  \
// r   g  ta  e
//       /  \
//      t    a
//We say that "rgtae" is a scrambled string of "great".
//
//Given two strings s1 and s2 of the same length, determine if s2 is a scrambled string of s1.
//
//给出两个长度相等的字符串 s1 和 s2，判断 s2 是否是 s1 的扰乱字符串。
//
//Example 1:
//    Input: s1 = "great", s2 = "rgeat"
//    Output: true
//
//Example 2:
//    Input: s1 = "abcde", s2 = "caebd"
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


class Solution {
public:
    bool isScramble(string s1, string s2) {
        return this->solution1(s1, s2);
    }
    
private:
    // 方法一。。时间复杂度 O()，空间复杂度 O()。N =
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 89.78% 的用户
    // 内存消耗 : 10.5 MB , 在所有 C++ 提交中击败了 79.82% 的用户
    // Runtime: 8 ms, faster than 69.82% of C++ online submissions for Scramble String.
    // Memory Usage: 10.5 MB, less than 76.19% of C++ online submissions for Scramble String.
    bool solution1 (string& s1, string& s2) {
        // 边界情况
        if (s1 == s2) {
            return true;
        }
        
        if (s1.size() != s2.size()) {
            return false;
        }
        
        string ss1(s1);
        string ss2(s2);
        
        sort(ss1.begin(), ss1.end());
        sort(ss2.begin(), ss2.end());
        
        if (ss1 != ss2) {
            return false;
        }
        
        for (int i = 1; i < s1.size(); i++) {
            // s1 前 i 个字符 匹配 s2 前 i 个字符
            if(isScramble(s1.substr(0, i), s2.substr(0, i))
               && isScramble(s1.substr(i, s1.size()), s2.substr(i, s2.size()))) {
                return true;
            }
            
            // s1 前 i 个字符 匹配 s2 后 i 个字符
            if (isScramble(s1.substr(0, i), s2.substr(s2.size() - i, i))
                && isScramble(s1.substr(i, s1.size()), s2.substr(0, s2.size() - i))) {
                return true;
            }
        }
        
        return false;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string s1 = "great", s2 = "rgeat"; // 预期结果 true
    string s1 = "abcde", s2 = "caebd"; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isScramble(s1, s2);
    if (ans) {
        cout << "True" << endl;
    } else {
        cout << "False" << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
