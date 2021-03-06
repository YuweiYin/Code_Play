//
//  main.cpp
//  Prob1221_Maximal_Square
//
//  Created by 阴昱为 on 2019/6/23.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1221. Maximal Square
//
//Given a 2D binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.
//
//在一个由 0 和 1 组成的二维矩阵内，找到只包含 1 的最大正方形，并返回其面积。
//
//Example:
//    Input:
//        1 0 1 0 0
//        1 0 1 1 1
//        1 1 1 1 1
//        1 0 0 1 0
//    Output: 4


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
    int maximalSquare(vector<vector<char>>& matrix) {
        return this->solution2(matrix);
    }
    
private:
    // 方法一，动态规划。
    // 时间复杂度 O(MN)，空间复杂度 O(MN)
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 99.05% 的用户
    // 内存消耗 : 11.2 MB , 在所有 C++ 提交中击败了 56.36% 的用户
    // Runtime: 20 ms, faster than 88.30% of C++ online submissions for Maximal Square.
    // Memory Usage: 11 MB, less than 61.52% of C++ online submissions for Maximal Square.
    int solution1 (vector<vector<char>>& matrix) {
        if (matrix.empty()) {
            return 0;
        }
        
        int row_len = (int)matrix.size();
        int col_len = (int)matrix[0].size();
        
        for (int i = 1; i < row_len; i++) {
            // 确保矩阵是合法矩形：每一行的向量都不空，且长度相等。
            if (matrix[i].empty() || (int)matrix[i].size() != col_len) {
                return 0;
            }
        }
        
        int square_len = 0; // 最大正方形的边长
        
        // 初始化记录边长的二维矩阵
        vector<vector<int>> dp = vector<vector<int>>(row_len + 1, vector<int>(col_len + 1, 0));
        
        // 状态转移方程：dp(i, j) = min(dp(i-1, j), dp(i-1, j−1), dp(i, j−1)) + 1
        // 如：左侧、左上方、上方都是 '1'（它们各自至少能形成边长为 1 的正方形）
        // 假设他们的 dp 值都为 1，那么在本位置就能形成边长为 1+1=2 的正方形
        for (int i = 1; i <= row_len; i++) {
            for (int j = 1; j <= col_len; j++) {
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = min(min(dp[i][j - 1], dp[i - 1][j]), dp[i - 1][j - 1]) + 1;
                    
                    if (dp[i][j] > square_len) {
                        square_len = dp[i][j]; // 更新最大边长
                    }
                }
            }
        }
        
        // 返回最大正方形面积
        return square_len * square_len;
    }
    
    
    // 方法二，优化空间消耗的动态规划。
    // 时间复杂度 O(MN)，空间复杂度 O(N)
    // 执行用时 : 20 ms , 在所有 C++ 提交中击败了 94.09% 的用户
    // 内存消耗 : 10.6 MB , 在所有 C++ 提交中击败了 96.41% 的用户
    // Runtime: 20 ms, faster than 88.30% of C++ online submissions for Maximal Square.
    // Memory Usage: 10.4 MB, less than 95.66% of C++ online submissions for Maximal Square.
    int solution2 (vector<vector<char>>& matrix) {
        if (matrix.empty()) {
            return 0;
        }
        
        int row_len = (int)matrix.size();
        int col_len = (int)matrix[0].size();
        
        for (int i = 1; i < row_len; i++) {
            // 确保矩阵是合法矩形：每一行的向量都不空，且长度相等。
            if (matrix[i].empty() || (int)matrix[i].size() != col_len) {
                return 0;
            }
        }
        
        int square_len = 0; // 最大正方形的边长
        
        vector<int> dp = vector<int>(col_len + 1, 0); // 初始化记录边长的 dp 向量
        
        int prev = 0;
        
        // 状态转移方程：dp[j] = min(dp[j-1], dp[j], prev)
        //  prev      dp[j]   // 向右移动，下一轮的prev就是本轮的dp[j]
        // dp[j-1]  new_dp[j] // 下一轮的dp[j-1]就是本轮的new_dp[j]
        for (int i = 1; i <= row_len; i++) {
            for (int j = 1; j <= col_len; j++) {
                int temp = dp[j]; // 记录未修改的本轮 dp[j]
                
                if (matrix[i - 1][j - 1] == '1') {
                    // 遇到 '1'，查看左侧(dp[j-1])、上方(dp[j])、左上角(prev)
                    dp[j] = min(min(dp[j - 1], dp[j]), prev) + 1;
                    
                    if (dp[j] > square_len) {
                        square_len = dp[j]; // 更新最大边长
                    }
                } else {
                    dp[j] = 0; // 遇到 '0'，dp[j] 置零
                }
                
                prev = temp; // 记录本轮修改之前的 dp[j]
            }
        }
        
        // 返回最大正方形面积
        return square_len * square_len;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果 4
    vector<vector<char>> matrix = {
        {'1', '0', '1', '0', '0'},
        {'1', '0', '1', '1', '1'},
        {'1', '1', '1', '1', '1'},
        {'1', '0', '0', '1', '0'}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->maximalSquare(matrix);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
