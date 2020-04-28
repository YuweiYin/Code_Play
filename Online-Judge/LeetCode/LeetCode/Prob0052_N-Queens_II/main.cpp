//
//  main.cpp
//  Prob1052_N-Queens_II
//
//  Created by 阴昱为 on 2019/7/23.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//52. N-Queens II
//
//The n-queens puzzle is the problem of placing n queens on an n×n chessboard such that no two queens attack each other.
//Given an integer n, return the number of distinct solutions to the n-queens puzzle.
//
//n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。
//给定一个整数 n，返回 n 皇后不同的解决方案的数量。
//
//Example:
//    Input: 4
//    Output: 2
//    Explanation: There are two distinct solutions to the 4-queens puzzle as shown below.
//    [
//     [".Q..",  // Solution 1
//      "...Q",
//      "Q...",
//      "..Q."],
//
//     ["..Q.",  // Solution 2
//      "Q...",
//      "...Q",
//      ".Q.."]
//     ]


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
    int totalNQueens(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一：回溯法。时间复杂度 O(N!)，空间复杂度 O(N^2)。N = n
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 39.92% 的用户
    // 内存消耗 : 8.3 MB , 在所有 C++ 提交中击败了 50.79% 的用户
    // Runtime: 8 ms, faster than 38.80% of C++ online submissions for N-Queens II.
    // Memory Usage: 8.5 MB, less than 37.82% of C++ online submissions for N-Queens II.
    int solution1 (int& n) {
        // 边界情况
        if (n == 0) {
            return 1; // 根据 LeetCode 标准结果
        }
        
        if (n == 1) {
            return 1;
        }
        
        if (n <= 3) {
            return 0;
        }
        
        int res = 0;
        vector<string> queens(n, string(n, '.')); // 皇后 'Q'，可放置的点为 '.'，因第 i 行皇后而不能放置的点为 'i'
        
        this->backtrack(res, queens, n, 0);
        
        return res;
    }
    
    void backtrack (int& res, vector<string>& queens, int& n, int cur_n) {
        if (cur_n >= n) {
            res ++; // 本题无需构造解
            return;
        }
        
        for (int pos = 0; pos < n; pos++) {
            if (queens[cur_n][pos] == '.') {
                this->forward(queens, n, cur_n, pos);
                this->backtrack(res, queens, n, cur_n + 1);
                this->back(queens, n, cur_n, pos);
            }
        }
    }
    
    // O(N)
    void forward (vector<string>& queens, int n, int cur_n, int pos) {
        queens[cur_n][pos] = 'Q';
        char q_index = cur_n + '0';
        
        // 行
        for (int i = 0; i < n; i++) {
            if (queens[cur_n][i] == '.') {
                queens[cur_n][i] = q_index;
            }
        }
        
        // 列
        for (int i = 0; i < n; i++) {
            if (queens[i][pos] == '.') {
                queens[i][pos] = q_index;
            }
        }
        
        // 斜线(左上)
        for (int i = cur_n - 1, j = pos - 1; i >= 0 && j >= 0; i--, j--) {
            if (queens[i][j] == '.') {
                queens[i][j] = q_index;
            }
        }
        
        // 斜线(右下)
        for (int i = cur_n + 1, j = pos + 1; i < n && j < n; i++, j++) {
            if (queens[i][j] == '.') {
                queens[i][j] = q_index;
            }
        }
        
        // 斜线(左下)
        for (int i = cur_n + 1, j = pos - 1; i < n && j >= 0; i++, j--) {
            if (queens[i][j] == '.') {
                queens[i][j] = q_index;
            }
        }
        
        // 斜线(右上)
        for (int i = cur_n - 1, j = pos + 1; i >= 0 && j < n; i--, j++) {
            if (queens[i][j] == '.') {
                queens[i][j] = q_index;
            }
        }
    }
    
    // O(N)
    void back (vector<string>& queens, int n, int cur_n, int pos) {
        queens[cur_n][pos] = '.';
        char q_index = cur_n + '0'; // 只还原因自己而变化的那些不可用点
        
        // 行
        for (int i = 0; i < n; i++) {
            if (queens[cur_n][i] == q_index) {
                queens[cur_n][i] = '.';
            }
        }
        
        // 列
        for (int i = 0; i < n; i++) {
            if (queens[i][pos] == q_index) {
                queens[i][pos] = '.';
            }
        }
        
        // 斜线(左上)
        for (int i = cur_n - 1, j = pos - 1; i >= 0 && j >= 0; i--, j--) {
            if (queens[i][j] == q_index) {
                queens[i][j] = '.';
            }
        }
        
        // 斜线(右下)
        for (int i = cur_n + 1, j = pos + 1; i < n && j < n; i++, j++) {
            if (queens[i][j] == q_index) {
                queens[i][j] = '.';
            }
        }
        
        // 斜线(左下)
        for (int i = cur_n + 1, j = pos - 1; i < n && j >= 0; i++, j--) {
            if (queens[i][j] == q_index) {
                queens[i][j] = '.';
            }
        }
        
        // 斜线(右上)
        for (int i = cur_n - 1, j = pos + 1; i >= 0 && j < n; i--, j++) {
            if (queens[i][j] == q_index) {
                queens[i][j] = '.';
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
//    int n = 4; // 预期结果 2
    int n = 8; // 预期结果 92
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->totalNQueens(n);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
