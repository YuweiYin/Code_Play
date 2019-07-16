//
//  main.cpp
//  Prob1793_Preimage_Size_of_Factorial_Zeroes_Function
//
//  Created by 阴昱为 on 2019/7/16.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//793. Preimage Size of Factorial Zeroes Function
//
//Let f(x) be the number of zeroes at the end of x!. (Recall that x! = 1 * 2 * 3 * ... * x, and by convention, 0! = 1.)
//For example, f(3) = 0 because 3! = 6 has no zeroes at the end, while f(11) = 2 because 11! = 39916800 has 2 zeroes at the end. Given K, find how many non-negative integers x have the property that f(x) = K.
//
//f(x) 是 x! 末尾是0的数量。（回想一下 x! = 1 * 2 * 3 * ... * x，且0! = 1）
//例如， f(3) = 0 ，因为3! = 6的末尾没有0；而 f(11) = 2 ，因为11!= 39916800末端有2个0。给定 K，找出多少个非负整数x ，有 f(x) = K 的性质。
//
//Example 1:
//    Input: K = 0
//    Output: 5
//    Explanation: 0!, 1!, 2!, 3!, and 4! end with K = 0 zeroes.
//
//Example 2:
//    Input: K = 5
//    Output: 0
//    Explanation: There is no x such that x! ends in K = 5 zeroes.
//
//Note:
//    K will be an integer in the range [0, 10^9].
//注意：
//    K是范围在 [0, 10^9] 的整数。


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


class Solution {
public:
    int preimageSizeFZF(int K) {
        return this->solution2(K);
    }
    
private:
    // 方法一：暴力法。时间复杂度 O(N), 空间复杂度 O(1), N = n
    // 25 / 44 个通过测试用例  最后执行的输入：98918711 超时
    int solution1 (int& K) {
        // 边界条件
        if (K < 0) {
            return 0;
        }
        
        int res = 0;
        
        int n = 0;
        int cur_k = this->trailingZeroes<int>(n);
        
        while (cur_k <= K) {
            if (cur_k < K) {
                if (n == 0) {
                    n = 5;
                } else {
                    n += 5;
                }
            } else {
                res ++;
                n++;
            }
            
            cur_k = this->trailingZeroes<int>(n);
        }
        
        return res;
    }
    
    // 方法二：暴力法优化+规律。时间复杂度 O(log_5 N), 空间复杂度 O(1), N = n
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Preimage Size of Factorial Zeroes Function.
    // Memory Usage: 8.3 MB, less than 26.23% of C++ online submissions for Preimage Size of Factorial Zeroes Function.
    int solution2 (int& K) {
        // 边界条件
        if (K < 0) {
            return 0;
        }
        
        int res = 0;
        
        // 先计算 K * 5 的阶乘末尾有多少个 0，即 cur_k，并计算 cur_k 与 K 的差距，按规律，cur_k 大于 K
        ll k = (ll)(K) * 5;
        ll cur_k = this->trailingZeroes<ll>(k);
        ll gap = cur_k - K;
        
        // cout << gap << ", " << cur_k << ", " << k << ", " << K << endl;
        
        // 目标是缩小 cur_k 与 K 的差距，cur_k 作为函数值不能直接改变，需要改变的是 k 值
        // 最合适的做法是 k -= gap * 4，此时 k 的函数值 cur_k 与 K 很接近
        k -= gap * 4;
        cur_k = this->trailingZeroes<ll>(k);
        gap = cur_k - K;
        
        // cout << gap << ", " << cur_k << ", " << k << ", " << K << endl;
        
        // 之后再 +/- 5 地调整 k 的值，使得 cur_k 的值 +/- 1
        if (gap > 0) {
            while (cur_k >= K) {
                if (cur_k > K) {
                    // 规律：k 每减 5，cur_k 就会减一（但不是连续减一，会跳过一些值）
                    // 如果 cur_k 跳过某些值，表明阶乘函数后 0 数目不可能等于这些值
                    k -= 5;
                } else {
                    // 非 0 即 5，找到即可
                    res = 5;
                    break;
                }
                cur_k = this->trailingZeroes<ll>(k);
            }
        } else if (gap < 0) {
            while (cur_k <= K) {
                if (cur_k < K) {
                    // 规律：k 每加 5，cur_k 就会加一（但不是连续加一，会跳过一些值）
                    // 如果 cur_k 跳过某些值，表明阶乘函数后 0 数目不可能等于这些值
                    k += 5;
                } else {
                    // 非 0 即 5，找到即可
                    res = 5;
                    break;
                }
                cur_k = this->trailingZeroes<ll>(k);
            }
        } else {
            // 直接命中
            res = 5;
        }
        
        return res;
    }
    
    // (LeetCode 172) 子过程：给定一个整数 n，返回 n! 结果尾数中零的数量。
    // 时间复杂度 O(log_5 N), 空间复杂度 O(1), N = n
    template <typename T>
    T trailingZeroes (T n) {
        // 边界条件
        if (n < 5) {
            return 0;
        }
        
        // 规律：5^1 的整倍数贡献 1 个 5，即贡献 10（2 的倍数很多）
        // 5^2 的整倍数贡献 2 个 5。考虑重复情况，则是 5^2 在 5^1 的贡献基础上额外贡献一个 5
        // 例：n = 101, res = (int)(101/5) + (int)(101/25) + (int)(101/125)  = 24
        T res = 0;
        
        do {
            n /= 5;
            res += n;
        } while (n > 0);
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    int K = 0; // 预期结果 5
//    int K = 4; // 预期结果 5
//    int K = 5; // 预期结果 0
//    int K = 200; // 预期结果 5
//    int K = 98918711; // 预期结果 0
//    int K = 98918713; // 预期结果 5
    int K = 1000000000; // 预期结果 5
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->preimageSizeFZF(K);
    cout << "Answer is " << ans << endl;
    
    // 观察规律
//    int cur_res = 0;
//    bool rest_all_five = true;
//    int test_num = 200;
//    for (int i = 0; i <= test_num; i++) {
//        cur_res = solution->preimageSizeFZF(i);
//        if (cur_res == 0) {
//            cout << i << endl; // 输出值为 0 的 i
//        } else if (cur_res != 5) {
//            rest_all_five = false;
//        }
//    }
//
//    if (rest_all_five) {
//        cout << "除了 0 都是 5" << endl; // 正解
//    } else {
//        cout << "除了 0 和 5 还有别的数" << endl;
//    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
