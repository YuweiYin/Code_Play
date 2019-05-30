//
//  main.cpp
//  fast_factorial
//
//  Created by 阴昱为 on 2019/5/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
#include <time.h>
//#include <iterator>
//#include <algorithm>
using namespace std;


// 正整数的快速求幂 base^exp
unsigned long long int power(unsigned long base, unsigned long exp) {
    unsigned long long int result = 1;
    
    while (exp) {
        if (exp & 0x01) {
            result *= base;
        }
        base *= base;
        exp >>= 1;
    }
    
    return result;
}


// 快速求组合数 C(n,n/2)
unsigned long combine(unsigned long n) {
    // 因为 (2^n + 1)^m = C(m,0) + C(m,1) * 2^n + C(m,2) * (2^n)^2 + ... + C(m,m) * (2^n)^m
    // 若以 2^n 为基数，则可以将 (2^n + 1)^m 看成第 k 低位为 C(m,k) 的 2^n 进制数，k 取值从 0 到 m
    // 所以如果将 (2^n + 1)^m 右移 (2^n)^i 位，相当于将低位的 C(m,0)~C(m,i-1) 去掉，剩下最低位系数是 C(m,i)
    // 所以如果将 (2^n + 1)^n 右移 (2^n)^(n/2) 位，此时最低位系数就是 C(n,n/2)，基数是 2^n
    
    // 位运算速度优于乘除法（浮点数运算），因此用 1<<n（1左移n位）来计算 2^n（2的n次方）
    unsigned long x = (1 << n) + 1; // x 值为 2^n + 1
    unsigned long mask = (1 << n) - 1; // mask 掩码值为 2^n - 1，二进制值为n个1
    
    // 注意：power(x, n) 很有溢出风险！！！！！:(
    // power(x, n) 即 (2^n + 1)^n，而 >> ((n >> 1) * n)) 表示除以 2^(n*n/2)，即右移 (2^n)^(n/2)
    // 基数为 2^n，需转换：按位与 & mask 表示只取低二进制 n 位的数值，这就是系数 C(n,n/2) 的真实值
    return (power(x, n) >> ((n >> 1) * n)) & mask;
}


// 求阶乘
unsigned long fastFactorial(unsigned long n) {
    unsigned long temp;
    
    if (n == 1) {
        // n 值为 1
        return 1;
    } else if ((n & 0x01) == 1) {
        // n 末位为 1，奇数，往下普通递归
        return n * fastFactorial(n - 1);
    } else {
        // n 末位为 0，偶数，可以二分分治递归
        // 位运算优于乘除法（浮点数运算），因此用 n>>1 来计算 n/2
        temp = fastFactorial(n >> 1); // 二分分治法，temp 值为 n/2 的阶乘
        return combine(n) * temp * temp;
    }
}


int main(int argc, const char * argv[]) {
    
    clock_t start, finish;
    double prog_duration;
    
    start = clock();
    
    int number = 10;
    unsigned long result;
    
    result = fastFactorial(number);
    
//    result = 1;
//    for (int i = 2; i <= number; i++) {
//        result *= i;
//    }
    
    cout << number << "! = " << result << endl;
    
    finish = clock();
    prog_duration = (double)(finish - start) / CLOCKS_PER_SEC;
    
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
