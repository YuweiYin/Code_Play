//
//  main.cpp
//  Prob1058_Length_of_Last_Word
//
//  Created by 阴昱为 on 2019/7/25.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//58. Length of Last Word
//
//Given a string s consists of upper/lower-case alphabets and empty space characters ' ', return the length of last word in the string.
//If the last word does not exist, return 0.
//Note: A word is defined as a character sequence consists of non-space characters only.
//
//给定一个仅包含大小写字母和空格 ' ' 的字符串，返回其最后一个单词的长度。
//如果不存在最后一个单词，请返回 0 。
//说明：一个单词是指由字母组成，但不包含任何空格的字符串。
//
//Example:
//    Input: "Hello World"
//    Output: 5


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
    int lengthOfLastWord(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一。时间复杂度 O(N)，空间复杂度 O(1)。N = s.size
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.6 MB , 在所有 C++ 提交中击败了 88.52% 的用户
    // Runtime: 4 ms, faster than 77.25% of C++ online submissions for Length of Last Word.
    // Memory Usage: 8.7 MB, less than 60.85% of C++ online submissions for Length of Last Word.
    int solution1 (string s) {
        // 边界情况
        if (s.empty()) {
            return 0;
        }
        
        int res = 0;
        int r_index = (int)s.size() - 1; // 从右往左扫描
        
        // 不考虑末尾的 ' '
        if (s[r_index] == ' ') {
            r_index --;
            
            while (r_index >= 0 && s[r_index] == ' ') {
                r_index --;
            }
        }
        
        // 整个 s 全为空格
        if (r_index < 0) {
            return 0;
        }
        
        // 扫描最后一个单词
        while (r_index >= 0 && s[r_index] != ' ') {
            res ++;
            r_index --;
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
    // 预期结果 5
    string s = "Hello World";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->lengthOfLastWord(s);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
