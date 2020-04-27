//
//  main.cpp
//  Prob1066_Plus_One
//
//  Created by 阴昱为 on 2019/7/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//66. Plus One
//
//Given a non-empty array of digits representing a non-negative integer, plus one to the integer.
//The digits are stored such that the most significant digit is at the head of the list, and each element in the array contain a single digit.
//You may assume the integer does not contain any leading zero, except the number 0 itself.
//
//给定一个由整数组成的非空数组所表示的非负整数，在该数的基础上加一。
//最高位数字存放在数组的首位， 数组中每个元素只存储一个数字。
//你可以假设除了整数 0 之外，这个整数不会以零开头。
//
//Example 1:
//    Input: [1,2,3]
//    Output: [1,2,4]
//    Explanation: The array represents the integer 123.
//
//Example 2:
//    Input: [4,3,2,1]
//    Output: [4,3,2,2]
//    Explanation: The array represents the integer 4321.


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
    vector<int> plusOne(vector<int>& digits) {
        return this->solution1(digits);
    }
    
private:
    // 方法一：最低位加 1，进位则看更高一位。时间复杂度 O(N), 空间复杂度 O(1), N = digits.size
    // 本题只需加一，所以进不进位可以只看当前位是否为 9，可以简化 O(N) 中隐含的常数。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 92.11% 的用户
    // 内存消耗 : 8.5 MB , 在所有 C++ 提交中击败了 41.37% 的用户
    // Runtime: 4 ms, faster than 76.61% of C++ online submissions for Plus One.
    // Memory Usage: 8.6 MB, less than 38.36% of C++ online submissions for Plus One.
    vector<int> solution1 (vector<int>& digits) {
        // 边界条件
        if (digits.empty()) {
            return {1};
        }
        
        // 只需加一，无需反转数组
        int len = (int)digits.size();
        int cur_sum = 0;
        int carry = 0;
        
        // 最低位加 K
        cur_sum = digits[len - 1] + 1;
        
        // 计算第一次得到的进位
        if (cur_sum >= 10) {
            carry = cur_sum / 10;
            cur_sum %= 10;
        } else {
            carry = 0;
        }
        
        digits[len - 1] = cur_sum;
        
        // 若有进位，则继续往高位加
        int i = len - 2;
        while (carry > 0) {
            // 到 digits 的头部了，最多进一位
            if (i < 0) {
                digits.insert(digits.begin(), 1);
                break;
            }
            
            cur_sum = digits[i] + carry;
            
            if (cur_sum >= 10) {
                carry = cur_sum / 10;
                cur_sum %= 10;
            } else {
                carry = 0;
            }
            
            digits[i--] = cur_sum;
        }
        
        return digits;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> digits = {9, 9, 9, 9, 9, 9, 9, 9, 9, 9}; // 预期结果 10000000000
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->plusOne(digits);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        cout << "Answer is ";
        for (size_t i = 0; i < ans.size(); i++) {
            cout << ans[i];
        }
        cout << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
