//
//  main.cpp
//  Prob1763_Partition_Labels
//
//  Created by 阴昱为 on 2019/6/17.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1763. Partition Labels
//
//A string S of lowercase letters is given. We want to partition this string into as many parts as possible so that each letter appears in at most one part, and return a list of integers representing the size of these parts.
//
//字符串 S 由小写字母组成。我们要把这个字符串划分为尽可能多的片段，同一个字母只会出现在其中的一个片段。返回一个表示每个字符串片段的长度的列表。
//
//Example 1:
//    Input: S = "ababcbacadefegdehijhklij"
//    Output: [9,7,8]
//    Explanation:
//    The partition is "ababcbaca", "defegde", "hijhklij".
//    This is a partition so that each letter appears in at most one part.
//    A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits S into less parts.
//
//Note:
//    S will have length in range [1, 500].
//    S will consist of lowercase letters ('a' to 'z') only.
//注意:
//    S的长度在[1, 500]之间。
//    S只包含小写字母'a'到'z'。


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
    vector<int> partitionLabels(string S) {
        return this->solution2(S);
    }
    
private:
    // 方法一。筛法。时间复杂度 O(N^2)?，空间复杂度 O(N)
    vector<int> solution1(string S) {
        if (S.empty()) {
            return {0};
        }
        
        int len = (int)S.size();
        
        if (len == 1) {
            return {1};
        }
        
        vector<int> res = {};
        
        // vector<int> group_num = vector<int>(len, 0);
        map<char, int> memo = {}; // 某字符，该字符所在组号
        int group_id = 1;
        
        for (int i = 0; i < len; i++) {
            if (memo.find(S[i]) == memo.end()) {
                // 如果检查到的这个字符没有组号了，表示这个字符曾经没有出现在任一组里
                // 需要把这个字符到最后一次出现这个字符间的所有字符都设置为同一组
                int pos = (int)S.find_last_of(S[i]);
                if (pos != (int)S.npos) {
                    // 如果从右到左找到另一个 S[i]，那么两个相同字符之间的字符都应当属于同一组
                    if (pos - i > 1) {
                        // 此时两个相等的 S[i] 字符之间存在字符
                        // 先找到这些字符里谁已经有组号了，找到这个组号，然后让这些字符都属于该组
                        // 否则给这些字符设定新组号
                        int cur_group_id = group_id;
                        bool find_id = false;
                        for (int j = i; j < pos; j++) {
                            if (memo.find(S[j]) != memo.end()) {
                                cur_group_id = memo[S[j]];
                                find_id = true;
                                break;
                            } else {
                                continue;
                            }
                        }
                        
                        // 让这些字符都属于同一组
                        for (int j = i; j <= pos; j++) {
                            memo[S[j]] = cur_group_id;
                        }
                        
                        // 如果没有在这些字符里找到组号，那么就消耗了一个组号
                        if (!find_id) {
                            group_id ++;
                        }
                        
                        i = pos; // i -> pos + 1
                    } else {
                        // 否则表明，要么就是两个连续的 S[i] 字符，要么是一个单独的 S[i] 字符，构成独立片段
                        for (int j = i; j <= pos; j++) {
                            memo[S[j]] = group_id;
                        }
                        group_id ++;
                        i = pos;
                    }
                } else {
                    // 异常情况，毕竟正向都出现了 S[i]，那么反向查找 S[i] 肯定也能找到
                    continue;
                }
            } else {
                // 如果检查到的这个字符已经有组号了，那一定是因为这个字符曾经出现在某组里面
                // 需要把这个字符到第一次出现这个字符间的所有字符都设置为同一组
                int pos = (int)S.find(S[i]);
                if (pos != (int)S.npos) {
                    // 如果从左到右找到另一个 S[i]，那么两个相同字符之间的字符都应当属于同一组
                    if (i - pos > 1) {
                        // 此时两个相等的 S[i] 字符之间存在字符，让这些字符都属于该组
                        int cur_group_id = memo[S[i]];
                        
                        // 让这些字符都属于同一组
                        for (int j = pos + 1; j < i; j++) {
                            memo[S[j]] = cur_group_id;
                        }
                        
                        continue;
                    } else {
                        // 否则表明，要么就是两个连续的 S[i] 字符，要么是一个单独的 S[i] 字符，构成独立片段
                        // 由于已有组号，所以不必再处理
                        continue;
                    }
                } else {
                    // 异常情况，毕竟正向都出现了 S[i]，那么反向查找 S[i] 肯定也能找到
                    continue;
                }
            }
        }
        
        // 整合分隔开的相同组，为一个整体（可以省略）
        
        // 查看各个字符的组号
//        for (int i = 0; i < len; i++) {
//            if (memo.find(S[i]) != memo.end()) {
//                cout << S[i] << ":" << memo[S[i]] << ", ";
//            }
//        }
//        cout << " End." <<endl;
        
        // 两两比较统计长度（前提是分隔开的相同组已被整合）
//        int count = 1;
//        for (int i = 0; i < len; i++) {
//            if (memo.find(S[i]) != memo.end()) {
//                // cout << S[i] << ": " << memo[S[i]] << ", count=" << count << endl;
//                if (i < (len - 1) && memo[S[i]] == memo[S[i + 1]]) {
//                    count ++;
//                } else {
//                    res.push_back(count);
//                    count = 1;
//                }
//            } else {
//                // 异常情况，因为每个字符都应有组号的
//                continue;
//            }
//        }
        
        // 前后比较统计长度
        for (int i = 0; i < len; i++) {
            if (memo.find(S[i]) != memo.end()) {
                // 从第一个 x 组元素，找到最后一个 x 组元素，其间的都是该组元素
                // cout << S[i] << ": " << memo[S[i]] << ", count=" << count << endl;
                int cur_group_id = memo[S[i]];
                bool find_flag = false;
                int j = len - 1;
                for (; j > i; j--) {
                    if (memo[S[j]] == cur_group_id) {
                        find_flag = true;
                        break;
                    }
                }
                
                if (find_flag) {
                    // 如果找到了，那就统计该组总元素个数
                    res.push_back(j - i + 1);
                    i = j; // i -> j + 1
                } else {
                    // 如果找不到，那就表示该字符只属于一个组
                    res.push_back(1);
                }
            } else {
                // 异常情况，因为每个字符都应有组号的
                continue;
            }
        }
        
        return res;
    }
    
    // 方法二。区间扩展法、贪心算法。时间复杂度 O(N)，空间复杂度 O(N)，较快。
    // 本题主要思路是区间交集问题：如果两个区间有交集，那么两区间内所有元素都是同一组。
    vector<int> solution2(string S) {
        vector<int> res = {};
        int len = (int)S.size();
        
        // 存放每个字符最后一次出现的下标位置
        map<char, int> memo = {};
        for (int i = len - 1; i >= 0; i--) {
            if (memo.find(S[i]) == memo.end()) {
                memo.insert({S[i], i});
            } else {
                continue;
            }
        }
        
        // preRight 表示上个区间的右端点
        // maxRight 表示当前组的字符最后出现位置的最大值
        int preRight = -1;
        int maxRight = 0;
        
        for (int i = 0; i < len; i++) {
            // 获得当前字符的最后出现的位置，即当前字符的区间右边界
            int right;
            if (memo.find(S[i]) != memo.end()) {
                right = memo[S[i]];
            } else {
                // 异常情况，因为每个字符都应被记录其最后出现的位置
                continue;
            }
            
            // 如果当前字符的右边界超过组最大右边界，则更新之，向右扩展
            if (right > maxRight) {
                maxRight = right;
            }
            
            // i 到达当前组的右边界，本组遍历结束
            if (i == maxRight) {
                // 添加区间的长度
                res.push_back(maxRight - preRight);
                
                // 将当前组右边界记录到 preIndex 中
                preRight = maxRight;
            }
            
            // 如果 i 未到达当前组的右边界，那么会继续找下一字符，直到抵达当前组的右边界
            // 在继续找字符的过程中，可能会不断扩展当前组的最大右边界值。
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string S = "ababcbacadefegdehijhklij"; // 预期结果 [9, 7, 8]
    string S = "mlullbhiuiujgvwvurcdvhzdk"; // 预期结果 [1, 23, 1]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->partitionLabels(S);
    if (!ans.empty()) {
        for (int i = 0; i < (int)ans.size(); i++) {
            cout << ans[i] << ", ";
        }
        cout << "End." << endl;
    } else {
        cout << "Answer is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
