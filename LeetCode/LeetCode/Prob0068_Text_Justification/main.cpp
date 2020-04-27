//
//  main.cpp
//  Prob1068_Text_Justification
//
//  Created by 阴昱为 on 2019/7/27.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//68. Text Justification
//
//Given an array of words and a width maxWidth, format the text such that each line has exactly maxWidth characters and is fully (left and right) justified.
//You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly maxWidth characters.
//Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line do not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.
//For the last line of text, it should be left justified and no extra space is inserted between words.
//
//Note:
//    A word is defined as a character sequence consisting of non-space characters only.
//    Each word's length is guaranteed to be greater than 0 and not exceed maxWidth.
//    The input array words contains at least one word.
//
//给定一个单词数组和一个长度 maxWidth，重新排版单词，使其成为每行恰好有 maxWidth 个字符，且左右两端对齐的文本。
//你应该使用“贪心算法”来放置给定的单词；也就是说，尽可能多地往每行中放置单词。必要时可用空格 ' ' 填充，使得每行恰好有 maxWidth 个字符。
//要求尽可能均匀分配单词间的空格数量。如果某一行单词间的空格不能均匀分配，则左侧放置的空格数要多于右侧的空格数。
//文本的最后一行应为左对齐，且单词之间不插入额外的空格。
//
//说明:
//    单词是指由非空格字符组成的字符序列。
//    每个单词的长度大于 0，小于等于 maxWidth。
//    输入单词数组 words 至少包含一个单词。
//
//Example 1:
//    Input:
//    words = ["This", "is", "an", "example", "of", "text", "justification."]
//    maxWidth = 16
//    Output:
//    [
//     "This    is    an",
//     "example  of text",
//     "justification.  "
//    ]
//
//Example 2:
//    Input:
//    words = ["What","must","be","acknowledgment","shall","be"]
//    maxWidth = 16
//    Output:
//    [
//     "What   must   be",
//     "acknowledgment  ",
//     "shall be        "
//    ]
//    Explanation: Note that the last line is "shall be    " instead of "shall     be",
//    because the last line must be left-justified instead of fully-justified.
//    Note that the second line is also left-justified becase it contains only one word.
//
//Example 3:
//    Input:
//    words = ["Science","is","what","we","understand","well","enough","to","explain",
//             "to","a","computer.","Art","is","everything","else","we","do"]
//    maxWidth = 20
//    Output:
//    [
//     "Science  is  what we",
//     "understand      well",
//     "enough to explain to",
//     "a  computer.  Art is",
//     "everything  else  we",
//     "do                  "
//    ]


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
    vector<string> fullJustify(vector<string>& words, int maxWidth) {
        return this->solution1(words, maxWidth);
    }
    
private:
    // 方法一。文本对齐过程模拟。时间复杂度 O(N)，空间复杂度 O(M)。
    // N = words.size, M = all_string.size
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 9 MB , 在所有 C++ 提交中击败了 67.97% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Text Justification.
    // Memory Usage: 9 MB, less than 72.53% of C++ online submissions for Text Justification.
    vector<string> solution1(vector<string>& words, int maxWidth) {
        if (words.empty() || maxWidth <= 0) {
            return {};
        }
        
        vector<string> res = {};
        
        int start = 0; // 当前行的首单词在 words 中的下标
        int cur_width = 0; // 当前行已占总宽度
        
        for (int i = 0; i < words.size(); i++) {
            if (cur_width + words[i].size() + i - start - 1 >= maxWidth) {
                // 当前行可放置当前单词 words[i]
                res.push_back("");
                
                if (i - start <= 1) {
                    // 非末尾行，仅有一个单词。该单词靠左填入行中，右侧由空格补齐。
                    res.back() += words[start];
                    res.back() += string(maxWidth - res.back().size(), ' ');
                } else {
                    // 非末尾行，有一个以上单词。通过单词总数和剩余空格数分配每两个单词间的空格数。
                    int quo = (maxWidth - cur_width) / (i - start - 1);
                    int rem = (maxWidth - cur_width) % (i - start - 1);
                    
                    for (int j = start; j < i - 1; j++) {
                        res.back() += words[j];
                        res.back() += string(j < start + rem ? quo + 1 : quo, ' ');
                    }
                    
                    res.back() += words[i - 1];
                }
                
                start = i;
                cur_width = 0;
            }
            
            cur_width += words[i].size();
        }
        
        // 末尾行。每个单词间有一个空格，空出的右侧由空格补齐。
        res.push_back("");
        for (int i = start; i < words.size() - 1; i++) {
            res.back() += words[i];
            res.back() += ' ';
        }
        
        res.back() += words.back();
        res.back() += string(maxWidth - res.back().size(), ' ');
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    int maxWidth = 16;
    // 预期结果 [
    // "This    is    an",
    // "example  of text",
    // "justification.  "
    // ]
    vector<string> words = {"This", "is", "an", "example", "of", "text", "justification."};
    
    // 预期结果 [
    // "What   must   be",
    // "acknowledgment  ",
    // "shall be        "
    // ]
//    vector<string> words = {"What","must","be","acknowledgment","shall","be"};
    
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<string> ans = solution->fullJustify(words, maxWidth);
    if (!ans.empty()) {
        for (int i = 0; i < (int)ans.size(); i++) {
            cout << ans[i] << endl;
        }
    } else {
        cout << "Answer is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
