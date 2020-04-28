//
//  main.cpp
//  Prob1258_Add_Digits
//
//  Created by 阴昱为 on 2019/7/1.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//258. Add Digits
//
//Given a non-negative integer num, repeatedly add all its digits until the result has only one digit.

//给定一个非负整数 num，反复将各个位上的数字相加，直到结果为一位数。
//
//Example:
//    Input: 38
//    Output: 2
//    Explanation: The process is like: 3 + 8 = 11, 1 + 1 = 2.
//    Since 2 has only one digit, return it.
//
//Follow up:
//    Could you do it without any loop/recursion in O(1) runtime?
//进阶:
//    你可以不使用循环或者递归，且在 O(1) 时间复杂度内解决这个问题吗？


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
    int addDigits(int num) {
        return this->solution1(num);
    }
    
private:
    // 方法一：找数学规律。时间复杂度 O(1)，空间复杂度 O(1)
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 95.24% 的用户
    // 内存消耗 : 8.3 MB , 在所有 C++ 提交中击败了 7.73% 的用户
    // Runtime: 4 ms, faster than 80.83% of C++ online submissions for Add Digits.
    // Memory Usage: 8.1 MB, less than 63.99% of C++ online submissions for Add Digits.
    int solution1 (int num) {
        // 边界情况
        if (num <= 0) {
            return num;
        }
        
        // 分析：对于四位数 num = 1000a + 100b + 10c + d，各位相加和为 sum1 = a + b + c + d
        // 差值 num - sum1 = 999a + 99b + 9c，显然差值总会是 9 的整倍数，所以最终结果是 num % 9
        if (num > 9) {
            // 在 num 大于 9 时做模运算处理
            num %= 9;
            
            if (num == 0) {
                num = 9; // 模运算后为 0，实则该为 9
            }
        }
        
        return num;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    int num = 38; // 预期结果 2
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans =solution->addDigits(num);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
