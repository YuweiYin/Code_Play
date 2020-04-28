//
//  main.cpp
//  Prob1633_Sum_of_Square_Numbers
//
//  Created by 阴昱为 on 2019/7/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//633. Sum of Square Numbers
//
//Given a non-negative integer c, your task is to decide whether there're two integers a and b such that a^2 + b^2 = c.
//
//给定一个非负整数 c ，你要判断是否存在两个整数 a 和 b，使得 a^2 + b^2 = c。
//
//Example 1:
//    Input: 5
//    Output: True
//    Explanation: 1 * 1 + 2 * 2 = 5
//
//Example 2:
//    Input: 3
//    Output: False


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    bool judgeSquareSum(int c) {
        return this->solution1(c);
    }
    
private:
    // 方法一：对撞指针。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 95.46% 的用户
    // 内存消耗 : 8 MB , 在所有 C++ 提交中击败了 90.00% 的用户
    // Runtime: 4 ms, faster than 83.84% of C++ online submissions for Sum of Square Numbers.
    // Memory Usage: 8 MB, less than 79.65% of C++ online submissions for Sum of Square Numbers.
    bool solution1 (int num) {
        // 边界情况
        if (num < 0) {
            return false;
        }
        
        if (num <= 2) {
            return true;
        }
        
        bool res = false;
        int left = 0;
        int right = this->mySqrtInt(num);
        int left_square = left * left, right_square = right * right;
        int sum = left_square + right_square;
        int addition = 0;
        
        int overflow_limit = MAX_INT32 - sum; // 防止上溢出 int
        
        while (left <= right) {
            if (sum == num) {
                return true;
            } else if (sum < num) {
                // (n+1)^2 = n^2 + (2*n + 1)
                addition = (left << 1) + 1;
                if (addition > overflow_limit) {
                    return false; // overflow
                } else {
                    overflow_limit -= addition; // update overflow_limit
                }
                sum += addition;
                left ++;
            } else {
                // n^2 = (n+1)^2 - (2*n + 1)
                sum -= ((right - 1) << 1) + 1;
                right --;
            }
        }
        
        return res;
    }
    
    // 获得某整数的正平方根的整数部分
    int mySqrtInt(int x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            double res = 1; // 迭代计算平方根
            double last = 0; // 记录上一轮的计算值
            int max_loop = 100; // 设置最大迭代计算次数
            const double EPS = 1e-1; // 精度值
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            // 只返回整数部分
            return int(res);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    int c = 5; // 预期结果 true
//    int c = 3; // 预期结果 false
//    int c = 2147482647; // 预期结果 false
    int c = 1000; // 预期结果 true
//    int c = 15; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->judgeSquareSum(c);
    if (ans) {
        cout << c << " is a sum of square numbers." << endl;
    } else {
        cout << c << " is NOT a sum of square numbers." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
