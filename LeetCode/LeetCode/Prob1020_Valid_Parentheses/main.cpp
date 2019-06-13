//
//  main.cpp
//  Prob1020_Valid_Parentheses
//
//  Created by 阴昱为 on 2019/6/13.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//20. Valid Parentheses
//
//Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
//
//An input string is valid if:
//    Open brackets must be closed by the same type of brackets.
//    Open brackets must be closed in the correct order.
//    Note that an empty string is also considered valid.
//
//给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
//
//有效字符串需满足：
//    左括号必须用相同类型的右括号闭合。
//    左括号必须以正确的顺序闭合。
//    注意空字符串可被认为是有效字符串。
//
//Example 1:
//    Input: "()"
//    Output: true
//
//Example 2:
//    Input: "()[]{}"
//    Output: true
//
//Example 3:
//    Input: "(]"
//    Output: false
//
//Example 4:
//    Input: "([)]"
//    Output: false
//
//Example 5:
//    Input: "{[]}"
//    Output: true


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
public:
    bool isValid(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一：栈
    bool solution1 (string s) {
        if (s.empty()) {
            return true;
        }
        
        if ((int)s.size() == 1 || s[0] == ')' || s[0] == ']' || s[0] == '}') {
            return false;
        }
        
        stack<char> parentheses_stack = {};
        
        for (int i = 0; i < (int)s.size(); i++) {
            if (s[i] == '(' || s[i] == '[' || s[i] == '{') {
                // cout << "push: " << s[i] << endl;
                parentheses_stack.push(s[i]);
            } else if (s[i] == ')' || s[i] == ']' || s[i] == '}') {
                if (parentheses_stack.empty()) {
                    return false;
                }
                if ((s[i] == ')' && parentheses_stack.top() == '(')
                        || (s[i] == ']' && parentheses_stack.top() == '[')
                        || (s[i] == '}' && parentheses_stack.top() == '{')) {
                    // cout << "pop: " << s[i] << endl;
                    parentheses_stack.pop();
                } else {
                    return false;
                }
            }
        }
        
        return parentheses_stack.empty();
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    string s = "()(){[()()]()}"; // 预期结果 true
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isValid(s);
    cout << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
