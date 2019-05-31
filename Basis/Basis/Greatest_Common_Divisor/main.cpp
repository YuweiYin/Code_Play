//
//  main.cpp
//  Greatest_Common_Divisor
//
//  Created by 阴昱为 on 2019/5/31.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
#include <time.h>
#include <iterator>
#include <algorithm>
using namespace std;

typedef long long ll;

const ll MOD = 1e9+7;


// 快速幂并取模，注释略
template <typename T>
T powerMod(T base, T exp) {
    T res = 1;
    base %= MOD;
    assert(exp >= 0); // assert 宏的原型定义在 <assert.h> 中，其作用是如果它的条件返回错误，则终止程序执行
    while (exp) {
        if (exp & 1) {
            res = res * base % MOD;
        }
        base = base * base % MOD;
        exp >>= 1;
    }
    return res;
}


// Greatest Common Divisor，辗转相除法、Euclid's Algorithm
// 核心思路：递归执行 gcd(a, b) = gcd(b, a % b)，直到 b == 0时，a 为最大公约数
// 求两数的最大公约数，如果为 1，表示两数互素
template <typename T>
T gcd (T a, T b) {
    // 如果上一轮 a % b == 0，即 b 整除 a，那么最大公约数就是 b。本轮 b == 0，执行 return a，即 return 上一轮的 b
    // 否则上一轮 a % b != 0，即 b 不能整除 a，那么本轮 b > 0，条件运算符执行 return gcd(b, a % b)，递归 gcd
    //    如果本轮 b 不能整除 a，那么 a % b != 0，下一轮的 b 仍然 > 0
    //    否则，本轮 a % b == 0，那么最大公约数就是本轮的 b。下一轮的 b == 0，返回下一轮的 a，也就是返回本轮的 b
    
    // cout << "a=" << a << "\tb=" << b << endl;
    
    return b ? gcd(b, a % b) : a;
    // return (b == 0) ? a : gcd(b, a % b);
}


// Extend Euclidean Algorithm 扩展欧几里得算法
// 返回值为 gcd(a, b) 即 a 和 b 的最大公约数
// 当 gcd(a, b) == 1 时，x 是 a 在模 b 意义下的乘法逆元

// 思路：
// 若 gcd(a, b) == 1，那么 a 在模 b 意义下就存在逆元，即 a * a^(-1) = 1 (mod b)
// 设 x = a^(-1)，a * x = 1 (mod b) 可以转换为 a * x + b * y = 1，其中 y 是某整数
// 观察等式左边，a * x + b * y 这个形式就是求解最大公约数 gcd(a, b) 前的假设，
// 因此用辗转相除法求 gcd(a, b) 的过程就可以得到 x 和 y 的值。
// 而且若 gcd(a, b) == 1，x 就必然能求出来。（在孙子定理/中国剩余定理里，求逆元都能求得）

// 那么如何在辗转相除的过程中得到 x 和 y 的值呢？
// 设 x_i、y_i 表示辗转相除第 i 轮时的 x 和 y 的值，i 从 1 开始计。
// 观察辗转相除法的执行过程，发现它会一直先递归执行 gcd(a, b) = gcd(b, a % b)，
// 直到 b == 0时，返回最大公约数 a，设最高轮次为 k，
// 则此时等式 a * x_k + b * y_k 等于 a，故有 x_k == 1, y_k == 0
// 所以想要求得 x_1 和 y_1 的值，就要从 x_k 和 y_k 倒着求回来。

// 那么从 x_k、y_k 到 x_(k-1)、y_(k-1) 的递推关系是怎样的呢？
// 分析辗转相除法的核心等式 gcd(a, b) = gcd(b, a % b)，把等式左边看成第 k-1 轮，右边看出第 k 轮
// 则拆解得 a * x_(k-1) + b * y_(k-1) = b * x_k + (a % b) * y_k
// 等价替换 (a % b) 为 (a - (a/b)*b)，提醒：(a/b)得到的是 a 对 b 的倍数 下取整部分。
// 于是原式化为 a * x_(k-1) + b * y_(k-1) = b * x_k + (a - (a/b)*b) * y_k
// 整理等式右侧 a * x_(k-1) + b * y_(k-1) = a * y_k + b * (x_k - (a/b) * y_k)
// 由于 a 和 b 是常数，对比等式两侧，可得递推关系：x_(k-1) = y_k 和 y_(k-1) = x_k - (a/b) * y_k
template <typename T>
T ex_gcd (T a, T b, T &x, T &y) {
    if(b == 0) {
        // 辗转相除到头，得到最大公约数，返回之
        x = 1;
        y = 0;
        return a;
    } else {
        T r = ex_gcd(b, a % b, x, y);
        // 得到最大公约数之后，一路反向传递之
        
        // 往回传递最大公约数过程中，不断根据递推关系修改参数 x 和 y
        T t = x;
        x = y; // x_(k-1) = y_k
        y = t - a / b * y; // y_(k-1) = x_k - (a/b) * y_k
        
        // 回传最大公约数
        return r;
    }
}


int main(int argc, const char * argv[]) {
    // 计时
    clock_t start, finish;
    double prog_duration;
    start = clock();
    
    ll a = 832, b = 1247;
    ll x, y;
    
    // ll gcd_ans = gcd<ll>(a, b); // 调用欧几里得算法
    ll gcd_ans = ex_gcd<ll>(a, b, x, y); // 调用扩展欧几里得算法
    
    // 输出展示结果
    if (gcd_ans == 1) {
        cout << a << " 与 " << b << " 互素，最大公约数是 1" << endl;
        cout << a << " 在 MOD " << b << " 意义下的乘法逆元是 " << (x + b) % b << endl;
    } else {
        cout << a << " 与 " << b << " 的最大公约数是 " << gcd_ans << endl;
    }
    
    // 1247 在 MOD 832 意义下的乘法逆元是 415
    cout << 1247 * 415 % 832 << endl; // 1
    // 832 在 MOD 1247 意义下的乘法逆元是 625
    cout << 832 * 625 % 1247 << endl; // 1
    
    // 计时
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
