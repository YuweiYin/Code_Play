//
//  main.cpp
//  Prob1063_Unique_Paths_II
//
//  Created by 阴昱为 on 2019/7/4.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//63. Unique Paths II
//
//A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).
//The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).
//Now consider if some obstacles are added to the grids. How many unique paths would there be?
//
//一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为“Start” ）。
//机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。
//现在考虑网格中有障碍物。那么从左上角到右下角将会有多少条不同的路径？
//
//An obstacle and empty space is marked as 1 and 0 respectively in the grid.
//网格中的障碍物和空位置分别用 1 和 0 来表示。
//
//Note: m and n will be at most 100.
//说明：m 和 n 的值均不超过 100。
//
//Example 1:
//    Input:
//    [
//      [0,0,0],
//      [0,1,0],
//      [0,0,0]
//    ]
//    Output: 2
//    Explanation:
//    There is one obstacle in the middle of the 3x3 grid above.
//    There are two ways to reach the bottom-right corner:
//        1. Right -> Right -> Down -> Down
//        2. Down -> Down -> Right -> Right


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
#define ull unsigned long long

// 全局常量
//#define PI acos(-1.0)
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
const ull MAX_INT32 = 2147483647;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        return this->solution2(obstacleGrid);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(M*N)，空间复杂度 O(N)。
    int solution1 (vector<vector<int>>& obstacleGrid) {
        // 边界情况
        if (obstacleGrid.empty()) {
            return 0;
        }
        
        if (obstacleGrid[0].empty()) {
            return 0;
        }
        
        // 如果首元素就是障碍，那么不会有任何可行路径
        if (obstacleGrid[0][0] == 1) {
            return 0;
        }
        
        int row = (int)obstacleGrid.size();
        int col = (int)obstacleGrid[0].size();
        
        // 如果只有一行，就看这行里面有没有障碍，有则 0，无则 1
        if (row == 1) {
            for (int j = 0; j < col; j++) {
                if (obstacleGrid[0][j] == 1) {
                    return 0;
                }
            }
            return 1;
        }
        
        // 如果只有一列，就看这列里面有没有障碍，有则 0，无则 1
        if (col == 1) {
            for (int i = 0; i < row; i++) {
                if (obstacleGrid[i][0] == 1) {
                    return 0;
                }
            }
            return 1;
        }
        
        // 令 dp[i][j] 是到达 i, j 的不同路径数量
        // 状态转移方程：dp[i][j] = dp[i-1][j] + dp[i][j-1]
        // 初始化 dp[i][0] 均为 1，dp[0][j] 均为 1，运行表格如下：
        // 1  1  1
        // 1  0  1 // 注意，中间为障碍物，遇到障碍物就要归零
        // 1  1  2
        // 优化：简化为一维 DP，状态转移方程为 dp[j] = dp[j] + dp[j-1]
        // 即：本轮新的 dp[j] = 上一轮 dp[j] + 本轮新的 dp[j-1]
        // 与之前的 dp[i][j] = dp[i-1][j] + dp[i][j-1] 效果相同，节约了存储空间
        
        // 在 LeetCode 测试用例 21 时，执行会出现 int 的溢出异常signed integer overflow:
        // 1605659841 + 1070439894 cannot be represented in type 'int' 所以改为 ull 类型
        vector<ull> dp = vector<ull>(col, 1);
        
        // 给 dp[0][j] 即 dp[j] 赋初值
        for (int j = 0; j < col; j++) {
            // 遇到障碍，则之后均为 0
            if (obstacleGrid[0][j] == 1) {
                while (j < col) {
                    dp[j++] = 0;
                }
                break;
            }
        }
        
        // 从坐标 (1,1) 开始执行状态转移方程
        for (int i = 1; i < row; i++) {
            for (int j = 1; j < col; j++) {
                if (obstacleGrid[i][j] == 1) {
                    // 遇到障碍则将此处 dp 值置零
                    dp[j] = 0;
                } else {
                    // 否则继续执行状态转移方程
                    dp[j] += dp[j - 1];
                }
            }
        }
        
        if (dp[col - 1] > MAX_INT32) {
            return MAX_INT32;
        } else {
            return (int)dp[col - 1];
        }
    }
    
    // 方法二：动态规划。时间复杂度 O(M*N)，空间复杂度 O(M*N)。
    // 如果数据不会溢出 int，则可以直接用 obstacleGrid 来 dp，空间复杂度 O(1)
    // 不过测试用例会溢出，所以要额外设置 dp 数组。
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 9.3 MB , 在所有 C++ 提交中击败了 29.17% 的用户
    // Runtime: 4 ms, faster than 85.66% of C++ online submissions for Unique Paths II.
    // Memory Usage: 9.3 MB, less than 24.00% of C++ online submissions for Unique Paths II.
    int solution2 (vector<vector<int>>& obstacleGrid) {
        // 边界情况
        if (obstacleGrid.empty()) {
            return 0;
        }
        
        if (obstacleGrid[0].empty()) {
            return 0;
        }
        
        // 如果首元素就是障碍，那么不会有任何可行路径
        if (obstacleGrid[0][0] == 1) {
            return 0;
        }
        
        int row = (int)obstacleGrid.size();
        int col = (int)obstacleGrid[0].size();
        
        // 如果只有一行，就看这行里面有没有障碍，有则 0，无则 1
        if (row == 1) {
            for (int j = 0; j < col; j++) {
                if (obstacleGrid[0][j] == 1) {
                    return 0;
                }
            }
            return 1;
        }
        
        // 如果只有一列，就看这列里面有没有障碍，有则 0，无则 1
        if (col == 1) {
            for (int i = 0; i < row; i++) {
                if (obstacleGrid[i][0] == 1) {
                    return 0;
                }
            }
            return 1;
        }
        
        // 令 dp[i][j] 是到达 i, j 的不同路径数量
        // 状态转移方程：dp[i][j] = dp[i-1][j] + dp[i][j-1]
        // 初始化 dp[i][0] 均为 1，dp[0][j] 均为 1，运行表格如下：
        // 1  1  1
        // 1  0  1 // 注意，中间为障碍物，遇到障碍物就要归零
        // 1  1  2
        
        // 在 LeetCode 测试用例 21 时，执行会出现 int 的溢出异常signed integer overflow:
        // 1053165744 + 1579748616 cannot be represented in type 'int'
        vector<vector<ull>> dp = vector<vector<ull>>(row, vector<ull>(col, 0));
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                dp[i][j] = obstacleGrid[i][j];
            }
        }
        
        // 设置起点的值为 1
        dp[0][0] = 1;
        
        // 给 dp[i][0] 赋初值
        for (int i = 1; i < row; i++) {
            // 遇到障碍，则之后均为 0
            if (dp[i][0] == 1) {
                while (i < row) {
                    dp[i++][0] = 0;
                }
                break;
            } else {
                // 否则设置该点值为 1
                dp[i][0] = 1;
            }
        }
        
        // 给 dp[0][j] 赋初值
        for (int j = 1; j < col; j++) {
            // 遇到障碍，则之后均为 0
            if (dp[0][j] == 1) {
                while (j < col) {
                    dp[0][j++] = 0;
                }
                break;
            } else {
                // 否则设置该点值为 1
                dp[0][j] = 1;
            }
        }
        
        // 状态转移方程：dp[i][j] = dp[i-1][j] + dp[i][j-1]
        for (int i = 1; i < row; i++) {
            for (int j = 1; j < col; j++) {
                if (dp[i][j] == 1) {
                    // 遇到障碍，设置该点值为 0
                    dp[i][j] = 0;
                } else {
                    // 否则继续执行状态转移方程
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
                }
            }
        }
        
        return (int)dp[row - 1][col - 1];
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果 2
//    vector<vector<int>> obstacleGrid = {
//        {0, 0, 0},
//        {0, 1, 0},
//        {0, 0, 0}
//    };
    
    // 预期结果 1637984640
    // TODO solution1 答案为 1662293184 有问题...
    vector<vector<int>> obstacleGrid = {
        {0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0},
        {0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1},
        {0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0},
        {1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1},
        {0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0},
        {0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0},
        {1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0},
        {0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0},
        {0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0},
        {0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0},
        {0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0},
        {1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,1},
        {0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0},
        {0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0},
        {0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1},
        {1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0},
        {0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1},
        {0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1},
        {1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0},
        {0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1},
        {0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->uniquePathsWithObstacles(obstacleGrid);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
