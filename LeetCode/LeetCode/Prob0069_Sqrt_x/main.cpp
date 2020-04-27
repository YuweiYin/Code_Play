//
//  main.cpp
//  Prob1069_Sqrt_x
//
//  Created by 阴昱为 on 2019/7/17.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//69. Sqrt(x)
//
//Implement int sqrt(int x).
//Compute and return the square root of x, where x is guaranteed to be a non-negative integer.
//Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.
//
//实现 int sqrt(int x) 函数。
//计算并返回 x 的平方根，其中 x 是非负整数。
//由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。
//
//Example 1:
//    Input: 4
//    Output: 2
//
//Example 2:
//    Input: 8
//    Output: 2
//    Explanation: The square root of 8 is 2.82842..., and since
//    the decimal part is truncated, 2 is returned.


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


class Solution {
public:
    // 牛顿-拉弗森方法求解平方根。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 93.25% 的用户
    // 内存消耗 : 8 MB , 在所有 C++ 提交中击败了 91.71% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Sqrt(x).
    // Memory Usage: 8.1 MB, less than 79.27% of C++ online submissions for Sqrt(x).
    int mySqrt(int x) {
        return this->mySqrtInt(x);
    }
    
private:
    // 计算 double 型数的正平方根
    double mySqrtDouble(double x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            // 牛顿-拉弗森方法求解平方根，梯度下降 Gradient Descent
            // 要求 x = sqrt(n)，即求 f(x) = x^2 - k 的根。
            // 构造 x_n+1 = x_n + alpha * f(x_n)，如果 f(x) 收敛，
            // 那么通过迭代求解，能使 x_n 趋近于根，alpha 的绝对值越大，变化速度越快。
            
            // f(x) 收敛的充分条件：若 f 二阶可导，那么在待求的零点 x 周围存在一个区域，
            // 只要起始点 x_0 位于这个邻近区域内，那么牛顿-拉弗森方法必定收敛。
            // 可以证明，求平方根时使用的 f(x) = x^2 - k 是收敛的，
            // 梯度 grad = f'(x)，令 alpha = -1 / grad，有 x_n+1 = x_n - f(x_n) / f'(x_n)
            // 对于求平方根问题，f'(x_n) = 2 * x_n，所以 x_n+1 = x_n - (x_n^2 - k) / (2 * x_n)
            // 为了简化计算过程，等式化简为 x_n+1 = (x_n  + k / x_n) / 2
            
            // 梯度下降法的问题：梯度为 0 达到驻点、在根两边震荡、离根越来越远。
            // 不过在求平方根时不会有上述问题。
            
            double res = 1; // 迭代计算平方根 x_n+1
            double last = 0; // 记录上一轮的计算值 x_n
            int max_loop = 100; // 设置最大迭代计算次数
            const double EPS = 1e-10; // 精度值
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            return res;
        }
    }
    
    // 获得某整数的正平方根的整数部分
    int mySqrtInt(int x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            double res = 1; // 迭代计算平方根
            double last = 0; // 记录上一轮的计算值
            int max_loop = 100; // 设置最大迭代计算次数
            const double EPS = 1e-1; // 精度值
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            // 只返回整数部分
            return int(res);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int x = 4; // 预期结果 2
//    int x = 8; // 预期结果 2
//    int x = 0x7fffffff; // 预期结果 46340
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->mySqrt(x);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
