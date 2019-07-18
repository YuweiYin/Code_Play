//
//  main.cpp
//  Prob1367_Valid_Perfect_Square
//
//  Created by 阴昱为 on 2019/7/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//367. Valid Perfect Square
//
//Given a positive integer num, write a function which returns True if num is a perfect square else False.
//Note: Do not use any built-in library function such as sqrt.
//
//给定一个正整数 num，编写一个函数，如果 num 是一个完全平方数，则返回 True，否则返回 False。
//说明：不要使用任何内置的库函数，如 sqrt。
//
//Example 1:
//    Input: 16
//    Output: true
//
//Example 2:
//    Input: 14
//    Output: false


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    bool isPerfectSquare(int num) {
        return this->solution3(num);
    }
    
private:
    // 方法一：。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 85.71% 的用户
    // 内存消耗 : 8 MB , 在所有 C++ 提交中击败了 67.38% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Valid Perfect Square.
    // Memory Usage: 8.1 MB, less than 29.19% of C++ online submissions for Valid Perfect Square.
    bool solution1 (int num) {
        // 边界情况
        if (num <= 0) {
            return false;
        }
        
        // 如果 num 是完全平方数，那么它的正平方根的整数部分就是它的完全平方根
        int sqrt_num = this->mySqrtInt(num);
        
        return sqrt_num * sqrt_num == num;
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
    
    // 方法二：公式法
    // 1 + 3 + 5 + 7 + ... + (2n-1) = n^2，即完全平方数肯定是前 n 个连续奇数的和
    bool solution2 (int num) {
        if (num <= 0) {
            return false;
        }
        
        int i = 1;
        
        while (num > 0) {
            num -= i;
            i += 2;
        }
        
        return num == 0;
    }
    
    // 方法三：二分查找
    bool solution3 (int num) {
        if (num <= 0) {
            return false;
        }
        
        if (num == 1) {
            return true;
        }
        
        int low = 1, high = num >> 1;
        while (low < high) {
            int mid = low + ((high - low) >> 1);
            
            if (mid >= num / mid) { // mid * mid >= num
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        
        return (long)low * low == num;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int num = 12321; // 预期结果 true
//    int num = 12345; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isPerfectSquare(num);
    if (ans) {
        cout << num << " is a valid perfect square." << endl;
    } else {
        cout << num << " is NOT a valid perfect square." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
