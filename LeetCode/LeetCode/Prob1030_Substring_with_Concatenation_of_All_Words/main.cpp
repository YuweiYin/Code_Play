//
//  main.cpp
//  Prob1030_Substring_with_Concatenation_of_All_Words
//
//  Created by 阴昱为 on 2019/6/29.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//30. Substring with Concatenation of All Words
//
//You are given a string, s, and a list of words, words, that are all of the same length. Find all starting indices of substring(s) in s that is a concatenation of each word in words exactly once and without any intervening characters.

//给定一个字符串 s 和一些长度相同的单词 words。找出 s 中恰好可以由 words 中所有单词串联形成的子串的起始位置。
//注意子串要与 words 中的单词完全匹配，中间不能有其他字符，但不需要考虑 words 中单词串联的顺序。
//
//Example 1:
//    Input:
//        s = "barfoothefoobarman",
//        words = ["foo","bar"]
//    Output: [0,9]
//    Explanation: Substrings starting at index 0 and 9 are "barfoor" and "foobar" respectively.
//    The output order does not matter, returning [9,0] is fine too.
//
//Example 2:
//    Input:
//        s = "wordgoodgoodgoodbestword",
//        words = ["word","good","best","word"]
//    Output: []


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
private:
    int w_len = 0;
    int width = 0;
    
public:
    vector<int> findSubstring(string s, vector<string>& words) {
        return this->solution1(s, words);
    }
    
private:
    // 方法一：。时间复杂度 O()，空间复杂度 O()。N = 
    vector<int> solution1 (string s, vector<string>& words) {
        // 边界情况
        if (s.empty() || words.empty()) {
            return {};
        }
        
//        int s_len = (int)s.size();
        this->w_len = (int)words.size();
        this->width = (int)words[0].size(); // 由题意，各个单词是等长的
        
        vector<int> res = {};
        map<string, int> word_count = {}; // 记录各个单词的个数
        map<string, vector<int>> word_index = {}; // 记录各个单词出现的下标列表
        
        for (int i = 0; i < this->w_len; i++) {
            if (word_count.find(words[i]) == word_count.end()) {
                word_count.insert({words[i], 1});
            } else {
                word_count[words[i]] ++;
            }
            
            if (word_index.find(words[i]) == word_index.end()) {
                word_index.insert({words[i], {}});
            }
            
            auto cur_index = s.find(words[i]); // 找第一个 words[i] 所在的 index
            while (cur_index != string::npos) {
                word_index[words[i]].push_back((int)cur_index);
                cur_index = s.find(words[i], cur_index + this->width); // 继续往后找
            }
        }
        
        cout << "word_count:" << endl;
        for (auto ite = word_count.begin(); ite != word_count.end(); ite++) {
            cout << ite->first << ": " << ite->second << endl;
        }
        
        cout << "\nword_index:" << endl;
        for (auto ite = word_index.begin(); ite != word_index.end(); ite++) {
            cout << ite->first << ": ";
            for (int j = 0; j < (int)(ite->second).size(); j++) {
                cout << ite->second[j] << ", ";
            }
            cout << "End." <<endl;
        }
        cout << "End." <<endl;
        
        this->backtrack(res, s, words, word_count, word_index, 0, 0);
        
        return res;
    }
    
    void backtrack (vector<int>& res, string s, vector<string> words, map<string, int>& word_count,
              map<string, vector<int>> word_index, int depth, int cur_index) {
        // 深度达到 words 列表长度，用尽了所有单词
        if (depth >= this->w_len) {
            res.push_back(cur_index - this->w_len * this->width);
            return;
        }
        
        for (int i = 0; i < this->w_len; i++) {
            if (word_count[words[i]] > 0) {
                // 在 s 中，从 cur_index 开始找单词子串 words[i]
                auto find_word = s.find(words[i], cur_index);
                if (find_word != string::npos) {
                    // 如果找得到，判断是否为连续单词
                    if (cur_index == 0 || (int)find_word == cur_index + this->width - 1) {
                        // cur_index == 0 表示是找到的第一个单词，直接加进来
                        // 如果 cur_index != 0，cur_index 是上个单词起点的下一位置，
                        // 如果与新找到的单词相隔 this->width - 1，则表示是连续单词，则执行回溯法
                        word_count[words[i]] --;
                        
                        this->backtrack(res, s, words, word_count, word_index, depth + 1, (int)find_word + 1);
                        
                        word_count[words[i]] ++;
                    }
                }
            }
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 [0 ,9] 解释：从索引 0 和 9 开始的子串分别是 "barfoor" 和 "foobar"
    // 输出的顺序不重要, [9, 0] 也是有效答案。
    string s = "barfoothefoobarman";
    vector<string> words = {"foo", "bar"};
    
    // 预期结果 []
//    string s = "wordgoodgoodgoodbestword";
//    vector<string> words = {"word", "good", "best", "word"};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans =solution->findSubstring(s, words);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            cout << ans[i] << ", ";
        }
        cout << "End." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
