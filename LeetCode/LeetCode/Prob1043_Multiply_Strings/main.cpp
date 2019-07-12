//
//  main.cpp
//  Prob1043_Multiply_Strings
//
//  Created by 阴昱为 on 2019/7/12.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//43. Multiply Strings
//
//Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2, also represented as a string.
//
//给定两个以字符串形式表示的非负整数 num1 和 num2，返回 num1 和 num2 的乘积，它们的乘积也表示为字符串形式。
//
//Example 1:
//    Input: num1 = "2", num2 = "3"
//    Output: "6"
//
//Example 2:
//    Input: num1 = "123", num2 = "456"
//    Output: "56088"
//
//Note:
//    The length of both num1 and num2 is < 110.
//    Both num1 and num2 contain only digits 0-9.
//    Both num1 and num2 do not contain any leading zero, except the number 0 itself.
//    You must not use any built-in BigInteger library or convert the inputs to integer directly.
//
//说明：
//    num1 和 num2 的长度小于110。
//    num1 和 num2 只包含数字 0-9。
//    num1 和 num2 均不以零开头，除非是数字 0 本身。
//    不能使用任何标准库的大数类型（比如 BigInteger）或直接将输入转换为整数来处理。


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
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    string multiply(string num1, string num2) {
        return this->solution1(num1, num2);
    }
    
private:
    // 方法一：模拟乘法。时间复杂度 O()，空间复杂度 O(), N =
    string solution1 (string num1, string num2) {
        // 边界条件
        if (num1.empty() || num2.empty()) {
            return "0";
        }
        
        // 已知条件：num1 和 num2 只包含数字 0-9，且均不以零开头（除非是数字 0 本身）
        if (num1 == "0" || num2 == "0") {
            return "0";
        }
        
        // 已知条件：num1 和 num2 是非负整数
        if (num1 == "1") {
            return num2;
        }
        
        if (num2 == "1") {
            return num1;
        }
        
        
        if (num1.size() < num2.size()) {
            // 让长串为 num1，短串为 num2
            this->swapString(num1, num2);
        } else if (num1.size() == num2.size() && num1 < num2) {
            // 让较大串为 num1，较小串为 num2
            this->swapString(num1, num2);
        }
        
        // 反转两串，让低位在前
        reverse(num1.begin(), num1.end());
        reverse(num2.begin(), num2.end());
        
        string res = "0";
        string cur_mul = "1";
        string base = "";
        
        // 模拟竖式相乘相加
        for (int i = 0; i < num2.size(); i++) {
            cur_mul = this->multiplyTwoStringNumber(num1, (int)(num2[i]) - 48);
            cur_mul = base + cur_mul;
            
            this->addTwoStringNumber(res, cur_mul);
            
            base += "0";
        }
        
        // 反转结果串，让高位在前
        reverse(res.begin(), res.end());
        
        return res;
    }
    
    // 串和某个一位数相乘
    string multiplyTwoStringNumber (string& num1, int num2) {
        string res = "";
        
        int cur_mul = 0;
        int carry = 0;
        
        for (int i = 0; i < num1.size(); i++) {
            // 保证 res 的位数够多
            if (i >= res.size()) {
                res.append("0");
            }
            
            cur_mul = ((int)num1[i] - 48) * num2 + carry;
            
            if (cur_mul >= 10) {
                carry = cur_mul / 10;
                cur_mul %= 10;
            } else {
                carry = 0;
            }
            
            res[i] = (char)(cur_mul + 48);
        }
        
        // 末尾还有进位的情况
        if (carry > 0) {
            res += to_string(carry);
        }
        
        return res;
    }
    
    // 两串相加
    void addTwoStringNumber (string& res, string& addition) {
        int cur_sum = 0;
        int carry = 0;
        
        for (int i = 0; i < addition.size(); i++) {
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
        
        // 末尾还有进位的情况
        if (carry == 1) {
            res += "1";
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
//    string num1 = "2", num2 = "3"; // 预期结果 6
//    string num1 = "123", num2 = "456"; // 预期结果 56088
//    string num1 = "12345", num2 = "12345"; // 预期结果 152399025
    string num1 = "0", num2 = "0"; // 预期结果 0
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->multiply(num1, num2);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
