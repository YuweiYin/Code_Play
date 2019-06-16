//
//  main.cpp
//  Prob1056_Merge_Intervals
//
//  Created by 阴昱为 on 2019/6/16.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1056. Merge Intervals
//
//Given a collection of intervals, merge all overlapping intervals.
//
//给出一个区间的集合，请合并所有重叠的区间。
//
//Example 1:
//    Input: [[1,3],[2,6],[8,10],[15,18]]
//    Output: [[1,6],[8,10],[15,18]]
//    Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].
//
//Example 2:
//    Input: [[1,4],[4,5]]
//    Output: [[1,5]]
//    Explanation: Intervals [1,4] and [4,5] are considered overlapping.
//
//NOTE: input types have been changed on April 15, 2019. Please reset to default code definition to get new method signature.


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
    // TODO 本题的两个方法还是不够快，C++ 提交结果中未超过 90+%
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        // 调用核心解决方案
        return this->solution2(intervals);
    }
    
private:
    // 方法一。区间包含判断法，顺序合并，两两合并。时间复杂度 O(NlogN)，空间复杂度 O(1)
    vector<vector<int>> solution1(vector<vector<int>>& intervals) {
        // 边界情况
        if (intervals.empty() || (int)intervals.size() == 1) {
            return intervals;
        }
        
        // 数据预处理，保证 intervals 的元素都是有且仅有两个元素的向量
//        for (auto ite = intervals.begin(); ite < intervals.end();) {
//            if ((*ite).size() != 2) {
//                intervals.erase(ite);
//            } else {
//                ite ++;
//            }
//        }
        
        // 区间排序，头号排序指标为更小的左边界，次级排序指标为更小的右边界
        sort(intervals.begin(), intervals.end(), this->myIntervalComp);
        
        vector<vector<int>> res = {};
        
        auto ite = intervals.begin();
        while (ite < intervals.end() - 1) {
            // 后一个起点不大于前一个终点，表示有交集
            if ((*(ite + 1))[0] <= (*ite)[1]) {
                // 改变前一个区间值
                *ite = {(*ite)[0], max((*ite)[1], (*(ite + 1))[1])};
                // 删去后一个区间（erase 函数效率太低）
                intervals.erase(ite + 1);
            } else {
                // 考虑下一组区间是否有交集
                ite ++;
            }
        }
        
        return intervals;
    }
    
    // 区间排序函数，头号排序指标为更小的左边界，次级排序指标为更小的右边界
    static bool myIntervalComp (vector<int>& a, vector<int>& b) {
        if (a.empty() || b.empty()) {
            return true;
        } else {
            if (a[0] == b[0]) {
                return a[1] < b[1];
            } else {
                return a[0] < b[0];
            }
        }
    }
    
    // 方法二。区间包含判断法，顺序合并，一次合并多个区间。时间复杂度 O(NlogN)，空间复杂度 O(N)
    vector<vector<int>> solution2(vector<vector<int>>& intervals) {
        // 边界情况
        if (intervals.empty() || (int)intervals.size() == 1) {
            return intervals;
        }
        
        // 数据预处理，保证 intervals 的元素都是有且仅有两个元素的向量
//        for (auto ite = intervals.begin(); ite < intervals.end();) {
//            if ((*ite).size() != 2) {
//                intervals.erase(ite);
//            } else {
//                ite ++;
//            }
//        }
        
        // 区间排序，头号排序指标为更小的左边界，次级排序指标为更小的右边界
        sort(intervals.begin(), intervals.end(), this->myIntervalComp);
        
        vector<vector<int>> res = {};
        
        int left = intervals[0][0];
        int right = intervals[0][1];
        int len = (int)intervals.size();
        
        for (int i = 1; i < len; i++) {
            if (intervals[i][0] <= right) {
                // 如果有交集，扩大右边界 right
                right = max(right, intervals[i][1]);
            } else {
                // 如果没交集，把之前的整段区间加入结果集
                res.push_back({left, right});
                
                // 然后处理新的区间
                left = intervals[i][0];
                right = intervals[i][1];
            }
        }
        // 把最后一段区间加到结果集
        res.push_back({left, right});
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期输出 [[1,6], [8,10], [15,18]]
    vector<vector<int>> intervals = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->merge(intervals);
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
