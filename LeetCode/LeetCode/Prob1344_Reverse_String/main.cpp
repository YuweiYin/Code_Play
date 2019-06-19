//
//  main.cpp
//  Prob1344_Reverse_String
//
//  Created by 阴昱为 on 2019/6/19.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1344. Reverse String
//
//Write a function that reverses a string. The input string is given as an array of characters char[].
//Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory.
//You may assume all the characters consist of printable ascii characters.
//
//编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 char[] 的形式给出。
//不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。
//你可以假设数组中的所有字符都是 ASCII 码表中的可打印字符。
//
//Example 1:
//    Input: ["h","e","l","l","o"]
//    Output: ["o","l","l","e","h"]
//
//Example 2:
//    Input: ["H","a","n","n","a","h"]
//    Output: ["h","a","n","n","a","H"]


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
    void reverseString(vector<char>& s) {
        return this->solution3(s);
    }
    
private:
    // 方法一。单指针扫描一半，若不同则交换。时间复杂度 O(N)，空间复杂度 O(1)
    void solution1 (vector<char>& s) {
        if (s.empty() || (int)s.size() == 1) {
            return;
        }
        
        int len = (int)s.size();
        int half = (int)(len / 2);
//        char temp;
        
        for (int i = 0; i < half; i++) {
            if (s[i] != s[len - 1 - i]) {
//                temp = s[i];
//                s[i] = s[len - 1 - i];
//                s[len - 1 - i] = temp;
                swap(s[i], s[len - 1 - i]);
            }
        }
    }
    
    // 方法二。双指针头尾夹逼，若不同则交换。时间复杂度 O(N)，空间复杂度 O(1)
    void solution2 (vector<char>& s) {
        if (s.empty() || (int)s.size() == 1) {
            return;
        }
        
        int i = 0;
        int j = (int)s.size() - 1;
//        char temp;
        
        // 省去了计算 len - 1 - i 的耗时
        while (i < j) {
            if (s[i] != s[j]) {
//                temp = s[i];
//                s[i] = s[j];
//                s[j] = temp;
                swap(s[i], s[j]);
            }
            i ++;
            j --;
        }
    }
    
    // 方法三。按位异或交换法，最快。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 60 ms , 在所有 C++ 提交中击败了 97.02% 的用户
    // 内存消耗 : 15.3 MB , 在所有 C++ 提交中击败了 74.29% 的用户
    void solution3 (vector<char>& s) {
        int i = 0;
        int j = (int)s.size() - 1;
        while (i < j) {
            s[i] = s[i] ^ s[j];
            s[j] = s[i] ^ s[j];
            s[i] = s[i] ^ s[j];
            i ++;
            j --;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<char> s = {'h', 'e', 'l', 'l', 'o'}; // 预期结果 ["o","l","l","e","h"]
//    vector<char> s = {'H', 'a', 'n', 'n', 'a', 'h'}; // 预期结果 ["h","a","n","n","a","H"]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->reverseString(s);
    if (!s.empty()) {
        for (int i = 0; i < (int)s.size(); i++) {
            cout << s[i] << ", ";
        }
        cout << "End." << endl;
    } else {
        cout << "Vector s is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
