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
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


class Solution {
private:
    string result = "";
    bool end_tag = false;
    
public:
    // 解决方案入口函数
    string MinAllSubstring(string str) {
        return this->solution1(str);
    }
    
private:
    // 方法一。贪心递归。
    // 时间复杂度 O(N^2), Omega(N)，空间复杂度 O(N)
    string solution1(string str) {
        
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
        
        this->greedySearch(dict, key, 0, "", MIN_INT32);
        
        return this->result;
    }
    
    // 贪心树型算法，每次尝试用字典序较小的数开头，成功搜索到的第一个解，就是最优解
    void greedySearch (map<char, vector<int>> dict, string key, int depth, string cur_str, int cur_index) {
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
                if (this->end_tag) {
                    return; // 结束结束结束～
                }
                
                if (index_vec[j] > cur_index) {
                    // 把 key[i] 从 key 中取出，加在 cur_str 之后，贪心递归执行
                    this->greedySearch(dict, key.substr(0, i) + key.substr(i + 1, key_len), depth + 1, cur_str + key[i], index_vec[j]);
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
    //    string str = "cdbdbbdbad"; // 预期结果 cbad
    string str = "cbbaadbabc"; // 预期结果 adbc
    
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
    
    return 0;
}
