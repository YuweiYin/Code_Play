//
//  main.cpp
//  Prob1980_Unique_Paths_III
//
//  Created by 阴昱为 on 2019/7/5.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//980. Unique Paths III
//
//On a 2-dimensional grid, there are 4 types of squares:
//    1 represents the starting square.  There is exactly one starting square.
//    2 represents the ending square.  There is exactly one ending square.
//    0 represents empty squares we can walk over.
//    -1 represents obstacles that we cannot walk over.
//Return the number of 4-directional walks from the starting square to the ending square, that walk over every non-obstacle square exactly once.
//
//在二维网格 grid 上，有 4 种类型的方格：
//    1 表示起始方格。且只有一个起始方格。
//    2 表示结束方格，且只有一个结束方格。
//    0 表示我们可以走过的空方格。
//    -1 表示我们无法跨越的障碍。
//返回在四个方向（上、下、左、右）上行走时，从起始方格到结束方格的不同路径的数目，每一个无障碍方格都要通过一次。
//
//Example 1:
//    Input: [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]
//    Output: 2
//    Explanation: We have the following two paths:
//    1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2)
//    2. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2)
//
//Example 2:
//    Input: [[1,0,0,0],[0,0,0,0],[0,0,0,2]]
//    Output: 4
//    Explanation: We have the following four paths:
//    1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2),(2,3)
//    2. (0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(1,3),(2,3)
//    3. (0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(1,1),(0,1),(0,2),(0,3),(1,3),(2,3)
//    4. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),(2,2),(2,3)
//
//Example 3:
//    Input: [[0,1],[2,0]]
//    Output: 0
//    Explanation:
//    There is no path that walks over every empty square exactly once.
//    Note that the starting and ending square can be anywhere in the grid.
//    请注意，起始和结束方格可以位于网格中的任意位置。
//
//Note:
//    1 <= grid.length * grid[0].length <= 20


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
//#define ull unsigned long long

// 全局常量
//#define PI acos(-1.0)
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ull MAX_INT32 = 2147483647;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    int uniquePathsIII(vector<vector<int>>& grid) {
        return this->solution1(grid);
    }
    
private:
    // 方法一：回溯法。时间复杂度 O(4^(row * col))，空间复杂度 O(1)。
    // 本题题设矩形面积不超过 20，所以回溯法还能接受。空间复杂度 O(1) 是因为直接用 grid，不另设数组。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 94.63% 的用户
    // 内存消耗 : 8.4 MB , 在所有 C++ 提交中击败了 94.12% 的用户
    // Runtime: 4 ms, faster than 88.06% of C++ online submissions for Unique Paths III.
    // Memory Usage: 8.5 MB, less than 81.74% of C++ online submissions for Unique Paths III.
    int solution1 (vector<vector<int>>& grid) {
        // 边界情况
        if (grid.empty()) {
            return 0;
        }
        
        if (grid[0].empty()) {
            return 0;
        }
        
        int row = (int)grid.size();
        int col = (int)grid[0].size();
        
        // 如果只有一行，要想有一条成功的路径，需要保证起点终点在首尾，并且中间没有障碍
        if (row == 1) {
            if ((grid[0][0] == 1 && grid[0][col - 1] == 2) ||
                (grid[0][0] == 2 && grid[0][col - 1] == 1)) {
                for (int j = 1; j < col - 1; j++) {
                    if (grid[0][j] != 0) {
                        return 0;
                    }
                }
                return 1;
            } else {
                return 0;
            }
        }
        
        // 如果只有一列，同上理
        if (col == 1) {
            if ((grid[0][0] == 1 && grid[row - 1][0] == 2) ||
                (grid[0][0] == 2 && grid[row - 1][0] == 1)) {
                for (int i = 1; i < row - 1; i++) {
                    if (grid[i][0] != 0) {
                        return 0;
                    }
                }
                return 1;
            } else {
                return 0;
            }
        }
        
        int res = 0, start_i = 0, start_j = 0, end_i = 0, end_j = 0, aim_depth = 0;
        int start_count = 0, end_count = 0; // 保证只有一个起点和一个终点
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                if (grid[i][j] != -1) {
                    // 记录总路径长度，包括起点和终点
                    aim_depth ++;
                }
                
                if (grid[i][j] == 1) {
                    // 记录起点位置
                    start_i = i;
                    start_j = j;
                    start_count ++;
                }
                
                if (grid[i][j] == 2) {
                    // 记录终点位置
                    end_i = i;
                    end_j = j;
                    end_count ++;
                }
            }
        }
        
        // 保证只有一个起点和一个终点
        if (start_count != 1 || end_count != 1) {
            return 0;
        }
        
        // 从 (start_i, start_j) 出发，深度优先回溯法搜索可行解
        grid[start_i][start_j] = 0;
        this->backtrack(res, grid, row, col, end_i, end_j, start_i, start_j, aim_depth, 1);
        
        return res;
    }
    
    void backtrack (int& res, vector<vector<int>>& grid, int& row, int& col, int& end_i, int& end_j,
                    int cur_i, int cur_j, int& aim_depth, int depth) {
        // 坐标越界，或者遇到障碍，或者长度溢出(异常情况)，都不继续前进
        if (cur_i < 0 || cur_i >= row || cur_j < 0 || cur_j >= col ||
            grid[cur_i][cur_j] == -1 || depth > aim_depth) {
            return;
        }
        
        // 如果遇到终点，判断已走路径是否和目标路径等长
        if (grid[cur_i][cur_j] == 2) {
            if (depth == aim_depth) {
                res ++;
            }
            return;
        }
        
        // 如果是可走的格子，则按四个方向尝试，前进->递归->回溯
        if (grid[cur_i][cur_j] == 0) {
            if (cur_i < row - 1) { // Down
                grid[cur_i][cur_j] = -1;
                this->backtrack(res, grid, row, col, end_i, end_j, cur_i + 1, cur_j, aim_depth, depth + 1);
                grid[cur_i][cur_j] = 0;
            }
            
            if (cur_j < col - 1) { // Right
                grid[cur_i][cur_j] = -1;
                this->backtrack(res, grid, row, col, end_i, end_j, cur_i, cur_j + 1, aim_depth, depth + 1);
                grid[cur_i][cur_j] = 0;
            }
            
            if (cur_i > 0) { // Up
                grid[cur_i][cur_j] = -1;
                this->backtrack(res, grid, row, col, end_i, end_j, cur_i - 1, cur_j, aim_depth, depth + 1);
                grid[cur_i][cur_j] = 0;
            }
            
            if (cur_j > 0) { // Left
                grid[cur_i][cur_j] = -1;
                this->backtrack(res, grid, row, col, end_i, end_j, cur_i, cur_j - 1, aim_depth, depth + 1);
                grid[cur_i][cur_j] = 0;
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
    // 预期结果 2
//    vector<vector<int>> grid = {
//        {1,0,0,0},
//        {0,0,0,0},
//        {0,0,2,-1}
//    };
    
    // 预期结果 4
//    vector<vector<int>> grid = {
//        {1,0,0,0},
//        {0,0,0,0},
//        {0,0,0,2}
//    };
    
    // 预期结果 0
//    vector<vector<int>> grid = {
//        {0,1},
//        {2,0}
//    };
    
    // 预期结果 4
    vector<vector<int>> grid = {
        {1,0,0,0,0},
        {0,0,0,0,0},
        {0,0,2,-1,0},
        {0,0,0,0,0}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->uniquePathsIII(grid);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
