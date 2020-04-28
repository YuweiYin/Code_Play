//
//  main.cpp
//  Prob1009_Palindrome_Number
//
//  Created by 阴昱为 on 2019/6/3.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//9. Palindrome Number
//
//Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.

//判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
//
//Example1:
//  Input: 121
//  Output: true
//
//Example2:
//  Input: -121
//  Output: false
//  Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
//
//Example3:
//  Input: 10
//  Output: false
//  Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
//
//Follow up:
//Coud you solve it without converting the integer to a string?
//进阶:
//你能不将整数转为字符串来解决这个问题吗？


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
    bool isPalindrome(int x) {
        return this->solution2(x);
    }
    
    bool isPalindrome(string x) {
        return this->solutionString(x);
    }
    
    // 判断数字是否为回文数-方法一。时间复杂度 O(n), 空间复杂度 O(1)
    bool solution1 (int x) {
        if (x == 0) {
            return true;
        }
        
        // 特殊情况：
        // 当 x < 0 时，x 不是回文数。
        // 同样地，如果数字的最后一位是 0，为了使该数字为回文，
        // 则其第一位数字也应该是 0。只有 0 满足这一属性
        if(x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }
        
        bool res = true;
        vector<int> x_list{};
        int temp = x;
        
        // 用向量存储每位数字
        while (temp > 0) {
            x_list.push_back(temp % 10);
            temp = (int)(temp / 10);
        }
        
        // 判断数字首末位是否相等
        for (vector<int>::iterator ite = x_list.begin(); (int)x_list.size() >= 2; ite++) {
            if (*x_list.begin() != *(x_list.end() - 1)) {
                return false;
            } else {
                x_list.erase(x_list.begin());
                x_list.erase(x_list.end() - 1);
            }
        }
        
        return res;
    }
    
    // 判断数字是否为回文数-方法二。时间复杂度 O(log_10(n)), 空间复杂度 O(1)
    bool solution2 (int x) {
        if(x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }
        
        int rev = 0;
        while(x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }
        
        // 当数字长度为奇数时，我们可以通过 revertedNumber/10 去除处于中位的数字。
        // 例如，当输入为 12321 时，在 while 循环的末尾我们可以得到 x = 12，revertedNumber = 123，
        // 由于处于中位的数字不影响回文（它总是与自己相等），所以我们可以简单地将其去除。
        return x == rev || x == rev / 10;
    }
    
    // 判断字符串是否为回文串。时间复杂度 , 空间复杂度
    bool solutionString (string x) {
        return false;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    int x = 123321;
    // string y = "abcba";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->isPalindrome(x) << endl;
    // cout << solution->isPalindrome(y) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
