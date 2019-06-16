//
//  main.cpp
//  Prob1057_Insert_Interval
//
//  Created by 阴昱为 on 2019/6/16.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1057. Insert Interval
//
//Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).
//You may assume that the intervals were initially sorted according to their start times.
//
//给出一个无重叠的 ，按照区间起始端点排序的区间列表。
//在列表中插入一个新的区间，你需要确保列表中的区间仍然有序且不重叠（如果有必要的话，可以合并区间）。
//
//Example 1:
//    Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
//    Output: [[1,5],[6,9]]
//
//Example 2:
//    Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
//    Output: [[1,2],[3,10],[12,16]]
//    Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
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



// Definition for an interval.
struct Interval {
    int start;
    int end;
    Interval () : start(0), end(0) {}
    Interval (int s, int e) : start(s), end(e) {}
};


class Solution {
public:
    // TODO 本题的几个方法还是不够快，C++ 提交结果中未超过 90+%
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        return this->solution3(intervals, newInterval);
    }
    
    // 牛客网 LeetCode 题目
    vector<Interval> insert(vector<Interval> &intervals, Interval newInterval) {
        return this->solution4(intervals, newInterval);
    }
    
private:
    // 方法零。先在有序向量中找到插入位置，然后只调整与新区间相关的区间。
    // 区间包含判断法，顺序合并，一次合并多个区间。时间复杂度 O(NlogN)，空间复杂度 O()
    vector<vector<int>> solution0(vector<vector<int>>& intervals, vector<int>& newInterval) {
        // 边界情况
        if (intervals.empty()) {
            return {newInterval};
        }
        
        if (newInterval[1] < intervals[0][0]) {
            // 如果新区间的右边界比原区间组第一个区间的左边界还小，则插入到首位置
            intervals.insert(intervals.begin(), newInterval);
            return intervals;
        }
        
        if (newInterval[0] > intervals[(int)intervals.size() - 1][1]) {
            // 如果新区间的左边界比原区间组最后一个区间的右边界还大，则插入到末尾位置
            intervals.insert(intervals.end(), newInterval);
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
        
        vector<vector<int>> res = {};
        
        int len = (int)intervals.size();
        
        // 二分查找定位插入位置
        int insert_index = this->divideSearch(intervals, newInterval, 0, len - 1);
        // cout << "insert_index = " << insert_index << endl;
        if (insert_index < 0) {
            cout << "Error ! insert_index = " << insert_index << endl;
            return intervals;
        }
        
        // 插入到 intervals 中
        intervals.insert(intervals.begin() + insert_index, newInterval);
        len = (int)intervals.size();
        
        // 在新区间前一个区间之前 的所有区间 都可以直接加入 res
        for (int i = 0; i < insert_index - 1; i ++) {
            res.push_back(intervals[i]);
        }
        
        // 根据插入位置来赋值：
        // 当插入区间不为首区间时，left 和 right 分别是新区间前一个区间的左边界和右边界，index 是新区间的下标
        // 当插入区间是首区间时，left 和 right 分别是新区间的左边界和右边界，index 是新区间下一个区间的下标
        int left, right, index;
        if (insert_index > 0) {
            left = intervals[insert_index - 1][0];
            right = intervals[insert_index - 1][1];
            index = insert_index;
        } else {
            left = intervals[0][0];
            right = intervals[0][1];
            index = 1;
        }
        
        for (; index < len; index++) {
            if (intervals[index][0] <= right) {
                // 如果有交集，扩大右边界 right
                right = max(right, intervals[index][1]);
            } else {
                // 如果没交集，把之前的整段区间加入结果集
                res.push_back({left, right});
                
                // 然后处理新的区间
                left = intervals[index][0];
                right = intervals[index][1];
            }
        }
        // 把最后一段区间加到结果集
        res.push_back({left, right});
        
        return res;
        
//        cout << left << ", " << right << ", " << i << endl;
//
//        int most_count = 2; // 至多无交集两次：插入区间的前一个区间与插入区间、插入区间与之后的区间
//        for (; i < len; i++) {
//            if (intervals[i][0] <= right) {
//                // 如果有交集，扩大右边界 right
//                right = max(right, intervals[i][1]);
//
//                merged_count ++;
//            } else {
//                most_count --;
//                cout << "most_count = " << most_count << endl;
//                cout << "merged_count = " << merged_count << endl;
//                // 如果没交集，不必处理后面的区间了
//                if (most_count <= 0) {
//                    break;
//                } else {
//                    // 如果合并过集合，那就把之前的整段区间加入结果集
//                    if (merged_count > 0) {
//                        if (insert_index == 0) {
//                            intervals[0] = {left, right};
//                            // 删除被合并的那些区间
//                            intervals.erase(intervals.begin() + 1,
//                                            intervals.begin() + 1 + merged_count);
//                        } else {
//                            intervals[insert_index - 1] = {left, right};
//                            // 删除被合并的那些区间
//                            intervals.erase(intervals.begin() + insert_index,
//                                            intervals.begin() + insert_index + merged_count);
//                        }
//                        merged_count = 0;
//                    }
//                }
//            }
//        }
//
//        cout << insert_index << ", " << merged_count << endl;
//        // 如果合并过集合，那就把之前的整段区间加入结果集
//        if (merged_count > 0) {
//            if (insert_index == 0) {
//                intervals[0] = {left, right};
//                // 删除被合并的那些区间
//                intervals.erase(intervals.begin() + 1,
//                                intervals.begin() + 1 + merged_count);
//            } else {
//                intervals[insert_index - 1] = {left, right};
//                // 删除被合并的那些区间
//                intervals.erase(intervals.begin() + insert_index,
//                                intervals.begin() + insert_index + merged_count);
//            }
//        }
//
//        return intervals;
    }
    
    // 在有序向量中进行二分查找，返回应该插入的下标（应该插入在该下标元素的前面）
    int divideSearch (vector<vector<int>> intervals, vector<int> newInterval, int left, int right) {
        if (left >= right) {
            if (newInterval[0] <= intervals[left][0]) {
                return left;
            } else {
                return left + 1;
            }
        }
        
        int mid = (right + left) / 2;
        
        if (newInterval[0] == intervals[mid][0]) {
            return mid;
        } else if (newInterval[0] < intervals[mid][0]) {
            return this->divideSearch(intervals, newInterval, left, mid - 1);
        } else {
            return this->divideSearch(intervals, newInterval, mid + 1, right);
        }
    }
    
    // 方法一。暴力法，加进新元素重新排序，然后处理合并。
    // 区间包含判断法，顺序合并，两两合并。时间复杂度 O(NlogN)，空间复杂度 O(1)
    vector<vector<int>> solution1(vector<vector<int>>& intervals, vector<int>& newInterval) {
        // 边界情况
        if (intervals.empty()) {
            return {newInterval};
        }
        
        if (newInterval[1] < intervals[0][0]) {
            // 如果新区间的右边界比原区间组第一个区间的左边界还小，则插入到首位置
            intervals.insert(intervals.begin(), newInterval);
            return intervals;
        }
        
        if (newInterval[0] > intervals[(int)intervals.size() - 1][1]) {
            // 如果新区间的左边界比原区间组最后一个区间的右边界还大，则插入到末尾位置
            intervals.insert(intervals.end(), newInterval);
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
        
        // 直接把新区间加到末尾
        intervals.push_back(newInterval);
        
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
    
    // 方法二。暴力法，加进新元素重新排序，然后处理合并。
    // 区间包含判断法，顺序合并，一次合并多个区间。时间复杂度 O(NlogN)，空间复杂度 O(N)
    vector<vector<int>> solution2(vector<vector<int>>& intervals, vector<int>& newInterval) {
        // 边界情况
        if (intervals.empty()) {
            return {newInterval};
        }
        
        if (newInterval[1] < intervals[0][0]) {
            // 如果新区间的右边界比原区间组第一个区间的左边界还小，则插入到首位置
            intervals.insert(intervals.begin(), newInterval);
            return intervals;
        }
        
        if (newInterval[0] > intervals[(int)intervals.size() - 1][1]) {
            // 如果新区间的左边界比原区间组最后一个区间的右边界还大，则插入到末尾位置
            intervals.insert(intervals.end(), newInterval);
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
        
        // 直接把新区间加到末尾
        intervals.push_back(newInterval);
        
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
    
    // 方法三。一遍扫描，时间复杂度 O(N)，空间复杂度 O(N)
    vector<vector<int>> solution3(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> res;
        
        int index = 0;
        // 把所有右边界小于新区间左边界的区间（它们不可能与新区间有交集）直接加入 res
        while (index < intervals.size() && intervals[index][1] < newInterval[0]) {
            res.push_back(intervals[index++]);
        }
        
        // 如果某区间的左边界小于等于新区间的右边界，表示二者有交集，处理之
        while (index < (int)intervals.size() && intervals[index][0] <= newInterval[1]) {
            // 修改新区间（扩张 or 不变）
            newInterval[1] = max(newInterval[1], intervals[index][1]);
            newInterval[0] = min(newInterval[0], intervals[index][0]);
            index ++;
        }
        // 处理到此，由于原题目的条件，之前的向量本来是排好序、无交集的
        // 所以合并操作只会连续执行，一旦停下，之后的区间就不可能再与新区间有交集了
        res.push_back(newInterval);
        
        // 把剩下的区间都加入 res
        while (index < intervals.size()) {
            res.push_back(intervals[index++]);
        }
        
        return res;
    }
    
    // 方法四，与方法二思路相同，用于牛客网的输入情况
    vector<Interval> solution4(vector<Interval> &intervals, Interval newInterval) {
        // 边界情况
        if (intervals.empty()) {
            return {newInterval};
        }
        
        if (newInterval.end < intervals[0].start) {
            // 如果新区间的右边界比原区间组第一个区间的左边界还小，则插入到首位置
            intervals.insert(intervals.begin(), newInterval);
            return intervals;
        }
        
        if (newInterval.start > intervals[(int)intervals.size() - 1].end) {
            // 如果新区间的左边界比原区间组最后一个区间的右边界还大，则插入到末尾位置
            intervals.insert(intervals.end(), newInterval);
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
        
        // 直接把新区间加到末尾
        intervals.push_back(newInterval);
        
        // 区间排序，头号排序指标为更小的左边界，次级排序指标为更小的右边界
        sort(intervals.begin(), intervals.end(), this->myIntervalObjectComp);
        
        vector<Interval> res = {};
        
        int left = intervals[0].start;
        int right = intervals[0].end;
        int len = (int)intervals.size();
        
        for (int i = 1; i < len; i++) {
            if (intervals[i].start <= right) {
                // 如果有交集，扩大右边界 right
                right = max(right, intervals[i].end);
            } else {
                // 如果没交集，把之前的整段区间加入结果集
                res.push_back({left, right});
                
                // 然后处理新的区间
                left = intervals[i].start;
                right = intervals[i].end;
            }
        }
        // 把最后一段区间加到结果集
        res.push_back({left, right});
        
        return res;
    }
    
    // 区间排序函数，头号排序指标为更小的左边界，次级排序指标为更小的右边界
    static bool myIntervalObjectComp (Interval& a, Interval& b) {
        if (a.start == b.start) {
            return a.end < b.end;
        } else {
            return a.start < b.start;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期输出 [[1,2], [3,10], [12,16]]
//    vector<vector<int>> intervals = {{1, 2}, {3, 5}, {6, 7}, {8, 10}, {12, 16}};
//    vector<int> newInterval = {4, 8};
    
//    vector<vector<int>> intervals = {{1, 5}}; // 预期输出 [[1,5]]
//    vector<int> newInterval = {2, 3};
    
//    vector<vector<int>> intervals = {{1, 5}}; // 预期输出 [[1,7]]
//    vector<int> newInterval = {1, 7};
    
    vector<vector<int>> intervals = {{0, 5}, {9, 12}}; // 预期输出 [[0,5], [7,16]]
    vector<int> newInterval = {7, 16};
    
    vector<Interval> intervals2 = {Interval(1, 2), Interval(3, 5), Interval(6, 7),
        Interval(8, 10), Interval(12, 16)};
    Interval newInterval2 = Interval(4, 8);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->insert(intervals, newInterval);
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
    
    vector<Interval> ans2 = solution->insert(intervals2, newInterval2);
    if (!ans2.empty()) {
        for (int i = 0; i < (int)ans2.size(); i++) {
            cout << "[" << ans2[i].start << "," << ans2[i].end << "], ";
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
