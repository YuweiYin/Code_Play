//
//  main.cpp
//  Prob1034_Find_First_and_Last_Position_of_Element_in_Sorted_Array
//
//  Created by 阴昱为 on 2019/7/2.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//34. Find First and Last Position of Element in Sorted Array
//
//Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target value.
//Your algorithm's runtime complexity must be in the order of O(log n).
//If the target is not found in the array, return [-1, -1].
//
//给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。
//你的算法时间复杂度必须是 O(log n) 级别。
//如果数组中不存在目标值，返回 [-1, -1]。
//
//Example 1:
//    Input: nums = [5,7,7,8,8,10], target = 8
//    Output: [3,4]
//
//Example 2:
//    Input: nums = [5,7,7,8,8,10], target = 6
//    Output: [-1,-1]


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
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        return this->solution2(nums, target);
    }
    
private:
    // 方法一：两次二分查找。
    // 时间复杂度 O(lg N)，空间复杂度 O(1)。N = nums.length
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 65.37% 的用户
    // 内存消耗 : 10.4 MB , 在所有 C++ 提交中击败了 76.10% 的用户
    // Runtime: 12 ms, faster than 47.75% of C++ online submissions for Find First and Last Position of Element in Sorted Array.
    // Memory Usage: 10.5 MB, less than 19.99% of C++ online submissions for Find First and Last Position of Element in Sorted Array.
    vector<int> solution1 (vector<int>& nums, int target) {
        // 边界情况
        if (nums.empty()) {
            return {-1, -1};
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            if (nums[0] == target) {
                return {0, 0};
            } else {
                return {-1, -1};
            }
        }
        
        int left_index = MAX_INT32;
        int right_index = MIN_INT32;
        
        // 二分查找，找到最靠左的 target 下标和最靠右的 target 下标
        this->binarySearchLeft(nums, left_index, target, 0, len - 1);
        this->binarySearchRight(nums, right_index, target, 0, len - 1);
        
        if (left_index == MAX_INT32 || right_index == MIN_INT32) {
            return {-1, -1};
        } else {
            return {left_index, right_index};
        }
    }
    
    // 方法二：一次二分查找。
    // 时间复杂度 O(lg N)，空间复杂度 O(1)。N = nums.length
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 65.37% 的用户
    // 内存消耗 : 10.2 MB , 在所有 C++ 提交中击败了 88.70% 的用户
    // Runtime: 4 ms, faster than 99.73% of C++ online submissions for Find First and Last Position of Element in Sorted Array.
    // Memory Usage: 10.5 MB, less than 17.78% of C++ online submissions for Find First and Last Position of Element in Sorted Array.
    vector<int> solution2 (vector<int>& nums, int target) {
        // 边界情况
        if (nums.empty()) {
            return {-1, -1};
        }
        
        int len = (int)nums.size();
        
        if (len == 1) {
            if (nums[0] == target) {
                return {0, 0};
            } else {
                return {-1, -1};
            }
        }
        
        int left_index = MAX_INT32;
        int right_index = MIN_INT32;
        int flag = 0; // -1 表示正在找 left_index，0 表示还在找第一个 target，1 表示正在找 right_index
        
        // 二分查找，找到最靠左的 target 下标和最靠右的 target 下标
        this->binarySearchLeftAndRight(nums, left_index, right_index, target, 0, len - 1, flag);
        
        if (left_index == MAX_INT32 || right_index == MIN_INT32) {
            return {-1, -1};
        } else {
            return {left_index, right_index};
        }
    }
    
    // 普通二分查找
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
    
    // 二分查找，找到最靠左的目标，记录其下标
    void binarySearchLeft (vector<int>& nums, int& left_index, int& target, int start, int end) {
        if (start > end || start < 0 || end >= (int)nums.size()) {
            return;
        }
        
        if (start == end) {
            // 最终情况，如果命中目标，记录较小的下标
            if (nums[start] == target && left_index > start) {
                left_index = start;
            }
            return;
        }
        
        int mid = (start + end) >> 1;
        if (nums[mid] == target) {
            // 命中目标，记录较小的下标
            if (left_index > mid) {
                left_index = mid;
            }
            // 继续往左找，找到最靠左的目标，记录其下标
            this->binarySearchLeft(nums, left_index, target, start, mid - 1);
        } else if (target < nums[mid]) {
            // 往左找
            this->binarySearchLeft(nums, left_index, target, start, mid - 1);
        } else {
            // 往右找
            this->binarySearchLeft(nums, left_index, target, mid + 1, end);
        }
    }
    
    // 二分查找，找到最靠右的目标，记录其下标
    void binarySearchRight (vector<int>& nums, int& right_index, int& target, int start, int end) {
        if (start > end || start < 0 || end >= (int)nums.size()) {
            return;
        }
        
        if (start == end) {
            // 最终情况，如果命中目标，记录较大的下标
            if (nums[start] == target && right_index < start) {
                right_index = start;
            }
            return;
        }
        
        int mid = (start + end) >> 1;
        if (nums[mid] == target) {
            // 命中目标，记录较大的下标
            if (right_index < mid) {
                right_index = mid;
            }
            // 继续往右找，找到最靠右的目标，记录其下标
            this->binarySearchRight(nums, right_index, target, mid + 1, end);
        } else if (target < nums[mid]) {
            // 往左找
            this->binarySearchRight(nums, right_index, target, start, mid - 1);
        } else {
            // 往右找
            this->binarySearchRight(nums, right_index, target, mid + 1, end);
        }
    }
    
    // 二分查找。找到最靠左的目标，记录其下标；找到最靠右的目标，记录其下标。
    void binarySearchLeftAndRight (vector<int>& nums, int& left_index, int& right_index,
                                   int& target, int start, int end, int flag) {
        if (start > end || start < 0 || end >= (int)nums.size()) {
            return;
        }
        
        if (start == end) {
            // 最终情况，如果命中目标
            if (nums[start] == target) {
                // 考虑是否更新左边界
                if (left_index > start) {
                    left_index = start;
                }
                // 考虑是否更新右边界
                if (right_index < start) {
                    right_index = start;
                }
            }
            return;
        }
        
        int mid = (start + end) >> 1;
        if (nums[mid] == target) {
            if (flag == 0) {
                // 命中目标，记录下标
                if (left_index > mid) {
                    left_index = mid;
                }
                if (right_index < mid) {
                    right_index = mid;
                }
                // 开始往左找，找到最靠左的目标，记录其下标。flag 置为 -1，表示开始找左边界
                this->binarySearchLeftAndRight(nums, left_index, right_index, target, start, mid - 1, -1);
                // 开始往右找，找到最靠右的目标，记录其下标。flag 置为 1，表示开始找右边界
                this->binarySearchLeftAndRight(nums, left_index, right_index, target, mid + 1, end, 1);
            } else if (flag < 0) {
                if (left_index > mid) {
                    left_index = mid;
                }
                // 继续往左找
                this->binarySearchLeftAndRight(nums, left_index, right_index, target, start, mid - 1, -1);
            } else {
                if (right_index < mid) {
                    right_index = mid;
                }
                // 继续往右找
                this->binarySearchLeftAndRight(nums, left_index, right_index, target, mid + 1, end, 1);
            }
        } else if (target < nums[mid]) {
            // 往左找。flag 仍然为 0，表示找第一次出现的 target
            this->binarySearchLeftAndRight(nums, left_index, right_index, target, start, mid - 1, 0);
        } else {
            // 往右找。flag 仍然为 0，表示找第一次出现的 target
            this->binarySearchLeftAndRight(nums, left_index, right_index, target, mid + 1, end, 0);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 [3, 4]
    vector<int> nums = {5, 7, 7, 8, 8, 10};
    int target = 8;
    
    // 预期结果 [-1, -1]
//    vector<int> nums = {5, 7, 7, 8, 8, 10};
//    int target = 6;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans =solution->searchRange(nums, target);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            cout << ans[i] << ", ";
        }
        cout << "End." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
