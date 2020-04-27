//
//  main.cpp
//  Prob1977_Squares_of_a_Sorted_Array
//
//  Created by 阴昱为 on 2019/6/15.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1977. Squares of a Sorted Array
//
//Given an array of integers A sorted in non-decreasing order, return an array of the squares of each number, also in sorted non-decreasing order.
//
//给定一个按非递减顺序排序的整数数组 A，返回每个数字的平方组成的新数组，要求也按非递减顺序排序。
//
//Example 1:
//    Input: [-4,-1,0,3,10]
//    Output: [0,1,9,16,100]
//
//Example 2:
//    Input: [-7,-3,2,3,11]
//    Output: [4,9,9,49,121]
//
//Note:
//    1 <= A.length <= 10000
//    -10000 <= A[i] <= 10000
//    A is sorted in non-decreasing order.



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
    vector<int> sortedSquares(vector<int>& A) {
        // 边界情况
        if (A.empty()) {
            return {};
        }
        
        if ((int)A.size() == 1) {
            return {A[0] * A[0]};
        }
        
        // 调用核心解决方案
        return this->solution2(A);
    }
    
private:
    // 方法一。暴力法。时间复杂度 O(NlogN)，空间复杂度 O(1)
    vector<int> solution1(vector<int>& A) {
        for (int i = 0; i < (int)A.size(); i++) {
            A[i] = A[i] * A[i];
        }
        
        sort(A.begin(), A.end());
        
        return A;
    }
    
    // 方法二。双指针。时间复杂度 O(N)，空间复杂度 O(N)
    // 整体非减序，那么各元素取平方后，原负数部分是非增序，原正数部分仍是非减序
    vector<int> solution2(vector<int>& A) {
        int len = (int)A.size();
        
        // 找到第一个非负的数的下标，right
        int right = 0;
        while (right < len && A[right] < 0) {
            right ++;
        }
        // left 为最后一个负数（绝对值最小的负数）
        int left = right - 1;
        
        vector<int> res = {};
        
        // left 向左，right 向右，两边展开
        while (left >= 0 && right < len) {
            // 把较小值加入结果向量 res 中
            if (A[left] * A[left] < A[right] * A[right]) {
                res.push_back(A[left] * A[left]);
                left --;
            } else {
                res.push_back(A[right] * A[right]);
                right ++;
            }
        }
        
        // 处理剩余元素
        while (left >= 0) {
            res.push_back(A[left] * A[left]);
            left --;
        }
        
        while (right < len) {
            res.push_back(A[right] * A[right]);
            right ++;
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
    vector<int> A = {-4, -1, 0, 3, 10}; // 预期输出 [0, 1, 9, 16, 100]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->sortedSquares(A);
    if (!ans.empty()) {
        for (auto ite = ans.begin(); ite < ans.end(); ite++) {
            cout << *ite << ", ";
        }
        cout << "End." << endl;
    } else {
        cout << "No Answer." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
