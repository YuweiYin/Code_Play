//
//  main.cpp
//  Binary_Indexed_Tree
//
//  Created by 阴昱为 on 2019/7/17.
//  Copyright © 2019 阴昱为. All rights reserved.
//

// Binary Indexed Tree（Fenwick Tree，树状数组）
//
// 典型问题：求一个数组中连续 N 项的和。
// 如果用一个循环，把这连续的 N 项加起来，时间复杂度为 O(N)。但用 BIT 则 O(lg N)
//
// BIT 是一个查询和修改复杂度都为 O(lg N) 的数据结构。
// 主要用于查询任意两位之间的所有元素之和，但是每次只能修改一个元素的值。
//
// 核心思想：
//    树状数组中的每个元素是原数组中一个或者多个连续元素的和。
//    在进行连续求和操作a[1]+…+a[n]时，只需要将树状数组中某几个元素的和即可。时间复杂度为O(lgn)
//
// a[]: 保存原始数据的数组
// e[]: 树状数组，其中的任意一个元素 e[i] 可能是一个或者多个 a 数组中元素的和。
//    如：e[2]=a[1]+a[2], e[3]=a[3], e[4]=a[1]+a[2]+a[3]+a[4]
// e[i]中的元素：如果数字 i 的二进制表示中末尾有 k 个连续的 0，
// 则 e[i] 是 a 数组中 2^k 个元素的和，则 e[i] = a[i-2^k+1] + a[i-2^k+2] + .. + a[i-1] + a[i]
// 也就是说，e[i] 中每一个元素管理着 a[] 中若干个元素的和，并且各个元素管理的区间没有重叠。
//
// 计算 2^k 的两个方法(利用机器补码特性): 2^k = (i & (-i)); 或者 2^k = (i & (i^(i-1));
// 比如 1010 和 110 的计算结果均为 10。而 1100 和 100 的计算结果均为 100。
// 示例简图：
//                  _____________8
//          _____4-/      /    / |
//       2-/  /  |      _6    /  |
// e: 1-/|   3   |   5-/ |   7   |    9
// a: 1  2   3   4   5   6   7   8    9
//    1  10  11 100 101 110 111 1000 1001
// 父结点：
//    离自己最近的、二进制编号末尾连续 0 比自己少的结点，如：e[1] 是 e[2] 的父亲，e[2] 是 e[4] 的父亲
//    e[4] = e[2]+e[3]+a[4] = a[1]+a[2]+a[3]+a[4] ，e[2]、e[3] 是 e[4] 的父亲。
//    计算方法：
//        lowbit(i) = ((i - 1) ^ i) & i ; // 或者 (i & (-i))b
//        结点 e[i] 的父节点为 e[i - lowbit(i)]
// 子结点：
//    离自己最近的、编号比自己小、且二进制编号末尾连续 0 比自己多的结点。如：e[6] 是 e[7] 的孩子，e[4] 是 e[6] 的孩子
//    计算方法：
//        lowbit(i) = ((i - 1) ^ i) & i ; // 或者 (i & (-i))
//        结点 e[i] 的子节点为 e[i + lowbit(i)]

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
#define ll long long

// 全局常量
//#define PI acos(-1.0)
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007; // 1e9+7 与 1e9+9 为孪生素数

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class BinaryIndexedTree {
private:
    vector<int> tree; // Binary Indexed Tree
    vector<int> nums; // 存放原始数据的数组
    
public:
    // 构造函数
    public BinaryIndexedTree (vector<int> nums) {
        this->nums = nums;
        
        int sum = 0;
        int lowbit;
        
        this->tree = vector<int>(nums.size() + 1);
        
        for (int i = 1; i < tree.size(); i++) {
            sum = 0;
            lowbit = i & ((i - 1) ^ i);
            
            for (int j = i; j > i - lowbit; j--) {
                sum += nums[j - 1];
            }
            
            tree[i] = sum;
        }
    }
    
    // 求数组下标 i 到 j 的范围和，即 nums[i]+..+nums[j]
    int rangeSum (int i, int j) {
        return this->prefixSum(j) - this->prefixSum(i - 1);
    }
    
    // 求数组下标 1 到 i 的范围和
    int prefixSum (int i) {
        int sum = 0;
        
        i ++;
        while (i > 0) {
            sum += tree[i];
            i -= i & ((i - 1) ^ i);
        }
        return sum;
    }
    
private:
    // 更新修改数组的值
    void update (int i, int val) {
        int diff = val - this->nums[i];
        this->nums[i] = val;
        
        i ++;
        while (i < this->tree.size()) {
            tree[i] += diff;
            i += i & ((i - 1) ^ i)
        }
    }
};


// 问题：LeetCode 315 计算右侧小于当前元素的个数
// 给定一个整数数组 nums，按要求返回一个新数组 counts。数组 counts 有该性质：
// counts[i] 的值是  nums[i] 右侧小于 nums[i] 的元素的数量。
class Solution {
public:
    vector<int> countSmaller(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    vector<int> solution1 (vector<int>& nums) {
        BinaryIndexedTree *bit = new BinaryIndexedTree(nums);
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {5, 2, 6, 1}; // 预期结果 [2,1,1,0]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->countSmaller(nums);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (size_t i = 0; i < ans.size(); i++) {
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
