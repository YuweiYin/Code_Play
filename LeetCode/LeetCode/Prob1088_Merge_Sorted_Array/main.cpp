//
//  main.cpp
//  Prob1088_Merge_Sorted_Array
//
//  Created by 阴昱为 on 2019/6/15.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1088. Merge Sorted Array
//
//Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.
//Note:
//    The number of elements initialized in nums1 and nums2 are m and n respectively.
//    You may assume that nums1 has enough space (size that is greater or equal to m + n) to hold additional elements from nums2.
//
//给定两个有序整数数组 nums1 和 nums2，将 nums2 合并到 nums1 中，使得 num1 成为一个有序数组。
//说明:
//    初始化 nums1 和 nums2 的元素数量分别为 m 和 n。
//    你可以假设 nums1 有足够的空间（空间大小大于或等于 m + n）来保存 nums2 中的元素。
//
//Example:
//    Input:
//        nums1 = [1,2,3,0,0,0], m = 3
//        nums2 = [2,5,6],       n = 3
//
//    Output: [1,2,2,3,5,6]


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


// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};


class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        // 边界情况处理
        if (nums1.empty() || m == 0) {
            nums1 = nums2;
            return;
        }
        
        if (nums2.empty() || n == 0) {
            return;
        }
        
        // 调用核心解决方案
        this->solution2(nums1, m, nums2, n);
    }
    
private:
    // 方法一。暴力法。时间复杂度 O(m+n)，空间复杂度 O(m+n)
    void solution1(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        vector<int> res = {};
        
        // 遍历一遍 nums1 和 nums2，存储值到 res 向量
        for (int i = 0; i < m; i++) {
            res.push_back(nums1[i]);
        }
        
        for (int i = 0; i < n; i++) {
            res.push_back(nums2[i]);
        }
        
        // 向量排序
        sort(res.begin(), res.end());
        
        // 修改 nums1 向量
        nums1 = res;
        return;
    }
    
    // 方法二。常规方法。时间复杂度 O(m+n)，空间复杂度 O(m+n) 或 O(1)
    void solution2(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int i = 0, j = 0;
        vector<int> res = {};
        
        // 在两数组不全为空的情况下，选择首部的较小元素
        while (i < m && j < n) {
            if (nums1[i] <= nums2[j]) {
                res.push_back(nums1[i++]);
            } else {
                res.push_back(nums2[j++]);
            }
        }
        
        // 处理剩余部分
        while (i < m) {
            res.push_back(nums1[i++]);
        }
        
        while (j < n) {
            res.push_back(nums2[j++]);
        }
        
        // 修改 nums1 向量
        nums1 = res;
        return;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> nums1 = {1, 2, 3, 0, 0, 0};
    int m = 3;
    vector<int> nums2 = {2, 5, 6};
    int n = 3;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->merge(nums1, m, nums2, n);
    for (int i = 0; i < (int)nums1.size(); i++) {
        cout << nums1[i] << ", ";
    }
    cout << "End." << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
