//
//  main.cpp
//  Prob1005_Longest_Palindromic_Substring
//
//  Created by 阴昱为 on 2019/5/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//


//5. Longest Palindromic Substring
//
//Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.
//
//给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。
//
//Example1:
//  Input: "babad"
//  Output: "bab"
//  Note: "aba" is also a valid answer.
//
//Example2:
//  Input: "cbbd"
//  Output: "bb"


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


class Solution {
public:
    // 无参构造函数
    Solution () {
        this->best_substring = "";
        this->max_len = 0;
    }
    
    // 含参构造函数
    Solution (string best_substring, int max_len) {
        this->best_substring = best_substring;
        this->max_len = max_len;
    }
    
    // LeetCode 处理入口函数
    string longestPalindrome (string s) {
        string ans = "";
        
//        if (this->manacher(s) >= 0) {
//            ans = this->best_substring;
//        }
        
//        ans = this->solution1(s);
//        ans = this->solution2(s);
//        ans = this->solution3(s);
        ans = this->solution4(s);
        
        return ans;
    }
    
    // Manacher 算法核心过程
    // TODO 计算回文串长度最大值时没问题，但是获取最长回文串时有问题
    // 对偶数次连续重复的字符如 aaaa 和 aaaaaa 等，结果只是 aa
    int manacher (string s) {
        if (s.empty()){
            return -1;
        }
        
        string manacher_string = this->initManacherString(s); // 把 s 改成 Manacher 字符串
        int best_index = -1; // 最长回文串所在的 radius 和 substring 数组坐标
        int radius[manacher_string.length()]; // 以每个字符为中心的最长回文串的半径
        string substring[manacher_string.length()]; // 以每个字符串为中心的最长回文串
        for (int i = 0; i < manacher_string.length(); i++) {
            radius[i] = 0;
            substring[i] = "";
        }
        
        int R = -1;
        int c = -1;
        int cur_len = 0;
        
        // 遍历一遍
        for (int i = 0; i < manacher_string.length(); i++) {
            string cur_substring = "";
            if (manacher_string[i] != '#') {
                cur_substring += manacher_string[i];
            }
            cout << "init_cur_substring = " << cur_substring << endl;
            
            radius[i] = R > i ? min(radius[2 * c - i], R - i + 1): 1;
            cout << "radius[" << i << "] = " << radius[i] << endl;
            cout << "manacher_string[" << i << "] = " << manacher_string[i] << endl;
            
            // 循环判断条件：坐标 i + radius[i] 和 i - radius[i] 不越界
            while(i + radius[i] < manacher_string.length() && i - radius[i] >= 0) {
                // 判断：两端字符相同
                if (manacher_string[i - radius[i]] == manacher_string[i + radius[i]]) {
                    char match_char = manacher_string[i - radius[i]];
                    cout << "match_char = " << match_char << endl;
                    
                    // 如果匹配的字符不是 '#'，就把匹配到的字符加在本轮回文串两端
                    if (match_char != '#') {
                        cur_substring = match_char + cur_substring + match_char;
                    }
                    radius[i] ++; // 回文串半径自增 1
                } else {
                    // 不匹配则退出，本轮回文串就记录到此为止
                    break;
                }
            }
            
            // 记录当前的回文串到数组
            substring[i] = cur_substring;
            
            if (i + radius[i] > R) {
                R = i + radius[i] - 1;
                c = i;
            }
            
            if (radius[i] > cur_len) {
                cur_len = radius[i];
                best_index = i;
            }
        }
        
        if (best_index < 0) {
            this->best_substring = "";
        } else {
            this->best_substring = substring[best_index];
        }
        
        for (int i = 0; i < manacher_string.length(); i++) {
            cout << "substring[" << i << "] = " << substring[i] << endl;
        }
        cout << "best_index = " << best_index << endl;
        
        // cout << "this->best_substring = " << this->best_substring << endl;
        
        this->max_len = cur_len - 1;
        return this->max_len;
    }
    
    // 解法1：暴力法，O(n^3)
    string solution1 (string s) {
        string res = ""; // 存放结果
        string temp = ""; // 存放子串
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; j < s.length(); j++) {
                temp = temp + s[j];
                string rev = temp; // rev存放子串反转结果
                reverse(rev.begin(), rev.end()); // 反转
                if (temp == rev) {
                    res = res.length() > temp.length() ? res : temp;
                }
            }
            temp = "";
        }
        return res;
    }
    
    // 解法2：反转法，O(n^3)，稍好于暴力法
    // 将字符串s反转得到字符串rev，再求他们的最长公共子串，
    // 再判断该最长公共子串是否就是我们要找的最长回文子串。
    string solution2(string s) {
        if (s.length() == 1) {
            // 大小为1的字符串必为回文串
            return s;
        }
        string rev = s; // rev存放s反转结果
        string res; // 存放结果
        reverse(rev.begin(), rev.end()); // 反转
        if (rev == s) {
            return s;
        }
        
        int len = 0; // 存放回文子串的长度
        // 查找s与rev的最长公共子串
        for (int i = 0; i < s.length(); i++) {
            string temp; // 存放待验证子串
            for (int j = i; j < s.length(); j++) {
                temp = temp + s[j];
                if (len >= temp.length()) {
                    continue;
                } else if(rev.find(temp)!=-1) {
                    // 在rev中找到temp
                    string q = temp; // q用来验证temp是否是回文子串
                    reverse(q.begin(), q.end());
                    if (q == temp) {
                        len = (int)temp.length();
                        res = temp;
                    }
                } else {
                    break;
                }
            }
            temp="";
        }
        
        return res;
    }
    
    // 解法3：动态规划DP，O(n^2)，但是DP表耗费内存
    string solution3(string s) {
        int len = (int)s.size();
        if (len == 0 || len == 1) {
            return s;
        }
        
        int start = 0; // 回文串起始位置
        int max_len = 1; // 回文串最大长度
        vector<vector<int>>  dp(len, vector<int>(len)); // 定义二维动态数组，DP表
        
        // 初始化DP表，dp[i][j] == 1 表示从下标 i 到下标 j 的子串是回文串
        for (int i = 0; i < len; i++) {
            // 单个字符是回文串
            dp[i][i] = 1;
            
            // 连续两个相同字符是回文串
            if (i < len - 1 && s[i] == s[i + 1]) {
                dp[i][i + 1] = 1;
                max_len = 2;
                start = i;
            }
        }
        
        // l 表示检索的子串长度，等于 3 表示先检索长度为 3 的子串
        for (int l = 3; l <= len; l++) {
            for (int i = 0; i + l - 1 < len; i++) {
                int j = i + l - 1; // 长度为 l 的子串终止字符位置
                
                // 判断：该子串两端字符相同，并且中间的子串是回文串
                if(s[i] == s[j] && dp[i + 1][j - 1] == 1) {
                    // 状态转移
                    dp[i][j] = 1; // 记录：从下标 i 到下标 j 的子串是回文串
                    start = i;
                    max_len = l; // l 是只增不减的，保证最终 max 值为最大长度
                }
            }
        }
        
        return s.substr(start, max_len); // 获取最长回文子串
    }
    
    // 解法4：中心扩展法，O(n^2)，空间效率大幅优于DP，时间效率也略高于DP
    // 回文中心的两侧互为镜像。因此回文可以从他的中心展开，并且只有2n-1个这样的中心
    // (一个元素为中心的情况有n个，两个元素为中心的情况有n-1个)
    string solution4 (string s) {
        int len = (int)s.size();
        if (len == 0 || len == 1) {
            return s;
        }
        
        int start = 0; // 记录最长回文子串起始位置
        int end = 0; // 记录最长回文子串终止位置
        int max_len = 0; // 记录最大回文子串的长度
        
        for (int i = 0; i < len; i++) {
            // 计算以 left 和 right 为中心字符坐标的回文串长度
            int len1 = this->countLengthOfPalindrome(s, i, i); // 一个元素为中心
            int len2 = this->countLengthOfPalindrome(s, i, i + 1); // 两个元素为中心
            
            // 记录最大长度
            int cur_len = max(len1, len2);
            if (max_len < cur_len) {
                max_len = cur_len;
            }
            
            // 修改最长回文串的起始位置 start、终止位置 end
            if (max_len > end - start + 1) {
                start = i - (int)((max_len - 1) / 2);
                end = i + (int)(max_len / 2);
            }
        }
        
        // 获取从 start 开始，长度为 mlen 长度的字符串，即最长回文串
        return s.substr(start, max_len);
    }
    
private:
    // const int MAX_LEN = 1000;
    string best_substring;
    int max_len;
    
    // Manacher 算法初始化，把字符'#'加在每两个字符之间、以及字符串两端
    string initManacherString (string s) {
        string str = "#";
        for (int i = 0; i < s.length(); i++) {
            str += s[i];
            str += "#";
        }
        return str;
    }
    
    // 计算以 left 和 right 为中心字符坐标的回文串长度
    // left == right 表示以一个字符为中心，否则是以相邻的两个字符为中心
    int countLengthOfPalindrome (string &s, int left, int right) {
        int L = left;
        int R = right;
        
        // 循环判断条件：L 和 R 不越界，并且此时两端的字符相同
        while (L >= 0 && R < s.length() && s[R] == s[L]) {
            // 增大子串范围
            L --;
            R ++;
        }
        
        return R - L - 1;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    string s = "fcbaaaaaabcd";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->longestPalindrome(s) << endl;
    // cout << solution->manacher(s) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
