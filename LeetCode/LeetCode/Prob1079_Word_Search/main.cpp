//
//  main.cpp
//  Prob1079_Word_Search
//
//  Created by 阴昱为 on 2019/7/31.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//79. Word Search
//
//Given a 2D board and a word, find if the word exists in the grid.
//The word can be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. The same letter cell may not be used more than once.
//
//给定一个二维网格和一个单词，找出该单词是否存在于网格中。
//单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。
//
//Example:
//
//    board =
//    [
//     ['A','B','C','E'],
//     ['S','F','C','S'],
//     ['A','D','E','E']
//    ]
//
//    Given word = "ABCCED", return true.
//    Given word = "SEE", return true.
//    Given word = "ABCB", return false.


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
    bool res = false;
    bool end_flag = false;
    
public:
    bool exist(vector<vector<char>>& board, string word) {
        return this->solution1(board, word);
    }
    
private:
    // 方法一。DFS 回溯法。时间复杂度 O()，空间复杂度 O(1)。
    // 执行用时 : 24 ms , 在所有 C++ 提交中击败了 97.56% 的用户
    // 内存消耗 : 9.9 MB , 在所有 C++ 提交中击败了 97.86% 的用户
    // Runtime: 20 ms, faster than 96.89% of C++ online submissions for Word Search.
    // Memory Usage: 9.8 MB, less than 98.58% of C++ online submissions for Word Search.
    bool solution1 (vector<vector<char>>& board, string word) {
        // 边界情况
        if (board.empty() || board[0].empty()) {
            if (word.empty()) {
                return true;
            } else {
                return false;
            }
        }
        
        if (word.empty()) {
            return true;
        }
        
        int row = (int)board.size();
        int col = (int)board[0].size();
        int depth = (int)word.size();
        
        // 如果单词长度比矩阵元素个数更多，则该单词不可能被搜索到
        if (depth > row * col) {
            return false;
        }
        
        // 考虑每个起始匹配位置
        for (int i = 0; i < row; i++) {
            if (this->res) {
                break; // 已搜索到
            }
            
            for (int j = 0; j < col; j++) {
                if (this->res) {
                    break; // 已搜索到
                }
                
                this->backtrack(board, word, depth, 0, row, col, i, j);
            }
        }
        
        return this->res;
    }
    
    void backtrack (vector<vector<char>>& board, string& word, int& depth, int cur_depth,
                    int& row, int& col, int cur_row, int cur_col) {
        if (this->end_flag) {
            return; // End Recursion
        }
        
        // 继续匹配
        char cur_char = board[cur_row][cur_col]; // 记录当前字符，用于回溯时恢复字符
        if (cur_char != '\0' && cur_char == word[cur_depth]) {
            // word 被完全匹配了
            if (cur_depth + 1 >= depth) {
                this->res = true;
                this->end_flag = true;
                return;
            }
            
            board[cur_row][cur_col] = '\0'; // 不能重复使用
            
            if (cur_row < row - 1) { // Down
                this->backtrack(board, word, depth, cur_depth + 1, row, col, cur_row + 1, cur_col);
            }
            
            if (cur_col < col - 1) { // Right
                this->backtrack(board, word, depth, cur_depth + 1, row, col, cur_row, cur_col + 1);
            }
            
            if (cur_row > 0) { // Up
                this->backtrack(board, word, depth, cur_depth + 1, row, col, cur_row - 1, cur_col);
            }
            
            if (cur_col > 0) { // Left
                this->backtrack(board, word, depth, cur_depth + 1, row, col, cur_row, cur_col - 1);
            }
            
            board[cur_row][cur_col] = cur_char; // 回溯，恢复字符
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<vector<char>> board = {
        {'A', 'B', 'C', 'E'},
        {'S', 'F', 'C', 'S'},
        {'A', 'D', 'E', 'E'}
    };
//    string word = "ABCCED"; // 预期结果 true
//    string word = "SEE"; // 预期结果 false
    string word = "ABCB"; // 预期结果 false
    
//    vector<vector<char>> board = {
//        {'a'}
//    };
//    string word = "a";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->exist(board, word);
    if (ans) {
        cout << word << " is in board." << endl;
    } else {
        cout << word << " is NOT in board." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
