//
//  main.cpp
//  Prob1301_Remove_Invalid_Parentheses
//
//  Created by 阴昱为 on 2019/6/14.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//301. Remove Invalid Parentheses
//
//Remove the minimum number of invalid parentheses in order to make the input string valid. Return all possible results.
//Note: The input string may contain letters other than the parentheses ( and ).
//
//删除最小数量的无效括号，使得输入的字符串有效，返回所有可能的结果。
//说明: 输入可能包含了除 ( 和 ) 以外的字符。
//
//Example 1:
//    Input: "()())()"
//    Output: ["()()()", "(())()"]
//
//Example 2:
//    Input: "(a)())()"
//    Output: ["(a)()()", "(a())()"]
//
//Example 3:
//    Input: ")("
//    Output: [""]


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

const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


class Solution {
private:
    // 方法一
    map<int, vector<string>> res_map = {}; // map<删除元素的个数, 合法括号式子>
    // stack<char> parentheses_stack = {}; // 本题只有小括号，可以不用栈模拟
    int left_count = 0; // 当前出现的左括号数量
    int right_count = 0; // 当前出现的右括号数量
    string cur_res = ""; // 当前式子
    int cur_delete_count = 0; // 当前删除的元素个数
    int mini_delete_count = MAX_INT32; // 最少需要删除的元素个数
    // int dfs_count = 0; // 统计 DFS 次数
    
    // 方法二
    vector<string> res = {};

public:
    vector<string> removeInvalidParentheses(string s) {
        // 边界情况判断
        if (s.empty()) {
            return {""};
        }
        
        int s_len = (int)s.size();
        
        // 字符串预处理：最左的 ')' 和最右的 '(' 必然是要被删除的
        for (int i = 0; i < s_len; i++) {
            if (s[i] == '(') {
                break;
            } else if (s[i] == ')') {
                s.erase(i, 1);
                i --;
            } else {
                continue;
            }
        }
        
        for (int i = s_len - 1; i >= 0; i--) {
            if (s[i] == ')') {
                break;
            } else if (s[i] == '(') {
                s.erase(i, 1);
            } else {
                continue;
            }
        }
        
        // cout << "s: " << s << endl;
        
        // 调用具体方法
        return this->solution2(s);
    }
    
private:
    // 方法一：树形 DFS，需考虑进一步剪枝，不然虽未超时、但仍太慢。
    vector<string> solution1(string s) {
        this->DFS(s, 0);
        
        // cout << "DFS 次数: " << this->dfs_count << endl;
        
        return this->res_map[this->mini_delete_count];
    }
    
    // 左子树：加入当前字符。右子树：不加当前字符。
    void DFS (string s, int index) {
        // this->dfs_count ++;
        if (index >= (int)s.size()) {
            // cout << "cur_res=" << this->cur_res << "  Skip=" << this->cur_delete_count;
            // cout << "  Count=" << this->count << endl;
            //if (this->parentheses_stack.empty()) {
            if (this->left_count == this->right_count) {
                if (this->cur_delete_count > this->mini_delete_count) {
                    return;
                }
                
                if (this->cur_delete_count < this->mini_delete_count) {
                    this->mini_delete_count = this->cur_delete_count;
                }
                
                // cout << "进入 cur_res = " << this->cur_res << endl;
                
                // 加入到映射表里
                if (this->res_map.find(this->mini_delete_count) == this->res_map.end()) {
                    this->res_map.insert({this->mini_delete_count, {this->cur_res}});
                } else {
                    // 避免重复
                    vector<string> temp = this->res_map[this->mini_delete_count];
                    if (find(temp.begin(), temp.end(), this->cur_res) == temp.end()) {
                        this->res_map[this->mini_delete_count].push_back(this->cur_res);
                    }
                }
            }
            return;
        }
        
        // 左子树：加入当前字符
        if (this->cur_delete_count <= this->mini_delete_count) {
            if (s[index] == '(') {
                // this->parentheses_stack.push('('); // 前进
                this->left_count ++;
                this->cur_res += s[index];
                
                this->DFS(s, index + 1); // 深度搜索左子树
                
                this->cur_res.erase((int)cur_res.size() - 1, 1); // 回溯还原
                this->left_count --;
                // this->parentheses_stack.pop();
            } else if (s[index] == ')') {
                //if (!this->parentheses_stack.empty() && this->parentheses_stack.top() == '(') {
                if (this->left_count > this->right_count) {
                    // 若左右括号匹配，则继续搜索左子树
                    // this->parentheses_stack.pop(); // 前进
                    this->right_count ++;
                    this->cur_res += s[index];
                    
                    this->DFS(s, index + 1); // 深度搜索左子树
                    
                    this->cur_res.erase((int)cur_res.size() - 1, 1); // 回溯还原
                    this->right_count --;
                    // this->parentheses_stack.push('(');
                } else {
                    // 不匹配，则尝试跳过该字符，即搜索右子树
                }
            } else {
                this->cur_res += s[index]; // 前进
                
                this->DFS(s, index + 1); // 深度搜索左子树
                
                this->cur_res.erase((int)cur_res.size() - 1, 1); // 回溯还原
            }
        }
        
        // 右子树：跳过当前字符。剪枝
        if (this->cur_delete_count < this->mini_delete_count) {
            this->cur_delete_count ++; // 前进
            this->DFS(s, index + 1); // 深度搜索右子树
            this->cur_delete_count --; // 回溯还原
        }
    }
    
    // 方法二：双向删除。高效。
    vector<string> solution2 (string s) {
        remove(move(s), {'(', ')'}, 0, 0);
        return this->res;
    }
    
    // 合法括号式子实质：正向遍历时，当前左括号数量不少于当前右括号数量；反向遍历时，当前右括号数量不少于当前左括号数量。
    // 同时满足正反向的括号式子，就是一个左右括号数量相等、嵌套合法的括号式子了。
    void remove(string s, const vector<char>& parentheses, int i_start, int j_start) {
        // 记录左括号数量减右括号数量之差（在反转执行中，左右括号颠倒）
        int diff = 0;
        
        for (int i = i_start; i < (int)s.size(); i++) {
            // 如果是左括号，则加 1；如果是右括号，则减 1
            if (s[i] == parentheses[0]) {
                diff ++;
            } else if (s[i] == parentheses[1]) {
                diff --;
            }
            
            // 如果左括号不少于右括号，则继续
            if (diff >= 0) {
                continue;
            }
            
            // 否则，右括号更多，不是合法串，删除一个右括号
            for (int j = j_start; j <= i; j++) {
                // 从左到右找，如果 j 是右括号，并且 j 不是连续的右括号（j 是串首字符 or j-1 字符不是右括号）
                if (s[j] == parentheses[1] && (j == j_start || s[j - 1] != parentheses[1])) {
                    // 删去 j 字符
                    string ss = s.substr(0, j) + s.substr(j + 1);
                    
                    // 对调整过的新字符串 ss 重新执行 remove 函数
                    // 从 ss 中的 i 位置开始匹配左右括号。如果不匹配，从 j 位置开始找右括号。不做重复工作
                    this->remove(move(ss), parentheses, i, j);
                }
            }
            
            // 删除操作已做完，返回
            return;
        }
        
        // 此时，整个 s 串是左括号数量不少于右括号的，但有效串是左右括号数量相等
        // 所以反转字符串，反向执行 reomve 函数，让右括号数量不少于左括号 -> 括号数匹配
        reverse(s.begin(), s.end());
        
        if (parentheses[0] == '(') {
            // 反向执行，颠倒 {'(', ')'} 为 {')', '('}，删除多余的 '('
            this->remove(move(s), {parentheses[1], parentheses[0]}, 0, 0);
        } else {
            // 反转两次的结果，是正序的合法串，获得结果
            this->res.push_back(move(s));
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string s = "(a)())()"; // 预期结果 ["(a)()()", "(a())()"]
//    string s = ")b(a)())()c("; // 预期结果 ["b(a)()()c", "b(a())()c"]
//    string s = ")t))()()bo)"; // 预期结果 ["t(()bo)", "t()(bo)", "t()()bo"]
    string s = "(())))(((((vp)()(("; // 预期结果 ["(())((vp))", "(())(vp)()"]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<string> ans = solution->removeInvalidParentheses(s);
    if (ans.empty()) {
        cout << "No Answer." << endl;
    } else {
        for (auto ite = ans.begin(); ite < ans.end(); ite++) {
            cout << *ite << endl;
        }
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
