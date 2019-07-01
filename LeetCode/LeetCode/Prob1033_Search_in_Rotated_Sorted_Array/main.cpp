//
//  main.cpp
//  Prob1033_Search_in_Rotated_Sorted_Array
//
//  Created by 阴昱为 on 2019/7/1.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//33. Search in Rotated Sorted Array
//
//Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
//(i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).
//You are given a target value to search. If found in the array return its index, otherwise return -1.
//You may assume no duplicate exists in the array.
//Your algorithm's runtime complexity must be in the order of O(log n).
//
//假设按照升序排序的数组在预先未知的某个点上进行了旋转。
//( 例如，数组 [0,1,2,4,5,6,7] 可能变为 [4,5,6,7,0,1,2] )。
//搜索一个给定的目标值，如果数组中存在这个目标值，则返回它的索引，否则返回 -1 。
//你可以假设数组中不存在重复的元素。
//你的算法时间复杂度必须是 O(log n) 级别。
//
//Example 1:
//    Input: nums = [4,5,6,7,0,1,2], target = 0
//    Output: 4
//
//Example 2:
//    Input: nums = [4,5,6,7,0,1,2], target = 3
//    Output: -1


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
    int search(vector<int>& nums, int target) {
        return this->solution1(nums, target);
    }
    
private:
    // 方法一：两次二分查找，先找转折点，再找目标数。
    // 时间复杂度 O(lg N)，空间复杂度 O(1)。N = nums.length
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 95.31% 的用户
    // 内存消耗 : 8.9 MB , 在所有 C++ 提交中击败了 71.98% 的用户
    // Runtime: 4 ms, faster than 88.79% of C++ online submissions for Search in Rotated Sorted Array.
    // Memory Usage: 8.8 MB, less than 26.69% of C++ online submissions for Search in Rotated Sorted Array.
    int solution1 (vector<int>& nums, int target) {
        // 边界情况
        if (nums.empty()) {
            return -1;
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            return nums[0] == target ? 0 : -1;
        }
        
        int res = -1;
        
        // 没有转折点，直接对整个数组进行二分查找
        if (nums[0] < nums[len - 1]) {
            return this->binarySearch(nums, target, 0, len - 1);
        }
        
        int min_index = this->findMinIndex(nums, 0, len - 1);
        
        // 没有转折点，直接对整个数组进行二分查找
        if (min_index <= 0) {
            return this->binarySearch(nums, target, 0, len - 1);
        }
        
        // 此时 nums[0..min_index-1] 为值较大的有序子数组
        // nums[min_index..len-1] 为值较小的有序子数组，nums[0] 可以区分两段
        if (target == nums[0]) {
            // 直接命中
            res = 0;
        } else if (target > nums[0]) {
            // 在值较大的有序子数组中查找
            res = this->binarySearch(nums, target, 1, min_index - 1);
        } else {
            // 在值较小的有序子数组中查找
            res = this->binarySearch(nums, target, min_index, len - 1);
        }
        
        return res;
    }
    
    // 找到最小值所在下标，即旋转点。nums 为升序、降序、升序结构
    int findMinIndex (vector<int>& nums, int start, int end) {
        if (start > end || start < 0 || end >= (int)nums.size()) {
            return -1;
        }
        
        if (start == end) {
            if (start >= (int)nums.size() - 1) {
                return -1;
            } else {
                if (nums[start] > nums[start + 1]) {
                    return start + 1;
                }
            }
        }
        
        int mid = (start + end) >> 1;
        if (nums[mid] > nums[mid + 1]) {
            // 找到了降序的那个位置
            return mid + 1;
        } else {
            if (nums[mid] > nums[start]) {
                // 如果 mid 值大于 start 值，表示从nums[start..mid] 都保持升序
                // 此时应在右侧子数组找旋转点
                return this->findMinIndex(nums, mid, end);
            } else {
                // 否则在左侧子数组找旋转点
                return this->findMinIndex(nums, start, mid);
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
            } else {
                return -1;
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
    // 预期结果 4
//    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};
//    int target = 0;
    
    // 预期结果 -1
//    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};
//    int target = 3;
    
    // 预期结果 -1
    vector<int> nums = {8, 1, 2, 3, 4, 5, 6};
    int target = 7;
    
    // 预期结果 7
//    vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 0};
//    int target = 0;
    
    // 预期结果 6
//    vector<int> nums = {0, 1, 2, 3, 4, 5, 6, 7};
//    int target = 6;
    
    // 预期结果 2
//    vector<int> nums = {1, 3, 5};
//    int target = 5;
    
    // 预期结果 0
//    vector<int> nums = {5, 1, 3};
//    int target = 5;
    
    // 预期结果 1
//    vector<int> nums = {8, 9, 2, 3, 4};
//    int target = 9;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans =solution->search(nums, target);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
