//
//  main.cpp
//  Prob1031_Next_Permutation
//
//  Created by 阴昱为 on 2019/6/25.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//31. Next Permutation
//
//Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.
//If such arrangement is not possible, it must rearrange it as the lowest possible order (ie, sorted in ascending order).
//The replacement must be in-place and use only constant extra memory.
//
//实现获取下一个排列的函数，算法需要将给定数字序列重新排列成字典序中下一个更大的排列。
//如果不存在下一个更大的排列，则将数字重新排列成最小的排列（即升序排列）。
//必须原地修改，只允许使用额外常数空间。
//
//Here are some examples. Inputs are in the left-hand column and its corresponding outputs are in the right-hand column.
//    1,2,3 → 1,3,2
//    3,2,1 → 1,2,3
//    1,1,5 → 1,5,1


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
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        this->solution1(nums);
    }
    
private:
    // 方法一：。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 92.52% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 78.89% 的用户
    // Runtime: 8 ms, faster than 87.90% of C++ online submissions for Next Permutation.
    // Memory Usage: 8.9 MB, less than 21.85% of C++ online submissions for Next Permutation.
    void solution1 (vector<int>& nums) {
        if (nums.empty() || nums.size() <= 1) {
            return;
        }
        
        int n_len = (int)nums.size();
        
        for (int i = n_len - 1; i >= 1; i--) {
            if (nums[i - 1] < nums[i]) {
                // 如果出现升序，那么 i-1..n_len-1 就要变了
                // 在子数组 i..n_len-1 中从右到左找到第一个比 nums[i - 1] 大的数的下标
                // 该子数组是降序排序，有序，所以采用二分查找，O(lg N)渐进时间内找出那个数
                int index = this->binarySearch(nums, nums[i - 1], i, n_len - 1);
                
                if (index < 0 || index >= n_len) {
                    return; // Error
                }
                
                // 交换二者
                nums[index] = nums[index] ^ nums[i - 1];
                nums[i - 1] = nums[index] ^ nums[i - 1];
                nums[index] = nums[index] ^ nums[i - 1];
                
                // 将 i..n_len-1 按升序排列
                sort(nums.begin() + i, nums.end());
                
                return;
            }
        }
        
        // 如果之前没有出现升序，表示原数组按降序(非升序)排列，已达到最大排列
        sort(nums.begin(), nums.end());
    }
    
    // 在降序数组 start..end 中找到第一个比 key 大的数的下标
    int binarySearch (vector<int> nums, int key, int start, int end) {
        if (end - start <= 1) {
            if (end < (int)nums.size() && nums[end] > key) {
                return end;
            }
            if (start < (int)nums.size() && nums[start] > key) {
                return start;
            }
            return -1; // Error
        }
        
        int mid = (end - start) / 2 + start;
        
        if (key >= nums[mid]) {
            // mid..end 中不存在比 key 大的数，往左找比 key 大的数
            return this->binarySearch(nums, key, start, mid);
        } else {
            // mid..end 中存在比 key 大的数了，往右找最小的区间
            return this->binarySearch(nums, key, mid, end);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {1, 2, 3}; // 预期结果 1, 3, 2
//    vector<int> nums = {3, 2, 1}; // 预期结果 1, 2, 3
//    vector<int> nums = {1, 1, 5}; // 预期结果 1, 5, 1
//    vector<int> nums = {2, 3, 1}; // 预期结果 3, 1, 2
//    vector<int> nums = {1, 3, 2}; // 预期结果 2, 1, 3
    vector<int> nums = {4, 10, 9, 8, 7, 6, 5, 3, 2, 1}; // 预期结果 5, 1, 2, 3, 4, 6, 7, 8, 9, 10
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->nextPermutation(nums);
    for (int i = 0; i < (int)nums.size(); i++) {
        cout << nums[i] << ", ";
    }
    cout << "End." << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
