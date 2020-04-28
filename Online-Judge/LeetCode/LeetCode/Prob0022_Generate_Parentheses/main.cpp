//
//  main.cpp
//  Prob1022_Generate_Parentheses
//
//  Created by 阴昱为 on 2019/6/13.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//22. Generate Parentheses
//
//Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
//
//给出 n 代表生成括号的对数，请你写出一个函数，使其能够生成所有可能的并且有效的括号组合。
//
//For example, given n = 3, a solution set is:
//
//    [
//     "((()))",
//     "(()())",
//     "(())()",
//     "()(())",
//     "()()()"
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


class Solution {
private:
    vector<string> res = {};
    string cur_res = "";

public:
    vector<string> generateParenthesis(int n) {
        return this->solution1(n);
    }
    
private:
    // 方法一：深度优先搜索
    vector<string> solution1(int n) {
        if (n <= 0) {
            return {};
        }
        
        if (n == 1) {
            return {"()"};
        }
        
        this->cur_res += '('; // 第一个总是要放置左括号
        int left_count = n - 1; // 剩余左括号总个数
        int right_count = n; // 右括号总个数
        
        this->DFS(left_count, right_count);
        
        return this->res;
    }
    
    void DFS (int left_count, int right_count) {
        if (left_count == 0 && right_count == 0) {
            this->res.push_back(this->cur_res);
            return;
        }
        
        if (left_count > 0) {
            this->cur_res += '('; // 前进，记录结果
            this->DFS(left_count - 1, right_count); // 深度搜索左子树
            this->cur_res.erase((int)cur_res.size() - 1, 1); // 回溯
        }
        
        if (right_count > 0) {
            // 保证剩余的左括号数目小于右括号数目就行，这样再来一个右括号也能有左括号与之匹配
            if (left_count < right_count) {
                this->cur_res += ')';  // 前进，记录结果
                this->DFS(left_count, right_count - 1);  // 深度搜索右子树
                this->cur_res.erase((int)cur_res.size() - 1, 1); // 回溯
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
    int n = 3; // 预期结果 ["((()))", "(()())", "(())()", "()(())", "()()()"]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<string> ans = solution->generateParenthesis(n);
    for (auto ite = ans.begin(); ite < ans.end(); ite++) {
        cout << *ite << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
