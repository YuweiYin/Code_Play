//
//  main.cpp
//  Prob1168_Excel_Sheet_Column_Title
//
//  Created by 阴昱为 on 2019/6/28.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//168. Excel Sheet Column Title
//
//Given a positive integer, return its corresponding column title as appear in an Excel sheet.
//给定一个正整数，返回它在 Excel 表中相对应的列名称。
//
//For example:
//    1 -> A
//    2 -> B
//    3 -> C
//    ...
//    26 -> Z
//    27 -> AA
//    28 -> AB
//    ...
//
//Example 1:
//    Input: 1
//    Output: "A"
//
//Example 2:
//    Input: 28
//    Output: "AB"
//
//Example 3:
//    Input: 701
//    Output: "ZY"


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
    string convertToTitle(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一：逐位转换，基数为 26。时间复杂度 O()，空间复杂度 O()。
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 6.50% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Excel Sheet Column Title.
    // Memory Usage: 8.1 MB, less than 53.98% of C++ online submissions for Excel Sheet Column Title.
    string solution1 (int n) {
        // 边界情况
        if (n <= 0) {
            return "";
        }
        
        string res = "";
        const int radix = 26; // 基数
        while (n > 0) {
            int cur_num = n % radix;
            
            if (cur_num == 0) { // 等于 0 表示该位应该为 Z
                res.insert(res.begin(), 'Z');
                n -= radix; // 由于 Z 不代表 0，而代表 26，所以要“夺取”更高位的一个 26
            } else {
                // res.insert(res.begin(), (char)(cur_num - 1 + 'A'));
                res.insert(res.begin(), (char)(cur_num + 64)); // 'A' ASCII 值为 65
            }
            
            n /= radix;
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
//    int n = 1; // 预期结果 "A"
//    int n = 28; // 预期结果 "AB"
//    int n = 52; // 预期结果 "AZ"
    int n = 701; // 预期结果 "ZY"
//    int n = 1000000001; // 预期结果 "CFDGSXM" (1e10+1)
//    int n = 2147483647; // 预期结果 "FXSHRXW"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans =solution->convertToTitle(n);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
