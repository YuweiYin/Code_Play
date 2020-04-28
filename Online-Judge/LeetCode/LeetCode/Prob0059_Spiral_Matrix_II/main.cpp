//
//  main.cpp
//  Prob1059_Spiral_Matrix_II
//
//  Created by 阴昱为 on 2019/7/25.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//59. Spiral Matrix II
//
//Given a positive integer n, generate a square matrix filled with elements from 1 to n^2 in spiral order.
//
//给定一个正整数 n，生成一个包含 1 到 n^2 所有元素，且元素按顺时针顺序螺旋排列的正方形矩阵。
//
//Example:
//    Input: 3
//    Output:
//    [
//     [ 1, 2, 3 ],
//     [ 8, 9, 4 ],
//     [ 7, 6, 5 ]
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
    vector<vector<int>> generateMatrix(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一。时间复杂度 O(N^2)，空间复杂度 O(N^2)。N = n
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 9 MB , 在所有 C++ 提交中击败了 37.27% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Spiral Matrix II.
    // Memory Usage: 8.9 MB, less than 48.90% of C++ online submissions for Spiral Matrix II.
    vector<vector<int>> solution1 (int n) {
        // 边界情况
        if (n <= 0) {
            return {};
        }
        
        if (n == 1) {
            return {{1}};
        }
        
        int x_max = n - 1, y_max = n - 1;
        int x_min = 0, y_min = 0;
        
        vector<vector<int>> res(n, vector<int>(n, 0));
        
        int len = n * n, cur_num = 1;
        int direction = 0, x = 0, y = 0;
        
        for (int i = 0; i < len; i++) {
            if (direction == 0) { // right
                if (y == y_max) {
                    // 到达右边界，改变方向向下
                    res[x++][y] = cur_num++;
                    x_min ++;
                    direction = 1;
                } else {
                    res[x][y++] = cur_num++;
                }
            } else if (direction == 1) { // down
                if (x == x_max) {
                    // 到达下边界，改变方向向左
                    res[x][y--] = cur_num++;
                    y_max --;
                    direction = 2;
                } else {
                    res[x++][y] = cur_num++;
                }
            } else if (direction == 2) { // left
                if (y == y_min) {
                    // 到达左边界，改变方向向上
                    res[x--][y] = cur_num++;
                    x_max --;
                    direction = 3;
                } else {
                    res[x][y--] = cur_num++;
                }
            } else if (direction == 3) { // up
                if (x == x_min) {
                    // 到达上边界，改变方向向右
                    res[x][y++] = cur_num++;
                    y_min ++;
                    direction = 0;
                } else {
                    res[x--][y] = cur_num++;
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
    
    // 预期结果
    // [
    //   [ 1, 2, 3 ],
    //   [ 8, 9, 4 ],
    //   [ 7, 6, 5 ]
    // ]
    int n = 3;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->generateMatrix(n);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < ans.size(); i++) {
            for (int j = 0; j < ans[i].size(); j++) {
                cout << ans[i][j] << ", ";
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
