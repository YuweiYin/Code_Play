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
    // 方法二。原地修改、首行/首列元素记录应归零的列/行。时间复杂度 O(M*N)，空间复杂度 O(1)。
    // 执行用时 : 68 ms , 在所有 C++ 提交中击败了 83.82% 的用户
    // 内存消耗 : 11.2 MB , 在所有 C++ 提交中击败了 96.35% 的用户
    // Runtime: 48 ms, faster than 66.92% of C++ online submissions for Set Matrix Zeroes.
    // Memory Usage: 11.3 MB, less than 97.90% of C++ online submissions for Set Matrix Zeroes.
    void solution1 (vector<vector<int>>& matrix) {
        bool isCol = false; // 首列是否需要设置为 0
        int row = (int)matrix.size();
        int col = (int)matrix[0].size();
        
        for (int i = 0; i < row; i++) {
            if (matrix[i][0] == 0) {
                // 若某列首元素为 0，则表示首列需要设置为 0
                isCol = true;
            }
            
            for (int j = 1; j < col; j++) {
                // 若某元素为 0，则设置改元素所在行和列的首元素为 0
                if (matrix[i][j] == 0) {
                    matrix[0][j] = 0;
                    matrix[i][0] = 0;
                }
            }
        }
        
        // 再次遍历矩阵，如果某元素所在行/列的首元素为 0，则将它设为 0
        for (int i = 1; i < row; i++) {
            for (int j = 1; j < col; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                    matrix[i][j] = 0;
                }
            }
        }
        
        // 如果 (0, 0) 位置为 0，则表示首行需要设置为 0
        if (matrix[0][0] == 0) {
            for (int j = 0; j < col; j++) {
                matrix[0][j] = 0;
            }
        }
        
        // 由于 (0, 0) 位置为 0 只能表示首行是否该设置为 0，
        // 而不能表示首列是否该设置为 0，所以需要 isCol 来对此进行判断。
        if (isCol) {
            for (int i = 0; i < row; i++) {
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
