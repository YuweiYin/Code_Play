//
//  main.cpp
//  Prob1080_Remove_Duplicates_from_Sorted_Array_II
//
//  Created by 阴昱为 on 2019/8/1.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//80. Remove Duplicates from Sorted Array II
//
//Given a sorted array nums, remove the duplicates in-place such that duplicates appeared at most twice and return the new length.
//Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory.
//
//给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素最多出现两次，返回移除后数组的新长度。
//不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。
//
//Example 1:
//    Given nums = [1,1,1,2,2,3],
//    Your function should return length = 5, with the first five elements of nums being 1, 1, 2, 2 and 3 respectively.
//    It doesn't matter what you leave beyond the returned length.
//
//Example 2:
//    Given nums = [0,0,1,1,1,1,2,3,3],
//    Your function should return length = 7, with the first seven elements of nums being modified to 0, 0, 1, 1, 2, 3 and 3 respectively.
//    It doesn't matter what values are set beyond the returned length.
//
//Clarification:
//    Confused why the returned value is an integer but your answer is an array?
//    Note that the input array is passed in by reference, which means modification to the input array will be known to the caller as well.

//Internally you can think of this:
//    // nums is passed in by reference. (i.e., without making a copy)
//    int len = removeDuplicates(nums);
//
//    // any modification to nums in your function would be known by the caller.
//    // using the length returned by your function, it prints the first len elements.
//    for (int i = 0; i < len; i++) {
//        print(nums[i]);
//    }
//
//说明:
//    为什么返回数值是整数，但输出的答案是数组呢?
//    请注意，输入数组是以“引用”方式传递的，这意味着在函数里修改输入数组对于调用者是可见的。
//
//你可以想象内部操作如下:
//    // nums 是以“引用”方式传递的。也就是说，不对实参做任何拷贝
//    int len = removeDuplicates(nums);
//
//    // 在函数里修改输入数组对于调用者是可见的。
//    // 根据你的函数返回的长度, 它会打印出数组中该长度范围内的所有元素。
//    for (int i = 0; i < len; i++) {
//            print(nums[i]);
//    }


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
    int removeDuplicates(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：快慢双指针。时间复杂度 O(N)，空间复杂度 O(1)。 N = nums.size
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 93.49% 的用户
    // 内存消耗 : 8.8 MB , 在所有 C++ 提交中击败了 73.60% 的用户
    // Runtime: 12 ms, faster than 85.42% of C++ online submissions for Remove Duplicates from Sorted Array II.
    // Memory Usage: 8.7 MB, less than 84.88% of C++ online submissions for Remove Duplicates from Sorted Array II.
    int solution1(vector<int>& nums) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int n_len = (int)nums.size();
        
        if (n_len <= 2) {
            return n_len;
        }
        
        int slow_index = 1; // 慢指针
        bool duplicate = false; // true 表示已出现一次重复
        
        for (int i = 1; i < n_len; i++) { // i 是快指针
            // 如果不重复，则表示有新的值，写入慢指针位置
            if (nums[i] != nums[i - 1]) {
                nums[slow_index++] = nums[i];
                duplicate = false;
            } else {
                if (!duplicate) {
                    // 如果值尚未重复出现，继续往后找
                    nums[slow_index++] = nums[i];
                    duplicate = true;
                } else {
                    // 如果值已经重复过了，则继续往后找
                    continue;
                }
            }
        }
        
        return slow_index;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {0, 0, 1, 1, 1, 1, 2, 3, 3}; // 预期结果 7
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->removeDuplicates(nums);
    cout << "Answer is " << ans << endl;
    
    for (int i = 0; i < ans; i++) {
        cout << nums[i] << ", ";
    }
    cout << "End." <<endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
