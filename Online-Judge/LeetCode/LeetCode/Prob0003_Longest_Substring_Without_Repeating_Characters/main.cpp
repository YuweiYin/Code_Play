//
//  main.cpp
//  Prob1003_Longest_Substring_Without_Repeating_Characters
//
//  Created by 阴昱为 on 2019/5/29.
//  Copyright © 2019 阴昱为. All rights reserved.
//


//3. Longest Substring Without Repeating Characters
//
//Given a string, find the length of the longest substring without repeating characters.
//
//给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
//
//Example1:
//  Input: "abcabcbb"
//  Output: 3
//  Explanation: The answer is "abc", with the length of 3.
//
//Example2:
//  Input: "bbbbb"
//  Output: 1
//  Explanation: The answer is "b", with the length of 1.
//
//Example3:
//  Input: "pwwkew"
//  Output: 3
//  Explanation: The answer is "wke", with the length of 3.
//  Note that the answer must be a substring, "pwke" is a subsequence and not a substring.


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
    int lengthOfLongestSubstring(string s) {
        
//        这道题主要用到思路是：滑动窗口
//        什么是滑动窗口？
//        其实就是一个队列，比如例题中的 abcabcbb，进入这个队列（窗口）为 abc 满足题目要求，
//        当再进入 a，队列变成了 abca，这时候不满足要求。所以，我们要移动这个队列！
//
//        如何移动？
//        我们只要把队列的左边的元素移出就行了，直到满足题目要求！
//        一直维持这样的队列，找出队列出现最长的长度时候，求出解！
//        时间复杂度：O(n)
        
        if(s.size() == 0) {
            return 0;
        }
        
        unordered_set<char> lookup; // 用哈希乱序集合，记录已经查看过的字符
        int maxLen = 0; // 记录最大的窗口长度
        int curLen = 0; // 记录当前窗口的长度
        int left = 0; // 记录滑动窗口的左边沿坐标
        
        for(int i = 0; i < s.size(); i++){
            // 循环停止条件：当前滑动窗口右边沿字符 s[i] 是不重复的（乱序集合中 find 不到）
            while (lookup.find(s[i]) != lookup.end()) {
                // 此时窗口右边沿字符 s[i] 是重复的，需要不断右移左边沿 left ++
                // 使得当前右边沿字符 s[i] 不再是重复的
                // 移动之前，先把当前左边沿字符 s[left] 从集合中移除
                lookup.erase(s[left]);
                left ++;
            }
            
            // 此时滑动窗口内的字符都不重复，计算此时的滑动窗口大小
            curLen = i - left + 1;
            
            // 判断是否更新最优解
            // maxLen = max(maxLen, i - left + 1);
            if (curLen > maxLen) {
                maxLen = curLen;
            }
            
            // 现在，当前的右边沿字符是已经历过的字符，需要加入集合
            lookup.insert(s[i]);
        }
        
        return maxLen;
    }
};


int main(int argc, const char * argv[]) {
    // 设置测试数据
    string test1 = "abcabcbb";
    string test2 = "bbbbb";
    string test3 = "pwwkew";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->lengthOfLongestSubstring(test1) << endl;
    cout << solution->lengthOfLongestSubstring(test2) << endl;
    cout << solution->lengthOfLongestSubstring(test3) << endl;
    
    return 0;
}
