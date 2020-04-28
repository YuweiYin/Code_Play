//
//  main.cpp
//  Prob1012_Integer_to_Roman
//
//  Created by 阴昱为 on 2019/6/7.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//12. Integer to Roman
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
//
//I can be placed before V (5) and X (10) to make 4 and 9.
//X can be placed before L (50) and C (100) to make 40 and 90.
//C can be placed before D (500) and M (1000) to make 400 and 900.
//Given an integer, convert it to a roman numeral. Input is guaranteed to be within the range from 1 to 3999.
//
//罗马数字包含以下七种字符： I， V， X， L，C，D 和 M。
//例如， 罗马数字 2 写做 II ，即为两个并列的 1。12 写做 XII ，即为 X + II 。 27 写做  XXVII, 即为 XX + V + II 。
//
//通常情况下，罗马数字中小的数字在大的数字的右边。但也存在特例，例如 4 不写做 IIII，而是 IV。数字 1 在数字 5 的左边，所表示的数等于大数 5 减小数 1 得到的数值 4 。同样地，数字 9 表示为 IX。这个特殊的规则只适用于以下六种情况：
//
//I 可以放在 V (5) 和 X (10) 的左边，来表示 4 和 9。
//X 可以放在 L (50) 和 C (100) 的左边，来表示 40 和 90。
//C 可以放在 D (500) 和 M (1000) 的左边，来表示 400 和 900。
//给定一个整数，将其转为罗马数字。输入确保在 1 到 3999 的范围内。
//
//Example 1:
//Input: 3
//Output: "III"
//
//Example 2:
//Input: 4
//Output: "IV"
//
//Example 3:
//Input: 9
//Output: "IX"
//
//Example 4:
//Input: 58
//Output: "LVIII"
//Explanation: L = 50, V = 5, III = 3.
//
//Example 5:
//Input: 1994
//Output: "MCMXCIV"
//Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.

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
    string intToRoman(int num) {
        return this->solution1(num);
    }
    
private:
    // 方法一：哈希法
    string solution1 (int num) {
        string res = "";
        vector<tuple<int, string>> dict = {
            make_tuple<int, string>(1000, "M"),
            make_tuple<int, string>(900, "CM"),
            make_tuple<int, string>(500, "D"),
            make_tuple<int, string>(400, "CD"),
            make_tuple<int, string>(100, "C"),
            make_tuple<int, string>(90, "XC"),
            make_tuple<int, string>(50, "L"),
            make_tuple<int, string>(40, "XL"),
            make_tuple<int, string>(10, "X"),
            make_tuple<int, string>(9, "IX"),
            make_tuple<int, string>(5, "V"),
            make_tuple<int, string>(4, "IV"),
            make_tuple<int, string>(1, "I")
        };
        
        int i = 0;
        // 从高数字往低找
        while (num > 0 && i < (int)dict.size()) {
            // 当前数字值大于该罗马数值
            if (num >= get<0>(dict[i])) {
                // 将罗马字符表示添加到结果
                res += get<1>(dict[i]);
                // 减去该罗马数值
                num -= get<0>(dict[i]);
            } else {
                i++;
            }
        }
        
        return res;
    }
    
    // 方法二：每一位转换
    string solution2 (int num) {
        string res = "";
        
        int count = 1;
        while (num > 0) {
            // 取出最末一位数字
            int n = num % 10;
            
            res = this->convert(count, n) + res;
            
            count ++;
            num /= 10;
        }
        
        return res;
    }
    
    // 1~9 对应转换
    string convert (int count, int n) {
        string s1 = "", s2 = "", s3 = "", res = "";
        switch (count) {
            case 1:
                s1 = "I";
                s2 = "V";
                s3 = "X";
                break;
            case 2:
                s1 = "X";
                s2 = "L";
                s3 = "C";
                break;
            case 3:
                s1 = "C";
                s2 = "D";
                s3 = "M";
                break;
            case 4:
                s1 = "M";
                break;
                
            default:
                return "";
        }
        
        switch (n) {
            case 0:
                res = "";
                break;
            case 1:
                res = s1;
                break;
            case 2:
                res = s1 + s1;
                break;
            case 3:
                res = s1 + s1 + s1;
                break;
            case 4:
                res = s1 + s2;
                break;
            case 5:
                res = s2;
                break;
            case 6:
                res = s2 + s1;
                break;
            case 7:
                res = s2 + s1 + s1;
                break;
            case 8:
                res = s2 + s1 + s1 + s1;
                break;
            case 9:
                res = s1 + s3;
                break;
                
            default:
                return "";
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
    int num = 1989;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->intToRoman(num) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
