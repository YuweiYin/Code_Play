//
//  main.cpp
//  Euler_Function
//
//  Created by 阴昱为 on 2019/5/31.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
#include <time.h>
#include <iterator>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;

//const ll MOD = 1e9+7;


// 普通方法求解欧拉函数值
// 欧拉函数 Alpha(n) 表示比 n 小、且与 n 互素的正整数，包含 1。
// 利用素数幂分解的性质，时间复杂度为 O(n*sqrt(n))
// 正整数 n 可以被分解为 n = p_1^q_1 * p_2^q_2 * ... * p_k^q_k，其中 p_i 都是素数。
// 欧拉函数值为 Alpha(n) = n * (1 - 1 / p_1) * (1 - 1 / p_2) * ... * (1 - 1 / p_k)
template <typename T>
T euler (T n) {
    T res = n, a = n;
    
    for (T i = 2; i * i <= a; i++) {
        if (a % i == 0) {
            // 先进行除法是为了防止中间数据的溢出
            // 结果累乘
            res = res / i * (i - 1);
            
            // 每个素数幂分解的素数 i 只在 Alpha(n) 里体现一次
            while(a % i == 0) {
                a /= i;
            }
        }
    }
    
    // 此时如果 a == 1，表示在 while(a % i == 0) {a /= i;} 时 a 被除尽了
    // 那么素数幂分解就到此为止了。否则，就还剩一个素数 p_k 没被计算在内
    if(a > 1) {
        res = res / a * (a - 1);
    }
    
    return res;
}


// 线性筛法求小于 m 的素数，并求 1~m 各个数的欧拉函数值，时间复杂度为 O(n*sqrt(m))
// 先筛出 n 以内的所有素数，再以素数筛每个数的欧拉函数值。
// 从 2 开始循环，把 2 的倍数的 φ 值 *(1-1/2)，则 φ[2]=2*1/2=1, φ[4]=4*1/2=2, φ[6]=6*1/2=3 等等
// 再是 3，把 3 的倍数的 φ 值 *(1-1/3)，则 φ[3]=3*2/3=2, φ[6]=3*2/3=2, φ[9]=9*2/3=6 等等
// 再5，再7...因为对每个素数都进行如此操作，因此每个 n 都进行了 φ(n)=n*（1-1/p_1)(1-1/p_2)....(1-1/p_k) 运算
template <typename T>
T* linearSievePrime (T m) {
    T euler[m + 1]; // euler[i] 存储 i 的欧拉函数值
    
    // 赋初值 euler[i] = i
    euler[1] = 1;
    for (int i = 2; i < m; i++) {
        euler[i] = (T)i;
    }
    
    // 遍历一遍，打表获得正整数 2 ~ MAX 的欧拉函数值
    for (int i = 2; i < m; i++) {
        if (euler[i] == (T)i) {
            for(int j = i; j < m; j += i) {
                // 先进行除法是为了防止中间数据的溢出
                euler[j] = euler[j] / (T)i * (T)(i - 1);
            }
        }
    }
    
    return euler;
}


// 在筛素数的同时求出所有数的欧拉函数值
// 既可以求出小于 m 的素数（prime 数组），也可以求出 1 ~ m-1 的欧拉函数的值（euler 数组）
template <typename T>
int linearSievePrimeEuler (T m, T* euler, T* prime, T* vis) {
    int count = 0; // 记录当前 prime 数组中共存储了多少个素数
    // T euler[m + 1]; // euler[i] 存储数 i 的欧拉函数值
    // T prime[m + 1]; // prime[i] 存储第 i 个素数的值，从 prime[0]=2 开始
    // T vis[m + 1]; // vis[i] 表示数 i 是否是合数，1 表示是合数，0 表示是素数
    
    for (int i = 2; i < m; i++) {
        // 如果数 i 是素数，则进行素数的处理
        if (vis[i] == 0) {
            prime[count++] = i; // 存储素数
            euler[i] = i - 1; // 计算欧拉函数值，如果 i 是素数，那么前面 i-1 个数都与它互素，φ(n)=n-1
        }
        
        // 线性筛法：将已经得到的各个素数乘以 i，处理得到的这些数（这些都是合数）
        for (int j = 0; j < count && i * prime[j] < m; j++) {
            // 将 prime[j] 各正整数倍数的 vis 数组值都计为 1，表示它们不是素数
            vis[i * prime[j]] = 1;
            
            if (i % prime[j] == 0) {
                // 此时，i 被 prime[j] 整除，记 i = k * prime[j]
                // 由欧拉函数的性质：φ(kp * p) = φ(kp) * p
                euler[i * prime[j]] = euler[i] * prime[j];
                break; // 防止重复计算，线性的根本
            } else {
                // 此时，i 不被 prime[j] 整除，而 prime[j] 又是素数，所以二者互素
                // 由欧拉函数的积性，若 gcd(a,b)=1，则 φ(a * b) = φ(a) * φ(b)
                euler[i * prime[j]] = euler[i] * euler[prime[j]];
            }
        }
    }
    
    return 0;
}


int main(int argc, const char * argv[]) {
    // 计时
    clock_t start, finish;
    double prog_duration;
    start = clock();
    
    // 普通方法求 euler_n 的欧拉函数值 φ(euler_n)
    ll euler_n = 15;
    ll euler_res = euler<ll>(euler_n);
    cout << euler_n << " 的欧拉函数值为 " << euler_res << endl;
    
    // 线性筛法求 1 ~ m-1 各个数的欧拉函数值
    int m = 18;
    ll euler[m + 1]; // euler[i] 存储 i 的欧拉函数值
    ll prime[m + 1]; // prime[i] 存储 i 的欧拉函数值
    ll vis[m + 1]; // vis[i] 存储 i 的欧拉函数值
    for (int i = 0; i <= m; i++) {
        euler[i] = i;
        prime[i] = 0;
        vis[i] = 0;
    }
    linearSievePrimeEuler<ll>(m, euler, prime, vis);
    for (int i = 0; i < m; i++) {
        cout << "euler[" << i << "]=" << euler[i];
        cout << "\tprime[" << i << "]=" << prime[i];
        cout << "\tvis[" << i << "]=" << vis[i] << endl;
    }
    
    // 计时
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
