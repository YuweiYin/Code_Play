//
//  main.cpp
//  Prob1172_Factorial_Trailing_Zeroes
//
//  Created by 阴昱为 on 2019/7/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//172. Factorial Trailing Zeroes
//
//Given an integer n, return the number of trailing zeroes in n!.
//
//给定一个整数 n，返回 n! 结果尾数中零的数量。
//
//Example 1:
//    Input: 3
//    Output: 0
//    Explanation: 3! = 6, no trailing zero.
//
//Example 2:
//    Input: 5
//    Output: 1
//    Explanation: 5! = 120, one trailing zero.
//
//Note: Your solution should be in logarithmic time complexity.
//说明: 你算法的时间复杂度应为 O(log n) 。


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
//const int MOD = 1000000007; // 1e9+7 与 1e9+9 为孪生素数

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    int trailingZeroes(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一：找规律。时间复杂度 O(log_5 N), 空间复杂度 O(1), N = n
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 87.53% 的用户
    // 内存消耗 : 8.1 MB , 在所有 C++ 提交中击败了 84.59% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Factorial Trailing Zeroes.
    // Memory Usage: 8.1 MB, less than 76.78% of C++ online submissions for Factorial Trailing Zeroes.
    int solution1 (int& n) {
        // 边界条件
        if (n < 5) {
            return 0;
        }
        
        // 规律：5^1 的整倍数贡献 1 个 5，即贡献 10（2 的倍数很多）
        // 5^2 的整倍数贡献 2 个 5。考虑重复情况，则是 5^2 在 5^1 的贡献基础上额外贡献一个 5
        // 例：n = 101, res = (int)(101/5) + (int)(101/25) + (int)(101/125)  = 24
        int res = 0;
        
        do {
            n /= 5;
            res += n;
        } while (n > 0);
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int n = 101; // 预期结果 24
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->trailingZeroes(n);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
