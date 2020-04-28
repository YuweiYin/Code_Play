//
//  main.cpp
//  Prob1171_Excel_Sheet_Column_Number
//
//  Created by 阴昱为 on 2019/6/28.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//171. Excel Sheet Column Number
//
//Given a column title as appear in an Excel sheet, return its corresponding column number.
//给定一个Excel表格中的列名称，返回其相应的列序号。
//
//For example:
//    A -> 1
//    B -> 2
//    C -> 3
//    ...
//    Z -> 26
//    AA -> 27
//    AB -> 28
//    ...
//
//Example 1:
//    Input: "A"
//    Output: 1
//
//Example 2:
//    Input: "AB"
//    Output: 28
//
//Example 3:
//    Input: "ZY"
//    Output: 701


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
const int MAX_LIMIT = 0x7fffffff / 26;


class Solution {
private:
    // 也可以用循环来设置
//    map<char, int> dict = {
//        {'A', 1}, {'B', 2}, {'C', 3}, {'D', 4}, {'E', 5},
//        {'F', 6}, {'G', 7}, {'H', 8}, {'I', 9}, {'J', 10},
//        {'K', 11}, {'L', 12}, {'M', 13}, {'N', 14}, {'O', 15},
//        {'P', 16}, {'Q', 17}, {'R', 18}, {'S', 19}, {'T', 20},
//        {'U', 21}, {'V', 22}, {'W', 23}, {'X', 24}, {'Y', 25},
//        {'Z', 26}
//    };
    
public:
    int titleToNumber(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一：逐位转换，基数为 26。时间复杂度 O()，空间复杂度 O()。
    // Runtime: 4 ms, faster than 85.73% of C++ online submissions for Excel Sheet Column Number.
    // Memory Usage: 8.2 MB, less than 34.33% of C++ online submissions for Excel Sheet Column Number.
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 35.92% 的用户
    int solution1 (string s) {
        // 边界情况
        if (s.empty()) {
            return 0;
        }
        
        int s_len = (int)s.size();
        
        int res = 0;
        int base = 1;
        // const int radix = 26; // 基数
        for (int i = s_len - 1; i >= 0; i--) {
            // res += base * this->dict[s[i]];
            res += base * (s[i] - 'A' + 1);
            
            // 已可结束循环，不再累乘 base 了，减小溢出风险
            if (i <= 0) {
                break;
            }
            
            // 避免溢出风险
            if (base >= MAX_LIMIT) {
                break;
            }
            
            base = (base << 4) + (base << 3) + (base << 1); // base *= radix
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
//    string s = "A"; // 预期结果 1
//    string s = "AB"; // 预期结果 28
//    string s = "ZY"; // 预期结果 701
    string s = "CFDGSXM"; // 预期结果 1000000001 (1e10+1)
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans =solution->titleToNumber(s);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
