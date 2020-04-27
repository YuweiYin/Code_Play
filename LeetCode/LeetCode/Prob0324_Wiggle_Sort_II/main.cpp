//
//  main.cpp
//  Prob1324_Wiggle_Sort_II
//
//  Created by 阴昱为 on 2019/6/17.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1324. Wiggle Sort II
//
//Given an unsorted array nums, reorder it such that nums[0] < nums[1] > nums[2] < nums[3]....
//
//Here, we will use the integers 0, 1, and 2 to represent the color red, white, and blue respectively.
//
//Note: You are not suppose to use the library's sort function for this problem.
//
//给定一个无序的数组 nums，将它重新排列成 nums[0] < nums[1] > nums[2] < nums[3]... 的顺序。
//
//Example 1:
//    Input: nums = [1, 5, 1, 1, 6, 4]
//    Output: One possible answer is [1, 4, 1, 5, 1, 6].
//
//Example 2:
//    Input: nums = [1, 3, 2, 2, 3, 1]
//    Output: One possible answer is [2, 3, 1, 3, 1, 2].
//
//Note:
//    You may assume all input has valid answer.
//说明:
//    你可以假设所有输入都会得到有效的结果。
//
//Follow Up:
//    Can you do it in O(n) time and/or in-place with O(1) extra space?
//进阶:
//    你能用 O(n) 时间复杂度和 / 或原地 O(1) 额外空间来实现吗？


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
    void wiggleSort(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一。排序后，分两半，交替取值。时间复杂度 O(N)，空间复杂度 O(N)
    // 由于本方法的基础操作更简单，所以本方法较快。
    void solution1(vector<int>& nums) {
        if (nums.empty() || (int)nums.size() == 1) {
            return;
        }
        
        int len = (int)nums.size();
        int half = (int)(len / 2);
        
        vector<int> res = {};
        
        // 降序排序
        sort(nums.begin(), nums.end(), this->myComp);
        
        bool choice = true; // choice 为真时，把较小数加入 res，否则加入较大数
        int i = 0, j = half;
        
        while (i < half && j < len) {
            if (choice) {
                choice = !choice;
                res.push_back(nums[j++]);
            } else {
                choice = !choice;
                res.push_back(nums[i++]);
            }
        }
        
        // 处理剩余情况
        if (choice) {
            if (j < len) {
                res.push_back(nums[j++]);
            }
        } else {
            if (i < half) {
                res.push_back(nums[i++]);
            }
        }
        
        // 修改 nums 向量
        nums = res;
    }
    
    void swap (int& a, int& b) {
        int temp = a;
        a = b;
        b = temp;
    }
    
    // 方法二。排序后插入。时间复杂度 O(N/2)，空间复杂度 O(N/2)
    // 由于本方法的基础操作更繁杂，所以本方法较慢。在超时 TLE 边缘试探
    // 例1：[1, 2, 3, 4, 5, 6] -> [4, 1, 2, 3, 5, 6]
    // -> [4, 1, 5, 2, 3, 6] -> [4, 1, 5, 2, 6, 3]
    // 例2：[1, 2, 3, 4, 5, 6, 7] -> [4, 1, 2, 3, 5, 6, 7]
    //  -> [4, 1, 5, 2, 3, 6, 7] -> [4, 1, 5, 2, 6, 3, 7]
    void solution2(vector<int>& nums) {
        if (nums.empty() || (int)nums.size() == 1) {
            return;
        }
        
        int len = (int)nums.size();
        int half = (int)(len >> 1);
        
        // 降序排列
        sort(nums.begin(), nums.end(), this->myComp);
        
        // 将后一半的较小数插入到较大数前
        // 注意：不能是升序排列后，将后一半的较大数插入到较小数后
        // 因为在前一半和后一半中有连续重复值的情况下，会出现问题
        int insert_index = 0; // 插入位置 2k+1 (k=0,1,2,3...)
        int insert_count = 0;
        
        int i;
        if (len % 2 == 0) {
            i = half;
        } else {
            // 奇数个时，取较多的一半
            i = half;
        }
        for (; i < len + insert_count && insert_index < len && insert_count < i; i += 2) {
            // cout << "insert: nums[" << i << "]=" << nums[i] << ",nums[" << insert_index << "]=" << nums[insert_index] << endl;
            nums.insert(nums.begin() + insert_index, nums[i]);
            
            insert_index += 2;
            insert_count ++;
        }
        
        nums = vector<int>(nums.begin(), nums.begin() + len);
    }
    
    static bool myComp (int& a, int& b) {
        return a > b;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {1, 5, 1, 1, 6, 4}; // 预期结果 [1, 6, 1, 5, 1, 4]
//    vector<int> nums = {1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2}; // 预期结果 [1,2,1,2,1,2,1,2,1,2,1,2]
//    vector<int> nums = {1, 3, 2, 2, 3, 1}; // 预期结果 [2, 3, 1, 3, 1, 2]
//    vector<int> nums = {1, 1, 2, 1, 2, 2, 1}; // 预期结果 [1, 2, 1, 2, 1, 2, 1]
//    vector<int> nums = {4, 5, 5, 6}; // 预期结果 [5, 6, 4, 5]
//    vector<int> nums = {4, 5, 5, 5, 5, 6, 6, 6}; // 预期结果 [5, 6, 5, 6, 5, 6, 4, 5]
//    vector<int> nums = {5, 3, 1, 2, 6, 7, 8, 5, 5}; // 预期结果 [5, 8, 5, 7, 3, 6, 2, 5, 1]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->wiggleSort(nums);
    if (!nums.empty()) {
        for (int i = 0; i < (int)nums.size(); i++) {
            cout << nums[i] << ", ";
        }
        cout << "End." << endl;
    } else {
        cout << "Vector Nums is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
