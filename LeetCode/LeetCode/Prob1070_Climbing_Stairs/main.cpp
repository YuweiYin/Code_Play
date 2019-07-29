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
    // 方法一。Fibonacci。时间复杂度 O(N)，空间复杂度 O(1)。N = n
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 75.90% 的用户
    // Runtime: 4 ms, faster than 58.74% of C++ online submissions for Climbing Stairs.
    // Memory Usage: 8 MB, less than 94.88% of C++ online submissions for Climbing Stairs.
    int solution1 (int n) {
        if (n <= 0) {
            return 0;
        }
        
        if (n == 1) {
            return 1;
        }
        
        int first = 1;
        int second = 2;
        
        for (int i = 3; i <= n; i++) {
            int third = first + second;
            first = second;
            second = third;
        }
        
        return second;
    }
    
    // 方法二。矩阵快速幂求 Fibonacci 数 - Binets 方法。时间复杂度 O(lg N)，空间复杂度 O(1)。N = n
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.4 MB , 在所有 C++ 提交中击败了 50.66% 的用户
    // Runtime: 4 ms, faster than 58.74% of C++ online submissions for Climbing Stairs.
    // Memory Usage: 8.5 MB, less than 18.65% of C++ online submissions for Climbing Stairs.
    int solution2 (int n) {
        if (n <= 0) {
            return 0;
        }
        
        if (n == 1) {
            return 1;
        }
        
        vector<vector<int>> q = {{1, 1}, {1, 0}};
        vector<vector<int>> res = this->fastPowerMatrix(q, n);
        
        return res[0][0];
    }
    
    // 矩阵快速幂 a^n
    vector<vector<int>> fastPowerMatrix(vector<vector<int>>& a, int n) {
        // 1 0
        // 0 1
        vector<vector<int>> res = {{1, 0}, {0, 1}};
        
        while (n > 0) {
            if ((n & 1) == 1) {
                res = this->multiplyMatrix(res, a);
            }
            
            n >>= 1;
            
            if (n <= 0) {
                break;
            }
            
            a = this->multiplyMatrix(a, a);
        }
        
        return res;
    }
    
    // 2*2 矩阵乘法 a*b
    vector<vector<int>> multiplyMatrix(vector<vector<int>>& a, vector<vector<int>>& b) {
        vector<vector<int>> product(2, vector<int>(2, 0));
        
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                product[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j];
            }
        }
        
        return product;
    }
    
    // 方法三。Fibonacci 公式。时间复杂度 O(lg N)，空间复杂度 O(1)。N = n
    // 但 n 较大时存在精度问题
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 78.41% 的用户
    // 内存消耗 : 8.1 MB , 在所有 C++ 提交中击败了 90.99% 的用户
    // Runtime: 4 ms, faster than 58.74% of C++ online submissions for Climbing Stairs.
    // Memory Usage: 8.4 MB, less than 50.51% of C++ online submissions for Climbing Stairs.
    int solution3 (int n) {
        if (n <= 0) {
            return 0;
        }
        
        if (n == 1) {
            return 1;
        }
        
        const double sqrt_5 = sqrt(5.0);
        double fibn = pow((1 + sqrt_5) / 2, n + 1) - pow((1 - sqrt_5) / 2, n + 1);
        
        return (int)(fibn / sqrt_5);
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int n = 30; // 预期结果 1346269
    
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
