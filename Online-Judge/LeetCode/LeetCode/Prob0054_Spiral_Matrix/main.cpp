//
//  main.cpp
//  Prob1054_Spiral_Matrix
//
//  Created by 阴昱为 on 2019/7/24.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//54. Spiral Matrix
//
//Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order.
//
//给定一个包含 m x n 个元素的矩阵（m 行, n 列），请按照顺时针螺旋顺序，返回矩阵中的所有元素。
//
//Example 1:
//    Input:
//    [
//     [ 1, 2, 3 ],
//     [ 4, 5, 6 ],
//     [ 7, 8, 9 ]
//    ]
//    Output: [1,2,3,6,9,8,7,4,5]
//
//Example 2:
//    Input:
//    [
//     [1, 2, 3, 4],
//     [5, 6, 7, 8],
//     [9,10,11,12]
//    ]
//    Output: [1,2,3,4,8,12,11,10,9,5,6,7]


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
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        return this->solution1(matrix);
    }
    
private:
    // 方法一。时间复杂度 O(M*N)，空间复杂度 O(M*N)。M*N is the size of matrix
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 84.38% 的用户
    // 内存消耗 : 8.5 MB , 在所有 C++ 提交中击败了 76.42% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Spiral Matrix.
    // Memory Usage: 8.6 MB, less than 69.75% of C++ online submissions for Spiral Matrix.
    vector<int> solution1 (vector<vector<int>>& matrix) {
        // 边界情况
        if (matrix.empty() || matrix[0].empty()) {
            return {};
        }
        
        int x_max = (int)matrix.size() - 1;
        int y_max = (int)matrix[0].size() - 1;
        int x_min = 0, y_min = 0;
        
        vector<int> res = {};
        
        int len = (x_max + 1) * (y_max + 1);
        int direction = 0, x = 0, y = 0;
        
        for (int i = 0; i < len; i++) {
            if (direction == 0) { // right
                if (y == y_max) {
                    // 到达右边界，改变方向向下
                    res.push_back(matrix[x++][y]);
                    x_min ++;
                    direction = 1;
                } else {
                    res.push_back(matrix[x][y++]);
                }
            } else if (direction == 1) { // down
                if (x == x_max) {
                    // 到达下边界，改变方向向左
                    res.push_back(matrix[x][y--]);
                    y_max --;
                    direction = 2;
                } else {
                    res.push_back(matrix[x++][y]);
                }
            } else if (direction == 2) { // left
                if (y == y_min) {
                    // 到达左边界，改变方向向上
                    res.push_back(matrix[x--][y]);
                    x_max --;
                    direction = 3;
                } else {
                    res.push_back(matrix[x][y--]);
                }
            } else if (direction == 3) { // up
                if (x == x_min) {
                    // 到达上边界，改变方向向右
                    res.push_back(matrix[x][y++]);
                    y_min ++;
                    direction = 0;
                } else {
                    res.push_back(matrix[x--][y]);
                }
            } else {
                break; // error
            }
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 [1,2,3,6,9,8,7,4,5]
//    vector<vector<int>> matrix = {
//        {1, 2, 3},
//        {4, 5, 6},
//        {7, 8, 9}
//    };
    
    // 预期结果 [1,2,3,4,8,12,11,10,9,5,6,7]
    vector<vector<int>> matrix = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->spiralOrder(matrix);
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
