//
//  main.cpp
//  Prob1415_Add_Strings
//
//  Created by 阴昱为 on 2019/7/13.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//415. Add Strings
//
//Given two non-negative integers num1 and num2 represented as string, return the sum of num1 and num2.
//
//给定两个字符串形式的非负整数 num1 和num2 ，计算它们的和。
//
//Note:
//    The length of both num1 and num2 is < 5100.
//    Both num1 and num2 contains only digits 0-9.
//    Both num1 and num2 does not contain any leading zero.
//    You must not use any built-in BigInteger library or convert the inputs to integer directly.
//
//注意：
//    num1 和num2 的长度都小于 5100.
//    num1 和num2 都只包含数字 0-9.
//    num1 和num2 都不包含任何前导零。
//    你不能使用任何內建 BigInteger 库， 也不能直接将输入的字符串转换为整数形式。


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
    string addStrings(string num1, string num2) {
        return this->solution1(num1, num2);
    }
    
private:
    // 方法一：逐位相加，注意进位。时间复杂度 O(N), 空间复杂度 O(1), N = max(num1.size, num2.size)
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 98.50% 的用户
    // 内存消耗 : 8.9 MB , 在所有 C++ 提交中击败了 83.76% 的用户
    // Runtime: 4 ms, faster than 94.04% of C++ online submissions for Add Strings.
    // Memory Usage: 9 MB, less than 69.37% of C++ online submissions for Add Strings.
    string solution1 (string num1, string num2) {
        // 边界条件
        if (num1.empty() || num2.empty()) {
            return "0";
        }
        
        // 已知条件：num1 和 num2 只包含数字 0-9，且均不以零开头（除非是数字 0 本身）
        if (num1 == "0" && num2 == "0") {
            return "0";
        }
        
        // 已知条件：num1 和 num2 是非负整数
        if (num1 == "0") {
            return num2;
        }
        
        if (num2 == "0") {
            return num1;
        }
        
        if (num1.size() < num2.size()) {
            // 让长串为 num1，短串为 num2
            this->swapString(num1, num2);
        }
        
        // 反转两串，让低位在前
        reverse(num1.begin(), num1.end());
        reverse(num2.begin(), num2.end());
        
        // 字符串数字相加
        this->addTwoStringNumber(num1, num2);
        
        // 反转结果串，让高位在前
        reverse(num1.begin(), num1.end());
        
        return num1;
    }
    
    // 两串相加
    void addTwoStringNumber (string& res, string& addition) {
        int cur_sum = 0;
        int carry = 0;
        int i = 0;
        
        // 逐位加 addition
        for (; i < addition.size(); i++) {
            // 保证 res 的位数够多
            if (i >= res.size()) {
                res.append("0");
            }
            
            cur_sum = (int)res[i] - 48 + (int)addition[i] - 48 + carry;
            
            if (cur_sum >= 10) {
                carry = 1;
                cur_sum -= 10;
            } else {
                carry = 0;
            }
            
            res[i] = (char)(cur_sum + 48);
        }
        
        // addition 加完后，有进位的情况
        while (carry > 0) {
            // 到 res 的末尾了
            if (i >= res.size()) {
                res.append("1");
                break;
            }
            
            cur_sum = (int)res[i] - 48 + carry;
            
            if (cur_sum >= 10) {
                carry = 1;
                cur_sum -= 10;
            } else {
                carry = 0;
            }
            
            res[i++] = (char)(cur_sum + 48);
        }
    }
    
    // 交换两个串
    void swapString (string& num1, string& num2) {
        string temp = num1;
        num1 = num2;
        num2 = temp;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string num1 = "2", num2 = "3"; // 预期结果 5
//    string num1 = "123", num2 = "456"; // 预期结果 579
//    string num1 = "12345", num2 = "12345"; // 预期结果 24690
//    string num1 = "0", num2 = "0"; // 预期结果 0
    string num1 = "9999999999", num2 = "9"; // 预期结果 10000000008
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->addStrings(num1, num2);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
