//
//  main.cpp
//  Prob1074_Search_a_2D_Matrix
//
//  Created by 阴昱为 on 2019/7/31.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//74. Search a 2D Matrix
//
//Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:
//    Integers in each row are sorted from left to right.
//    The first integer of each row is greater than the last integer of the previous row.
//
//编写一个高效的算法来判断 m x n 矩阵中，是否存在一个目标值。该矩阵具有如下特性：
//    每行中的整数从左到右按升序排列。
//    每行的第一个整数大于前一行的最后一个整数。
//
//Example 1:
//    Input:
//    matrix = [
//              [1,   3,  5,  7],
//              [10, 11, 16, 20],
//              [23, 30, 34, 50]
//              ]
//    target = 3
//    Output: true
//
//Example 2:
//    Input:
//    matrix = [
//              [1,   3,  5,  7],
//              [10, 11, 16, 20],
//              [23, 30, 34, 50]
//              ]
//    target = 13
//    Output: false


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
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        return this->solution1(matrix, target);
    }
    
private:
    // 方法一。按规律搜索。时间复杂度 O(M+N)，空间复杂度 O(1)。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 80.98% 的用户
    // 内存消耗 : 9.5 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    // Runtime: 8 ms, faster than 94.71% of C++ online submissions for Search a 2D Matrix.
    // Memory Usage: 9.7 MB, less than 91.18% of C++ online submissions for Search a 2D Matrix.
    bool solution1 (vector<vector<int>>& matrix, int target) {
        // 边界情况，矩阵为空
        if (matrix.empty() || matrix[0].empty()) {
            return false;
        }
        
        int row = (int)matrix.size();
        int col = (int)matrix[0].size();
        
        // target 比最小值更小，或比最大值更大，则必然找不到
        if (target < matrix[0][0] || target > matrix[row - 1][col - 1]) {
            return false;
        }
        
        // 从右上角往下找，若比目标值更大，则往左找
        // 先定位行标 x，时间 O(row)
        int x = 0;
        while (x < row) {
            if (matrix[x][col - 1] == target) {
                return true;
            } else if (matrix[x][col - 1] > target) {
                break;
            }
            x ++;
        }
        
        if (x >= row) {
            return false;
        }
        
        // 再从 x 行中找 target，时间 O(col)
        for (int j = col - 1; j >= 0; j--) {
            if (matrix[x][j] == target) {
                return true;
            }
        }
        
        return false;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<vector<int>> matrix = {
        {1,   3,  5,  7},
        {10, 11, 16, 20},
        {23, 30, 34, 50}
    };
    int target = 3; // 预期结果 true
//    int target = 13; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->searchMatrix(matrix, target);
    if (ans) {
        cout << target << " is in matrix." << endl;
    } else {
        cout << target << " is NOT in matrix." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
