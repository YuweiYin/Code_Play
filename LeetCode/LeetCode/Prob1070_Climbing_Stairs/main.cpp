//
//  main.cpp
//  Prob1070_Climbing_Stairs
//
//  Created by 阴昱为 on 2019/7/28.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//70. Climbing Stairs
//
//You are climbing a stair case. It takes n steps to reach to the top.
//Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
//
//Note: Given n will be a positive integer.
//
//假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
//每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
//
//注意：给定 n 是一个正整数。
//
//Example 1:
//    Input: 2
//    Output: 2
//    Explanation: There are two ways to climb to the top.
//        1. 1 step + 1 step
//        2. 2 steps
//
//Example 2:
//    Input: 3
//    Output: 3
//    Explanation: There are three ways to climb to the top.
//        1. 1 step + 1 step + 1 step
//        2. 1 step + 2 steps
//        3. 2 steps + 1 step


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
public:
    int climbStairs(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一。Partition 分配函数。时间复杂度 O()，空间复杂度 O()。N = n
    int solution1(int n) {
        if (n <= 0) {
            return 0;
        }
        
        int res = 0;
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int n = 3; // 预期结果 3
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->climbStairs(n);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
