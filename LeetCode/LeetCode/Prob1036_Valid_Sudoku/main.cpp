//
//  main.cpp
//  Prob1036_Valid_Sudoku
//
//  Created by 阴昱为 on 2019/7/2.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//36. Valid Sudoku
//
//Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
//    1. Each row must contain the digits 1-9 without repetition.
//    2. Each column must contain the digits 1-9 without repetition.
//    3. Each of the 9 3x3 sub-boxes of the grid must contain the digits 1-9 without repetition.
//
//The Sudoku board could be partially filled, where empty cells are filled with the character '.'.
//
//判断一个 9x9 的数独是否有效。只需要根据以下规则，验证已经填入的数字是否有效即可。
//    1. 数字 1-9 在每一行只能出现一次。
//    2. 数字 1-9 在每一列只能出现一次。
//    3. 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。
//
//数独部分空格内已填入了数字，空白格用 '.' 表示。
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
//    Output: true
//
//Example 2:
//    Input:
//    [
//     ["8","3",".",".","7",".",".",".","."],
//     ["6",".",".","1","9","5",".",".","."],
//     [".","9","8",".",".",".",".","6","."],
//     ["8",".",".",".","6",".",".",".","3"],
//     ["4",".",".","8",".","3",".",".","1"],
//     ["7",".",".",".","2",".",".",".","6"],
//     [".","6",".",".",".",".","2","8","."],
//     [".",".",".","4","1","9",".",".","5"],
//     [".",".",".",".","8",".",".","7","9"]
//    ]
//    Output: false
//    Explanation: Same as Example 1, except with the 5 in the top left corner being
//    modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.
//
//Note:
//    A Sudoku board (partially filled) could be valid but is not necessarily solvable.
//    Only the filled cells need to be validated according to the mentioned rules.
//    The given board contain only digits 1-9 and the character '.'.
//    The given board size is always 9x9.


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
    bool isValidSudoku(vector<vector<char>>& board) {
        return this->solution1(board);
    }
    
private:
    // 方法一：。
    // 时间复杂度 O()，空间复杂度 O(1)。N = 9
    bool solution1 (vector<vector<char>>& board) {
        // 边界情况
        if (board.empty()) {
            return false;
        }
        
        if (board[0].empty()) {
            return false;
        }
        
        int row = (int)board.size();
        int col = (int)board[0].size();
        
        bool res = true;
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 true
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
    
    // 预期结果 false
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
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isValidSudoku(board);
    if (ans) {
        cout << "This is a VALID Sudoku." << endl;
    } else {
        cout << "This is NOT a valid Sudoku." << endl;
    }
    
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
