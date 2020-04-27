//
//  main.cpp
//  ByteCamp_2019_Alg_6
//
//  Created by 阴昱为 on 2019/7/9.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//ByteCamp 2019 算法挑战 第六期
//题目描述：
//    给定一个只包含a，b，c的字符串，每次可以进行这样的操作：选择两个相邻的不同字符，将其替换为第三个字符。
//    输入：字符串
//    输出：经过不断操作后的字符串的最短长度
//
//    例子：
//        输入：bcab
//        输出：1
//        解释：bcab->aab->ac->b


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

class Solution {
public:
    // 解决方案入口函数
    int MinRest(string s) {
        return this->solution2(s);
    }
    
private:
    // 方法一：两遍扫描、按规律消除。时间复杂度 O(N), 空间复杂度 O(1)
    int solution1 (string s) {
        // 边界条件
        if (s.empty()) {
            return 0;
        }
        
        // 分析：通过一定的模式可以消减连续重复的字符
        // 预处理之后，串中没有连续重复的字符，每三个进行判断，只会有两种消减模式
        // 结果只可能是 3 种：剩一个或者剩两个，或者剩 s.size 个(s全为同一字符)
        
        int i = 1, count = 1;
        
        // cout << s << endl;
        s.append("x"); // 使得最末尾的连续字符也能被消减
        
        // 预处理：消除连续重复的字符（低于3个就不预处理了）
        while (i < s.size() && s.size() > 2) {
            while (i < s.size() && s[i] == s[i - 1]) {
                // 出现重复字符，找有多少个重复字符
                count ++;
                i ++;
            }
            
            if (count == s.size() - 1) {
                // 除了末尾的 x，前面全为同一字符，因此直接返回 count
                return count;
            } else {
                if (count == 1) {
                    i ++;
                } else {
                    if (count % 2 == 0) { // "aa..aab" 型(偶数个a) -> "b"
                        s.erase(i - count, count);
                        i -= count; // s.size -= count
                    } else { // "aa..ab" 型(奇数个a) -> "ab"
                        s.erase(i - count, count - 1);
                        i += 2 - count; // s.size -= count - 1
                    }
                    // cout << s << endl;
                    count = 1;
                }
            }
        }
        
        s.erase(s.size() - 1, 1); // 清除掉末尾的 x
        // cout << s << endl;
        
        // 如果预处理后剩余不到 3 个，直接判断结果
        if (s.size() == 1) {
            return 1;
        }
        
        if (s.size() == 2) {
            if (s[0] == s[1]) { // "aa" 型 -> 2
                return 2;
            } else { // "ab" 型 -> 2
                return 1;
            }
        }
        
        // 三个三个地消减，两种模式： "aba" 型 和 "abc?" 型
        i = 0;
        while (i < s.size() - 2 && s.size() > 2) {
            if (s[i] == s[i + 2]) { // "aba" 型 -> "b"
                s[i + 2] = s[i + 1];
                s.erase(i, 2);
            } else { // "abc?" 型 -> "?" (不管'?'是什么，总可以化为'?')
                if (s.size() == 3) {
                    // 目前 s 只剩三个字符，不能往后看一位
                    // "abc" 型 只能变成 "aa" 或者 "cc"
                    return 2;
                } else {
                    s.erase(i, 3);
                }
            }
            // cout << s << endl;
        }
        
        // 根据结果模式来判断能剩余几个字符
        if (s.size() == 1) {
            return 1;
        }
        
        if (s.size() == 2) {
            if (s[0] == s[1]) { // "aa" 型 -> 2
                return 2;
            } else { // "ab" 型 -> 2
                return 1;
            }
        }
        
        return (int)s.size();
    }
    
    // 方法二：两遍扫描、按规律直接计算结果。时间复杂度 O(N), 空间复杂度 O(1)
    int solution2 (string s) {
        // 边界条件
        if (s.empty()) {
            return 0;
        }
        
        // 如果全为同一字符，则结果为 s.size()
        bool all_same = true;
        
        for (int i = 1; i < s.size(); i++) {
            // 判断是否出现与 s[0] 不同的字符
            if (s[i] != s[0]) {
                all_same = false;
                break;
            }
        }
        
        if (all_same) {
            return (int)s.size();
        }
        
        // 如果不全为同一字符，则看 a,b,c 的奇偶性，全奇或全偶则结果为 2，否则为 1
        bool a_even = true;
        bool b_even = true;
        bool c_even = true;
        
        for (int i = 0; i < s.size(); i++) {
            // 遇到 a/b/c 则改变 a/b/c 的奇偶性
            if (s[i] == 'a') {
                a_even = !a_even;
            } else if (s[i] == 'b') {
                b_even = !b_even;
            } else if (s[i] == 'c') {
                c_even = !c_even;
            } else {
                continue; // Other Characters
            }
        }
        
        if ((a_even && b_even && c_even) ||
            (!a_even && !b_even && !c_even)) {
            return 2; // 全奇或全偶则结果为 2
        } else {
            return 1; // 否则为 1
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // Case 1 预期结果 1
//    string s = "aaabbcccaccaccabbb"; // -> "acab" 1
    
    // Case 2 预期结果 1
    string s = "bacbbbbccbbcbbcabbbbb"; // -> "bacab" 1
    
    // Case 3 预期结果 5
//    string s = "aaaaa";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->MinRest(s);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
