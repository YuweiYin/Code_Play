//
//  main.cpp
//  Prob1089_Gray_Code
//
//  Created by 阴昱为 on 2019/8/20.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//89. Gray Code
//
//The gray code is a binary numeral system where two successive values differ in only one bit.
//Given a non-negative integer n representing the total number of bits in the code, print the sequence of gray code. A gray code sequence must begin with 0.
//
//格雷编码是一个二进制数字系统，在该系统中，两个连续的数值仅有一个位数的差异。
//给定一个代表编码总位数的非负整数 n，打印其格雷编码序列。格雷编码序列必须以 0 开头。
//
//Example 1:
//    Input: 2
//    Output: [0,1,3,2]
//    Explanation:
//    00 - 0
//    01 - 1
//    11 - 3
//    10 - 2
//
//    For a given n, a gray code sequence may not be uniquely defined.
//    For example, [0,2,3,1] is also a valid gray code sequence.
//
//    00 - 0
//    10 - 2
//    11 - 3
//    01 - 1
//
//Example 2:
//    Input: 0
//    Output: [0]
//    Explanation: We define the gray code sequence to begin with 0.
//    A gray code sequence of n has size = 2n, which for n = 0 the size is 20 = 1.
//    Therefore, for n = 0 the gray code sequence is [0].


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


class Solution {
public:
    vector<int> grayCode(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一。。时间复杂度 O()，空间复杂度 O()。N =
    vector<int> solution1 (int n) {
        // 边界情况
        if (n < 0) {
            return {};
        }
        
        vector<int> res = {};
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    int n = 0; // 预期结果 [0]
    int n = 2; // 预期结果 [0,1,3,2]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->grayCode(n);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < ans.size(); i++) {
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
