//
//  main.cpp
//  Prob1065_Valid_Number
//
//  Created by 阴昱为 on 2019/7/26.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//65. Valid Number
//
//Validate if a given string can be interpreted as a decimal number.
//
//验证给定的字符串是否可以解释为十进制数字。
//
//Some examples:
//    "0" => true
//    " 0.1 " => true
//    "abc" => false
//    "1 a" => false
//    "2e10" => true
//    " -90e3   " => true
//    " 1e" => false
//    "e3" => false
//    " 6e-1" => true
//    " 99e2.5 " => false
//    "53.5e93" => true
//    " --6 " => false
//    "-+3" => false
//    "95a54e53" => false
//
//Note: It is intended for the problem statement to be ambiguous. You should gather all requirements up front before implementing one. However, here is a list of characters that can be in a valid decimal number:
//
//说明: 我们有意将问题陈述地比较模糊。在实现代码之前，你应当事先思考所有可能的情况。
//这里给出一份可能存在于有效十进制数字中的字符列表：
//    Numbers 0-9
//    Exponent - "e"
//    Positive/negative sign - "+"/"-"
//    Decimal point - "."
//
//Of course, the context of these characters also matters in the input.
//当然，在输入中，这些字符的上下文也很重要。
//
//Update (2015-02-10):
//    The signature of the C++ function had been updated. If you still see your function signature accepts a const char * argument, please click the reload button to reset your code definition.
//
//
//更新于 2015-02-10:
//    C++函数的形式已经更新了。如果你仍然看见你的函数接收 const char * 类型的参数，请点击重载按钮重置你的代码。


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
    bool isNumber(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一。时间复杂度 O(N)，空间复杂度 O(1)。N = s.size
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.1 MB , 在所有 C++ 提交中击败了 81.54% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Valid Number.
    // Memory Usage: 8 MB, less than 89.97% of C++ online submissions for Valid Number.
    bool solution1 (string& s) {
        // 边界情况
        if (s.empty()) {
            return false;
        }
        
        int trim_start = 0;
        int trim_end = (int)s.size() - 1;
        bool all_blank = true;
        
        // 清除字符串前端的连续空格
        for (int i = 0; i <= trim_end; i++) {
            if (s[i] != ' ') {
                trim_start = i;
                all_blank = false;
                break;
            }
        }
        
        // s 全为空格
        if (all_blank) {
            return false;
        }
        
        // s 仅有一个非空字符
        if (trim_start == trim_end) {
            // 则该字符必须要是一个数字
            if (this->charIsNumber(s[trim_start])) {
                return true;
            } else {
                return false;
            }
        }
        
        // 清除字符串后端的连续空格
        for (int i = trim_end; i >= trim_start; i--) {
            if (s[i] != ' ') {
                trim_end = i;
                break;
            }
        }
        
        // s 仅有一个非空字符
        if (trim_start == trim_end) {
            // 则该字符必须要是一个数字
            if (this->charIsNumber(s[trim_start])) {
                return true;
            } else {
                return false;
            }
        }
        
        // 对有效范围的子串进行扫描检验
        bool num_show = false; // 关键位置是否出现数字
        bool exp_show = false; // 是否出现指数符号 'e'
//        bool dot_show = false; // 是否出现小数点 '.'
        // 首先，首位只能是正负号或者数字或者小数点(即小数点前是0，可以省略)
        if (s[trim_start] == '+' || s[trim_start] == '-') {
            // 如果是正负号，直接忽略之
            trim_start ++;
            
            // 但不能全字符串仅一个正负号
            if (trim_start > trim_end) {
                return false;
            }
        }
        
        // 此时首位就只能是数字或者小数点
        while (trim_start <= trim_end && this->charIsNumber(s[trim_start])) {
            if (!num_show) {
                num_show = true;
            }
            trim_start ++;
        }
        
        // 如果此时串结束，且关键位置至少出现了一个数字，则为合法
        if (trim_start > trim_end) {
            return num_show;
        }
        
        // 如果还有字符，必须要是小数点 '.' 或者指数符号 'e'
        if (s[trim_start] == '.') {
            trim_start ++;
            
            // 如果是小数点，之后还可能出现 'e'，先处理小数点和 'e' 之间的数
            // 中间可以有数字，也可以没数字，但不能出现其它字符
            while (trim_start <= trim_end && this->charIsNumber(s[trim_start])) {
                if (!num_show) {
                    num_show = true;
                }
                trim_start ++;
            }
            
            // 如果此时串结束，且关键位置至少出现了一个数字，则为合法
            if (trim_start > trim_end) {
                return num_show;
            }
            
            // 否则此时只能是 'e' 才合法
            if (s[trim_start] == 'e') {
                exp_show = true;
            } else {
                return false;
            }
        } else if (s[trim_start] == 'e') {
            exp_show = true;
        } else {
            return false;
        }
        
        if (exp_show) {
            // 之前一位必须要是数字或者小数点
            if (trim_start == 0 || (!this->charIsNumber(s[trim_start - 1]) &&
                                    s[trim_start - 1] != '.')) {
                return false;
            }
            
            trim_start ++;
            
            // 之后可以紧跟一个正负号
            if (s[trim_start] == '+' || s[trim_start] == '-') {
                trim_start ++;
            }
            
            // 然后必须全是数字(至少有一个数字)
            if (this->charIsNumber(s[trim_start])) {
                trim_start ++;
            } else {
                return false;
            }
            
            while (trim_start <= trim_end) {
                // 此处不是关键位置，不改变 num_show
                if (!this->charIsNumber(s[trim_start])) {
                    return false;
                }
                trim_start ++;
            }
        }
        
        // 关键位置至少要出现一个数字
        return num_show;
    }
    
    bool charIsNumber (char& ch) {
        return ch >= '0' && ch <= '9';
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string s = "0"; // => true
//    string s = " -.1 "; // => true
//    string s = " -."; // => false
//    string s = " 0.1 "; // => true
//    string s = "abc"; // => false
//    string s = "1 a"; // => false
//    string s = "2e10"; // => true
//    string s = " -90e3   "; // => true
//    string s = " 1e"; // => false
//    string s = "e3"; // => false
//    string s = " 6e-1"; // => true
//    string s = " 99e2.5 "; // => false
//    string s = "53.5e93"; // => true
//    string s = " --6 "; // => false
//    string s = "-+3"; // => false
//    string s = "95a54e53"; // => false
    string s = "46.e3"; // => true
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isNumber(s);
    if (ans) {
        cout << s << " is a valid number." << endl;
    } else {
        cout << s << " is NOT a valid number." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
