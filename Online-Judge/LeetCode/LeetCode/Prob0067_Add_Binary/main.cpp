//
//  main.cpp
//  Prob1067_Add_Binary
//
//  Created by 阴昱为 on 2019/7/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//67. Add Binary
//
//Given two binary strings, return their sum (also a binary string).
//The input strings are both non-empty and contains only characters 1 or 0.
//
//给定两个二进制字符串，返回他们的和（用二进制表示）。
//输入为非空字符串且只包含数字 1 和 0。
//
//Example 1:
//    Input: a = "11", b = "1"
//    Output: "100"
//
//Example 2:
//    Input: a = "1010", b = "1011"
//    Output: "10101"


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
//const int MOD = 1000000007; // 1e9+7 与 1e9+9 为孪生素数

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    string addBinary(string a, string b) {
        return this->solution1(a, b);
    }
    
private:
    // 方法一：逐位相加，注意进位。时间复杂度 O(N), 空间复杂度 O(1), N = max(a.size, b.size)
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 76.33% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 46.94% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Add Binary.
    // Memory Usage: 8.7 MB, less than 49.10% of C++ online submissions for Add Binary.
    string solution1 (string a, string b) {
        // 边界条件
        if (a.empty() || a == "0") {
            return b;
        }
        
        if (b.empty() || b == "0") {
            return a;
        }
        
        // 让大串为 a，小串为 b
        if (a.size() < b.size()) {
            this->swapString(a, b);
        } else if (a.size() == b.size() && a < b) {
            this->swapString(a, b);
        }
        
        // 反转两串，让低位在前
        reverse(a.begin(), a.end());
        reverse(b.begin(), b.end());
        
        // 二进制字符串数字相加
        this->addTwoBinaryStringNumber(a, b);
        
        // 反转结果串，让高位在前
        reverse(a.begin(), a.end());
        
        return a;
    }
    
    void swapString (string& a, string& b) {
        string temp = a;
        a = b;
        b = temp;
    }
    
    // 二进制字符串数字相加，之前保证了 a 为较大串
    void addTwoBinaryStringNumber (string& a, string& b) {
        int cur_sum = 0;
        int carry = 0;
        
        int i = 0;
        for (; i < b.size(); i++) {
            cur_sum = a[i] - '0' + b[i] - '0' + carry;
            
            if (cur_sum >= 2) {
                carry = 1;
                cur_sum -= 2;
            } else {
                carry = 0;
            }
            
            a[i] = (char)(cur_sum + '0');
        }
        
        // 若有进位，则继续往 a 的高位加
        while (carry > 0) {
            // 到 a 的尾部了，最多进一位
            if (i >= a.size()) {
                a += '1';
                break;
            }
            
            if (a[i] == '1') {
                a[i++] = '0';
            } else {
                a[i] = '1';
                break;
            }
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string a = "11", b = "1"; // 预期结果 "100"
//    string a = "1010", b = "1011"; // 预期结果 "10101"
    string a = "100010", b = "11"; // 预期结果 "100101"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->addBinary(a, b);
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
