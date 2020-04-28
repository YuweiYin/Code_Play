//
//  main.cpp
//  Prob1029_Divide_Two_Integers
//
//  Created by 阴昱为 on 2019/6/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1029. Divide Two Integers
//
//Given two integers dividend and divisor, divide two integers without using multiplication, division and mod operator.
//Return the quotient after dividing dividend by divisor.
//The integer division should truncate toward zero.
//
//给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。
//返回被除数 dividend 除以除数 divisor 得到的商。
//
//Example 1:
//    Input: dividend = 10, divisor = 3
//    Output: 3
//
//Example 2:
//    Input: dividend = 7, divisor = -3
//    Output: -2
//
//Note:
//    Both dividend and divisor will be 32-bit signed integers.
//    The divisor will never be 0.
//    Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−2^31,  2^31 − 1]. For the purpose of this problem, assume that your function returns 2^31 − 1 when the division result overflows.
//说明:
//    被除数和除数均为 32 位有符号整数。
//    除数不为 0。
//    假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−2^31,  2^31 − 1]。本题中，如果除法结果溢出，则返回 2^31 − 1。


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

const int MAX_INT32 = 0x7fffffff;
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
const int HALF_MAX_INT32 = MAX_INT32 >> 1;


class Solution {
public:
    int divide(int dividend, int divisor) {
        // 边界情况：除数为 0，结果溢出
        if (divisor == 0) {
            return MAX_INT32;
        }
        
        // 边界情况：被除数为 0，结果为 0
        if (dividend == 0) {
            return 0;
        }
        
        // 边界情况：除数为 1，结果为被除数
        if (divisor == 1) {
            return dividend;
        }
        
        // MIN_INT32 / -1 溢出
        if (dividend == MIN_INT32 && divisor == -1) {
            return MAX_INT32;
        }
        
        // 调用核心解决方案
        return this->solution2(dividend, divisor);
    }
    
private:
    // 方法一。循环做减法。时间复杂度 O(dividend / divisor)，空间复杂度 O(1)
    int solution1(int dividend, int divisor) {
        // 用于记录结果的符号，被除数与除数正负性的同或
        bool positive = true;
        // 如果被除数是 MIN_INT32 且除数不为 -1，那么需要正常做除法，但是把 MIN_INT32 取负号是溢出 int 的
        // 所以用 residual 来记录被除数为 MIN_INT32，它转为正数时会成为 MAX_INT32，少了 1
        bool residual = false;
        
        // 调用预处理过程
        int pre_ans = this->pretreatment(positive, residual, dividend, divisor);
        if (pre_ans != MIN_INT32) {
            // 如果不等于正常约定值，则表示中途有返回值，直接返回该返回值即可
            return pre_ans;
        }
        
        // 如果被除数小于除数，商为 0，余数为被除数
        if (dividend < divisor) {
            return 0;
        }
        
        // 循环减法
        int res = 0;
        // 第一次操作单独处理，因为要决定第二次是否要补上被除数的缺失值
        if (dividend >= divisor) {
            dividend -= divisor;
            res ++;
        }
        if (residual && dividend < MAX_INT32) {
            dividend ++;
        }
        while (dividend >= divisor && res <= MAX_INT32) {
            dividend -= divisor;
            res ++;
        }
        
        // 根据符号输出结果
        if (positive) {
            return res;
        } else {
            return -res;
        }
    }
    
    // 方法一-优化。先用移位操作大致定位结果位置，再循环做减法。
    // 时间复杂度 O(lg(dividend / divisor))，空间复杂度 O(1)
    int solution2(int dividend, int divisor) {
        // 用于记录结果的符号，被除数与除数正负性的同或
        bool positive = true;
        // 如果被除数是 MIN_INT32 且除数不为 -1，那么需要正常做除法，但是把 MIN_INT32 取负号是溢出 int 的
        // 所以用 residual 来记录被除数为 MIN_INT32，它转为正数时会成为 MAX_INT32，少了 1
        bool residual = false;
        
        // 调用预处理过程
        int pre_ans = this->pretreatment(positive, residual, dividend, divisor);
        if (pre_ans != MIN_INT32) {
            // 如果不等于正常约定值，则表示中途有返回值，直接返回该返回值即可
            return pre_ans;
        }
        
        // 如果被除数小于除数，商为 0，余数为被除数
        if (dividend < divisor) {
            return 0;
        }
        
        // 循环减法
        int res = 0;
        // 第一次操作单独处理，因为要决定第二次是否要补上被除数的缺失值
        if (dividend >= divisor) {
            dividend -= divisor;
            res ++;
        }
        if (residual && dividend < MAX_INT32) {
            dividend ++;
        }
        
        // Core 核心部分：用移位操作来迅速定位商范围，指数级逼近！
        while (dividend >= divisor && res <= MAX_INT32) {
            int div_exp = divisor;
            int exp_count = 1;
            
            while (dividend >= div_exp && div_exp <= HALF_MAX_INT32) {
                div_exp <<= 1; // 移位 k 次，表示使用了 2^k 个 divisor
                exp_count <<= 1; // 使用了 2^k 个 divisor，商增加 2^k
            }
            
            // 跳出循环时，div_exp 多左移一次，才使得 dividend < div_exp，exp_count 也多左移了一次
            // 所以改变 dividend 和 res 前要将 div_exp 和 exp_count 右移一次
            dividend -= (div_exp >> 1);
            res += (exp_count >> 1);
        }
        
        // 根据符号输出结果
        if (positive) {
            return res;
        } else {
            return -res;
        }
    }
    
    // 预处理，记录结果的符号，并把被除数和除数的符号转为正数
    int pretreatment (bool& positive, bool& residual, int& dividend, int& divisor) {
        if (dividend > 0 && divisor < 0) {
            if (divisor == MIN_INT32) {
                // 如果被除数是 MIN_INT32，它不能直接取负号变为正数
                // 不过显然，任何 MAX_INT32 都小于 MIN_INT32 的绝对值，所以商为 0
                return 0;
            }
            // 正常取负号转换，把除数转为正数，没有缺失值
            divisor = -divisor;
            positive = false;
        } else if (dividend < 0 && divisor > 0) {
            if (dividend == MIN_INT32) {
                // 把被除数转为正数，记录缺失的 1
                dividend = MAX_INT32;
                residual = true;
            } else {
                // 正常取负号转换，把被除数转为正数，没有缺失值
                dividend = -dividend;
            }
            positive = false;
        } else if (dividend < 0 && divisor < 0) {
            if (dividend == MIN_INT32 && divisor == MIN_INT32) {
                // 最小除以最小，商为 1
                return 1;
            } else if (divisor == MIN_INT32) {
                // 被除数不是最小，但除数是最小，商为 0
                return 0;
            } else if (dividend == MIN_INT32) {
                // 把被除数转为正数，记录缺失的 1
                dividend = MAX_INT32;
                divisor = -divisor;
                residual = true;
            } else {
                // 正常取负号转换，把被除数和除数都转为正数，没有缺失值
                dividend = -dividend;
                divisor = -divisor;
            }
        }
        
        // 约定的正常返回值
        return MIN_INT32;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    int dividend = -10, divisor = -3; // 预期结果 3
//    int dividend = 7, divisor = -3; // 预期结果 -2
//    int dividend = -2147483648, divisor = -1; // 预期结果 MAX_INT32
//    int dividend = -2147483648, divisor = -2; // 预期结果 1073741824
//    int dividend = 2147483647, divisor = -2; // 预期结果 -1073741823
    int dividend = -2147483648, divisor = 2; // 预期结果 -1073741824
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->divide(dividend, divisor);
    if (ans != MAX_INT32) {
        cout << ans << endl;
    } else {
        cout << "Overflow." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
