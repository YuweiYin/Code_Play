//
//  main.cpp
//  Prob1072_Edit_Distance
//
//  Created by 阴昱为 on 2019/8/12.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//72. Edit Distance
//
//Given two words word1 and word2, find the minimum number of operations required to convert word1 to word2.
//You have the following 3 operations permitted on a word:
//    1. Insert a character
//    2. Delete a character
//    3. Replace a character
//
//给定两个单词 word1 和 word2，计算出将 word1 转换成 word2 所使用的最少操作数 。
//你可以对一个单词进行如下三种操作：
//    1. 插入一个字符
//    2. 删除一个字符
//    3. 替换一个字符
//
//Example 1:
//    Input: word1 = "horse", word2 = "ros"
//    Output: 3
//    Explanation:
//    horse -> rorse (replace 'h' with 'r')
//    rorse -> rose (remove 'r')
//    rose -> ros (remove 'e')
//
//Example 2:
//    Input: word1 = "intention", word2 = "execution"
//    Output: 5
//    Explanation:
//    intention -> inention (remove 't')
//    inention -> enention (replace 'i' with 'e')
//    enention -> exention (replace 'n' with 'x')
//    exention -> exection (replace 'n' with 'c')
//    exection -> execution (insert 'u')


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
    int minDistance(string word1, string word2) {
        return this->solution1(word1, word2);
    }
    
private:
    // 方法一。动态规划。时间复杂度 O(M*N)，空间复杂度 O(M*N)。M = word1.size, N = word2.size
    // 执行用时 : 20 ms , 在所有 C++ 提交中击败了 64.87% 的用户
    // 内存消耗 : 11.2 MB , 在所有 C++ 提交中击败了 35.30% 的用户
    // Runtime: 12 ms, faster than 67.54% of C++ online submissions for Edit Distance.
    // Memory Usage: 11.2 MB, less than 65.63% of C++ online submissions for Edit Distance.
    int solution1 (string& word1, string& word2) {
        // 边界情况
        if (word1 == word2) {
            return 0;
        }
        
        int len1 = (int)word1.size();
        int len2 = (int)word2.size();
        
        if (len1 == 0) {
            return len2;
        }
        
        if (len2 == 0) {
            return len1;
        }
        
        vector<vector<int>> dp(len1 + 1, vector<int>(len2 + 1));
        
        // 初始化编辑距离
        for (int i = 0; i < len1 + 1; i++) {
            // 从 word1 的前 i 个字符组成的单词变成 0 个字符的单词，需要 i 步操作
            dp[i][0] = i;
        }
        for (int j = 0; j < len2 + 1; j++) {
            // 从 0 个字符的单词变成 word2 的前 j 个字符组成的单词，需要 j 步操作
            dp[0][j] = j;
        }
        
        // 动态规划计算
        int insert_char = 0, delete_char = 0, replace_char = 0;
        for (int i = 1; i < len1 + 1; i++) {
            for (int j = 1; j < len2 + 1; j++) {
                insert_char = dp[i - 1][j] + 1; // 插入字符到 word1
                delete_char = dp[i][j - 1] + 1; // 从 word1 删除字符
                replace_char = dp[i - 1][j - 1]; // 两边均插入一个字符
                
                // 在两边均插入一个字符的情况下，如果当前字符是不同的，
                // 则可以通过额外的一步替换操作来使两边插入的字符相同。
                if (word1[i - 1] != word2[j - 1]) {
                    replace_char ++;
                }
                
                // 三种操作中取最小代价，更新 DP 表
                dp[i][j] = min(insert_char, min(delete_char, replace_char));
            }
        }
        
        return dp[len1][len2];
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string word1 = "horse", word2 = "ros"; // 预期结果 3
    string word1 = "intention", word2 = "execution"; // 预期结果 5
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->minDistance(word1, word2);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
