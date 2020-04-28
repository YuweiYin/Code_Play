//
//  main.cpp
//  Prob1541_Reverse_String_II
//
//  Created by 阴昱为 on 2019/6/19.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1541. Reverse String II
//
//Given a string and an integer k, you need to reverse the first k characters for every 2k characters counting from the start of the string. If there are less than k characters left, reverse all of them. If there are less than 2k but greater than or equal to k characters, then reverse the first k characters and left the other as original.
//
//给定一个字符串和一个整数 k，你需要对从字符串开头算起的每个 2k 个字符的前k个字符进行反转。如果剩余少于 k 个字符，则将剩余的所有全部反转。如果有小于 2k 但大于或等于 k 个字符，则反转前 k 个字符，并将剩余的字符保持原样。
//
//Example:
//    Input: s = "abcdefg", k = 2
//    Output: "bacdfeg"
//
//Restrictions:
//    The string consists of lower English letters only.
//    Length of the given string and k will in the range [1, 10000]
//要求:
//    该字符串只包含小写的英文字母。
//    给定字符串的长度和 k 在[1, 10000]范围内。


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
    string reverseStr(string s, int k) {
        return this->solution1(s, k);
    }
    
private:
    // 方法一。跳跃双指针夹逼，若前后找到两个不同的字符则交换。
    // 时间复杂度 O(N)，空间复杂度 O(1)
    // Runtime: 8 ms, faster than 82.76% of C++ online submissions for Reverse String II.
    // Memory Usage: 9.6 MB, less than 47.22% of C++ online submissions for Reverse String II.
    string solution1 (string s, int k) {
        if (s.empty() || (int)s.size() == 1 || k <= 1) {
            return s;
        }
        
        int s_len = (int)s.size();
        int k_2 = k << 1;
        
        int left;
        int right;
        
        for (int i = 0; i < s_len;) {
            if (i + k_2 < s_len) {
                // 剩余的数目比 2k 还多，未到尾部
                left = i;
                right = i + k - 1;
                
                while (left < right) {
                    this->mySwap(s, left++, right--);
                }
                
                i += k_2;
            } else if (i + k >= s_len) {
                // 剩余的数目小于等于 k，所以把这些全部反转即可
                left = i;
                right = s_len - 1;
                
                while (left < right) {
                    this->mySwap(s, left++, right--);
                }
                
                break;
            } else {
                // 剩余的数目小于等于 2k，但大于 k，只把前 k 个反转即可
                left = i;
                right = i + k - 1;
                
                while (left < right) {
                    this->mySwap(s, left++, right--);
                }
                
                break;
            }
        }
        
        return s;
    }
    
    // 如果 s[i] 不等于 s[j]，则交换之
    void mySwap (string& s, int i, int j) {
        if (s[i] != s[j]) {
            s[i] = s[i] ^ s[j];
            s[j] = s[i] ^ s[j];
            s[i] = s[i] ^ s[j];
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    string s = "abcdefg"; // 预期结果 "bacdfeg"
    int k = 2;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->reverseStr(s, k);
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
