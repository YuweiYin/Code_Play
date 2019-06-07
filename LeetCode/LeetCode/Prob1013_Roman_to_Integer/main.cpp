//
//  main.cpp
//  Prob1013_Roman_to_Integer
//
//  Created by 阴昱为 on 2019/6/7.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//13. Roman to Integer
//
//Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
//    Symbol       Value
//    I             1
//    V             5
//    X             10
//    L             50
//    C             100
//    D             500
//    M             1000
//For example, two is written as II in Roman numeral, just two one's added together. Twelve is written as, XII, which is simply X + II. The number twenty seven is written as XXVII, which is XX + V + II.
//Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:
//I can be placed before V (5) and X (10) to make 4 and 9.
//X can be placed before L (50) and C (100) to make 40 and 90.
//C can be placed before D (500) and M (1000) to make 400 and 900.
//Given a roman numeral, convert it to an integer. Input is guaranteed to be within the range from 1 to 3999.
//
//例如， 罗马数字 2 写做 II ，即为两个并列的 1。12 写做 XII ，即为 X + II 。 27 写做  XXVII, 即为 XX + V + II 。
//通常情况下，罗马数字中小的数字在大的数字的右边。但也存在特例，例如 4 不写做 IIII，而是 IV。数字 1 在数字 5 的左边，所表示的数等于大数 5 减小数 1 得到的数值 4 。同样地，数字 9 表示为 IX。这个特殊的规则只适用于以下六种情况：
//
//I 可以放在 V (5) 和 X (10) 的左边，来表示 4 和 9。
//X 可以放在 L (50) 和 C (100) 的左边，来表示 40 和 90。
//C 可以放在 D (500) 和 M (1000) 的左边，来表示 400 和 900。
//给定一个罗马数字，将其转换成整数。输入确保在 1 到 3999 的范围内。
//
//Example 1:
//    Input: "III"
//    Output: 3
//
//Example 2:
//    Input: "IV"
//    Output: 4
//
//Example 3:
//    Input: "IX"
//    Output: 9
//
//Example 4:
//    Input: "LVIII"
//    Output: 58
//    Explanation: L = 50, V= 5, III = 3.
//
//Example 5:
//    Input: "MCMXCIV"
//    Output: 1994
//    Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.

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
    int romanToInt(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一：哈希法
    int solution1 (string s) {
        int res = 0;
        
//        map<string, int> dict = {
//            make_pair<string, int>("M", 1000),
//            make_pair<string, int>("CM", 900),
//            make_pair<string, int>("D", 500),
//            make_pair<string, int>("CD", 400),
//            make_pair<string, int>("C", 100),
//            make_pair<string, int>("XC", 90),
//            make_pair<string, int>("L", 50),
//            make_pair<string, int>("XL", 40),
//            make_pair<string, int>("X", 10),
//            make_pair<string, int>("IX", 9),
//            make_pair<string, int>("V", 5),
//            make_pair<string, int>("IV", 4),
//            make_pair<string, int>("I", 1)
//        };
        map<string, int> dict = {
            {"M", 1000}, {"CM", 900}, {"D", 500}, {"CD", 400},
            {"C", 100}, {"XC", 90}, {"L", 50}, {"XL", 40},
            {"X", 10}, {"IX", 9}, {"V", 5}, {"IV", 4}, {"I", 1}
        };
        
        // 从前往后匹配
        while (!s.empty()) {
            if (dict.find(s.substr(0, 2)) != dict.end()) {
                // 先找两位字符的罗马字符
                // 找到后把该罗马字符对应的数值加到结果中
                res += dict[s.substr(0, 2)];
                // 删去这两个字符
                s.erase(0, 2);
            } else if (dict.find(s.substr(0, 1)) != dict.end()) {
                // 如果两位字符不匹配，则找一位字符的罗马字符
                res += dict[s.substr(0, 1)];
                s.erase(0, 1);
            } else {
                break;
            }
        }
        
        return res;
    }
    
    // 方法二：无序哈希表
    int solution2 (string s) {
        // 注意：此时的 IX、XC、CM 不是 9、90、900 而是 8、80、800
        // IV、XL、CD 不是 4、40、400 而是 3、30、300
        // 这样 index 就可以一次往后移动一位，每一位都加
        // 比如遇到 I，先加一个 1，之后一位如果是 V，那么发现这两位是 IV，
        // 此时加 3 就够了，二者结合起来就是加 4，效果相同。
        unordered_map<string, int> dict = {
            {"I", 1}, {"IV", 3}, {"V", 5}, {"IX", 8},
            {"X", 10}, {"XL", 30}, {"L", 50}, {"XC", 80},
            {"C", 100}, {"CD", 300}, {"D", 500}, {"CM", 800},
            {"M", 1000}
        };
        
        int res = 0;
        if (s.empty()) {
            return res;
        }
        
        // 先把第一位加上去
        res += dict[s.substr(0, 1)];
        
        for(int i = 1; i < (int)s.size(); i++) {
            // 当前字符
            string one_char = s.substr(i, 1);
            // 组合前一字符加当前字符
            string two_char = s.substr(i - 1, 2);
            // 如果组合字符存在，则加上组合字符代表的值，否则加上当前字符代表的值
            res += dict[two_char] ? dict[two_char] : dict[one_char];
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
    string s = "MCMLXXXIX";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->romanToInt(s) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
