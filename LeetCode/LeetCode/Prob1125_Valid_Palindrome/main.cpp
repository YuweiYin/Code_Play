//
//  main.cpp
//  Prob1125_Valid_Palindrome
//
//  Created by 阴昱为 on 2019/10/5.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//125. Valid Palindrome
//
//Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
//Note: For the purpose of this problem, we define empty string as valid palindrome.
//
//给定一个字符串，验证它是否是回文串，只考虑字母和数字字符，可以忽略字母的大小写。
//说明：本题中，我们将空字符串定义为有效的回文串。
//
//Example 1:
//    Input: "A man, a plan, a canal: Panama"
//    Output: true
//
//Example 2:
//    Input: "race a car"
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

#include <regex>

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
//const int negative_infinity = -0x40000000;


class Solution {
public:
    bool isPalindrome(string s) {
        return this->solution2(s);
    }
    
private:
    // 方法一：字符串预处理。时间复杂度 O(N)，空间复杂度 O(1)。
    // 执行用时 : 144 ms , 在所有 C++ 提交中击败了 5.29% 的用户
    // 内存消耗 : 33.3 MB , 在所有 C++ 提交中击败了 5.10% 的用户
    // Runtime: 148 ms, faster than 5.09% of C++ online submissions for Valid Palindrome.
    // Memory Usage: 33.2 MB, less than 6.12% of C++ online submissions for Valid Palindrome.
    bool solution1 (string s) {
        // 边界情况
        if (s.empty()) {
            return true;
        }
        
        // 字符串转小写
        transform(s.begin(), s.end(), s.begin(), ::tolower); // 转大写则使用 toupper
        
        s = this->trim(s);
        // cout << s << endl;
        
        if (s.empty()) {
            return true;
        }
        
        int len = (int)s.size();
        int half = len / 2;
        
        for (int i = 0; i < half; i++) {
            if (s[i] != s[len - 1 - i]) {
                return false;
            }
        }
        
        return true;
    }
    
    // 正则替换，除了字母和数字外的字符全替换为空
    string trim (string s) {
        // cout << s << endl;
        
        regex regex_str("[^a-zA-Z0-9]");
        string replace_str("");
        
        // string str = regex_replace(s, regex_str, replace_str);
        // cout << str << endl;
        
        return regex_replace(s, regex_str, replace_str);
    }
    
    // 方法二：对撞指针。时间复杂度 O(N)，空间复杂度 O(1)。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 99.12% 的用户
    // 内存消耗 : 9.5 MB , 在所有 C++ 提交中击败了 13.38% 的用户
    // Runtime: 8 ms, faster than 83.52% of C++ online submissions for Valid Palindrome.
    // Memory Usage: 9.5 MB, less than 36.74% of C++ online submissions for Valid Palindrome.
    bool solution2 (string s) {
        // 边界情况
        if (s.empty()) {
            return true;
        }
        
        // 字符串转小写
        // transform(s.begin(), s.end(), s.begin(), ::tolower); // 转大写则使用 toupper
        
        if (s.empty()) {
            return true;
        }
        
        int len = (int)s.size();
        int left = 0, right = len - 1;
        
        while (left < right) {
            if (!this->valid(s[left])) {
                left ++;
                continue;
            }
            
            if (!this->valid(s[right])) {
                right --;
                continue;
            }
            
            if (s[left] != s[right]) {
                if (this->is_digit(s[left]) || this->is_digit(s[right])) {
                    // 如果其中一个是数字，那么 s[left] != s[right] 就表示二者真的不同
                    return false;
                } else {
                    // 如果是因为大小写原因而不相等，则都转为小写字符再比较
                    if (this->is_upper(s[left])) {
                        s[left] = tolower(s[left]);
                    }
                    
                    if (this->is_upper(s[right])) {
                        s[right] = tolower(s[right]);
                    }
                    
                    if (s[left] != s[right]) {
                        return false;
                    }
                }
            }
            
            left ++;
            right --;
        }
        
        return true;
    }
    
    bool valid (char ch) {
        if ((ch >= '0' && ch <= '9') ||
            (ch >= 'a' && ch <= 'z') ||
            (ch >= 'A' && ch <= 'Z')) {
            return true;
        } else {
            return false;
        }
    }
    
    bool is_digit (char ch) {
        if (ch >= '0' && ch <= '9') {
            return true;
        } else {
            return false;
        }
    }
    
    bool is_lower (char ch) {
        if (ch >= 'a' && ch <= 'z') {
            return true;
        } else {
            return false;
        }
    }
    
    bool is_upper (char ch) {
        if (ch >= 'A' && ch <= 'Z') {
            return true;
        } else {
            return false;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    string s = "A man, a plan, a canal: Panama"; // 预期结果 true
//    string s = "race a car"; // 预期结果 false
//    string s = ""; // 预期结果 true
//    string s = ". "; // 预期结果 true
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isPalindrome(s);
    if (ans) {
        cout << "Yes, s is a Palindrome." << endl;
    } else {
        cout << "No, s is NOT a Palindrome." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
