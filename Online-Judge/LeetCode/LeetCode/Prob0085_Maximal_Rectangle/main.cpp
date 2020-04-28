//
//  main.cpp
//  Prob1085_Maximal_Rectangle
//
//  Created by 阴昱为 on 2019/6/22.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1085. Maximal Rectangle
//
//Given a 2D binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.
//
//给定一个仅包含 0 和 1 的二维二进制矩阵，找出只包含 1 的最大矩形，并返回其面积。
//
//Example:
//    Input:
//    [
//      ["1","0","1","0","0"],
//      ["1","0","1","1","1"],
//      ["1","1","1","1","1"],
//      ["1","0","0","1","0"]
//    ]
//    Output: 6


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
private:
    int result = 0;
    
public:
    int maximalRectangle(vector<vector<char>>& matrix) {
        return this->solution2(matrix);
    }
    
private:
    // 方法一。二维分割夹逼，遇到 '0' 时分割为四块矩形，递归执行 4 个子程序。
    // 由于重叠子问题较多，在大用例时会超时
    // 时间复杂度 O()，空间复杂度 O()
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
        
        this->DFS(matrix, 0, col_len - 1, 0, row_len - 1);
        
        return this->result;
    }
    
    void DFS (vector<vector<char>> matrix, int left, int right, int up, int down) {
        bool valid = true;
        int zero_i = -1, zero_j = -1;
        
        for (int i = up; valid && i <= down; i++) {
            for (int j = left; j <= right; j++) {
                if (matrix[i][j] == '0') {
                    zero_i = i;
                    zero_j = j;
                    valid = false;
                    break;
                }
            }
        }
        
        if (valid) {
            int cur_area = (right - left + 1) * (down - up + 1);
            if (cur_area > this->result) {
                this->result = cur_area;
            }
        } else {
            // 剪枝条件：1.触及边界。2.该侧矩形最大可能面积还不如目前最优解
            if (zero_i > 0 && (right - left + 1) * (zero_i - up) > this->result) {
                // '0' 上方的矩形
                this->DFS(matrix, left, right, up, zero_i - 1);
            }
            if (zero_i < down && (right - left + 1) * (down - zero_j) > this->result) {
                // '0' 下方的矩形
                this->DFS(matrix, left, right, zero_i + 1, down);
            }
            if (zero_j > 0 && (zero_j - left) * (down - up + 1) > this->result) {
                // '0' 左侧的矩形
                this->DFS(matrix, left, zero_j - 1, up, down);
            }
            if (zero_j < right && (right - zero_j) * (down - up + 1) > this->result) {
                // '0' 右侧的矩形
                this->DFS(matrix, zero_j + 1, right, up, down);
            }
        }
    }
    
    // 方法二。动态规划
    // 时间复杂度 O(MN)，空间复杂度 O(MN)
    // 执行用时 : 24 ms , 在所有 C++ 提交中击败了 96.25% 的用户
    // 内存消耗 : 10.5 MB , 在所有 C++ 提交中击败了 95.82% 的用户
    // Runtime: 24 ms, faster than 84.22% of C++ online submissions for Maximal Rectangle.
    // Memory Usage: 10.7 MB, less than 77.98% of C++ online submissions for Maximal Rectangle.
    int solution2 (vector<vector<char>>& matrix) {
        if(matrix.empty()) {
            return 0;
        }
        
        int row_len = (int)matrix.size(); // 矩阵行数
        int col_len = (int)matrix[0].size(); // 矩阵列数
        
        vector<int> left = vector<int>(col_len, 0); // 某行某元素能达到的左边界(左侧最近的 '0' 的坐标 + 1)
        vector<int> right = vector<int>(col_len, col_len); // 某行某元素能达到的右边界(右侧最近的 '0' 的坐标)
        vector<int> height = vector<int>(col_len, 0); // 某行某元素所在列能达到的高度
        // 从 i 行的 j 号元素往上、往左、往右扩展出的矩形的面积 area[i][j] = (rgiht[j] - left[j]) * height[j]
        
        int res = 0;
        
        // 遍历每行
        for (int i = 0; i < row_len; i++) {
            int cur_left = 0; // 该行当前左侧最近的 '0' 的坐标 + 1
            int cur_right = col_len; // 该行当前右侧最近的 '0' 的坐标
            
            // 在该行中遍历，更新每个元素的高度向量 height
            for(int j = 0; j < col_len; j++) {
                if(matrix[i][j] == '1') {
                    // 对连续的 '1'，增长高度(在上一行 j 号元素所能达到的高度上加一)
                    height[j] ++;
                } else {
                    // 若遇到 '0'，高度置零
                    height[j] = 0;
                }
            }
            
            // 在该行中，从左到右遍历，更新每个元素的左边界向量 left
            for(int j = 0; j < col_len; j++) {
                if(matrix[i][j] == '1') {
                    // 对连续的 '1'，保持或缩小左边界(对比上一行的 j 号元素)
                    left[j] = max(left[j], cur_left);
                } else {
                    // 若遇到 '0', “碰壁”
                    // 将 left[j] 置为 0，看似增长了边界宽度，但是因为它的高度为 0，所以边界再长、面积还是 0
                    // 意义在于下一行计算 left[j] = max(left[j], cur_left) 时，即是计算 max(0, cur_left)，
                    // 而 cur_left >= 0，所以就等于下一行 left[j] = cur_left
                    left[j] = 0;
                    
                    // 记录左侧最近的 '0' 的位置 + 1
                    cur_left = j + 1;
                }
            }
            
            // 在该行中，从右到左遍历，更新每个元素的右边界向量 right
            for(int j = col_len - 1; j >= 0; j--) {
                if(matrix[i][j] == '1') {
                    // 对连续的 '1'，保持或缩小右边界(对比上一行的 j 号元素)
                    right[j] = min(right[j], cur_right);
                } else {
                    // 若遇到 '0', “碰壁”
                    // 将 right[j] 置为 col_len，看似增长了边界宽度，但是因为它的高度为 0，所以边界再长、面积还是 0
                    // 意义在于下一行计算 right[j] = min(right[j], cur_right) 时，即是计算 min(0, cur_right)，
                    // 而 cur_right <= col_len，所以就等于下一行 right[j] = cur_right
                    right[j] = col_len;
                    
                    // 记录右侧最近的 '0' 的位置
                    cur_right = j;
                }
            }
            
//            cout << "left:" << endl;
//            for(int j = 0; j < col_len; j++) {
//                cout << left[j] << ", ";
//            }
//            cout << "End." << endl;
//
//            cout << "right:" << endl;
//            for(int j = 0; j < col_len; j++) {
//                cout << right[j] << ", ";
//            }
//            cout << "End." << endl;
//
//            cout << "height:" << endl;
//            for(int j = 0; j < col_len; j++) {
//                cout << height[j] << ", ";
//            }
//            cout << "End." << endl;
            
            // 在该行中遍历，计算每个元素通过往上、往左、往右操作，扩展出的矩形的面积，更新最大值
            for(int j = 0; j < col_len; j++) {
                res = max(res, (right[j] - left[j]) * height[j]);
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
    // 预期结果 6
    vector<vector<char>> matrix = {
        {'1', '0', '1', '0', '0'},
        {'1', '0', '1', '1', '1'},
        {'1', '1', '1', '1', '1'},
        {'1', '0', '0', '1', '0'}
    };
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->maximalRectangle(matrix);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
