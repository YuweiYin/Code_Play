//
//  main.cpp
//  Prob1048_Rotate_Image
//
//  Created by 阴昱为 on 2019/7/22.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//48. Rotate Image
//
//You are given an n x n 2D matrix representing an image.
//Rotate the image by 90 degrees (clockwise).
//
//Note:
//    You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.
//
//给定一个 n × n 的二维矩阵表示一个图像。
//将图像顺时针旋转 90 度。
//
//说明：
//    你必须在原地旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要使用另一个矩阵来旋转图像。
//
//Example 1:
//    Given input matrix =
//    [
//     [1,2,3],
//     [4,5,6],
//     [7,8,9]
//    ],
//
//    rotate the input matrix in-place such that it becomes:
//    [
//     [7,4,1],
//     [8,5,2],
//     [9,6,3]
//    ]
//
//Example 2:
//    Given input matrix =
//    [
//     [ 5, 1, 9,11],
//     [ 2, 4, 8,10],
//     [13, 3, 6, 7],
//     [15,14,12,16]
//    ],
//
//    rotate the input matrix in-place such that it becomes:
//    [
//     [15,13, 2, 5],
//     [14, 3, 4, 1],
//     [12, 6, 8, 9],
//     [16, 7,10,11]
//    ]


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
    void rotate(vector<vector<int>>& matrix) {
        this->solution1(matrix);
    }
    
private:
    // 方法一：四连旋转。时间复杂度 O(N^2)，空间复杂度 O(1)。N = matrix.size
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 81.67% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    // Runtime: 4 ms, faster than 85.89% of C++ online submissions for Rotate Image.
    // Memory Usage: 9.1 MB, less than 48.07% of C++ online submissions for Rotate Image.
    void solution1 (vector<vector<int>>& matrix) {
        // 边界情况
        if (matrix.empty() || matrix[0].empty()) {
            return;
        }
        
        int m = (int)matrix.size();
        int n = (int)matrix[0].size();
        
        if (m != n) {
            return; // 按照题意，要旋转方阵
        }
        
        for (int i = 0; i < (int)(n / 2); i++) {
            for (int j = i; j < n - 1 - i; j++) {
                // (i,j) -> (j,n-1-i) -> (n-1-i,n-1-j) -> (n-1-j,i)
//                cout << "(" << i << "," << j << ") -> ";
//                cout << "(" << j << "," << n-1-i << ") -> ";
//                cout << "(" << n-1-i << "," << n-1-j << ") -> ";
//                cout << "(" << n-1-j << "," << i << ")" << endl;
                
                int temp = matrix[i][j];
                matrix[i][j] = matrix[n - 1 - j][i];
                matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j];
                matrix[n - 1 - i][n - 1 - j] = matrix[j][n -1 - i];
                matrix[j][n - 1 - i] = temp;
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
    // 预期结果
    //[
    //  [15, 13, 2, 5],
    //  [14, 3, 4, 1],
    //  [12, 6, 8, 9],
    //  [16, 7, 10, 11]
    //]
    vector<vector<int>> matrix = {
        {5, 1, 9, 11},
        {2, 4, 8, 10},
        {13, 3, 6, 7},
        {15, 14, 12, 16}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->rotate(matrix);
    for (int i = 0; i < matrix.size(); i++) {
        for (int j = 0; j < matrix[0].size(); j++) {
            cout << matrix[i][j] << ", ";
        }
        cout << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
