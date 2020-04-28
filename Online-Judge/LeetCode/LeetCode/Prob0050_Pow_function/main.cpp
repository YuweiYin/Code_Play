//
//  main.cpp
//  Prob1050_Pow_function
//
//  Created by 阴昱为 on 2019/6/25.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//50. Pow(x, n)
//
//Implement pow(x, n), which calculates x raised to the power n (x^n).
//
//实现 pow(x, n) ，即计算 x 的 n 次幂函数。
//
//Example 1:
//    Input: 2.00000, 10
//    Output: 1024.00000
//
//Example 2:
//    Input: 2.10000, 3
//    Output: 9.26100
//
//Example 3:
//    Input: 2.00000, -2
//    Output: 0.25000
//    Explanation: 2-2 = 1/22 = 1/4 = 0.25
//
//Note:
//    -100.0 < x < 100.0
//    n is a 32-bit signed integer, within the range [−231, 231 − 1]


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
const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

const int MAX_INT32 = 0x7fffffff;
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    double myPow(double x, int n) {
        return this->solution1(x, n);
    }
    
private:
    // 方法一：快速幂（双精度数 ^ 整数）。时间复杂度 O(lg N)，空间复杂度 O(1)
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.3 MB , 在所有 C++ 提交中击败了 82.23% 的用户
    // Runtime: 4 ms, faster than 81.60% of C++ online submissions for Pow(x, n).
    // Memory Usage: 8.2 MB, less than 91.23% of C++ online submissions for Pow(x, n).
    double solution1 (double x, int n) {
        if (n == 0) {
            return 1; // 指数为 0
        }
        
        if (fabs(x - 0.0) < EPS) {
            return 0;  // 底数为 0
        }
        
        if (fabs(x - 1.0) < EPS) {
            return 1.0;  // 底数为 1.0
        }
        
        if (fabs(x + 1.0) < EPS) {
            // 底数为 -1.0
            if (n % 2 == 0) {
                return 0 - x; // -1.0 的偶数次方为 1.0
            } else {
                return x; // -1.0 的奇数次方为 -1.0
            }
        }
        
        // 指数小于零
        bool rest_negative_exp = false; // 如果为真，表示最终还需要乘一次底数
        if (n < 0) {
            x = 1 / x; // 底数取倒数
            // 指数取反，但注意如果 n 原本为 MIN_INT32
            // 那么不能直接取反，因为会溢出
            if (n <= MIN_INT32) {
                rest_negative_exp = true;
                n = MAX_INT32;
            } else {
                n = 0 - n;
            }
        }
        
        double res = 1.0;
        
        // 指数不为 0 则继续循环处理
        while (n) {
            if (n & 1) {
                // 若指数的当前二进制位为 1，则累乘到 res
                res = res * x;
            }
            
            // 累乘底数之前做乘法溢出判断
            if (n == 1 || x > SQRT_MAX_INT32) {
                break;
            }
            
            // 累乘底数 a^k -> a^(2k) 也即 (a^k)^2
            x = x * x;
            
            // 指数右移一位
            n >>= 1;
        }
        
        if (rest_negative_exp) {
            res *= x;
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    double x = 2.00000, n = 10; // 预期结果 1024.00000
//    double x = 2.10000, n = 3; // 预期结果 9.26100
//    double x = 2.00000, n = -2; // 预期结果 0.25000
    double x = -1.00000, n = -2147483648; // 预期结果 1.0
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    double ans = solution->myPow(x, n);
    cout << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
