//
//  main.cpp
//  Prob1041_First_Missing_Positive
//
//  Created by 阴昱为 on 2019/7/6.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//41. First Missing Positive
//
//Given an unsorted integer array, find the smallest missing positive integer.
//
//给定一个未排序的整数数组，找出其中没有出现的最小的正整数。
//
//Example 1:
//    Input: [1,2,0]
//    Output: 3
//
//Example 2:
//    Input: [3,4,-1,1]
//    Output: 2
//
//Example 3:
//    Input: [7,8,9,11,12]
//    Output: 1
//
//Note:
//    Your algorithm should run in O(n) time and uses constant extra space.
//说明:
//    你的算法的时间复杂度应为O(n)，并且只能使用常数级别的空间。


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
    int firstMissingPositive(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 92.82% 的用户
    // 内存消耗 : 8.5 MB , 在所有 C++ 提交中击败了 91.01% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for First Missing Positive.
    // Memory Usage: 8.7 MB, less than 31.98% of C++ online submissions for First Missing Positive.
    int solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return 1;
        }
        
        // 分析：要求时间复杂度为 O(N)，空间复杂度为 O(1)
        // 所以不能用交换排序，因为这样时间 Omega(N logN)
        // 也不能用计数排序，或者其它表格记录方法，因为这样空间 Omega(N)
        // 注意到负数、零以及大于 N 的数不用考虑。假设 nums.size() == 4
        // 那么只有集合(不考虑顺序)为 {1,2,3,4} 时，结果才会大于 4，结果应为 5
        // 所以考虑利用 nums 原地处理，第一轮扫描把正整数放到该放的位置，
        // i-1 位置存放数值为 i 的数字。第二轮扫描只需看第一次出现的不合法的数字
        int len = (int)nums.size();
        int res = len + 1; // 如果第二轮扫描没有出现不合法的数字，那么结果应为 len + 1
        
        int index = 0;
        while (index < len) {
            if (nums[index] <= 0 || nums[index] > len) {
                nums[index] = -1; // 统一越界数字为 -1
                index ++;
            } else {
                // 数字不越界
                if (nums[index] == index + 1) {
                    index ++; // 数字被放在了该放的位置，则考察下一个位置的数字
                } else {
                    // 若当前数字没有放在该放的位置，则将它交换移动到合理位置，下一轮循环处理被交换过来的数字
                    // 注意判断，如果待交换的二者为相同数字，则无需交换，直接把当前数字设为 -1，以免循环永远交换下去
                    if (nums[index] == nums[nums[index] - 1]) {
                        nums[index] = -1;
                        index ++;
                    } else {
                        this->swapInt(nums[index], nums[nums[index] - 1]);
                    }
                }
            }
        }
        
        // 第二轮扫描，只需找到第一个没放在相应位置的数字，或者越界数字，那么下标 i+1 就是解
        for (int i = 0; i < len; i++) {
            if (nums[i] != i + 1 || nums[i] < 0) {
                res = i + 1;
                break;
            }
        }
        
        return res;
    }
    
    void swapInt (int& a, int& b) {
        int temp = a;
        a = b;
        b = temp;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {1, 2, 0}; // 预期结果 3
//    vector<int> nums = {3, 4, -1, 1}; // 预期结果 2
//    vector<int> nums = {7, 8, 9, 11, 12}; // 预期结果 1
//    vector<int> nums = {1}; // 预期结果 2
    vector<int> nums = {1, 1}; // 预期结果 2
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->firstMissingPositive(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
