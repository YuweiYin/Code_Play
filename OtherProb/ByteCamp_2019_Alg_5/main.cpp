//
//  main.cpp
//  ByteCamp_2019_Alg_5
//
//  Created by 阴昱为 on 2019/6/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//ByteCamp 2019 算法挑战 第五期
//题目描述：
//    输入一个由'.'和'S'组成的长度为N的数组A，你可以最多做K次操作，每次操作选择一个数组中的位置，把相应位置连同左右邻居都变成'.'。
//    问K次操作之后，数组中最多可以有多少个'.'。
//    输入：
//        N K
//        A
//    输出：
//        最终数组A中'.'的个数。


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

int recur_count = 0; // 递归次数计数器
int loop_count = 0; // 循环次数计数器

class Solution {
private:
    int result = 0;
    bool end_flag = false;
    
public:
    // 解决方案入口函数
    int MaxDot(vector<char> A, int K) {
        return this->solution1(A, K);
    }
    
private:
    // 方法一。贪心递归。
    // 时间复杂度 O(), Omega(), 空间复杂度 O()
    int solution1 (vector<char> A, int K) {
        // 边界条件
        if (A.empty()) {
            return 0;
        }
        
        int A_len = (int)A.size();
        
        if (A_len == 1) {
            if (A[0] == '.' || K >= 1) {
                return 1;
            } else {
                return 0;
            }
        }
        
        // 如果 K 次"无脑"操作超过 A 长度，自然可以把 A 全变成 '.'
        if (3 * K >= A_len) {
            return A_len;
        }
        
        // 数组中原本含有 '.' 的个数
        int base_dot_count = 0;
        for (int i = 0; i < A_len; i++) {
            if (A[i] == '.') {
                base_dot_count ++;
            }
        }
        
        // 对形如 "..SSS" 和 "SSS.." 的结构，转换成 "....." 是一定最佳的，不必考虑对周围收益值的影响
        // 先进行该处理，减少 K 值，降低递归树的深度。使用滑动窗口
        int start = 0;
        int end = 4;
        while (K > 0 && end < A_len) {
            if (A[start] == '.' && A[start + 1] == '.' && A[start + 2] == 'S'
                && A[start + 3] == 'S' && A[start + 4] == 'S') {
                // 匹配上 "..SSS" 结构
                A[start + 2] = '.';
                A[start + 3] = '.';
                A[start + 4] = '.';
                
                K --;
                base_dot_count += 3;
                
                start += 3;
                end += 3;
            } else if (A[start] == 'S' && A[start + 1] == 'S' && A[start + 2] == 'S'
                       && A[start + 3] == '.' && A[start + 4] == '.') {
                // 匹配上 "SSS.." 结构
                A[start] = '.';
                A[start + 1] = '.';
                A[start + 2] = '.';
                
                K --;
                base_dot_count += 3;
                
                start += 5;
                end += 5;
            } else {
                start ++;
                end ++;
            }
        }
        
        // 如果已经没有剩余的可操作次数了，直接返回 base_dot_count
        if (K <= 0) {
            return base_dot_count;
        }
        
        vector<int> benefit = vector<int>(A_len, 0); // 记录每个位置进行操作的收益
        vector<bool> used = vector<bool>(A_len, false); // 记录每个位置是否已被使用
        
        // 记录中间每个位置进行操作的收益
        for (int i = 1; i < A_len - 1; i++) {
            if (A[i - 1] == 'S') {
                benefit[i] ++;
            }
            if (A[i] == 'S') {
                benefit[i] ++;
            }
            if (A[i + 1] == 'S') {
                benefit[i] ++;
            }
        }
        
        // 数组长度 >= 3 的话，正常来说是不会选择首元素或尾元素的
        // 选 A[1] 的效果总不弱于 A[0]，选 A[len - 2] 的效果总不弱于 A[len - 2]
        // 不过本程序不对数组长度为 2 时单独处理，所以还是可能选择到首尾元素的
        
        // 首元素的收益
        if (A[0] == 'S') {
            benefit[0] ++;
        }
        if (A[1] == 'S') {
            benefit[0] ++;
        }
        
        // 尾元素的收益
        if (A[A_len - 1] == 'S') {
            benefit[A_len - 1] ++;
        }
        if (A[A_len - 2] == 'S') {
            benefit[A_len - 1] ++;
        }
        
        this->end_flag = false;
        this->greedySearch(A, K, benefit, used, 0, base_dot_count);
        
        return this->result;
    }
    
    // 贪心树型算法，每次尝试用当前最大的收益值
    void greedySearch (vector<char>& A, int& K, vector<int>& benefit,
                       vector<bool>& used, int depth, int cur_res) {
        recur_count ++;
        
        if (this->end_flag) {
            return; // End Recursion
        }
        
        // 如果深度达到 K，表示用尽了操作次数
        if (depth >= K) {
            if (cur_res > this->result) {
                this->result = cur_res;
            }
            return;
        }
        
        int len = (int)benefit.size();
        
        // 找到当前收益极大值，至多为 3
        auto max_ite = max_element(benefit.begin(), benefit.end());
        
        if (*max_ite > 0) {
            // 以当前收益值等于极大值的、未使用过的那些点作为递归树的根
            for (int i = 0; i < len; i++) {
                if (this->end_flag) {
                    return; // End Recursion
                }
                if (!used[i] && benefit[i] == *max_ite) {
                    // 记下当前位置的收益
                    int bene = benefit[i];
                    // 如果加上该收益，使得 '.' 个数达到了最大可能值 A.length，则直接结束全部递归
                    if (cur_res + bene >= len) {
                        this->result = len;
                        this->end_flag = true;
                        return;
                    }
                    
                    // 前进，修改相关的收益值 -1 -2 -3 -2 -1
                    used[i] = true;
                    if (i >= 2) {
                        benefit[i - 2] -= 1;
                    }
                    if (i >= 1) {
                        benefit[i - 1] -= 2;
                    }
                    benefit[i] -= 3;
                    if (i < len - 1) {
                        benefit[i + 1] -= 2;
                    }
                    if (i < len - 2) {
                        benefit[i + 2] -= 1;
                    }
                    
                    // 递归
                    this->greedySearch(A, K, benefit, used, depth + 1, cur_res + bene);
                    if (this->end_flag) {
                        return; // End Recursion
                    }
                    
                    // 回溯，修改相关的收益值 +1 +2 +3 +2 +1
                    used[i] = false;
                    if (i >= 2) {
                        benefit[i - 2] += 1;
                    }
                    if (i >= 1) {
                        benefit[i - 1] += 2;
                    }
                    benefit[i] += 3;
                    if (i < len - 1) {
                        benefit[i + 1] += 2;
                    }
                    if (i < len - 2) {
                        benefit[i + 2] += 1;
                    }
                }
            }
        } else {
            return;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // Case 1 预期结果 6
//    vector<char> A = {'S', '.', 'S', 'S', '.', 'S'};
//    int K = 2;
    
    // Case 2 预期结果 6
//    vector<char> A = {'S', '.', 'S', 'S', 'S', '.', 'S'};
//    int K = 2;
    
    // Case 3 预期结果 6
//    vector<char> A = {'S', '.', 'S', 'S', 'S', 'S'};
//    int K = 2;
    
    // Case 4 预期结果 8
    vector<char> A = {'S', '.', '.', 'S', 'S', 'S', 'S', 'S', 'S'};
    int K = 2;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->MaxDot(A, K);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    cout << "recur_count = " << recur_count << endl;
    cout << "loop_count = " << loop_count << endl;
    
    return 0;
}
