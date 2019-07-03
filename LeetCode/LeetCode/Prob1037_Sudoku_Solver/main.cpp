//
//  main.cpp
//  Prob1037_Sudoku_Solver
//
//  Created by 阴昱为 on 2019/7/3.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//37. Sudoku Solver
//
//Write a program to solve a Sudoku puzzle by filling the empty cells.
//A sudoku solution must satisfy all of the following rules:
//    1. Each of the digits 1-9 must occur exactly once in each row.
//    2. Each of the digits 1-9 must occur exactly once in each column.
//    3. Each of the the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
//Empty cells are indicated by the character '.'.
//
//编写一个程序，通过已填充的空格来解决数独问题。
//一个数独的解法需遵循如下规则：
//    1. 数字 1-9 在每一行只能出现一次。
//    2. 数字 1-9 在每一列只能出现一次。
//    3. 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。
//空白格用 '.' 表示。
//
//Example 1:
//    Input:
//    [
//     ["5","3",".",".","7",".",".",".","."],
//     ["6",".",".","1","9","5",".",".","."],
//     [".","9","8",".",".",".",".","6","."],
//     ["8",".",".",".","6",".",".",".","3"],
//     ["4",".",".","8",".","3",".",".","1"],
//     ["7",".",".",".","2",".",".",".","6"],
//     [".","6",".",".",".",".","2","8","."],
//     [".",".",".","4","1","9",".",".","5"],
//     [".",".",".",".","8",".",".","7","9"]
//    ]
//    Output: void
//    一个正确的解如下：
//    [
//     ["5","3","4","6","7","8","9","1","2"],
//     ["6","7","2","1","9","5","3","4","8"],
//     ["1","9","8","3","4","2","5","6","7"],
//     ["8","5","9","7","6","1","4","2","3"],
//     ["4","2","6","8","5","3","7","9","1"],
//     ["7","1","3","9","2","4","8","5","6"],
//     ["9","6","1","5","3","7","2","8","4"],
//     ["2","8","7","4","1","9","6","3","5"],
//     ["3","4","5","2","8","6","1","7","9"]
//    ]
//
//Note:
//    The given board contain only digits 1-9 and the character '.'.
//    You may assume that the given Sudoku puzzle will have a single unique solution.
//    The given board size is always 9x9.
//Note:
//    给定的数独序列只包含数字 1-9 和字符 '.' 。
//    你可以假设给定的数独只有唯一解。
//    给定数独永远是 9x9 形式的。


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
private:
    bool end_recursion = false;
    
public:
    void solveSudoku(vector<vector<char>>& board) {
        this->solution1(board);
    }
    
    bool isValidSudoku(vector<vector<char>>& board) {
        return this->solution2(board);
    }
    
private:
    // 方法一：回溯法，无序哈希表记录。时间复杂度 O((N!)^N)，空间复杂度 O(N^2)。N = 9
    // 蛮力法：生成所有可能的填充 1~9 的解，逐个判断合法性。时间复杂度 O(N^(N^2))
    // 比较：回溯法 (9!)^9 约比 9^81 减少 10^27 倍。
    // 执行用时 : 36 ms , 在所有 C++ 提交中击败了 42.01% 的用户
    // 内存消耗 : 12.1 MB , 在所有 C++ 提交中击败了 12.32% 的用户
    // Runtime: 28 ms, faster than 25.98% of C++ online submissions for Sudoku Solver.
    // Memory Usage: 12.1 MB, less than 18.88% of C++ online submissions for Sudoku Solver.
    void solution1 (vector<vector<char>>& board) {
        // 边界情况
        if (board.empty()) {
            return;
        }
        
        if (board[0].empty()) {
            return;
        }
        
        if (!this->isValidSudoku(board)) {
            return;
        }
        
        // 计算行、列、格子总数
        int row = (int)board.size();
        int col = (int)board[0].size();
        int block = (row / 3) * (col / 3);
        
        // 记录每行、每列、每个格子的元素，如果 map 重复了，表示不合法
        vector<unordered_map<char, int>> map_row_count(row);
        vector<unordered_map<char, int>> map_col_count(col);
        vector<unordered_map<char, int>> map_block_count(block);
        
        // 对每个元素进行判断，遍历整个数独表
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                char cur_num = board[i][j];
                
                // 计算当前坐标 (i, j) 属于哪个格子
                int block_index = (i / 3) * 3 + j / 3;
                
                // 空则记录为 0
                if(cur_num == '.') {
                    map_row_count[i][cur_num] = 0;
                    map_col_count[j][cur_num] = 0;
                    map_block_count[block_index][cur_num] = 0;
                }
                
                // 若三个表中有一个表的 num 键值大于 0，则表示重复
                if(map_row_count[i][cur_num] > 0 ||
                   map_col_count[j][cur_num] > 0 ||
                   map_block_count[block_index][cur_num] > 0) {
                    continue;
                }
                
                // 设置键值
                map_row_count[i][cur_num] = 1;
                map_col_count[j][cur_num] = 1;
                map_block_count[block_index][cur_num] = 1;
            }
        }
        
        this->backtrack(board, 0, 0, row, col, map_row_count, map_col_count, map_block_count);
        
        return;
    }
    
    void backtrack (vector<vector<char>>& board, int i, int j, int& row, int& col,
                    vector<unordered_map<char, int>>& map_row_count,
                    vector<unordered_map<char, int>>& map_col_count,
                    vector<unordered_map<char, int>>& map_block_count) {
        if (this->end_recursion) {
            return; // End Recursion Now!
        }
        
        if (board[i][j] == '.') {
            // 如果当前未填数字，则尝试填写 1~9
            for (char num = '1'; num <= '9'; num++) {
                if (this->end_recursion) {
                    return; // End Recursion Now!
                }
                
                // 计算当前坐标 (i, j) 属于哪个格子
                int block_index = (i / 3) * 3 + j / 3;
                
                // 若三个表中有一个表的 num 键值大于 0，则表示重复，不能填这个 num
                if(map_row_count[i][num] > 0 ||
                   map_col_count[j][num] > 0 ||
                   map_block_count[block_index][num] > 0) {
                    continue;
                }
                
                // 前进
                map_row_count[i][num] = 1;
                map_col_count[j][num] = 1;
                map_block_count[block_index][num] = 1;
                board[i][j] = num;
                
                // 递归
                if (i >= row - 1 && j >= col - 1) {
                    // 全部填完了，结束填写
                    this->end_recursion = true;
                    return;
                }
                
                if (j >= col - 1) {
                    // 填下一行
                    this->backtrack(board, i + 1, 0, row, col, map_row_count, map_col_count, map_block_count);
                } else {
                    // 填下一列
                    this->backtrack(board, i, j + 1, row, col, map_row_count, map_col_count, map_block_count);
                }
                
                if (this->end_recursion) {
                    return; // End Recursion Now!
                }
                
                // 回溯
                map_row_count[i][num] = 0;
                map_col_count[j][num] = 0;
                map_block_count[block_index][num] = 0;
                board[i][j] = '.';
            }
        } else {
            // 如果当前已填数字，则尝试填写下一个格子
            if (i >= row - 1 && j >= col - 1) {
                // 全部填完了，结束填写
                this->end_recursion = true;
                return;
            }
            
            if (j >= col - 1) {
                // 填下一行
                this->backtrack(board, i + 1, 0, row, col, map_row_count, map_col_count, map_block_count);
            } else {
                // 填下一列
                this->backtrack(board, i, j + 1, row, col, map_row_count, map_col_count, map_block_count);
            }
        }
    }
    
    // 验证一个数独是否合法
    bool solution2 (vector<vector<char>>& board) {
        // 边界情况
        if (board.empty()) {
            return false;
        }
        
        if (board[0].empty()) {
            return false;
        }
        
        // 计算行、列、格子总数
        int row = (int)board.size();
        int col = (int)board[0].size();
        int block = (row / 3) * (col / 3);
        
        // 记录每行、每列、每个格子的元素，如果 map 重复了，表示不合法
        vector<unordered_map<char, int>> map_row_count(row);
        vector<unordered_map<char, int>> map_col_count(col);
        vector<unordered_map<char, int>> map_block_count(block);
        
        // 对每个元素进行判断，遍历整个数独表
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                char cur_num = board[i][j];
                
                // 空则跳过
                if(cur_num == '.') {
                    continue;
                }
                
                // 计算当前坐标 (i, j) 属于哪个格子
                int block_index = (i / 3) * 3 + j / 3;
                
                // 若三个表中有一个表存在 cur_num 键值(count 函数返回值为 1)，则表示重复了
                if(map_row_count[i].count(cur_num) ||
                   map_col_count[j].count(cur_num) ||
                   map_block_count[block_index].count(cur_num)) {
                    return false;
                }
                
                // 设置键值
                map_row_count[i][cur_num] = 1;
                map_col_count[j][cur_num] = 1;
                map_block_count[block_index][cur_num] = 1;
            }
        }
        
        return true;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    vector<vector<char>> board = {
        {'5','3','.','.','7','.','.','.','.'},
        {'6','.','.','1','9','5','.','.','.'},
        {'.','9','8','.','.','.','.','6','.'},
        {'8','.','.','.','6','.','.','.','3'},
        {'4','.','.','8','.','3','.','.','1'},
        {'7','.','.','.','2','.','.','.','6'},
        {'.','6','.','.','.','.','2','8','.'},
        {'.','.','.','4','1','9','.','.','5'},
        {'.','.','.','.','8','.','.','7','9'}
    };
    
    // 不合法的数独，不能填数
//    vector<vector<char>> board = {
//        {'8','3','.','.','7','.','.','.','.'},
//        {'6','.','.','1','9','5','.','.','.'},
//        {'.','9','8','.','.','.','.','6','.'},
//        {'8','.','.','.','6','.','.','.','3'},
//        {'4','.','.','8','.','3','.','.','1'},
//        {'7','.','.','.','2','.','.','.','6'},
//        {'.','6','.','.','.','.','2','8','.'},
//        {'.','.','.','4','1','9','.','.','5'},
//        {'.','.','.','.','8','.','.','7','9'}
//    };
    
    // Before 输出数独表格
//    int row = (int)board.size();
//    int col = (int)board[0].size();
//    for (int i = 0; i < row; i++) {
//        for (int j = 0; j < col; j++) {
//            cout << board[i][j] << " ";
//        }
//        cout << endl;
//    }
//    cout << endl;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isValidSudoku(board);
    if (ans) {
        cout << "Before: This is a VALID Sudoku." << endl;
        
        solution->solveSudoku(board);
        
        ans = solution->isValidSudoku(board);
        if (ans) {
            cout << "After: This is a VALID Sudoku." << endl;
        } else {
            cout << "After: This is NOT a valid Sudoku." << endl;
        }
        
        // After 输出数独表格
//        for (int i = 0; i < row; i++) {
//            for (int j = 0; j < col; j++) {
//                cout << board[i][j] << " ";
//            }
//            cout << endl;
//        }
//        cout << endl;
    } else {
        cout << "Before: This is NOT a valid Sudoku." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
