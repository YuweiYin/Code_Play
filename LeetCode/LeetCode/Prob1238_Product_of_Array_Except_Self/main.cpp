//
//  main.cpp
//  Prob1238_Product_of_Array_Except_Self
//
//  Created by 阴昱为 on 2019/7/8.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//238. Product of Array Except Self
//
//Given an array nums of n integers where n > 1,  return an array output such that output[i] is equal to the product of all the elements of nums except nums[i].
//
//给定长度为 n 的整数数组 nums，其中 n > 1，返回输出数组 output ，其中 output[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积。
//
//Example:
//    Input:  [1,2,3,4]
//    Output: [24,12,8,6]
//
//Note: Please solve it without division and in O(n).
//Follow up:
//    Could you solve it with constant space complexity? (The output array does not count as extra space for the purpose of space complexity analysis.)
//
//说明: 请不要使用除法，且在 O(n) 时间复杂度内完成此题。
//进阶：
//    你可以在常数空间复杂度内完成这个题目吗？（ 出于对空间复杂度分析的目的，输出数组不被视为额外空间。）


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
    vector<int> productExceptSelf(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：交错双指针。时间复杂度 O(N)，空间复杂度 O(1), N = nums.size()
    // 执行用时 : 56 ms , 在所有 C++ 提交中击败了 93.00% 的用户
    // 内存消耗 : 12.3 MB , 在所有 C++ 提交中击败了 91.12% 的用户
    // Runtime: 44 ms, faster than 52.97% of C++ online submissions for Product of Array Except Self.
    // Memory Usage: 12.5 MB, less than 70.90% of C++ online submissions for Product of Array Except Self.
    vector<int> solution1 (vector<int>& nums) {
        // 边界条件
        int len = (int)nums.size();
        
        if (len <= 1) {
            return nums;
        }
        
        vector<int> res(len, 1); // 结果数组，初始值均为 1
        
        int left = 0; // 左指针/游标
        int right = len - 1; // 左指针/游标
        int left_mul = 1; // 从最左出发，累乘 nums[0..len-1]
        int right_mul = 1; // 从最右出发，累乘 nums[len-1..0]
        
        // 思路：每个数被左边和右边的累乘积各自乘一遍
        // res 的每个数被乘两次。以坐标 i 举例，当 left = i 和 right = i 时分别乘一次
        // 第一次 res[i] 乘法，即 left = i 时，left_mul = 累乘 nums[0..i-1], (i=0时则累乘1)
        // 第二次 res[i] 乘法，即 right = i 时，right_mul = 累乘 nums[i+1..len-1],
        // 最终 res[i] = 累乘 nums[0..i-1] * 累乘 nums[i+1..len-1] 即为 res[0] 该有的结果
        while (right >= 0) { // 双指针同步进退，所以无需判断 left < len。另外，与 0 判断执行更快
            res[left] *= left_mul;
            res[right] *= right_mul;
            
            left_mul *= nums[left++];
            right_mul *= nums[right--];
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {1, 2, 3, 4}; // 预期结果 [24,12,8,6]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->productExceptSelf(nums);
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
