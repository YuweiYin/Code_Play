//
//  main.cpp
//  Prob1027_Remove_Element
//
//  Created by 阴昱为 on 2019/6/24.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//27. Remove Element
//
//Given an array nums and a value val, remove all instances of that value in-place and return the new length.
//Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory.
//The order of elements can be changed. It doesn't matter what you leave beyond the new length.
//
//给定一个数组 nums 和一个值 val，你需要原地移除所有数值等于 val 的元素，返回移除后数组的新长度。
//不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。
//元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。
//
//Example 1:
//    Given nums = [3,2,2,3], val = 3,
//    Your function should return length = 2, with the first two elements of nums being 2.
//    It doesn't matter what you leave beyond the returned length.
//
//Example 2:
//    Given nums = [0,1,2,2,3,0,4,2], val = 2,
//    Your function should return length = 5, with the first five elements of nums containing 0, 1, 3, 0, and 4.
//    Note that the order of those five elements can be arbitrary.
//    It doesn't matter what values are set beyond the returned length.
//
//Clarification:
//    Confused why the returned value is an integer but your answer is an array?
//    Note that the input array is passed in by reference, which means modification to the input array will be known to the caller as well.
//    Internally you can think of this:
//
//        // nums is passed in by reference. (i.e., without making a copy)
//        int len = removeElement(nums, val);
//
//        // any modification to nums in your function would be known by the caller.
//        // using the length returned by your function, it prints the first len elements.
//        for (int i = 0; i < len; i++) {
//            print(nums[i]);
//        }
//
//说明:
//    为什么返回数值是整数，但输出的答案是数组呢?
//    请注意，输入数组是以“引用”方式传递的，这意味着在函数里修改输入数组对于调用者是可见的。
//    你可以想象内部操作如下:
//
//        // nums 是以“引用”方式传递的。也就是说，不对实参作任何拷贝
//        int len = removeElement(nums, val);
//
//        // 在函数里修改输入数组对于调用者是可见的。
//        // 根据你的函数返回的长度, 它会打印出数组中该长度范围内的所有元素。
//        for (int i = 0; i < len; i++) {
//                print(nums[i]);
//        }


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
    int removeElement(vector<int>& nums, int val) {
        return this->solution1(nums, val);
    }
private:
    int solution1(vector<int>& nums, int val) {
        // 边界情况
        if (nums.empty()) {
            return 0;
        }
        
        int n_len = (int)nums.size();
        int new_index = 0; // 慢指针
        
        for (int i = 0; i < n_len; i++) { // i 是快指针
            // 如果不等于 val，写入慢指针位置
            if (nums[i] != val) {
                if (new_index < i) {
                    nums[new_index] = nums[i];
                }
                new_index ++;
            }
            // 如果值重复，继续往后找
        }
        
        return new_index;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {0, 1, 2, 2, 3, 0, 4, 2}; // 预期结果 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4
    int val = 2;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->removeElement(nums, val);
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
