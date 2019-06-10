//
//  main.cpp
//  Draw_Cards
//
//  Created by 阴昱为 on 2019/6/10.
//  Copyright © 2019 阴昱为. All rights reserved.
//


// 题目描述：
// 抽卡游戏，规则如下：每次抽卡抽中橙卡的概率是 1/4，
// 如果连续 3 次没有抽中橙卡，那么第 4 次一定会抽中橙卡。
// 请问：抽 100 次卡，抽中橙卡的张数的数学期望是多少？
// 另外，能否给出解析解？

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


class Solution {
private:
    map<int, double> dp = {};

public:
    Solution () {
        this->dp = {};
    }
    
    double drawCardsSolution (int n) {
        if (this->dp.find(n) != this->dp.end()) {
            return this->dp[n];
        }
        
        for (int i = (int)dp.size(); i <= n; i++) {
            this->dp.insert({i, this->drawCards(i)});
        }
        
//        for (int i = 0; i <= n; i++) {
//            cout << i << ": " << this->dp[i] << endl;
//        }
        
        return this->dp[n];
    }

private:
    double drawCards (int n) {
        if (this->dp.find(n) != this->dp.end()) {
            return this->dp[n];
        }
        
        if (n >= 4) {
            return (1 + drawCards(n - 4)) / 64 * 27 +
            (1 + drawCards(n - 3)) / 64 * 9 +
            (1 + drawCards(n - 2)) / 16 * 3 +
            (1 + drawCards(n - 1)) / 4;
        } else if (n == 3) {
            return (1 + drawCards(n - 3)) / 64 * 9 +
            (1 + drawCards(n - 2)) / 16 * 3 +
            (1 + drawCards(n - 1)) / 4;
        } else if (n == 2) {
            return (1 + drawCards(n - 2)) / 16 * 3 +
            (1 + drawCards(n - 1)) / 4;
        } else if (n == 1) {
            return (1 + drawCards(n - 1)) / 4;
        } else {
            return 0;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    clock_t start, finish;
    double prog_duration;
    start = clock();
    
    int n = 100;
    
    Solution* solution = new Solution();
    
    cout << solution->drawCardsSolution(n) << endl;
//    cout << solution->drawCardsSolution(n - 1) << endl;
//    cout << solution->drawCardsSolution(n + 2) << endl;
//    cout << solution->drawCardsSolution(2 * n) << endl;
    
    // 计时
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
