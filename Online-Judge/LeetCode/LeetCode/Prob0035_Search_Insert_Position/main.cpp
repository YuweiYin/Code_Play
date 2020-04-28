//
//  main.cpp
//  Prob1035_Search_Insert_Position
//
//  Created by 阴昱为 on 2019/7/2.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//35. Search Insert Position
//
//Given a sorted array and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
//You may assume no duplicates in the array.
//
//给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。
//你可以假设数组中无重复元素。
//
//Example 1:
//    Input: [1,3,5,6], 5
//    Output: 2
//
//Example 2:
//    Input: [1,3,5,6], 2
//    Output: 1
//
//Example 3:
//    Input: [1,3,5,6], 7
//    Output: 4
//
//Example 4:
//    Input: [1,3,5,6], 0
//    Output: 0


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
    int searchInsert(vector<int>& nums, int target) {
        return this->solution1(nums, target);
    }
    
private:
    // 方法一：二分查找。
    // 时间复杂度 O(lg N)，空间复杂度 O(1)。N = nums.length
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 92.63% 的用户
    // 内存消耗 : 9 MB , 在所有 C++ 提交中击败了 71.37% 的用户
    // Runtime: 4 ms, faster than 99.27% of C++ online submissions for Search Insert Position.
    // Memory Usage: 8.8 MB, less than 74.68% of C++ online submissions for Search Insert Position.
    int solution1 (vector<int>& nums, int target) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            if (nums[0] == target) {
                return 0;
            } else {
                return target < nums[0] ? 0 : 1;
            }
        }
        
        int res = -1;
        
        // 二分查找，找到最靠左的 target 下标和最靠右的 target 下标
        res = this->binarySearch(nums, target, 0, len - 1);
        
        return res;
    }
    
    // 二分查找
    int binarySearch (vector<int>& nums, int& target, int start, int end) {
        if (start < 0 || end >= (int)nums.size()) {
            return -1; // Error
        }
        
        // 指针交叉，上一轮的 start 和 end 相差为一，mid 等于 start，
        // 然后 mid-1 就比 start 小了，所以本轮会出现交叉
        if (start > end) {
            // 如果是
            if (start >= (int)nums.size()) {
                return (int)nums.size();
            } else {
                return start;
            }
        }
        
        if (start == end) {
            // 此处与普通二分查找不同
            if (target <= nums[start]) {
                return start;
            } else {
                return start + 1;
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
    // 预期结果 2
//    vector<int> nums = {1, 3, 5, 6};
//    int target = 5;
    
    // 预期结果 1
//    vector<int> nums = {1, 3, 5, 6};
//    int target = 2;
    
    // 预期结果 4
//    vector<int> nums = {1, 3, 5, 6};
//    int target = 7;
    
    // 预期结果 0
//    vector<int> nums = {1, 3, 5, 6};
//    int target = 0;
    
    // 预期结果 0
    vector<int> nums = {1, 3};
    int target = -1;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->searchInsert(nums, target);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
