//
//  main.cpp
//  Prob1004_Median_of_Two_Sorted_Arrays
//
//  Created by 阴昱为 on 2019/5/29.
//  Copyright © 2019 阴昱为. All rights reserved.
//


//4. Median of Two Sorted Arrays
//
//There are two sorted arrays nums1 and nums2 of size m and n respectively.
//Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
//You may assume nums1 and nums2 cannot be both empty.
//
//给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。
//请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
//你可以假设 nums1 和 nums2 不会同时为空。
//
//Example1:
//  nums1 = [1, 3]
//  nums2 = [2]
//  The median is 2.0
//
//Example2:
//  nums1 = [1, 2]
//  nums2 = [3, 4]
//  The median is (2 + 3)/2 = 2.5


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


class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if (nums1.size() <= 0 && nums2.size() <= 0) {
            return 0;
        }
        
        // 笨蛋方法1：时间复杂度 O(m+n)，用O(m+n)的时间合并两个有序数组，然后O(1)随机查找
        // 笨蛋方法2：时间复杂度 O(m+n)，用O((m+n)/2)的时间有序遍历两个有序数组，遍历到一半就得到结果
        // 方法3：二分查找，时间复杂度O(log(m+n))
        double ans = 0.0;
        long size_sum = nums1.size() + nums2.size();
        long mid = floor(size_sum / 2);
        vector<int>::iterator ite1 = nums1.begin();
        vector<int>::iterator ite2 = nums2.begin();
        vector<int> nums;
        
        // 遍历，合并两个排序数组
        while (ite1 != nums1.end() || ite2 != nums2.end()) {
            if (ite1 == nums1.end()) {
                nums.push_back(*ite2);
                ite2 ++;
            } else if (ite2 == nums2.end()) {
                nums.push_back(*ite1);
                ite1 ++;
            } else {
                if (*ite1 < *ite2) {
                    nums.push_back(*ite1);
                    ite1 ++;
                } else {
                    nums.push_back(*ite2);
                    ite2 ++;
                }
            }
        }
        
        // 根据总元素个数的奇偶性，分别处理
        if (nums.size() > 0) {
            if (size_sum % 2 == 0) {
                if (mid >= 1) {
                    ans = double(nums[mid - 1] + nums[mid]) / 2;
                }
            } else {
                ans = double(nums[mid]);
            }
        }
        
        return ans;
    }
};


int main(int argc, const char * argv[]) {
    // 设置测试数据
    vector<int> nums1 = {1, 3};
    vector<int> nums2 = {2, 4};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->findMedianSortedArrays(nums1, nums2) << endl;
    
    return 0;
}
