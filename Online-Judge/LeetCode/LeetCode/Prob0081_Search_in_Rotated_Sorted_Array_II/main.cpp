//
//  main.cpp
//  Prob1081_Search_in_Rotated_Sorted_Array_II
//
//  Created by 阴昱为 on 2019/8/1.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//81. Search in Rotated Sorted Array II
//
//Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
//(i.e., [0,0,1,2,2,5,6] might become [2,5,6,0,0,1,2]).
//You are given a target value to search. If found in the array return true, otherwise return false.
//
//假设按照升序排序的数组在预先未知的某个点上进行了旋转。
//( 例如，数组 [0,0,1,2,2,5,6] 可能变为 [2,5,6,0,0,1,2] )。
//编写一个函数来判断给定的目标值是否存在于数组中。若存在返回 true，否则返回 false。
//
//Example 1:
//    Input: nums = [2,5,6,0,0,1,2], target = 0
//    Output: true
//
//Example 2:
//    Input: nums = [2,5,6,0,0,1,2], target = 3
//    Output: false
//
//Follow up:
//    This is a follow up problem to Search in Rotated Sorted Array, where nums may contain duplicates.
//    Would this affect the run-time complexity? How and why?
//
//进阶:
//    这是 搜索旋转排序数组 的延伸题目，本题中的 nums  可能包含重复元素。
//    这会影响到程序的时间复杂度吗？会有怎样的影响，为什么？


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    bool search(vector<int>& nums, int target) {
        return this->solution1(nums, target);
    }
    
private:
    // 方法一：先进行伪二分查找，找转折点，再进行二分查找，找目标数。
    // 时间复杂度 O(N)，空间复杂度 O(1)。N = nums.length
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 55.36% 的用户
    // 内存消耗 : 8.6 MB , 在所有 C++ 提交中击败了 64.14% 的用户
    // Runtime: 4 ms, faster than 98.84% of C++ online submissions for Search in Rotated Sorted Array II.
    // Memory Usage: 8.8 MB, less than 70.70% of C++ online submissions for Search in Rotated Sorted Array II.
    int solution1 (vector<int>& nums, int target) {
        // 边界情况
        if (nums.empty()) {
            return false;
        }
        
        int len = (int)nums.size();
        int start = nums[0];
        
        if (len == 1) {
            return start == target;
        }
        
        // 没有转折点，直接对整个数组进行二分查找
        if (start < nums[len - 1]) {
            return this->binarySearch(nums, target, 0, len - 1) >= 0;
        }
        
        // 判断是否全为相同值 O(N)
//        bool all_same = true;
//        for (int i = 0; i < len; i++) {
//            if (nums[i] != start) {
//                all_same = false;
//                break;
//            }
//        }
//
//        if (all_same) {
//            return target == start;
//        }
        
        int min_index = this->findMinIndex(nums, 0, len - 1);
        
        // 没有转折点，直接对整个数组进行二分查找
        if (min_index <= 0) {
            return this->binarySearch(nums, target, 0, len - 1) >= 0;
        }
        
        int res = -1;
        // 此时 nums[0..min_index-1] 为值较大的有序子数组
        // nums[min_index..len-1] 为值较小的有序子数组，nums[0] 可以区分两段
        if (target == start) {
            // 直接命中
            res = 0;
        } else if (target > start) {
            // 在值较大的有序子数组中查找
            res = this->binarySearch(nums, target, 1, min_index - 1);
        } else {
            // 在值较小的有序子数组中查找
            res = this->binarySearch(nums, target, min_index, len - 1);
        }
        
        return res >= 0;
    }
    
    // 找到最小值所在下标，即旋转点。nums 为升序、降序、升序结构
    int findMinIndex (vector<int>& nums, int start, int end) {
        if (start > end || start < 0 || end >= (int)nums.size()) {
            return -1;
        }
        
        if (start + 1 == end) {
            if (nums[start] > nums[end]) {
                return end;
            } else {
                return -1; // 没有转折点
            }
        }
        
        if (start == end) {
            if (start >= (int)nums.size() - 1) {
                return -1;
            } else {
                if (nums[start] > nums[start + 1]) {
                    return start + 1; // 最小值点
                } else {
                    return -1; // 没有转折点
                }
            }
        }
        
        int mid = (start + end) >> 1;
        if (nums[mid] > nums[mid + 1]) {
            // 找到了降序的那个位置
            return mid + 1;
        } else {
            if (nums[mid] > nums[start]) {
                // 如果 mid 值大于 start 值，表示从 nums[start..mid] 都保持升序
                // 此时应在右侧子数组找旋转点
                return this->findMinIndex(nums, mid, end);
            } else {
                // 否则左右侧子数组都要考虑
                int left = this->findMinIndex(nums, start, mid);
                if (left > 0) {
                    return left;
                } else {
                    return this->findMinIndex(nums, mid, end);
                }
            }
        }
    }
    
    // 二分查找
    int binarySearch (vector<int>& nums, int& target, int start, int end) {
        if (start > end || start < 0 || end >= (int)nums.size()) {
            return -1;
        }
        
        if (start == end) {
            if (nums[start] == target) {
                return start;
            }
        }
        
        int mid = (start + end) >> 1;
        if (nums[mid] == target) {
            // 命中目标
            return mid;
        } else if (target < nums[mid]) {
            // 往左找
            return this->binarySearch(nums, target, start, mid - 1);
        } else {
            // 往右找
            return this->binarySearch(nums, target, mid + 1, end);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {2, 5, 6, 0, 0, 1, 2};
    vector<int> nums = {0, 0, 0, 0, 0};
    int target = 0; // 预期结果 true
//    int target = 3; // 预期结果 false
    
//    vector<int> nums = {2, 2, 2, 3, 1};
//    int target = 1; // 预期结果 true
    
//    vector<int> nums = {1, 3, 1, 1, 1};
//    int target = 3; // 预期结果 true
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    bool ans = solution->search(nums, target);
    if (ans) {
        cout << target << " is in nums." << endl;
    } else {
        cout << target << " is NOT in nums." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
