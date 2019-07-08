//
//  main.cpp
//  Prob1628_Maximum_Product_of_Three_Numbers
//
//  Created by 阴昱为 on 2019/7/8.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//628. Maximum Product of Three Numbers
//
//Given an integer array, find three numbers whose product is maximum and output the maximum product.
//
//给定一个整型数组，在数组中找出由三个数组成的最大乘积，并输出这个乘积。
//
//Example 1:
//    Input: [1,2,3]
//    Output: 6
//
//Example 2:
//    Input: [1,2,3,4]
//    Output: 24
//
//Note:
//    The length of the given array will be in range [3,10^4] and all elements are in the range [-1000, 1000].
//    Multiplication of any three numbers in the input won't exceed the range of 32-bit signed integer.
//
//注意:
//    给定的整型数组长度范围是[3,10^4]，数组中所有的元素范围是[-1000, 1000]。
//    输入的数组中任意三个数的乘积不会超出32位有符号整数的范围。


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
    int maximumProduct(vector<int>& nums) {
        return this->solution2(nums);
    }
    
private:
    // 方法一：排序。时间复杂度 O(N lgN)，空间复杂度 O(1), N = nums.size()
    // 执行用时 : 108 ms , 在所有 C++ 提交中击败了 26.63% 的用户
    // 内存消耗 : 10.7 MB , 在所有 C++ 提交中击败了 91.15% 的用户
    // Runtime: 64 ms, faster than 58.61% of C++ online submissions for Maximum Product of Three Numbers.
    // Memory Usage: 10.9 MB, less than 33.97% of C++ online submissions for Maximum Product of Three Numbers.
    int solution1 (vector<int>& nums) {
        // 边界条件
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len < 3) {
            return 0;
        }
        
        if (len == 3) {
            return nums[0] * nums[1] * nums[2];
        }
        
        // 排序
        sort(nums.begin(), nums.end());
        
        // 如果最小值不为负，直接取最大的前三个数的乘积
        if (nums[0] >= 0) {
            return nums[len - 3] * nums[len - 2] * nums[len - 1];
        }
        
        // 如果最小值为负，可能结果是 负*负*正 or 正*正*正
        int product_1 = nums[len - 3] * nums[len - 2] * nums[len - 1];
        int product_2 = nums[0] * nums[1] * nums[len - 1];
        
        return product_1 > product_2 ? product_1 : product_2;
    }
    
    // 方法二：一遍扫描找最大的三个数，和最小的两个数。时间复杂度 O(N)，空间复杂度 O(1), N = nums.size()
    // 执行用时 : 56 ms , 在所有 C++ 提交中击败了 90.42% 的用户
    // 内存消耗 : 10.9 MB , 在所有 C++ 提交中击败了 78.13% 的用户
    // Runtime: 60 ms, faster than 63.36% of C++ online submissions for Maximum Product of Three Numbers.
    // Memory Usage: 11.1 MB, less than 5.15% of C++ online submissions for Maximum Product of Three Numbers.
    int solution2 (vector<int>& nums) {
        // 边界条件
        if (nums.empty()) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        if (len < 3) {
            return 0;
        }
        
        if (len == 3) {
            return nums[0] * nums[1] * nums[2];
        }
        
        // 找顺序统计量，五个数分别为：最大值、第二大值、第三大值、最小值、第二小值
        int max_1, max_2, max_3, min_1, min_2;
        max_1 = this->selectOrderStatistic(nums, len, 0, len - 1);
        max_2 = this->selectOrderStatistic(nums, len - 1, 0, len - 1);
        max_3 = this->selectOrderStatistic(nums, len - 2, 0, len - 1);
        min_1 = this->selectOrderStatistic(nums, 1, 0, len - 1);
        min_2 = this->selectOrderStatistic(nums, 2, 0, len - 1);
        
        // 如果最小值不为负，直接取最大的前三个数的乘积
        if (min_1 >= 0) {
            return max_1 * max_2 * max_3;
        }
        
        // 如果最小值为负，可能结果是 负*负*正 or 正*正*正
        int product_1 = max_1 * max_2 * max_3;
        int product_2 = min_1 * min_2 * max_1;
        
        return product_1 > product_2 ? product_1 : product_2;
    }
    
    void exchange (vector<int>& nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    // 快排随机划分，返回最终的主元位置
    int randomizedPartition (vector<int>& nums, int l, int r) {
        // 随机交换某个下标为 l..r 的数到末尾 r 处
        this->exchange(nums, rand()%(r - l) + l, r);
        
        // 随机交换某个下标为 l..r 的数到末尾 r 处
        this->exchange(nums, rand()%(r - l) + l, r);
        
        // 快排的划分，主元 pivot 为 nums[r]
        int i = l - 1;
        for (int j = l; j < r; j++) {
            if (nums[j] <= nums[r]) {
                this->exchange(nums, ++i, j);
            }
        }
        
        // 把主元放在划分点位置
        i++;
        this->exchange(nums, i, r);
        
        return i;
    }
    
    // 在 nums 向量的坐标 l..r 间，查找第 k 小的数（第 k 个顺序统计量）
    int selectOrderStatistic(vector<int>& nums, int k, int l, int r) {
        if (l == r) {
            return nums[l];
        }
        
        int q = this->randomizedPartition(nums, l, r);
        int less = q - l + 1; // A[l..q] 中的元素个数，也就是比 num[q] 更小的元素个数
        
        if (k == less) {
            // 命中，num[q] 即为第 k 顺序统计量（数组中第 k 小的数）
            return nums[q];
        } else if (k < less) {
            // k 比 less 更小，需要在左子数组中继续递归查找第 k 小的数
            return selectOrderStatistic(nums, k, l, q - 1);
        } else {
            // k 比 less 更大，需要在右子数组中继续递归查找第 k - less 小的数
            return selectOrderStatistic(nums, k - less, q + 1, r);
        }
        
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<int> nums = {1, 2, 3}; // 预期结果 6
//    vector<int> nums = {1, 2, 5, 4, 2}; // 预期结果 40
    vector<int> nums = {1, 2, 5, -2, -7, 4, 2}; // 预期结果 70
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->maximumProduct(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
