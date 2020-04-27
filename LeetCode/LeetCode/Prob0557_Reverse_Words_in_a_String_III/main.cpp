//
//  main.cpp
//  Prob1557_Reverse_Words_in_a_String_III
//
//  Created by 阴昱为 on 2019/6/20.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1557. Reverse Words in a String III
//
//Given a string, you need to reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.
//
//给定一个字符串，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。
//
//Example 1:
//    Input: "Let's take LeetCode contest"
//    Output: "s'teL ekat edoCteeL tsetnoc"
//
//Note: In the string, each word is separated by single space and there will not be any extra space in the string.
//注意：在字符串中，每个单词由单个空格分隔，并且字符串中不会有任何额外的空格。


// 设置系统栈深度
#pragma comment(linker, "/STACK:1024000000,1024000000")

// 引入头文件
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>

#include <math.h>
#include <time.h>
#include <regex>

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
    string reverseWords(string s) {
        return this->solution1(s);
    }
    
private:
    // 方法一。顺序遍历字符串，遇到分隔符则反转前一个单词，双指针夹逼、反转每个字符串。
    // 时间复杂度 O(N)，空间复杂度 O(1)
    string solution1 (string s) {
        if (s.empty() || (int)s.size() == 1) {
            return s;
        }
        
        int s_len = (int)s.size();
        int left; // 反转字符串时的左指针
        int right; // 反转字符串时的右指针
        int start = 0; // 空格之后的第一个字符
        char delim = ' '; // 分割符，本题为空格
        
        for (int end = 0; end < s_len; end++) {
            if (s[end] == delim) {
                if (start < end) {
                    left = start;
                    right = end - 1;
                    while (left < right) {
                        this->stringCharSwap(s, left++, right--);
                    }
                    
                    start = end + 1; // start 移动到空格的下一个位置
                    end ++; // end 循环结束时 += 2，移动到空格的下下个位置
                }
            }
        }
        
        // 末尾情况，如果最后一个空格的后面还有字符未处理
        if (start < s_len) {
            left = start;
            right = s_len - 1;
            while (left < right) {
                this->stringCharSwap(s, left++, right--);
            }
        }
        
        return s;
    }
    
    // 方法二。用空格分割成单词序列，双指针夹逼、反转每个字符串。
    // 本题不用反转各个单词之间的顺序，所以不分割成单词序列也可以
    // 时间复杂度 O(N)，空间复杂度 O(N)
    string solution2 (string s) {
        if (s.empty() || (int)s.size() == 1) {
            return s;
        }
        
        // 用 delim 空格分割字符串为向量
        string delim = " ";
//        vector<string> s_vec = this->myStringSplit1(s.data(), delim.data());
//        vector<string> s_vec = this->myStringSplit1(s.c_str(), delim.c_str());
//        vector<string> s_vec = this->myStringSplit2(s, delim);
        vector<string> s_vec = this->regexSplit(s, delim); // 最快
        
        string res = "";
        
        int v_len = (int)s_vec.size();
        
        int left = 0;
        int right = v_len - 1;
        
        // 反转向量中的 string 元素（本题不用）
//        while (left < right) {
//            this->vectorStringSwap(s_vec, left++, right--);
//        }
        
        // 反转每个 string 元素中的 char
        for (int i = 0; i < v_len; i++) {
            left = 0;
            right = (int)s_vec[i].size() - 1;
            
            while (left < right) {
                this->stringCharSwap(s_vec[i], left++, right--);
            }
        }
        
        // join 拼凑成一个字符串
        int index;
        for (index = 0; index < v_len - 1; index++) {
            res += s_vec[index] + delim;
        }
        res += s_vec[index];
        
        return res;
    }
    
    // 如果 v[i] 不等于 v[j]，则交换之
    void vectorStringSwap (vector<string>& v, int i, int j) {
        if (v[i] != v[j]) {
            string temp = v[i];
            v[i] = v[j];
            v[j] = temp;
        }
    }
    
    // 如果 s[i] 不等于 s[j]，则交换之
    void stringCharSwap (string& s, int i, int j) {
        if (s[i] != s[j]) {
            s[i] = s[i] ^ s[j];
            s[j] = s[i] ^ s[j];
            s[i] = s[i] ^ s[j];
        }
    }
    
    // 1. C 语言 strtok 函数实现 C++ string split
    vector<string> myStringSplit1 (const char *s, const char *delim) {
        vector<string> res = {};
        
        if (s && strlen(s)) {
            size_t len = strlen(s);
            char *src = new char[len + 1];
            
            strcpy(src, s);
            src[len] = '\0';
            
            char *tokenPtr = strtok(src, delim);
            
            while (tokenPtr != NULL) {
                string token = tokenPtr;
                res.emplace_back(token);
                
                tokenPtr = strtok(NULL, delim);
            }
            delete[] src;
        }
        
        return res;
    }
    
    // 2. string::find 实现 split
    vector<string> myStringSplit2 (const string& s, const string& delim) {
        vector<string> res = {};
        string::size_type pos1, pos2;
        
        size_t len = s.length();
        pos2 = s.find(delim);
        pos1 = 0;
        
        while(string::npos != pos2) {
            // 找到 delim 后，存储 delim 之前的字符串
            res.emplace_back(s.substr(pos1, pos2 - pos1));
            
            pos1 = pos2 + delim.size(); // 右移 pos1
            pos2 = s.find(delim, pos1); // 从 pos1 开始往后找 delim
        }
        
        // 末尾的情况
        if(pos1 != len) {
            res.emplace_back(s.substr(pos1));
        }
        
        return res;
    }
    
    // 3. 正则表达式方式 实现 split
    // #include <regex>
    vector<string> regexSplit(const string& s, const string& delim) {
        vector<string> res = {};
        
        regex pattern(delim);
        
        sregex_token_iterator ite(s.begin(), s.end(), pattern, -1);
        sregex_token_iterator end;
        
        while (ite != end) {
            res.emplace_back(*ite++);
        }
        
        return res;
    }
    
    // 4. 使用 boost 实现 split
    // #include <boost/algorithm/string.hpp>
    // using namesapce boost;
//    vector<string> boostSplit(const string& s, const string& delim) {
//        vector<string> res = {};
//
//        boost::split(res, s, boost::is_any_of(delim) );
//
//        return res;
//    }
    
    // 5. sds sdssplitlen 函数 实现 split
//    vector<string> sdsSplit (const string& s, const string& delim) {
//        vector<string> res = {};
//
//        int len = 0;
//        sds* array = sdssplitlen(s.c_str(), s.length(), delim, 1, &len);
//
//        for (int i = 0; i < len; i++) {
//            　　res.emplace_back(array[i]);
//        }
//
//        return res;
//    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    string s = "Let's take LeetCode contest"; // 预期结果 "s'teL ekat edoCteeL tsetnoc"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->reverseWords(s);
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
