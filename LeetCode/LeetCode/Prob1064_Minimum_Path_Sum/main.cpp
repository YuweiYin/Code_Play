//
//  main.cpp
//  Prob1064_Minimum_Path_Sum
//
//  Created by 阴昱为 on 2019/7/10.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//64. Minimum Path Sum
//
//Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the sum of all numbers along its path.
//Note: You can only move either down or right at any point in time.
//
//给定一个包含非负整数的 m x n 网格，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。
//说明：每次只能向下或者向右移动一步。
//
//Example:
//    Input:
//    [
//      [1,3,1],
//      [1,5,1],
//      [4,2,1]
//    ]
//    Output: 7
//    Explanation: Because the path 1→3→1→1→1 minimizes the sum.


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        return this->solution1(grid);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(M*N)，空间复杂度 O(M)。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 85.60% 的用户
    // 内存消耗 : 10.3 MB , 在所有 C++ 提交中击败了 98.52% 的用户
    // Runtime: 4 ms, faster than 99.54% of C++ online submissions for Minimum Path Sum.
    // Memory Usage: 10.3 MB, less than 100.00% of C++ online submissions for Minimum Path Sum.
    int solution1 (vector<vector<int>>& grid) {
        // 边界情况
        if (grid.empty() || grid[0].empty()) {
            return 0;
        }
        
        int row = (int)grid.size();
        int col = (int)grid[0].size();
        
        if (row == 1 && col == 1) {
            return grid[0][0];
        }
        
        // 另外，如果就地取材，在 grid 中进行 DP，则空间复杂度为 O(1)
        // 状态转移方程为 grid(i,j) = grid(i,j) + min(grid(i+1,j), grid(i,j+1))
        vector<int> dp(col, MAX_INT32);
        dp[0] = 0; // 初始位置
        
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                // 状态转移
                if (j == 0) {
                    // 在最左侧，没有 dp[j - 1]，只看上面路径累加本结点的代价
                    dp[j] = dp[j] + grid[i][j];
                } else {
                    // 从左边路径 dp[j - 1] 和上面路径 dp[j] 中挑较小代价者，并累加本结点的代价
                    dp[j] = min(dp[j - 1], dp[j]) + grid[i][j];
                }
            }
        }
        
        return dp[col - 1];
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<vector<int>> grid = {
        {1, 3, 1},
        {1, 5, 1},
        {4, 2, 1}
    }; // 预期结果 7 解释: 因为路径 1→3→1→1→1 的总和最小。
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->minPathSum(grid);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
