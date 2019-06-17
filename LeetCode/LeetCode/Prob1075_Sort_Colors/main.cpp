//
//  main.cpp
//  Prob1075_Sort_Colors
//
//  Created by 阴昱为 on 2019/6/16.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1075. Sort Colors
//
//Given an array with n objects colored red, white or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white and blue.
//
//Here, we will use the integers 0, 1, and 2 to represent the color red, white, and blue respectively.
//
//Note: You are not suppose to use the library's sort function for this problem.
//
//给定一个包含红色、白色和蓝色，一共 n 个元素的数组，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。
//
//此题中，我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。
//
//注意:不能使用代码库中的排序函数来解决这道题。
//
//Example:
//    Input: [2,0,2,1,1,0]
//    Output: [0,0,1,1,2,2]
//
//Follow up:
//    A rather straight forward solution is a two-pass algorithm using counting sort.
//    First, iterate the array counting number of 0's, 1's, and 2's, then overwrite array with total number of 0's, then 1's and followed by 2's.
//    Could you come up with a one-pass algorithm using only constant space?
//
//进阶：
//    一个直观的解决方案是使用计数排序的两趟扫描算法。
//    首先，迭代计算出0、1 和 2 元素的个数，然后按照0、1、2的排序，重写当前数组。
//    你能想出一个仅使用常数空间的一趟扫描算法吗？


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
    void sortColors(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一。三计数器、一遍扫描。时间复杂度 O(N)，空间复杂度 O(1)
    void solution1(vector<int>& nums) {
        if (nums.empty() || (int)nums.size() == 1) {
            return;
        }
        
        int len = (int)nums.size();
        int zero_count = 0; // red
        int one_count = 0; // white
//        int two_count = 0; // blue
        
        for (int i = 0; i < len; i++) {
            int index = 0;
            if (nums[i] == 0) {
                // 如果当前是 0，则将它应该位于 zero_count 位置
                index = zero_count;
                if (i > index) {
                    // 如果 0 不在它该在的位置，那么把该位置的元素替换到后面去
                    this->swap(nums[i], nums[index]);
                    
                    // 如果被 0 替换到后面去的是 1，那么还要考虑 1 不能在 2 之后
                    if (nums[i] == 1) {
                        index = zero_count + one_count;
                        if (i > index) {
                            this->swap(nums[i], nums[index]);
                        }
                    }
                }
                zero_count ++;
            } else if (nums[i] == 1) {
                // 同理，如果当前是 0，则将它应该位于 zero_count + one_count 位置
                index = zero_count + one_count;
                if (i > index) {
                    // 如果 1 不在它该在的位置，那么把该位置的元素替换到后面去
                    this->swap(nums[i], nums[index]);
                }
                one_count ++;
            }
//            else if (nums[i] == 2) {
//                // 本题中 2 是末尾元素，所以不用替换到前面去
//                index = zero_count + one_count + two_count;
//                if (i > index) {
//                    this->swap(nums[i], nums[index]);
//                }
//                two_count ++;
//            } else {
//                continue;
//            }
        }
    }
    
    void swap (int& a, int& b) {
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
    vector<int> nums = {2, 0, 2, 1, 1, 0}; // 预期输出 [0,0,1,1,2,2]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->sortColors(nums);
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
