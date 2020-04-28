//
//  main.cpp
//  Prob2003_Check_If_Word_Is_Valid_After_Substitutions
//
//  Created by 阴昱为 on 2019/6/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1003. Check If Word Is Valid After Substitutions
//
//We are given that the string "abc" is valid.
//
//From any valid string V, we may split V into two pieces X and Y such that X + Y (X concatenated with Y) is equal to V.  (X or Y may be empty.)  Then, X + "abc" + Y is also valid.
//
//If for example S = "abc", then examples of valid strings are: "abc", "aabcbc", "abcabc", "abcabcababcc".  Examples of invalid strings are: "abccba", "ab", "cababc", "bac".
//
//Return true if and only if the given string S is valid.
//
//给定有效字符串 "abc"。
//
//对于任何有效的字符串 V，我们可以将 V 分成两个部分 X 和 Y，使得 X + Y（X 与 Y 连接）等于 V。（X 或 Y 可以为空。）那么，X + "abc" + Y 也同样是有效的。
//
//例如，如果 S = "abc"，则有效字符串的示例是："abc"，"aabcbc"，"abcabc"，"abcabcababcc"。无效字符串的示例是："abccba"，"ab"，"cababc"，"bac"。
//
//如果给定字符串 S 有效，则返回 true；否则，返回 false。
//
//Example 1:
//    Input: "aabcbc"
//    Output: true
//    Explanation:
//    We start with the valid string "abc".
//    Then we can insert another "abc" between "a" and "bc", resulting in "a" + "abc" + "bc" which is "aabcbc".
//
//Example 2:
//    Input: "abcabcababcc"
//    Output: true
//    Explanation:
//    "abcabcabc" is valid after consecutive insertings of "abc".
//    Then we can insert "abc" before the last letter, resulting in "abcabcab" + "abc" + "c" which is "abcabcababcc".
//
//Example 3:
//    Input: "abccba"
//    Output: false
//
//Example 4:
//    Input: "cababc"
//    Output: false
//
//Note:
//    1 <= S.length <= 20000
//    S[i] is 'a', 'b', or 'c'
//提示：
//    1 <= S.length <= 20000
//    S[i] 为 'a'、'b'、或 'c'


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
    bool isValid(string S) {
        int s_len = (int)S.size();
        
        // 显然字符串长度需要是 3 的正整数倍
        if (s_len < 3 || s_len % 3 != 0) {
            return false;
        }
        
        // 长度为 3 时，只能是 "abc" 才合法
        if (s_len == 3) {
            return S == "abc";
        }
        
        return this->solution1(S);
    }
    
private:
    // 方法一：栈模拟
    bool solution1(string S) {
        bool res = true;
        
        stack<char> stack_abc = {};
        int s_len = (int)S.size();
        
        for (int i = 0; i < s_len; i++) {
            if (S[i] == 'a') {
                // 出现 a 直接让 a 入栈
                stack_abc.push(S[i]);
            } else if (S[i] == 'b') {
                // 出现 b 就要保证栈顶元素是 a，然后让 b 入栈
                if (stack_abc.empty() || stack_abc.top() != 'a') {
                    return false;
                } else {
                    stack_abc.push(S[i]);
                }
            } else if (S[i] == 'c') {
                // 出现 c 就要保证栈顶两个元素是 b 和 a，然后弹出 b 和 a
                // 栈内元素不足 2 个，必不能匹配
                if ((int)stack_abc.size() < 2) {
                    return false;
                }
                
                // 保证栈顶第一个是 'b'
                if (stack_abc.top() == 'b') {
                    // cout << "Pop: b" << endl;
                    stack_abc.pop();
                    
                    // 保证栈顶第二个是 'a'
                    if (stack_abc.top() == 'a') {
                        // cout << "Pop: a" << endl;
                        stack_abc.pop();
                    } else {
                        return false;
                    }
                } else {
                    return false;
                }
            } else {
                // 其他字符，本题中默认只有 abc，所以此处是例外情况
                // stack_abc.push(S[i]);
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
//    string S = "abcabcababcc"; // 预期结果 true
    string S = "abccba"; // 预期结果 false
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->isValid(S);
    if (ans) {
        cout << "True." << endl;
    } else {
        cout << "False." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
