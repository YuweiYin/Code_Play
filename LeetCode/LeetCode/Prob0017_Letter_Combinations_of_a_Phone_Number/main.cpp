//
//  main.cpp
//  Prob1017_Letter_Combinations_of_a_Phone_Number
//
//  Created by 阴昱为 on 2019/6/12.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//17. Letter Combinations of a Phone Number
//
//Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent.
//A mapping of digit to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
//
//给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。
//给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。
//
// 1:!@#    2:abc   3:def
// 4:ghi    5:jkl   6:mno
// 7:pqrs   8:tuv   9:wxyz
// *        0       #
//
//Example:
//    Input: "23"
//    Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
//Note:
//    Although the above answer is in lexicographical order, your answer could be in any order you want.
//    尽管上面的答案是按字典序排列的，但是你可以任意选择答案输出的顺序。


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
    map<char, vector<char>> dict = {};
    vector<string> res = {};

public:
    Solution () {
        dict.insert({'2', {'a', 'b', 'c'}});
        dict.insert({'3', {'d', 'e', 'f'}});
        dict.insert({'4', {'g', 'h', 'i'}});
        dict.insert({'5', {'j', 'k', 'l'}});
        dict.insert({'6', {'m', 'n', 'o'}});
        dict.insert({'7', {'p', 'q', 'r', 's'}});
        dict.insert({'8', {'t', 'u', 'v'}});
        dict.insert({'9', {'w', 'x', 'y', 'z'}});
    }
    
    vector<string> letterCombinations(string digits) {
        return this->solution1(digits);
    }
    
private:
    // 方法一：DFS
    vector<string> solution1 (string digits) {
        if (digits.empty()) {
            return {""};
        }
        
        // 预处理 digits，使其中只含有 2～9 数字
        string _digits = "";
        for (int i = 0; i < (int)digits.size(); i++) {
            if (dict.find(digits[i]) != dict.end()) {
                _digits += digits[i];
            }
//            if (digits[i] >= '2' && digits[i] <= '9') {
//                _digits += digits[i];
//            }
        }
        
        this->DFS(_digits, "", 0);
        
        return this->res;
    }
    
    // 深度优先搜索
    void DFS (string digits, string cur_str, int i) {
        if (i > (int)digits.size() - 1) {
            return;
        }
        
        char cur_char = digits[i];
        
        if (i == (int)digits.size() - 1) {
//            if (dict.find(cur_char) != dict.end()) {
//                for (int j = 0; j < (int)dict[cur_char].size(); j++) {
//                    this->res.push_back(cur_str + dict[cur_char][j]);
//                }
//            } else {
//                this->res.push_back(cur_str);
//            }
            // 预处理后，不用上述判断
            for (int j = 0; j < (int)dict[cur_char].size(); j++) {
                this->res.push_back(cur_str + dict[cur_char][j]);
            }
            
            return;
        }
        
        for (int j = 0; j < (int)dict[cur_char].size(); j++) {
//            if (dict.find(cur_char) != dict.end()) {
//                this->BFS(digits, cur_str + dict[cur_char][j], i + 1);
//            } else {
//                this->BFS(digits, cur_str, i + 1);
//            }
            // 预处理后，不用上述判断，深度往下遍历
            this->DFS(digits, cur_str + dict[cur_char][j], i + 1);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    string digits = "12#3";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<string> ans = solution->letterCombinations(digits);
    if (!ans.empty()) {
        for (int i = 0; i < (int)ans.size() - 1; i++) {
            cout << ans[i] << ", ";
        }
        cout << ans[(int)ans.size() - 1] << endl;
    } else {
        cout << "No Answer." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
