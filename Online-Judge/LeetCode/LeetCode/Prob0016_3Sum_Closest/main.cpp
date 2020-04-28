//
//  main.cpp
//  Prob1016_3Sum_Closest
//
//  Created by 阴昱为 on 2019/6/11.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//16. 3Sum Closest
//
//Given an array nums of n integers and an integer target, find three integers in nums such that the sum is closest to target. Return the sum of the three integers. You may assume that each input would have exactly one solution.
//
//给定一个包括 n 个整数的数组 nums 和一个目标值 target。找出 nums 中的三个整数，
//使得它们的和与 target 最接近。返回这三个数的和。假定每组输入只存在唯一答案。
//
//Example:
//    Given array nums = [-1, 2, 1, -4], and target = 1.
//    The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).


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
    int threeSumClosest(vector<int>& nums, int target) {
        return this->solution1(nums, target);
    }
    
private:
    // 方法一：转化为 2Sum 问题后，夹逼求和
    int solution1 (vector<int>& nums, int target) {
        if (nums.empty() || (int)nums.size() < 3) {
            return -1;
        }
        
        int closest_sum = nums[0] + nums[1] + nums[2];
        
        // 原数组仅有三个元素，直接输出三数之和
        if ((int)nums.size() == 3) {
            return closest_sum;
        }
        
        // 元素排序
        sort(nums.begin(), nums.end());
        
        int nums_len = (int) nums.size();
        for (int i = 0; i < nums_len; i++) {
            // 固定一个值，当前目标就是找两个数等于 0 减这个值，转化为 2Sum 问题
            int cur_target = target - nums[i];
            
            // 双指针夹逼法
            int left = i + 1; // left 从比 nums[i] 大一点的数开始向右逼近
            int right = nums_len - 1; // right 从最大的数开始向左逼近
            
            while (left < right) {
                // 计算当前三数之和与目标之差，以及当前最优与目标之差
                int cur_gap = abs(nums[left] + nums[right] - cur_target);
                int closest_gap = abs(closest_sum - target);
                
                if (cur_gap == 0 || closest_gap == 0) {
                    // 达到最好情况，直接输出
                    return target;
                } else if (cur_gap < closest_gap) {
                    // 此时加起来更接近于得到目标值，存储下来
                    closest_sum = nums[left] + nums[right] + nums[i];
                    
                    if (nums[left] + nums[right] < cur_target) {
                        // 若有重复值，left 右移
                        while(left < right && nums[left] == nums[left + 1]) {
                            left ++;
                        }
                        // 不足，则增大较小数，即 left 右移
                        left ++;
                    } else if (nums[left] + nums[right] > cur_target) {
                        // 若有重复值，right 左移
                        while(left < right && nums[right] == nums[right - 1]) {
                            right --;
                        }
                        // 有余，则减小较大数，即 right 左移
                        right --;
                    } else {
                        // 此时等同于 cur_gap == 0，达到最好情况
                        return target;
                    }
                } else if (nums[left] + nums[right] < cur_target) {
                    // 不足，则增大较小数，即 left 右移
                    left ++;
                } else if (nums[left] + nums[right] > cur_target) {
                    // 有余，则减小较大数，即 right 左移
                    right --;
                } else {
                    // 异常
                    break;
                }
            } // end while
        } // end for
        
        return closest_sum;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {-1, 2, 1, -4}; // 预期结果 2
//    int target = 1;
//    vector<int> nums = {1, 1, 1, 1}; // 预期结果 3
//    int target = 3;
    vector<int> nums = {1, 2, 4, 8, 16, 32, 64, 128}; // 预期结果 82
    int target = 82;
    
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->threeSumClosest(nums, target) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
