//
//  main.cpp
//  Prob6028_Armstrong_Number
//
//  Created by 阴昱为 on 2019/6/27.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//5028. Armstrong Number
//
//The k-digit number N is an Armstrong number if and only if the k-th power of each digit sums to N.
//Given a positive integer N, return true if and only if it is an Armstrong number.
//
//Example 1:
//    Input: 153
//    Output: true
//    Explanation:
//    153 is a 3-digit number, and 153 = 1^3 + 5^3 + 3^3.
//
//Example 2:
//    Input: 123
//    Output: false
//    Explanation:
//    123 is a 3-digit number, and 123 != 1^3 + 2^3 + 3^3 = 36.
//
//Note:
//    1 <= N <= 10^8
//
//Hint:
//    1. Check if the given k-digit number equals the sum of the k-th power of it's digits.
//    2. How to compute the sum of the k-th power of the digits of a number ? Can you divide the number into digits using division and modulus operations ?
//    3. You can find the least significant digit of a number by taking it modulus 10. And you can remove it by dividing the number by 10 (integer division). Once you have a digit, you can raise it to the power of k and add it to the sum.


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
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    bool isArmstrong(int N) {
        return this->solution1(N);
    }
    
private:
    // 方法一：直接拆数位判断。时间复杂度 O(log_10 N)，空间复杂度 O(1)。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    bool solution1 (int N) {
        // 边界情况
        if (N < 0) {
            return false;
        }
        
        if (N == 0) {
            return true;
        }
        
        int N_copy = N;
        
        int exp = 0;
        while (N > 0) {
            N /= 10;
            exp ++; // 计算位数
        }
        
        N = N_copy;
        int count = 0;
        while (N > 0) {
            int num = N % 10;
            
            // 累加各位数字的 exp 次幂
            count += this->power<int>(num, exp);
            if (count > N_copy) {
                return false;
            }
            
            N /= 10;
        }
        
        return count == N_copy;
    }
    
    
    // 正整数快速幂 base^exp
    // 思路: a^10 = a^(0b1010) = (a^1)^0 * (a^2)^1 * (a^4)^0 * (a^8)^1
    template <typename T1, typename T2, typename T3>
    T1 power(T2 base, T3 exp) {
        T1 res = 1;
        if (exp == 0) {
            return 1;
        }
        
        if (exp < 0) {
            return 0;
        }
        
        if (base == 1 || base == 0) {
            return base;
        }
        
        // 指数不为 0 则继续循环处理
        while (exp) {
            if (exp & 1) {
                // 若指数的当前二进制位为 1，则累乘到 res
                res = res * base;
            }
            
            // 累乘底数之前做乘法溢出判断
            if (exp == 1 || base > SQRT_MAX_INT32) {
                break;
            }
            
            // 累乘底数 a^k -> a^(2k) 也即 (a^k)^2
            base = base * base;
            
            // 指数右移一位
            exp >>= 1;
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
    int N = 153; // 预期结果 true
//    int N = 121; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans =solution->isArmstrong(N);
    if (ans) {
        cout << N << " is Armstrong Number." << endl;
    } else {
        cout << N << " is NOT Armstrong Number." << endl;
    }
    
    
    //    int count = 1;
    //    sort(A.begin(), A.end());
    //    while (next_permutation(A.begin(), A.end())) {
    //        count ++;
    //    }
    //    cout << "count = " << count << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
