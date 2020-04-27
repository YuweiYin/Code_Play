//
//  main.cpp
//  ByteCamp_2019_Alg_4
//
//  Created by 阴昱为 on 2019/6/21.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//ByteCamp 2019 算法挑战 第四期
//题目描述：
//    给定一个字符串 str（只包含小写字母），返回字典序最小的且包含原字符串中所有的不同字符的子序列。
//Example1:
//    Input: cdbdbbdbad
//    Output: cbad
//Example2:
//    Input: cbbaadbabc
//    Output: adbc


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

int recur_count = 0; // 递归次数计数器
int loop_count = 0; // 循环次数计数器

class Solution {
private:
    string result = "";
    bool end_tag = false;
    
public:
    // 解决方案入口函数
    string MinAllSubstring(string str) {
        return this->solution2(str);
    }
    
private:
    // 方法一。贪心递归，高效剪枝。线性时间复杂度。
    // 时间复杂度 O(N), Omega(lgN), 空间复杂度 O(N)
    string solution1(string str) {
        
        map<char, vector<int>> dict = {}; // 记录某个字符各次出现的下标列表
        
        // 记录每个字符各次出现的下标
        for (int i = 0; i < (int)str.size(); i++) {
            if (dict.find(str[i]) == dict.end()) {
                dict.insert({str[i], {i}});
            } else {
                dict[str[i]].emplace_back(i);
            }
        }
        
        // key 按字母序排列的各个键值
        string key = "";
        for (auto ite = dict.begin(); ite != dict.end(); ite++) {
            key += ite->first;
        }
        
        this->greedySearch(dict, key, 0, str, "", -1);
        
        return this->result;
    }
    
    // 贪心树型算法，每次尝试用字典序较小的数开头，成功搜索到的第一个解，就是最优解
    void greedySearch (map<char, vector<int>> dict, string key, int depth,
                       string str, string cur_str, int cur_index) {
        recur_count ++;
        
        if (this->end_tag) {
            return; // 结束结束结束～
        }
        
        // 判断 key 里面的所有字母，是否都包含在当前字母后面所能出现的字母中，
        // 如果不是，那么再往后找也不足以构成一个解
        if (!this->restEnough(key, str, cur_index)) {
            return;
        }
        
        int key_len = (int)key.size();
        
        // 如果深度达到字典长度，表示用尽了所有字符，找到的第一个解就是最优解
        if (depth >= (int)dict.size()) {
            this->result = cur_str;
            this->end_tag = true;
            return;
        }
        
        // 对于未使用的每一个字符
        for (int i = 0; i < key_len; i++) {
            if (this->end_tag) {
                return; // 结束结束结束～
            }
            
            vector<int> index_vec = dict[key[i]]; // 当前字符在原串中出现的下标列表
            
            // 如果当前字符的所有出现的坐标中，存在比 cur_index 更大的下标
            for (int j = 0; j < (int)index_vec.size(); j++) {
                loop_count ++;
                
                if (this->end_tag) {
                    return; // 结束结束结束～
                }
                
                if (index_vec[j] > cur_index) {
                    // 把 key[i] 从 key 中取出，加在 cur_str 之后，贪心递归执行
                    this->greedySearch(dict, key.substr(0, i) + key.substr(i + 1, key_len),
                                       depth + 1, str, cur_str + key[i], index_vec[j]);
                    break;
                }
            }
        }
    }
    
    // 判断 key 里面的所有字母，是否都包含在当前字母后面所能出现的字母中，如果不是，那么再往后找也没有意义了
    bool restEnough (string key, string str, int cur_index) {
        if (key.empty()) {
            return true;
        }
        
        int key_len = (int)key.size();
        
        // key 不空，但是 str 的索引到最尾了
        if (cur_index >= (int)str.size() - 1 || cur_index < -1) {
            return false;
        }
        
        int res = true;
        
        string sub = str.substr(cur_index + 1);
        
        for (int i = 0; i < key_len; i++) {
            // 如果找不到，那就返回 false，结束
            if (sub.find(key[i]) == string::npos) {
                return false;
            }
        }
        
        return res;
    }
    
    // 老方法。贪心递归、剪枝不足。
    // 时间复杂度 O(N^2), Omega(N)，空间复杂度 O(N)
    string solution2(string str) {
        map<char, vector<int>> dict = {};
        
        // 记录每个字符各次出现的下标
        for (int i = 0; i < (int)str.size(); i++) {
            if (dict.find(str[i]) == dict.end()) {
                dict.insert({str[i], {i}});
            } else {
                dict[str[i]].emplace_back(i);
            }
        }
        
        // key 按字母序排列的各个键值
        string key = "";
        for (auto ite = dict.begin(); ite != dict.end(); ite++) {
            key += ite->first;
        }
        
        this->greedySearchSlow(dict, key, 0, "", -1);
        
        return this->result;
    }
    
    // 贪心树型算法，每次尝试用字典序较小的数开头，成功搜索到的第一个解，就是最优解
    void greedySearchSlow (map<char, vector<int>> dict, string key, int depth, string cur_str, int cur_index) {
        recur_count ++;
        
        if (this->end_tag) {
            return; // 结束结束结束～
        }
        
        // 如果深度达到字典长度，表示用尽了所有字符，找到的第一个解就是最优解
        if (depth >= (int)dict.size()) {
            this->result = cur_str;
            this->end_tag = true;
            return;
        }
        
        int key_len = (int)key.size();
        
        // 对于未使用的每一个字符
        for (int i = 0; i < key_len; i++) {
            if (this->end_tag) {
                return; // 结束结束结束～
            }
            
            vector<int> index_vec = dict[key[i]]; // 当前字符在原串中出现的下标列表
            
            // 如果当前字符的所有出现的坐标中，存在比 cur_index 更大的下标
            for (int j = 0; j < (int)index_vec.size(); j++) {
                loop_count ++;
                
                if (this->end_tag) {
                    return; // 结束结束结束～
                }
                
                if (index_vec[j] > cur_index) {
                    // 把 key[i] 从 key 中取出，加在 cur_str 之后，贪心递归执行
                    this->greedySearchSlow(dict, key.substr(0, i) + key.substr(i + 1, key_len), depth + 1, cur_str + key[i], index_vec[j]);
                    break;
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
//    string str = "cdbdbbdbad"; // Case 1 预期结果 cbad
//    string str = "cbbaadbabc"; // Case 2 预期结果 adbc
    
    // Case 3 预期结果 abcdefghij
    // 老方法贪心递归：最优情况-程序执行时间: 0.281ms. recur_count = 11 loop_count = 10
    // 新剪枝方法的贪心递归：程序执行时间: 0.275ms. recur_count = 11 loop_count = 10
//    string str = "abcdefghij";
    
    // Case 4 预期结果 jihgfedcba
    // 老方法贪心递归：最坏情况-程序执行时间: 11.791ms. recur_count = 1024=2^10 loop_count = 5120
    // 新剪枝方法的贪心递归：程序执行时间: 0.74ms. recur_count = 56 loop_count = 55
//    string str = "jihgfedcba";
    
    // Case 5 预期结果 nmlkjihgfedcba
    // 老方法贪心递归：最坏情况-程序执行时间: 259.99ms. recur_count = 16384=2^14 loop_count = 114688
    // 新剪枝方法的贪心递归：程序执行时间: 1.551ms. recur_count = 106 loop_count = 105
//    string str = "nmlkjihgfedcba";
    
    // Case 6 预期结果 zyxwvutsrqponmlkjihgfedcba
    // 老方法贪心递归：最坏情况-程序执行时间: 特别久. recur_count = 1024=2^26
    // 新剪枝方法的贪心递归：程序执行时间: 8.868ms. recur_count = 352 loop_count = 351
//    string str = "zyxwvutsrqponmlkjihgfedcba";
    
    // Case 7 预期结果 abcdefghijklmnopqrstuvwxyz
    // 老方法贪心递归：最优情况-程序执行时间: 1.129ms. recur_count = 27 loop_count = 26
    // 新剪枝方法的贪心递归：程序执行时间: 0.994ms. recur_count = 27 loop_count = 26
//    string str = "aaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwwxxxxxyyyyyzzzzz";
    
    // Case 8 预期结果 zyxwvutsrqponmlkjihgfedcba
    // 老方法贪心递归：最坏情况-程序执行时间: 特别久. recur_count = 1024=2^26
    // 新剪枝方法的贪心递归：程序执行时间: 9.488ms. recur_count = 352 loop_count = 351
//    string str = "zzzzzyyyyyxxxxxwwwwwvvvvvuuuuutttttsssssrrrrrqqqqqpppppooooonnnnnmmmmmlllllkkkkkjjjjjiiiiihhhhhgggggfffffeeeeedddddcccccbbbbbaaaaa";
    
    // Case 9 预期结果 abcdefghijklmnopqrstuvwxyz
    // 老方法贪心递归：最优情况-程序执行时间: 1.457ms. recur_count = 27 loop_count = 26
    // 新剪枝方法的贪心递归：程序执行时间: 1.509ms. recur_count = 27 loop_count = 26
//    string str = "aaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwwxxxxxyyyyyzzzzzaaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwwxxxxxyyyyyzzzzzaaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwwxxxxxyyyyyzzzzzaaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwwxxxxxyyyyyzzzzzaaaaabbbbbcccccdddddeeeeefffffggggghhhhhiiiiijjjjjkkkkklllllmmmmmnnnnnooooopppppqqqqqrrrrrssssstttttuuuuuvvvvvwwwwwwxxxxxyyyyyzzzzz";
    
    // Case 10 预期结果 zyxwvutsrqponmlkjihgfedcba
    // 老方法贪心递归：最坏情况-程序执行时间: 特别久.
    // 新剪枝方法的贪心递归：程序执行时间: 8.969ms. recur_count = 258 loop_count = 5347
    string str = "zzzzzyyyyyxxxxxwwwwwvvvvvuuuuutttttsssssrrrrrqqqqqpppppooooonnnnnmmmmmlllllkkkkkjjjjjiiiiihhhhhgggggfffffeeeeedddddcccccbbbbbaaaaazzzzzyyyyyxxxxxwwwwwvvvvvuuuuutttttsssssrrrrrqqqqqpppppooooonnnnnmmmmmlllllkkkkkjjjjjiiiiihhhhhgggggfffffeeeeedddddcccccbbbbbaaaaazzzzzyyyyyxxxxxwwwwwvvvvvuuuuutttttsssssrrrrrqqqqqpppppooooonnnnnmmmmmlllllkkkkkjjjjjiiiiihhhhhgggggfffffeeeeedddddcccccbbbbbaaaaazzzzzyyyyyxxxxxwwwwwvvvvvuuuuutttttsssssrrrrrqqqqqpppppooooonnnnnmmmmmlllllkkkkkjjjjjiiiiihhhhhgggggfffffeeeeedddddcccccbbbbbaaaaazzzzzyyyyyxxxxxwwwwwvvvvvuuuuutttttsssssrrrrrqqqqqpppppooooonnnnnmmmmmlllllkkkkkjjjjjiiiiihhhhhgggggfffffeeeeedddddcccccbbbbbaaaaa";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->MinAllSubstring(str);
    if (!ans.empty()) {
        cout << ans << endl;
    } else {
        cout << "Answer is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    cout << "recur_count = " << recur_count << endl;
    cout << "loop_count = " << loop_count << endl;
    
    return 0;
}
