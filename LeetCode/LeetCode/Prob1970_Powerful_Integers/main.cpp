//
//  main.cpp
//  Prob1970_Powerful_Integers
//
//  Created by 阴昱为 on 2019/6/29.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//970. Powerful Integers
//
//Given two positive integers x and y, an integer is powerful if it is equal to x^i + y^j for some integers i >= 0 and j >= 0.
//Return a list of all powerful integers that have value less than or equal to bound.
//You may return the answer in any order.  In your answer, each value should occur at most once.

//给定两个正整数 x 和 y，如果某一整数等于 x^i + y^j，其中整数 i >= 0 且 j >= 0，那么我们认为该整数是一个强整数。
//返回值小于或等于 bound 的所有强整数组成的列表。
//你可以按任何顺序返回答案。在你的回答中，每个值最多出现一次。
//
//Example 1:
//    Input: x = 2, y = 3, bound = 10
//    Output: [2,3,4,5,7,9,10]
//    Explanation:
//    2 = 2^0 + 3^0
//    3 = 2^1 + 3^0
//    4 = 2^0 + 3^1
//    5 = 2^1 + 3^1
//    7 = 2^2 + 3^1
//    9 = 2^3 + 3^0
//    10 = 2^0 + 3^2
//
//Example 2:
//    Input: x = 3, y = 5, bound = 15
//    Output: [2,4,6,8,10,14]
//
//Note:
//    1 <= x <= 100
//    1 <= y <= 100
//    0 <= bound <= 10^6


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
const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    vector<int> powerfulIntegers(int x, int y, int bound) {
        return this->solution1(x, y, bound);
    }
    
private:
    // 方法一：暴力法，双循环，集合去重。时间复杂度 O(lg^2 N)，空间复杂度 O(lg^2 N)。N = bound
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 96.42% 的用户
    // 内存消耗 : 8.3 MB , 在所有 C++ 提交中击败了 90.35% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Powerful Integers.
    // Memory Usage: 8.5 MB, less than 49.01% of C++ online submissions for Powerful Integers.
    vector<int> solution1 (int x, int y, int bound) {
        // 边界情况
        if (x <= 0 || y <= 0 || bound < 0) {
            return {};
        }
        
        vector<int> res = {};
        
        // unordered_set 底层实现为 Hash Table
        // 数据插入和查找的时间复杂度很低，几乎是常数时间。代价是消耗比较多的内存、且无自动排序功能
        unordered_set<int> res_set = {};
        
        // set 底层实现为 RB-Tree
        // 具有自动排序的功能，因此 map 内部所有的数据，在任何时候，都是有序的
        // set<int> res_set = {};
        
        const int loop_limit = 20; // 19 < lg 1e6 < 20
        for (int i = 0; i < loop_limit; i++) {
            int power_x = this->power<int>(x, i);
            if (power_x > bound) {
                break; // 超过目标值，不必往后找了
            }
            
            for (int j = 0; j < loop_limit; j++) {
                int power_y = this->power<int>(y, j);
                if (power_y > bound) {
                    break; // 超过目标值，不必往后找了
                }
                
                int sum = power_x + power_y;
                if (sum <= bound) {
                    res_set.insert(sum); // 合法值加入集合
                }
            }
        }
        
        // 把集合中的元素分配给向量
        res.assign(res_set.begin(), res_set.end());
        return res;
    }
    
    // 正整数快速幂 base^exp
    // 思路: a^10 = a^(0b1010) = (a^1)^0 * (a^2)^1 * (a^4)^0 * (a^8)^1
    template <typename T1, typename T2, typename T3>
    T1 power(T2 base, T3 exp) {
        if (exp == 0 || base == 1) {
            return 1;
        }
        
        if (exp < 0) {
            return 0;
        }
        
        T1 res = 1;
        // 指数不为 0 则继续循环处理
        while (exp) {
            if (exp & 1) {
                // 若指数的当前二进制位为 1，则累乘到 res
                res = res * base;
            }
            
            // 累乘底数之前做乘法溢出判断
            if (exp == 1 || base > SQRT_MAX_INT32) {
                break;
            }
            
            // 累乘底数 a^k -> a^(2k) 也即 (a^k)^2
            base = base * base;
            
            // 指数右移一位
            exp >>= 1;
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    int x = 2, y = 3, bound = 10; // 预期结果 [2,3,4,5,7,9,10]
//    int x = 3, y = 5, bound = 15; // 预期结果 [2,4,6,8,10,14]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans =solution->powerfulIntegers(x, y, bound);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            cout << ans[i] << ", ";
        }
        cout << "End." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
