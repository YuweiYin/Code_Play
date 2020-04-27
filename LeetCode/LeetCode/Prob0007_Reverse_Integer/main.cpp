//
//  main.cpp
//  Prob1007_Reverse_Integer
//
//  Created by 阴昱为 on 2019/6/1.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//7. Reverse Integer
//
//Given a 32-bit signed integer, reverse digits of an integer.
//给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
//
//Example1:
//  Input: 123
//  Output: 321
//
//Example2:
//  Input: -123
//  Output: -321
//
//Example3:
//  Input: 120
//  Output: 21
//Note:
//Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−231,  231 − 1]. For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows.
//注意:
//假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−2^31, 2^31 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。


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
#define ll long long

// 全局常量
//#define PI acos(-1.0)
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

const int MAX_INT32 = 0x7fffffff;
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


class Solution {
public:
    int reverse(int x) {
        return this->solution1(x);
    }
    
    // 方法一：时间复杂度 O(log_10(x)), 空间复杂度 O(1)
    // 在 res * 10 前判断当前 res 是否超过了 INT_MAX / 10（或 INT_MIN / 10）
    int solution1 (int x) {
        int res = 0;
        
        while (x != 0) {
            int pop = x % 10;
            x /= 10;
            
            if (res > INT_MAX / 10 || (res == INT_MAX / 10 && pop > 7)) {
                // 后半部分的判断，是因为最大值是 2147483647，如果当前 res 等于 INT_MAX / 10
                // 表示当前 res == 214748364，只剩末位需要判断，如果末位超过 7，那 res 乘 10 加末位就溢出了
                return 0;
            }
            if (res < INT_MIN / 10 || (res == INT_MIN / 10 && pop < -8)) {
                // 同理，后半部分的判断是因为最小负数为 -2147483648，需要将末位与 -8 相比判断
                return 0;
            }
            
            // 累积每一位
            res = res * 10 + pop;
        }
        
        return res;
    }
    
    // 用一个范围更大的 long long 型数来存储反转值，然后判断溢出
    // 这个方法不是完美满足题目要求，题目可能是假设机器至多存储 int32_t
    int solution2 (int x) {
        ll y = x;
        if (y == 0) {
            return 0;
        }
        
        // 除去末尾的 0
        while (y % 10 == 0) {
            y = (int)(y / 10);
        }
        
        // 记录正负符号，若为负 则转为正
        bool positive = true;
        if (y < 0) {
            y = -y;
            positive = false;
        }
        
        vector<int> y_list{};
        // 将数 y 的每一位（从低位到高位）加入向量
        while (y > 0) {
            int num = y % 10;
            y_list.push_back(num);
            y = (int)(y / 10);
        }
        
        // 判断溢出
        if ((int)y_list.size() > 10) {
            return 0;
        }
        
        ll res = 0;
        ll base = 1;
        // 从尾到头逆序累加
        for (vector<int>::iterator ite = y_list.end() - 1; ite >= y_list.begin(); ite--) {
            res += *ite * base;
            base *= 10;
        }
        
        // 根据符号输出结果
        if (positive) {
            // 判断溢出
            if (res > MAX_INT32) {
                return 0;
            } else {
                return (int)res;
            }
        } else {
            // 判断溢出
            if (-res < MIN_INT32) {
                return 0;
            } else {
                return (int)-res;
            }
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    int x = -15123;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->reverse(x) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
