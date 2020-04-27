//
//  main.cpp
//  Prob1015_3Sum
//
//  Created by 阴昱为 on 2019/6/9.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//15. 3Sum
//
//Given an array nums of n integers, are there elements a, b, c in nums such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.
//Note:
//    The solution set must not contain duplicate triplets.
//
//给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。
//注意：答案中不可以包含重复的三元组。
//
//Example:
//    Given array nums = [-1, 0, 1, 2, -1, -4],
//    A solution set is:
//    [
//      [-1, 0, 1],
//      [-1, -1, 2]
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
    vector<vector<int>> threeSum(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：转化为 2Sum 问题后，夹逼求和
    vector<vector<int>> solution1 (vector<int>& nums) {
        vector<vector<int>> res = {}; // 最终结果
        
        if (nums.empty() || (int)nums.size() < 3) {
            return res;
        }
        
        // 元素排序
        sort(nums.begin(), nums.end());
        
        int nums_len = (int) nums.size();
        for (int i = 0; i < nums_len; i++) {
            // 避免重复操作，平均节省大致一半时间
            if (nums[i] > 0) {
                break;
            }
            
            // 不计算重复值
            if(i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            
            // 固定一个值，当前目标就是找两个数等于 0 减这个值，转化为 2Sum 问题
            int cur_target = 0 - nums[i];
            
            // 双指针夹逼法
            int left = i + 1; // left 从比 nums[i] 大一点的数开始向右逼近
            int right = nums_len - 1; // right 从最大的数开始向左逼近
            
            while (left < right) {
                if (nums[left] + nums[right] == cur_target) {
                    // 此时加起来得到目标值，存储下来
                    res.push_back({nums[i], nums[left], nums[right]});
                    
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
                } else if (nums[left] + nums[right] < cur_target) {
                    // 不足，则增大较小数，即 left 右移
                    left ++;
                } else if (nums[left] + nums[right] > cur_target) {
                    // 有余，则减小较大数，即 right 左移
                    right --;
                }
            }
        }
        
        // 排序，使得小数字的三元组在前（观察夹逼过程，发现此时 res 已经是该排序状态）
        // sort(res.begin(), res.end(), this->myComp);
        
        return res;
    }
    
    // 方法二：转化为 2Sum 问题后，一遍哈希，超时!
    vector<vector<int>> solution2 (vector<int>& nums) {
        vector<vector<int>> res = {}; // 最终结果
        map<vector<int>, bool> memo = {}; // 避免重复
        
        if (nums.empty() || (int)nums.size() < 3) {
            return res;
        }
        
        // 元素排序
        sort(nums.begin(), nums.end());
        
        // 优化：从 first_zero_index 开始找，大致可以节省一半的工作量
        // 找到第一个 >= 0 的元素
//        vector<int>::iterator ite = find_if(nums.begin(), nums.end(), [](int n) {return n >= 0;});
//        int first_zero_index = 0;
//        if (ite != nums.end()) {
//            // 找到它的坐标
//            first_zero_index = (int)distance(nums.begin(), ite);
//        } else {
//            // 若不存在 >= 0 的元素，那么 nums 中的数全是负数，不可能挑出 3 个加起来和为 0
//            return res;
//        }
        
        int nums_len = (int) nums.size();
        for (int i = 0; i < nums_len; i++) {
            // 下面这个判断操作，和 i 从 first_zero_index 开始找的效果类似
            if (nums[i] > 0) {
                break;
            }
            
            // 不计算重复值
            if(i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            
            // 固定一个值，当前目标就是找两个数等于 0 减这个值，转化为 2Sum 问题
            int cur_target = 0 - nums[i];
            map<int, int> hashmap;
            
            // j 仍然要兼顾所有元素
            for (int j = 0; j < nums_len; j++) {
                if (j == i) {
                    continue;
                }
                // 计算当前元素值与目标值的差值
                int diff = cur_target - nums[j];
                
                // 如果哈希表中已有该差值对应的元素坐标，则找到一组答案
                if (hashmap.find(diff) != hashmap.end()) {
                    // cout << "-0-> " << i << ", " << hashmap[diff] << ", " << j << endl;
                    // cout << "-1-> " << nums[i] << ", " << nums[hashmap[diff]] << ", " << nums[j] << endl;
                    // cout << endl;
                    
                    vector<int> ans = {nums[i], nums[hashmap[diff]], nums[j]};
                    sort(ans.begin(), ans.end());
                    
                    // 避免重复
                    if (memo.find(ans) == memo.end()) {
                        memo.insert({ans, true});
                        
                        res.push_back(ans);
                    }
                }
                
                // 否则将键值对(当前元素值, 当前元素坐标)存储进哈希表
                hashmap[nums[j]] = j;
            }
        }
        
        // 排序，使得小数字的三元组在前
        sort(res.begin(), res.end(), this->myComp);
        
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
    
    // 预期结果 [[-4,-2,6],[-4,0,4],[-4,1,3],[-4,2,2],[-2,-2,4],[-2,0,2]]
    vector<int> nums = {-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<vector<int>> ans = solution->threeSum(nums);
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
