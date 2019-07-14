//
//  main.cpp
//  Prob1989_Add_to_Array-Form_of_Integer
//
//  Created by 阴昱为 on 2019/7/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//989. Add to Array-Form of Integer
//
//For a non-negative integer X, the array-form of X is an array of its digits in left to right order.  For example, if X = 1231, then the array form is [1,2,3,1].
//Given the array-form A of a non-negative integer X, return the array-form of the integer X+K.
//
//对于非负整数 X 而言，X 的数组形式是每位数字按从左到右的顺序形成的数组。例如，如果 X = 1231，那么其数组形式为 [1,2,3,1]。
//给定非负整数 X 的数组形式 A，返回整数 X+K 的数组形式。
//
//Example 1:
//    Input: A = [1,2,0,0], K = 34
//    Output: [1,2,3,4]
//    Explanation: 1200 + 34 = 1234
//
//Example 2:
//    Input: A = [2,7,4], K = 181
//    Output: [4,5,5]
//    Explanation: 274 + 181 = 455
//
//Example 3:
//    Input: A = [2,1,5], K = 806
//    Output: [1,0,2,1]
//    Explanation: 215 + 806 = 1021
//
//Example 4:
//    Input: A = [9,9,9,9,9,9,9,9,9,9], K = 1
//    Output: [1,0,0,0,0,0,0,0,0,0,0]
//    Explanation: 9999999999 + 1 = 10000000000
//
//Note：
//    1 <= A.length <= 10000
//    0 <= A[i] <= 9
//    0 <= K <= 10000
//    If A.length > 1, then A[0] != 0
//
//提示：
//    1 <= A.length <= 10000
//    0 <= A[i] <= 9
//    0 <= K <= 10000
//    如果 A.length > 1，那么 A[0] != 0


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
    vector<int> addToArrayForm(vector<int>& A, int K) {
        return this->solution1(A, K);
    }
    
private:
    // 方法一：最低位加 K，进位则考虑下一位。时间复杂度 O(N), 空间复杂度 O(1), N = A.size
    // 执行用时 : 164 ms , 在所有 C++ 提交中击败了 93.54% 的用户
    // 内存消耗 : 12.2 MB , 在所有 C++ 提交中击败了 96.10% 的用户
    // Runtime: 108 ms, faster than 97.22% of C++ online submissions for Add to Array-Form of Integer.
    // Memory Usage: 12.3 MB, less than 81.45% of C++ online submissions for Add to Array-Form of Integer.
    vector<int> solution1 (vector<int>& A, int K) {
        // 边界条件
        if (A.empty()) {
            A = {0};
            this->addIntToArray(A, K);
            return A;
        }
        
        // 已知条件：A 只包含数字 0-9，且不以零开头（除非是数字 0 本身）
        if (K == 0) {
            return A;
        }
        
        // 反转 A，让低位在前
        reverse(A.begin(), A.end());
        
        // 字符串数字相加
        this->addIntToArray(A, K);
        
        // 反转结果串，让高位在前
        reverse(A.begin(), A.end());
        
        return A;
    }
    
    // 向量 A 加数字 K
    void addIntToArray (vector<int>& A, int K) {
        int cur_sum = 0;
        int carry = 0;
        
        // 最低位加 K
        cur_sum = A[0] + K;
        
        // 计算第一次得到的进位
        if (cur_sum >= 10) {
            carry = cur_sum / 10;
            cur_sum %= 10;
        } else {
            carry = 0;
        }
        
        A[0] = cur_sum;
        
        // 若有进位，则继续往高位加
        int i = 1;
        while (carry > 0) {
            // 到 A 的末尾了
            if (i >= A.size()) {
                A.push_back(0);
            }
            
            cur_sum = A[i] + carry;
            
            if (cur_sum >= 10) {
                carry = cur_sum / 10;
                cur_sum %= 10;
            } else {
                carry = 0;
            }
            
            A[i++] = cur_sum;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> A = {9, 9, 9, 9, 9, 9, 9, 9, 9, 9};
    int K = 9; // 预期结果 10000000008
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->addToArrayForm(A, K);
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
