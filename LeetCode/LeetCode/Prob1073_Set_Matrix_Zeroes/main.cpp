//
//  main.cpp
//  Prob1073_Set_Matrix_Zeroes
//
//  Created by 阴昱为 on 2019/7/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//73. Set Matrix Zeroes
//
//Given a m x n matrix, if an element is 0, set its entire row and column to 0. Do it in-place.
//
//给定一个 m x n 的矩阵，如果一个元素为 0，则将其所在行和列的所有元素都设为 0。请使用原地算法。
//
//Example 1:
//    Input:
//    [
//     [1,1,1],
//     [1,0,1],
//     [1,1,1]
//    ]
//    Output:
//    [
//     [1,0,1],
//     [0,0,0],
//     [1,0,1]
//    ]
//
//Example 2:
//    Input:
//    [
//     [0,1,2,0],
//     [3,4,5,2],
//     [1,3,1,5]
//    ]
//    Output:
//    [
//     [0,0,0,0],
//     [0,4,5,0],
//     [0,3,1,0]
//    ]
//
//Follow up:
//    A straight forward solution using O(mn) space is probably a bad idea.
//    A simple improvement uses O(m + n) space, but still not the best solution.
//    Could you devise a constant space solution?
//
//进阶:
//    一个直接的解决方案是使用  O(mn) 的额外空间，但这并不是一个好的解决方案。
//    一个简单的改进方案是使用 O(m + n) 的额外空间，但这仍然不是最好的解决方案。
//    你能想出一个常数空间的解决方案吗？


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
    void setZeroes(vector<vector<int>>& matrix) {
        this->solution1(matrix);
    }
    
private:
    // 方法一。。时间复杂度 O(M*N)，空间复杂度 O(1)。
    // 执行用时 : 68 ms , 在所有 C++ 提交中击败了 84.18% 的用户
    // 内存消耗 : 11.3 MB , 在所有 C++ 提交中击败了 93.02% 的用户
    // Runtime: 48 ms, faster than 67.32% of C++ online submissions for Set Matrix Zeroes.
    // Memory Usage: 11.3 MB, less than 99.79% of C++ online submissions for Set Matrix Zeroes.
    void solution1 (vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) {
            return;
        }
        
        bool col0_flag = false;
        int row = (int)matrix.size();
        int col = (int)matrix[0].size();
        
        for (int i = 0; i < row; i++) {
            if (matrix[i][0] == 0) {
                col0_flag = true;
            }
            
            for (int j = 1; j < col; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = matrix[0][j] = 0;
                }
            }
        }
        
        for (int i = row - 1; i >= 0; i--) {
            for (int j = col - 1; j >= 1; j--) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                    matrix[i][j] = 0;
                }
            }
            
            if (col0_flag) {
                matrix[i][0] = 0;
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
    // 预期结果 "/home"
    vector<vector<int>> matrix = {
        {0, 1, 2, 0},
        {3, 4, 5, 2},
        {1, 3, 1, 5}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->setZeroes(matrix);
    if (matrix.empty() || matrix[0].empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < matrix.size(); i++) {
            for (int j = 0; j < matrix[i].size(); j++) {
                cout << matrix[i][j] << ", ";
            }
            cout << "End." << endl;
        }
    }
    
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
