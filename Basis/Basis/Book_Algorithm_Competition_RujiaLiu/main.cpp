//
//  main.cpp
//  Book_Algorithm_Competition_RujiaLiu
//
//  Created by 阴昱为 on 2019/5/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
#include <time.h>
#include <iterator>
#include <algorithm>
using namespace std;

typedef long long ll;

// Greatest Common Divisor，辗转相除法、Euclid's Algorithm
// 求两数的最大公约数，如果为 1，表示两数互素
ll gcd (ll a, ll b) {
    // 如果上一轮 a % b == 0，即 b 整除 a，那么最大公约数就是 b。本轮 b == 0，执行 return a，即 return 上一轮的 b
    // 否则上一轮 a % b != 0，即 b 不能整除 a，那么本轮 b > 0，条件运算符执行 return gcd(b, a % b)，递归 gcd
    //    如果本轮 b 不能整除 a，那么 a % b != 0，下一轮的 b 仍然 > 0
    //    否则，本轮 a % b == 0，那么最大公约数就是本轮的 b。下一轮的 b == 0，返回下一轮的 a，也就是返回本轮的 b
    
    // cout << "a=" << a << "\tb=" << b << endl;
    
    return b ? gcd(b, a % b) : a;
    // return (b == 0) ? a : gcd(b, a % b);
}

int main(int argc, const char * argv[]) {
    
    clock_t start, finish;
    double prog_duration;
    
    start = clock();
    
    ll a = 1248, b = 832;
    ll gcd_ans = gcd(a, b);
    if (gcd_ans == 1) {
        cout << a << " 与 " << b << " 互素，最大公约数是 1" << endl;
    } else {
        cout << a << " 与 " << b << " 的最大公约数是 " << gcd_ans << endl;
    }
    
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
