//
//  main.cpp
//  Prob1018_4Sum
//
//  Created by 阴昱为 on 2019/6/11.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//18. 4Sum
//
//Given an array nums of n integers and an integer target, are there elements a, b, c, and d in nums such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.
//Note:
//    The solution set must not contain duplicate quadruplets.
//
//给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。
//注意：
//    答案中不可以包含重复的四元组。
//
//Example:
//    Given array nums = [1, 0, -1, 0, -2, 2], and target = 0.
//    A solution set is:
//    [
//      [-1,  0, 0, 1],
//      [-2, -1, 1, 2],
//      [-2,  0, 0, 2]
//    ]


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
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        return this->solution1(nums, target);
    }
    
private:
    // 方法一：转化为 2Sum 问题后，夹逼求和
    vector<vector<int>> solution1 (vector<int>& nums, int target) {
        vector<vector<int>> res = {}; // 最终结果
        
        if (nums.empty() || (int)nums.size() < 4) {
            return res;
        }
        
        // 元素排序
        sort(nums.begin(), nums.end());
        
        int nums_len = (int) nums.size();
        for (int i = 0; i < nums_len; i++) {
            // 固定一个值，当前目标就是找三个数之和等于 target 减这个值，转化为 3Sum 问题
            int cur_target_i = target - nums[i];
            
            for (int j = i + 1; j < nums_len; j++) {
                // 再固定一个值，当前目标就是找两个数之和等于 target 减这个值，转化为 2Sum 问题
                int cur_target_j = cur_target_i - nums[j];
                
                // 双指针夹逼法
                int left = j + 1; // left 从比 nums[i] 大一点的数开始向右逼近
                int right = nums_len - 1; // right 从最大的数开始向左逼近
                
                while (left < right) {
                    if (nums[left] + nums[right] == cur_target_j) {
                        // 此时加起来得到目标值，若不重复，则存储下来
                        vector<int> ans = {nums[i], nums[j], nums[left], nums[right]};
                        if (find(res.begin(), res.end(), ans) == res.end()) {
                            res.push_back(ans);
                        }
                        
                        // 若有重复值，left 右移
                        while(left < right && nums[left] == nums[left + 1]) {
                            left ++;
                        }
                        left ++; // 移到下一个值
                        
                        // 若有重复值，right 左移
                        while(left < right && nums[right] == nums[right - 1]) {
                            right --;
                        }
                        right --; // 移到下一个值
                    } else if (nums[left] + nums[right] < cur_target_j) {
                        // 不足，则增大较小数，即 left 右移
                        left ++;
                    } else if (nums[left] + nums[right] > cur_target_j) {
                        // 有余，则减小较大数，即 right 左移
                        right --;
                    }
                } // end while
            } // end for j
        } // end for i
        
        // 排序，使得小数字的三元组在前（观察夹逼过程，发现此时 res 已经是该排序状态）
        // sort(res.begin(), res.end(), this->myComp);
        
        return res;
    }
    
    // 自定义排序函数
    static bool myComp (const vector<int> &a, const vector<int> &b) {
        int size_min = min((int)a.size(), (int)b.size());
        for (int i = 0; i < size_min; i++) {
            // 相等则看下一个元素
            if (a[i] == b[i]) {
                continue;
            }
            // 谁小谁在前
            return a[i] < b[i];
        }
        // 全都相等，则不动排序
        return true;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    //    vector<int> nums = {-1, 0, 1, 2, -1, -4};
    //    vector<int> nums = {-1, 0, 1, 2, -1, -2, -2, -3, 0, 4, -4, 0, 0};
    //    vector<int> nums = {0, 0, 0, 0, -1, 0, 1};
    //    vector<int> nums = {-1, -1, -1, 0, 1, 1, 1, 1, 1, 2};
    
    // 预期结果 [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    // vector<int> nums = {1, 0, -1, 0, -2, 2};
    // 预期结果 [[-3,-2,2,3],[-3,-1,1,3],[-3,0,0,3],[-3,0,1,2],
    // [-3,0,1,2],[-2,-1,0,3],[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
    vector<int> nums = {-3, -2, -1, 0, 0, 1, 2, 3};
    int target = 0;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->fourSum(nums, target);
    for (int i = 0; i < (int)ans.size(); i++) {
        for (int j = 0; j < (int)ans[i].size(); j++) {
            cout << ans[i][j] << ", ";
        }
        cout << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
