//
//  main.cpp
//  Prob1986_Interval_List_Intersections
//
//  Created by 阴昱为 on 2019/6/16.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1986. Interval List Intersections
//
//Given two lists of closed intervals, each list of intervals is pairwise disjoint and in sorted order.
//
//Return the intersection of these two interval lists.
//
//(Formally, a closed interval [a, b] (with a <= b) denotes the set of real numbers x with a <= x <= b.  The intersection of two closed intervals is a set of real numbers that is either empty, or can be represented as a closed interval.  For example, the intersection of [1, 3] and [2, 4] is [2, 3].)
//
//给定两个由一些闭区间组成的列表，每个区间列表都是成对不相交的，并且已经排序。
//
//返回这两个区间列表的交集。
//
//（形式上，闭区间 [a, b]（其中 a <= b）表示实数 x 的集合，而 a <= x <= b。两个闭区间的交集是一组实数，要么为空集，要么为闭区间。例如，[1, 3] 和 [2, 4] 的交集为 [2, 3]。）
//
//Example 1:
//    Input: A = [[0,2],[5,10],[13,23],[24,25]], B = [[1,5],[8,12],[15,24],[25,26]]
//    Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
//    Reminder: The inputs and the desired output are lists of Interval objects, and not arrays or lists.
//
//Note:
//    0 <= A.length < 1000
//    0 <= B.length < 1000
//    0 <= A[i].start, A[i].end, B[i].start, B[i].end < 10^9
//NOTE: input types have been changed on April 15, 2019. Please reset to default code definition to get new method signature.
//注意：输入和所需的输出都是区间对象组成的列表，而不是数组或列表。


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
    vector<vector<int>> intervalIntersection(vector<vector<int>>& A, vector<vector<int>>& B) {
        // 边界情况
        if (A.empty() || B.empty()) {
            return {};
        }
        
        // 数据预处理，保证 A 和 B 的元素都是有且仅有两个元素的向量
        for (auto ite = A.begin(); ite < A.end();) {
            if ((*ite).size() != 2) {
                A.erase(ite);
            } else {
                ite ++;
            }
        }
        
        for (auto ite = B.begin(); ite < B.end();) {
            if ((*ite).size() != 2) {
                B.erase(ite);
            } else {
                ite ++;
            }
        }
        
        // 调用核心解决方案
        return this->solution1(A, B);
    }
    
private:
    // 方法一。区间包含判断法。时间复杂度 O()，空间复杂度 O()，较快
    vector<vector<int>> solution1(vector<vector<int>>& A, vector<vector<int>>& B) {
        vector<vector<int>> res = {};
        
        int A_len = (int)A.size();
        int B_len = (int)B.size();
        
        int A_index = 0;
        int B_index = 0;
        
        while (A_index < A_len && B_index < B_len) {
            int low = max(A[A_index][0], B[B_index][0]); // 交集的起点
            int high = min(A[A_index][1], B[B_index][1]); // 交集的终点
            
            // 起点不大于终点，表示有交集
            if (low <= high) {
                res.push_back({low, high});
            }
            
            // 终点更小那个区间是已经使用过的，所以考虑该区间的下一个区间
            if (A[A_index][1] < B[B_index][1]) {
                A_index ++;
            } else {
                B_index ++;
            }
        }
        
        return res;
    }
    
    // 方法二。区间端点比较法。时间复杂度 O(m+n)，空间复杂度 O(m+n)，基础判断语句较多，因此较慢
    vector<vector<int>> solution2(vector<vector<int>>& A, vector<vector<int>>& B) {
        vector<vector<int>> res = {};
        
        int A_len = (int)A.size();
        int B_len = (int)B.size();
        
        int A_index = 0;
        int B_index = 0;
        
        while (A_index < A_len && B_index < B_len) {
            if (A[A_index][0] <= B[B_index][0]) { // A.start <= B.start
                if (A[A_index][1] >= B[B_index][0]) { // A.end >= B.start
                    if (A[A_index][1] >= B[B_index][1]) { // A.end >= B.end
                        // 此时表明 B 是 A 的子集
                        res.push_back({B[B_index][0], B[B_index][1]});
                        // B[B_index] 用尽了，考虑下一个 B
                        B_index ++;
                    } else { // A.end < B.end
                        // 此时 B 比 A 末尾还多一些元素
                        res.push_back({B[B_index][0], A[A_index][1]});
                        // A[A_index] 用尽了，考虑下一个 A
                        A_index ++;
                    }
                } else { // A.end < B.start
                    // 此时 A 远在 B 之前，二者无交集，考虑下一个 A
                    A_index ++;
                }
            } else { // A.start > B.start
                if (B[B_index][1] >= A[A_index][0]) { // B.end >= A.start
                    if (B[B_index][1] >= A[A_index][1]) { // B.end >= A.end
                        // 此时表明 A 是 B 的子集
                        res.push_back({A[A_index][0], A[A_index][1]});
                        // A[A_index] 用尽了，考虑下一个 A
                        A_index ++;
                    } else { // B.end < A.end
                        // 此时 A 比 B 末尾还多一些元素
                        res.push_back({A[A_index][0], B[B_index][1]});
                        // B[B_index] 用尽了，考虑下一个 B
                        B_index ++;
                    }
                } else { // B.end < A.start
                    // 此时 B 远在 A 之前，二者无交集，考虑下一个 B
                    B_index ++;
                }
            }
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
    // 预期输出 [[1,2], [5,5], [8,10], [15,23], [24,24], [25,25]]
    vector<vector<int>> A = {{0, 2}, {5, 10}, {13, 23}, {24, 25}};
    vector<vector<int>> B = {{1, 5}, {8, 12}, {15, 24}, {25, 26}};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->intervalIntersection(A, B);
    if (!ans.empty()) {
        for (int i = 0; i < (int)ans.size(); i++) {
            if (!ans[i].empty()) {
                cout << "[";
                for (int j = 0; j < (int)ans[i].size(); j++) {
                    cout << ans[i][j] << ",";
                }
                cout << "],";
            }
        }
        cout << "End." << endl;
    } else {
        cout << "No Answer." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
