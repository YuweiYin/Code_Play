//
//  main.cpp
//  Prob1006_ZigZag_Conversion
//
//  Created by 阴昱为 on 2019/5/31.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//6. ZigZag Conversion
//
//The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
//  P   A   H   N
//  A P L S I I G
//  Y   I   R
//And then read line by line: "PAHNAPLSIIGYIR"
//Write the code that will take a string and make this conversion given a number of rows:
//  string convert(string s, int numRows);
//
//将一个给定字符串根据给定的行数，以从上往下、从左到右进行 Z 字形排列。
//比如输入字符串为 "LEETCODEISHIRING" 行数为 3 时，排列如下：
//  L   C   I   R
//  E T O E S I I G
//  E   D   H   N
//之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，比如："LCIRETOESIIGEDHN"。
//请你实现这个将字符串进行指定行数变换的函数：
//  string convert(string s, int numRows);
//
//Example1:
//  Input: s = "PAYPALISHIRING", numRows = 3
//  Output: "PAHNAPLSIIGYIR"
//
//Example2:
//  Input: s = "PAYPALISHIRING", numRows = 4
//  Output: "PINALSIGYAHRPI"
//  Explanation:
//      P     I    N
//      A   L S  I G
//      Y A   H R
//      P     I


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


class Solution {
public:
    string convert (string s, int numRows) {
        if (s.empty() || numRows <= 0) {
            return "";
        }
        
        if (numRows == 1) {
            return s;
        }
        
        string res = "";
        
        res = this->solution2(s, numRows);
        
        return res;
    }
    
    // 模拟法：
    // 模拟 Z 字形过程构建二维数组，然后逐行输出
    string solution1 (string s, int numRows) {
        string res = "";
        
        int s_len = (int)s.length();
        int max_row = 1;
        
        // 确定二维数组的列数
        if (s_len > numRows) {
            int module = 2 * (numRows - 1); // 记录每个模块的字符个数
            int module_num = 0; // 记录总共有多少个整体模块
            if (module > 0) {
                module_num = int(s_len / module);
            }
            int module_row = module_num * (numRows - 1); // 记录整体模块部分的列数目
            int rest_len = s_len - module_num * module; // 记录剩余部分的字符个数
            int rest_row = 1; // 记录剩余部分的列数目
            if (rest_len > numRows) {
                rest_row += rest_len - numRows;
            }
            max_row = module_row + rest_row;
        }
        
        // 初始化二维数组
        char zigzag[numRows][max_row];
        for (int i = 0; i < numRows; i ++) {
            for (int j = 0; j < max_row; j ++) {
                zigzag[i][j] = '\0';
            }
        }
        
        // 模拟遍历过程，构造 Z 字形二维数组
        int s_index = 0, x = 0, y = 0;
        int direction = 1; // 0 表示停下，1 表示向下走，2 表示向右上走
        while (direction != 0) {
            if (direction == 1) {
                // 向下走
                // cout << x << "," << y << "," << s[s_index] << endl;
                zigzag[x++][y] = s[s_index++];
                if (x >= numRows) {
                    direction = 2;
                    x -= 2;
                    y ++;
                }
            } else if (direction == 2) {
                // 向右上走
                // cout << x << "," << y << "," << s[s_index] << endl;
                zigzag[x--][y++] = s[s_index++];
                if (x < 0) {
                    direction = 1;
                    x += 2;
                    y --;
                }
            } else {
                // 异常情况
                direction = 0;
            }
            
            if (s_index >= s_len) {
                // 停止，或者直接 break
                direction = 0;
            }
        }
        
        // 按行遍历构造好的二维数组
        for (int i = 0; i < numRows; i ++) {
            for (int j = 0; j < max_row; j ++) {
                if (zigzag[i][j] == '\0') {
                    // cout << " ";
                    continue;
                } else {
                    // cout << zigzag[i][j];
                    res += zigzag[i][j];
                }
            }
            // cout << endl;
        }
        
        return res;
    }
    
    // 规律法：
    // 仔细分析，找出每一行依次出现的字符所在 s 串的坐标 index 相对于 Z 字形二维数组的行列 i,j 之间的关系
    string solution2 (string s, int numRows) {
        string res = "";
        int s_len = (int)s.length();
        
        for (int i = 0; i < numRows; i++) {
            int k = 0;
            if (i == 0) {
                // 第 0 行，最初的一行。
                // 在该行出现的字符，在 s 中的坐标是 0, 2n-2, 4n-4...
                // 规律为 2k(n-1), k=0,1,2,3...
                while ((k << 1) * (numRows - 1) < s_len) {
                    res += s[(k << 1) * (numRows - 1)];
                    k ++;
                }
            } else if (i == numRows - 1) {
                // 第 n - 1 行，最后一行。
                // 在该行出现的字符，在 s 中的坐标是 n-1, 3n-3, 5n-5...
                // 规律为 (2k+1)(n-1), k=0,1,2,3...
                while (((k << 1) + 1) * (numRows - 1) < s_len) {
                    res += s[((k << 1) + 1) * (numRows - 1)];
                    k ++;
                }
            } else {
                // 中间第 i 行。
                // 在该行出现的字符，在 s 中的坐标分为两个规律部分，以 i=1 为例，
                // 分别是 1, 2n-3, 4n-5... 和 2n-1, 4n-3, 6n-5... 两组数据交替出现
                // 规律为 2k(n-1)+m, k=0,1,2,3... 和 2k(n-1)-m, k=1,2,3,...
                while ((k << 1) * (numRows - 1) - i < s_len) {
                    int index = (k << 1) * (numRows - 1);
                    if (index >= i) {
                        res += s[index - i];
                    }
                    
                    // 在 2k(n-1)-m 符合条件的情况下，用相同的 k 判断 2k(n-1)+m 是否也成立
                    if (index + i < s_len) {
                        res += s[index + i];
                    }
                    k ++;
                }
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
    // string s = "LEETCODEISHIRING";
    // int numRows = 3; // "LCIRETOESIIGEDHN"
    // int numRows = 4; // "LDREOEIIECIHNTSG"
    
    string s = "ABC";
    int numRows = 2; // "AB"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->convert(s, numRows) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
