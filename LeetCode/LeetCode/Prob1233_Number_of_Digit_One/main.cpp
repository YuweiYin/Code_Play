//
//  main.cpp
//  Prob1233_Number_of_Digit_One
//
//  Created by 阴昱为 on 2019/7/15.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//233. Number of Digit One
//
//Given an integer n, count the total number of digit 1 appearing in all non-negative integers less than or equal to n.
//
//给定一个整数 n，计算所有小于等于 n 的非负整数中数字 1 出现的个数。
//
//Example:
//    Input: 13
//    Output: 6
//    Explanation: Digit 1 occurred in the following numbers: 1, 10, 11, 12, 13.


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
    int countDigitOne(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一：找规律。时间复杂度 O(log_10 n), 空间复杂度 O(log_10 n), N = n
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.3 MB , 在所有 C++ 提交中击败了 15.69% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Number of Digit One.
    // Memory Usage: 8.2 MB, less than 66.88% of C++ online submissions for Number of Digit One.
    int solution1 (int& n) {
        // 边界条件
        if (n < 1) {
            return 0;
        }
        
        // 规律：0~9 有 1 个，10~19 有 10+1 个，20~99 有 8*1 个。
        // 所以 0~99 有 20 个，100~199 有 100+20 个，200~999 有 8*20 个。
        // 所以 0~999 有 300 个，1000~1999 有 1000+300 个，2000~9999 有 8*300 个。
        int res = 0;
        int count = 0;
        int base = 1;
        
        vector<int> n_vec = {};
        vector<int> base_vec = {0};
        
        int num = n;
        while (num > 0) {
            n_vec.insert(n_vec.begin(), num % 10);
            num /= 10;
            
            if (num <= 0) {
                break;
            }
            
            count += 1;
            base_vec.insert(base_vec.begin(), count * base); // 反序 0, 1, 20, 300, 4000, 50000...
            base *= 10;
        }
        
//        for (int i = 0; i < base_vec.size(); i++) {
//            cout << base_vec[i] << ", ";
//        }
//        cout << "End." << endl;
//
//        for (int i = 0; i < n_vec.size(); i++) {
//            cout << n_vec[i] << ", ";
//        }
//        cout << "End." << endl;
        
        num = n;
        for (int i = 0; i < n_vec.size(); i++, base /= 10) {
            if (n_vec[i] == 0) {
                // 0 * base_vec[i]
                continue;
            } else if (n_vec[i] == 1) {
                // 1 * base_vec[i] + 千位 1 对后面数字的增益
                // 例如：n=1789，在看千位时，除了 1 * 300 外，还要把 1000~1789 的千位 1 扣除下来
                // 这样计算后面的数时就不用管前面的 1 了
                res += base_vec[i] + num % base + 1;
            } else {
                // n_vec[i] * base_vec[i] + base 此时 base 就代表了所有千位 1 的增益
                // 例如：n=6789，在看千位时，除了 1 * 300 外，还要把 1000~1789 的千位 1 扣除下来
                res += n_vec[i] * base_vec[i] + base;
            }
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
//    int n = 999; // 预期结果 300
//    int n = 6789; // 预期结果 3059
//    int n = 1789; // 预期结果 1349
    int n = 17089; // 预期结果 14209
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->countDigitOne(n);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
