//
//  main.cpp
//  Prob1996_Number_of_Squareful_Arrays
//
//  Created by 阴昱为 on 2019/6/27.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//996. Number of Squareful Arrays
//
//Given an array A of non-negative integers, the array is squareful if for every pair of adjacent elements, their sum is a perfect square.
//Return the number of permutations of A that are squareful.  Two permutations A1 and A2 differ if and only if there is some index i such that A1[i] != A2[i].
//
//给定一个非负整数数组 A，如果该数组每对相邻元素之和是一个完全平方数，则称这一数组为正方形数组。
//返回 A 的正方形排列的数目。两个排列 A1 和 A2 不同的充要条件是存在某个索引 i，使得 A1[i] != A2[i]。
//
//Example 1:
//    Input: [1,17,8]
//    Output: 2
//    Explanation:
//    [1,8,17] and [17,8,1] are the valid permutations.
//
//Example 2:
//    Input: [2,2,2]
//    Output: 1
//
//Note:
//    1 <= A.length <= 12
//    0 <= A[i] <= 1e9


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
private:
    // node_count[x] 数组 A 中值为 x 的结点数量
    map<int, int> node_count = {}; // for solution2
    
    // node_edge[x] : 在 A 中满足 x + y 是完全平方数的所有 y。"xy" 可以看作成一条可行边
    map<int, vector<int>> node_edge = {}; // for solution2

public:
    int numSquarefulPerms(vector<int>& A) {
        return this->solution2(A);
    }
    
private:
    // 阶乘 n!
    int factorial (int n) {
        if (n <= 1) {
            return 1;
        }
        
        // 12! = 479 001 600 < MAX_INT32
        // 13! = 6 227 020 800 > MAX_INT32
        if (n > 12) {
            return 0; // Overflow
        }
        
        int res = 1;
        
        for (int i = 2; i <= n; i++) {
            res *= i;
        }
        
        return res;
    }
    
    // 判断一个数是否为完全平方数
    bool checkSquareNumber (int n) {
        int m = (int)sqrt(n);
        if (n == m * m) {
            return true;
        } else {
            return false;
        }
    }
    
    // 方法一：库函数，暴力查找，超时。时间复杂度 O(N!)，空间复杂度 O(1)
    // 49 / 76 个通过测试用例，第 50 个测试用例 [89,72,71,44,50,72,26,79,33,27,84] 超时
    // 第 50 个测试用例的程序执行时间: 2599.66ms.
    int solution1 (vector<int>& A) {
        // 边界情况
        if (A.empty()) {
            return 0;
        }
        
        int A_len = (int)A.size();
        
        // A_len > 12 ，阶乘溢出 MAX_INT32
        if (A_len > 12) {
            return 0;
        }
        
        // A 中仅有一个数，判断该数是否为完全平方数
        if (A_len == 1) {
            if (this->checkSquareNumber(A[0])) {
                return 1;
            } else {
                return 0;
            }
        }
        
        // 先将数组排序，从小到大。初始排列
        sort(A.begin(), A.end());
        int res = 0;
        
        // 计算总的不重复排列个数有多少个
        // A_len! 除以重复数字的重复个数的阶乘
        // 比如 {2, 2, 2, 7, 7} 有 5! / (3! * 2!) = 10 种可能
        int fact = this->factorial(A_len); // 把重复的也计算在其中了
        int fact_copy = fact;
        bool unique = true; // 数组没有重复元素
        int divide = 1;
        int dupli_count = 1;
        for (int i = 1; i < A_len; i++) {
            if (A[i] == A[i - 1]) {
                // 前后数字相同
                unique = false;
                dupli_count ++;
                divide *= dupli_count;
            } else {
                // 出现不同数字
                if (dupli_count > 1) {
                    fact /= divide;
                    divide = 1;
                    dupli_count = 1;
                }
            }
        }
        
        // 往后依次找 fact 个排列，并且验证每个排列是否合法
        // 如果 A 数组没有重复元素，只用找一半，因为另一半是反序
        int max_loop;
        if (unique) {
            max_loop = fact_copy / 2;
        } else {
            max_loop = fact;
        }
        for (int i = 0; i < max_loop; i++) { // do
            bool valid = true;
            
            for (int j = 1; j < A_len; j++) {
                // 验证每两个数加起来是否为完全平方数
                if (this->checkSquareNumber(A[j - 1] + A[j])) {
                    continue;
                } else {
                    // 若不是，则不合法，退出小循环
                    valid = false;
                    break;
                }
            }
            
            if (valid) {
                res ++;
            }
            
            // 形成下个排列
            if (next_permutation(A.begin(), A.end())) { // while
                continue;
            } else {
                break;
            }
        }
        
        if (unique) {
            // 返回一半结果的两倍
            return res << 1;
        } else {
            return res;
        }
    }
    
    // 构造一张图，有 A 中所有的结点，以及一些边 x-y，如果 A[x] + A[y] 是完全平方数
    // 目标就是求这张图的所有哈密顿路径，即经过图中所有点仅一次的路径。
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 92.94% 的用户
    // 内存消耗 : 8.6 MB , 在所有 C++ 提交中击败了 71.79% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Number of Squareful Arrays.
    // Memory Usage: 8.8 MB, less than 38.96% of C++ online submissions for Number of Squareful Arrays.
    int solution2 (vector<int>& A) {
        // 边界情况
        if (A.empty()) {
            return 0;
        }
        
        int A_len = (int)A.size();
        
        // A_len > 12 ，阶乘溢出 MAX_INT32
        if (A_len > 12) {
            return 0;
        }
        
        // A 中仅有一个数，判断该数是否为完全平方数
        if (A_len == 1) {
            if (this->checkSquareNumber(A[0])) {
                return 1;
            } else {
                return 0;
            }
        }
        
        // count[x] : 数组 A 中值为 x 的结点数量
        for (int i = 0; i < A_len; i++) {
            if (this->node_count.find(A[i]) == this->node_count.end()) {
                this->node_count.insert({A[i], 1});
            } else {
                this->node_count[A[i]] ++;
            }
        }
        
        // node_edge[x] : 在 A 中满足 x + y 是完全平方数的所有 y。"xy" 可以看作成一条可行边
        for (auto x = this->node_count.begin();x != this->node_count.end(); x++) {
            this->node_edge.insert({x->first, {}});
        }
        
        for (auto x = this->node_count.begin();x != this->node_count.end(); x++) {
            for (auto y = this->node_count.begin();y != this->node_count.end(); y++) {
                if (this->checkSquareNumber(x->first + y->first)) {
                    this->node_edge[x->first].push_back(y->first);
                }
            }
        }
        
        // 查看哈希表的值
//        cout << "MAP node_count" << endl;
//        for (auto x = this->node_count.begin();x != this->node_count.end(); x++) {
//            cout << x->first << ": " << x->second << endl;
//        }
//
//        cout << "\nMAP node_edge" << endl;
//        for (auto x = this->node_edge.begin();x != this->node_edge.end(); x++) {
//            cout << x->first << ": ";
//            for (int j = 0; j < x->second.size(); j++) {
//                cout << x->second[j] << "->";
//            }
//            cout << "End." << endl;
//        }
        
        int res = 0;
        // 累加每个数字开头的可行解数量
        for (auto x = this->node_count.begin(); x != this->node_count.end(); x++) {
            res += backtrack(x->first, A_len - 1);
        }
        
        return res;
    }
    
    // 回溯法。x 表示当前加入的结点的数值，rest_node 表示总共还剩多少个节点未被访问。
    int backtrack (int x, int rest_node) {
        int res = 1; // 如果本轮 backtrack 递归到结尾了，有一个可行解，则会返回 1
        
        // 前进，使用该结点
        this->node_count[x] --;
        
        // 如果尚未使用完所有结点
        if (rest_node > 0) {
            res = 0; // 本轮 backtrack 递归未到结尾，尚未有解
            
            // edge 数组中的每个值都是可以与 x 构成完全平方数的可行结点
            vector<int> edge = this->node_edge[x];
            for (int i = 0; i < (int)edge.size(); i++) {
                // 如果当前可行边的端点尚未使用，则使用之。否则看下一个可行结点
                if (this->node_count[edge[i]] > 0) {
                    res += backtrack(edge[i], rest_node - 1);
                }
            }
        }
        
        // 回溯，放回该结点
        this->node_count[x] ++;
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    vector<int> A = {1, 17, 8}; // 预期结果 2 // 解释：[1,8,17] 和 [17,8,1] 都是有效的排列
//    vector<int> A = {2, 2, 2}; // 预期结果 1
//    vector<int> A = {2, 2, 7}; // 预期结果 3
//    vector<int> A = {}; // 预期结果 0
//    vector<int> A = {3}; // 预期结果 0
//    vector<int> A = {1, 3}; // 预期结果 2
//    vector<int> A = {4}; // 预期结果 1
//    vector<int> A = {2, 2}; // 预期结果 1
    vector<int> A = {89, 72, 71, 44, 50, 72, 26, 79, 33, 27, 84}; // 预期结果 0
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans =solution->numSquarefulPerms(A);
    cout << "Answer is " << ans << endl;
    
//    int count = 1;
//    sort(A.begin(), A.end());
//    while (next_permutation(A.begin(), A.end())) {
//        count ++;
//    }
//    cout << "count = " << count << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
