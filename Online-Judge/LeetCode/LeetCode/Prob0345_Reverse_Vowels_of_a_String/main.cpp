//
//  main.cpp
//  Prob1345_Reverse_Vowels_of_a_String
//
//  Created by 阴昱为 on 2019/6/19.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1345. Reverse Vowels of a String
//
//Write a function that takes a string as input and reverse only the vowels of a string.
//
//编写一个函数，以字符串作为输入，反转该字符串中的元音字母。
//
//Example 1:
//    Input: "hello"
//    Output: "holle"
//
//Example 2:
//    Input: "leetcode"
//    Output: "leotcede"
//
//Note:
//    The vowels does not include the letter "y".
//说明:
//    元音字母不包含字母"y"。


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
//    set<char> vowels_set = {'a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U'};
    
public:
    string reverseVowels(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一。双指针头尾夹逼，逐个判断是否元音字母吗，若前后找到两个不同的元音字母则交换。
    // 时间复杂度 O(N)，空间复杂度 O(1)
    // Runtime: 8 ms, faster than 96.64% of C++ online submissions for Reverse Vowels of a String.
    // Memory Usage: 10 MB, less than 59.97% of C++ online submissions for Reverse Vowels of a String.
    string solution1 (string s) {
        if (s.empty() || (int)s.size() == 1) {
            return s;
        }
        
        int len = (int)s.size();
        int i = 0;
        int j = len - 1;
        string vowels_str = "AEIOUaeiou";
        auto npos = vowels_str.npos;
        
        // 双指针头尾夹逼。重点：提升判断是否元音字母的效率、以及交换效率
        while (i < j) {
            // 从左到右找到一个元音字母
            while (i < j && vowels_str.find(s[i]) == npos) {
//            while (i < j && this->vowels_set.find(s[i]) == this->vowels_set.end()) {
                i ++;
            }
            
            // 从右到左找到一个元音字母
            while (i < j && vowels_str.find(s[j]) == npos) {
//            while (i < j && this->vowels_set.find(s[j]) == this->vowels_set.end()) {
                j --;
            }
            
            // 如果这两个元音字母不在串中同一位置，且这俩不同，则用按位异或法交换二者
            if (i < j && s[i] != s[j]) {
//                swap(s[i], s[j]);
                s[i] = s[i] ^ s[j];
                s[j] = s[i] ^ s[j];
                s[i] = s[i] ^ s[j];
            }
            i ++;
            j --;
        }
        
        return s;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string s = "hello"; // 预期结果 "holle"
//    string s = "leetcode"; // 预期结果 "leotcede"
    string s = ".,"; // 预期结果 ".,"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->reverseVowels(s);
    if (!ans.empty()) {
        cout << ans << endl;
    } else {
        cout << "String ans is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
