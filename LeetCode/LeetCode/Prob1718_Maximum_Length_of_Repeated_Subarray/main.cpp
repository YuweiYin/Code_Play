//
//  main.cpp
//  Prob1718_Maximum_Length_of_Repeated_Subarray
//
//  Created by 阴昱为 on 2019/7/19.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//718. Maximum Length of Repeated Subarray
//
//Given two integer arrays A and B, return the maximum length of an subarray that appears in both arrays.
//
//给两个整数数组 A 和 B ，返回两个数组中公共的、长度最长的子数组的长度。
//
//Example 1:
//    Input:
//        A: [1,2,3,2,1]
//        B: [3,2,1,4,7]
//    Output: 3
//    Explanation:
//        The repeated subarray with maximum length is [3, 2, 1].
//
//Note:
//    1 <= len(A), len(B) <= 1000
//    0 <= A[i], B[i] < 100


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


class Solution {
public:
    int findLength(vector<int>& A, vector<int>& B) {
        return this->solution1(A, B);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(M*N)，空间复杂度 O(M*N)。M = A.size, N = B.size
    // 执行用时 : 1716 ms , 在所有 C++ 提交中击败了 5.36% 的用户
    // 内存消耗 : 13.7 MB , 在所有 C++ 提交中击败了 67.86% 的用户
    // Runtime: 936 ms, faster than 5.02% of C++ online submissions for Maximum Length of Repeated Subarray.
    // Memory Usage: 13.6 MB, less than 58.16% of C++ online submissions for Maximum Length of Repeated Subarray.
    int solution1 (vector<int>& A, vector<int>& B) {
        // 边界情况
        if (A.empty() || B.empty()) {
            return 0;
        }
        
        int A_len = (int)A.size();
        int B_len = (int)B.size();
        
        // A: [1,2,3,2,1] B: [3,2,1,4,7]
        // DP  3  2  1  4  7
        //   ---------------
        // 1 | 0  0  1  0  0
        // 2 | 0  1  0  0  0
        // 3 | 1  0  0  0  0
        // 2 | 0  1  0  0  0
        // 1 | 0  0  1  0  0
        //
        // 看左上到右下方向，最多有多长的连续 1，即为最优值
        vector<vector<bool>> dp(A_len, vector<bool>(B_len, false));
        
        // 写入 DP 表
        for (int i = 0; i < A_len; i++) {
            for (int j = 0; j < B_len; j++) {
                if (A[i] == B[j]) {
                    dp[i][j] = true;
                }
            }
        }
        
        int res = 0;
        int cur_len = 0, m = 0, n = 0;
        
        // "剪枝"：循环最多达到 len - res 就可以了，
        // 如果超过它，选取的连续斜向 1 不可能超过最优值 res 了
        for (int i = 0; i < A_len - res; i++) {
            for (int j = 0; j < B_len - res; j++) {
                if (dp[i][j]) {
                    cur_len = 1;
                    
                    // 斜向往右下找 1
                    for (m = i + 1, n = j + 1; m < A_len && n < B_len; m++, n++) {
                        if (dp[m][n]) {
                            cur_len ++;
                        } else {
                            break;
                        }
                    }
                    
                    // 更新最优值
                    if (cur_len > res) {
                        res = cur_len;
                    }
                }
            }
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
    // 预期结果 3
    vector<int> A = {1, 2, 3, 2, 1};
    vector<int> B = {3, 2, 1, 4, 7};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->findLength(A, B);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
