//
//  main.cpp
//  Prob1008_String_to_Integer_atoi
//
//  Created by 阴昱为 on 2019/6/2.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//8. String to Integer (atoi)
//
//Implement atoi which converts a string to an integer.
//The function first discards as many whitespace characters as necessary until the first non-whitespace character is found. Then, starting from this character, takes an optional initial plus or minus sign followed by as many numerical digits as possible, and interprets them as a numerical value.
//
//The string can contain additional characters after those that form the integral number, which are ignored and have no effect on the behavior of this function.
//
//If the first sequence of non-whitespace characters in str is not a valid integral number, or if no such sequence exists because either str is empty or it contains only whitespace characters, no conversion is performed.
//
//If no valid conversion could be performed, a zero value is returned.
//
//Note:
//
//Only the space character ' ' is considered as whitespace character.
//Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−2^31,  2^31 − 1]. If the numerical value is out of the range of representable values, INT_MAX (2^31 − 1) or INT_MIN (−2^31) is returned.

//请你来实现一个 atoi 函数，使其能将字符串转换成整数。
//首先，该函数会根据需要丢弃无用的开头空格字符，直到寻找到第一个非空格的字符为止。
//当我们寻找到的第一个非空字符为正或者负号时，则将该符号与之后面尽可能多的连续数字组合起来，作为该整数的正负号；假如第一个非空字符是数字，则直接将其与之后连续的数字字符组合起来，形成整数。
//该字符串除了有效的整数部分之后也可能会存在多余的字符，这些字符可以被忽略，它们对于函数不应该造成影响。
//注意：假如该字符串中的第一个非空格字符不是一个有效整数字符、字符串为空或字符串仅包含空白字符时，则你的函数不需要进行转换。
//在任何情况下，若函数不能进行有效的转换时，请返回 0。
//说明：
//假设我们的环境只能存储 32 位大小的有符号整数，那么其数值范围为 [−2^31,  2^31 − 1]。如果数值超过这个范围，qing返回  INT_MAX (2^31 − 1) 或 INT_MIN (−2^31) 。
//
//Example1:
//  Input: "42"
//  Output: 42
//
//Example2:
//  Input: "   -42"
//  Output: -42
//  Explanation: The first non-whitespace character is '-', which is the minus sign.
//      Then take as many numerical digits as possible, which gets 42.
//
//Example3:
//  Input: "4193 with words"
//  Output: 4193
//  Explanation: Conversion stops at digit '3' as the next character is not a numerical digit.
//Note:
//Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−231,  231 − 1]. For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows.
// Example4:
//Input: "words and 987"
//  Output: 0
//  Explanation: The first non-whitespace character is 'w', which is not a numerical
//      digit or a +/- sign. Therefore no valid conversion could be performed.
//
// Example5:
//  Input: "-91283472332"
//  Output: -2147483648
//  Explanation: The number "-91283472332" is out of the range of a 32-bit signed integer.
//      Thefore INT_MIN (−2^31) is returned.
//注意:
//假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−2^31, 2^31 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。


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
#define ll long long

// 全局常量
//#define PI acos(-1.0)
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

const int MAX_INT32 = 0x7fffffff;
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


class Solution {
public:
    int myAtoi(string str) {
        return this->solution1(str);
    }
    
    int atoi(const char *str) {
        return this->solution2(str);
    }
    
    // 方法一：时间复杂度 O(n), 空间复杂度 O(1)
    int solution1 (string str) {
        // 如果字符串为空，直接返回 0
        if (str.empty()) {
            return 0;
        }
        
        // 除去开头的空格
        while (*str.begin() == ' ') {
            str.erase(str.begin());
        }
        
        int res = 0; // 最终结果
        bool positive = true; // 记录正负号
        
        // 判断正负号，判断完后删除符号位字符
        if (*str.begin() == '+') {
            str.erase(str.begin());
        } else if (*str.begin() == '-') {
            positive = false;
            str.erase(str.begin());
        } else if (*str.begin() < '0' || *str.begin() > '9') {
            // 首位不是正负号or数字
            return 0;
        }
        
        // 除去数字开头的 0
        while (*str.begin() == '0') {
            str.erase(str.begin());
        }
        
        int res_len = 0; // 记录结果的位数，最多 10 位
        while (!str.empty() && res_len <= 10 && *str.begin() >= '0' && *str.begin() <= '9') {
            int number = (int)(*str.begin() - '0');
            
            // 如果到了第 11 位还是数字，那么肯定溢出了，返回最值即可
            if (res_len >= 10) {
                if (positive) {
                    return MAX_INT32;
                } else {
                    return MIN_INT32;
                }
            }
            
            // 判断溢出
            if (res_len == 9) {
                if (positive) {
                    // MAX_INT32 = 2147483647 (0x7FFFFFFF)
                    if (res > 214748364 || (res == 214748364 && number >= 7)) {
                        return MAX_INT32;
                    }
                } else {
                    // MIN_INT32 = -2147483648 (0x80000000)
                    if (res > 214748364 || (res == 214748364 && number >= 8)) {
                        return MIN_INT32;
                    }
                }
            }
            // 累加末位、增加 res 长度、删去 str 头字符
            res = res * 10 + number;
            res_len ++;
            str.erase(str.begin());
        }
        
        // 根据正负号输出结果
        if (positive) {
            return res;
        } else {
            return -res;
        }
    }
    
    // 方法一：（牛客网版本）时间复杂度 O(n), 空间复杂度 O(1)
    int solution2 (const char *s) {
        string str = s;
        // 如果字符串为空，直接返回 0
        if (str.empty()) {
            return 0;
        }
        
        // 除去开头的空格
        while (*str.begin() == ' ') {
            str.erase(str.begin());
        }
        
        int res = 0; // 最终结果
        bool positive = true; // 记录正负号
        
        // 判断正负号，判断完后删除符号位字符
        if (*str.begin() == '+') {
            str.erase(str.begin());
        } else if (*str.begin() == '-') {
            positive = false;
            str.erase(str.begin());
        } else if (*str.begin() < '0' || *str.begin() > '9') {
            // 首位不是正负号or数字
            return 0;
        }
        
        // 除去数字开头的 0
        while (*str.begin() == '0') {
            str.erase(str.begin());
        }
        
        int res_len = 0; // 记录结果的位数，最多 10 位
        while (!str.empty() && res_len <= 10 && *str.begin() >= '0' && *str.begin() <= '9') {
            int number = (int)(*str.begin() - '0');
            
            // 如果到了第 11 位还是数字，那么肯定溢出了，返回最值即可
            if (res_len >= 10) {
                if (positive) {
                    return MAX_INT32;
                } else {
                    return MIN_INT32;
                }
            }
            
            // 判断溢出
            if (res_len == 9) {
                if (positive) {
                    // MAX_INT32 = 2147483647 (0x7FFFFFFF)
                    if (res > 214748364 || (res == 214748364 && number >= 7)) {
                        return MAX_INT32;
                    }
                } else {
                    // MIN_INT32 = -2147483648 (0x80000000)
                    if (res > 214748364 || (res == 214748364 && number >= 8)) {
                        return MIN_INT32;
                    }
                }
            }
            // 累加末位、增加 res 长度、删去 str 头字符
            res = res * 10 + number;
            res_len ++;
            str.erase(str.begin());
        }
        
        // 根据正负号输出结果
        if (positive) {
            return res;
        } else {
            return -res;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // string str = "   -419 3 with words"; // -419
    // string str = "  0000000000012345678"; // 12345678
    // string str = "2147483646"; // 2147483646
    // string str = "-2147483648"; // -2147483648
    string str = "-20000000000000000000"; // -2147483648
    
    char *s = (char *)str.data();
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->myAtoi(str) << endl;
    cout << solution->atoi(s) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
