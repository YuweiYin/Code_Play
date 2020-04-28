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
#define ll long long

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
private:
    // for solution3
    ll P = 113; // 小素数
    ll MOD = 1e9 + 7; // 模数
    ll Pinv = 0; // P 在 MOD 下的逆元
    
public:
    int findLength(vector<int>& A, vector<int>& B) {
        return this->solution3(A, B);
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
    
    // 方法二：真-动态规划。时间复杂度 O(M*N)，空间复杂度 O(M*N)。M = A.size, N = B.size
    // 执行用时 : 260 ms , 在所有 C++ 提交中击败了 81.63% 的用户
    // 内存消耗 : 106.4 MB , 在所有 C++ 提交中击败了 39.88% 的用户
    // Runtime: 168 ms, faster than 67.33% of C++ online submissions for Maximum Length of Repeated Subarray.
    // Memory Usage: 106.3 MB, less than 28.37% of C++ online submissions for Maximum Length of Repeated Subarray.
    int solution2 (vector<int>& A, vector<int>& B) {
        // 边界情况
        if (A.empty() || B.empty()) {
            return 0;
        }
        
        int A_len = (int)A.size();
        int B_len = (int)B.size();
        
        // A: [1,2,3,2,1] B: [3,2,1,4,7]
        // dp[i+1][j+1] = dp[i][j] + 1
        // DP  3  2  1  4  7
        //   ---------------
        // 1 | 0  0  1  0  0
        // 2 | 0  1  0  0  0
        // 3 | 1  0  0  0  0
        // 2 | 0  2  0  0  0
        // 1 | 0  0  3  0  0
        vector<vector<int>> dp(A_len + 1, vector<int>(B_len + 1, 0));
        
        int res = 0;
        
        for (int i = 0; i < A_len; i++) {
            for (int j = 0; j < B_len; j++) {
                if (A[i] == B[j]) {
                    dp[i + 1][j + 1] = dp[i][j] + 1; // state change
                    
                    if (dp[i + 1][j + 1] > res) {
                        res = dp[i + 1][j + 1]; // update maximum
                    }
                }
            }
        }
        
        return res;
    }
    
    // 方法三：Rabin-Karp 算法 + 二分查找 + 哈希散列。
    // 时间复杂度 O((M+N) * lg(min(M,N)))，空间复杂度 O(M)。M = A.size, N = B.size
    int solution3 (vector<int>& A, vector<int>& B) {
        // 边界情况
        if (A.empty() || B.empty()) {
            return 0;
        }
        
        int A_len = (int)A.size();
        int B_len = (int)B.size();
        
        // 如果数组 A 和 B 有一个长度为 k 的公共子数组，那么它们一定有长度为 j <= k 的公共子数组。
        // 这样可以通过二分查找的方法找到最大的 k。二分查找的下界为 0，上界为 min(len(A), len(B))。
        // 在二分查找的每一步中，可以考虑使用哈希的方法来判断数组 A 和 B 中是否存在相同的长度为 mid 的子数组。
        
        // 使用 Rabin-Karp 算法求出一个序列的哈希值。具体地，我们制定一个素数 p，那么序列 S 的哈希值为
        // 形象地来说，就是把 S 看成一个类似 p 进制的数（但左侧为低位，右侧为高位），它的十进制值就是这个它的哈希值。
        // 由于这个值一般会非常大，因此会将它对另一个素数 M 取模。
        // 当要在一个序列 S 中算出所有长度为 l 的子序列的哈希值时，
        // 可以用类似滑动窗口的方法，在线性时间内得到这些子序列的哈希值。
        // 为了保证百分百的正确性，当两个字符串的哈希值相等时，需要判断它们对应的字符串是否相等，防止哈希碰撞。
        
        // 调用扩展欧几里得算法，计算 this->Pinv，即 P 在模 MOD 下的逆元
        ll y = 0;
        this->ex_gcd<ll>(this->P, this->MOD, this->Pinv, y);
        if (this->Pinv < 0) {
            this->Pinv += this->MOD;
        }
        
        int low = 0, high = min(A_len, B_len) + 1;
        
        while (low < high) {
            int mid = (low + high) / 2;
            
            if (this->check(mid, A, B)) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        
        return low - 1;
    }
    
    bool check (int mid, vector<int>& A, vector<int>& B) {
        map<int, vector<int>> hashes = {};
        vector<int> A_roll = this->rolling(A, mid);
        vector<int> B_roll = this->rolling(B, mid);
        int k = 0;
        
        for (int i = 0; i < A_roll.size(); i++) {
            if (hashes.find(A_roll[i]) == hashes.end()) {
                hashes.insert({A_roll[i], {k}});
            } else {
                hashes[A_roll[i]].push_back(k);
            }
            k ++;
        }
        
        k = 0;
        for (int i = 0; i < B_roll.size(); i++) {
            vector<int> x;
            if (hashes.find(B_roll[i]) == hashes.end()) {
                x = {};
            } else {
                x = hashes[B_roll[i]];
            }
            
            for (int j = 0; j < x.size(); j++) {
                bool equal = true;
                // 比较 A[i..i+mid] 是否等于 B[j..j+mid]
                for (int count = 0; count <= mid; count ++) {
                    if (A[i + count] != B[j + count]) {
                        equal = false;
                        break;
                    }
                }
                
                // 相等则返回 true
                if (equal) {
                    return true;
                }
            }
            
            k++;
        }
        
        return false;
    }
    
    vector<int> rolling (vector<int>& source, int length) {
        int s_len = (int)source.size();
        vector<int> ans(s_len - length + 1);
        long h = 0, power = 1;
        
        if (length == 0) {
            return ans;
        }
        
        for (int i = 0; i < s_len; i++) {
            h = (h + source[i] * power) % this->MOD;
            
            if (i < length - 1) {
                power = (power * this->P) % this->MOD;
            } else {
                ans[i - (length - 1)] = (int) h;
                h = (h - source[i - (length - 1)]) * Pinv % MOD;
                
                if (h < 0) {
                    h += this->MOD;
                }
            }
        }
        
        return ans;
    }
    
    // Greatest Common Divisor，辗转相除法、Euclid's Algorithm
    // 核心思路：递归执行 gcd(a, b) = gcd(b, a % b)，直到 b == 0时，a 为最大公约数
    // 求两数的最大公约数，如果为 1，表示两数互素
    template <typename T>
    T gcd (T a, T b) {
        return b ? gcd(b, a % b) : a;
    }
    
    // Extend Euclidean Algorithm 扩展欧几里得算法
    // 返回值为 gcd(a, b) 即 a 和 b 的最大公约数
    // 当 gcd(a, b) == 1 时，x 是 a 在模 b 意义下的乘法逆元
    template <typename T>
    T ex_gcd (T a, T b, T &x, T &y) {
        if(b == 0) {
            // 辗转相除到头，得到最大公约数，返回之
            x = 1;
            y = 0;
            return a;
        } else {
            T r = ex_gcd(b, a % b, x, y);
            // 得到最大公约数之后，一路反向传递之
            
            // 往回传递最大公约数过程中，不断根据递推关系修改参数 x 和 y
            T t = x;
            x = y; // x_(k-1) = y_k
            y = t - a / b * y; // y_(k-1) = x_k - (a/b) * y_k
            
            // 回传最大公约数
            return r;
        }
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
