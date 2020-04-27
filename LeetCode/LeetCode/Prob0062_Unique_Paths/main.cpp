//
//  main.cpp
//  Prob1062_Unique_Paths
//
//  Created by 阴昱为 on 2019/7/4.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//62. Unique Paths
//
//A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).
//The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).
//How many possible unique paths are there?
//
//一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为“Start” ）。
//机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。
//问总共有多少条不同的路径？
//
//Note: m and n will be at most 100.
//说明：m 和 n 的值均不超过 100。
//
//Example 1:
//    Input: m = 3, n = 2
//    Output: 3
//    Explanation:
//    From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
//    1. Right -> Right -> Down
//    2. Right -> Down -> Right
//    3. Down -> Right -> Right
//
//Example 2:
//    Input: m = 7, n = 3
//    Output: 28


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
    int uniquePaths(int m, int n) {
        return this->solution2(m, n);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(M*N)，空间复杂度 O(M)。
    // 如果 M 和 N 差距特别大，可以考虑做个判断，只让 dp 表长为 min(M,N)
    // 执行用时 : 0 ms , 在所有 C++ 提交中击败了 100.00% 的用户
    // 内存消耗 : 8.4 MB , 在所有 C++ 提交中击败了 42.89% 的用户
    // Runtime: 8 ms, faster than 8.28% of C++ online submissions for Unique Paths.
    // Memory Usage: 8.5 MB, less than 50.61% of C++ online submissions for Unique Paths.
    int solution1 (int m, int n) {
        // 边界情况
        if (m <= 0 || n <= 0) {
            return 0;
        }
        
        if (m == 1 || n == 1) {
            return 1;
        }
        
        // 令 dp[i][j] 是到达 i, j 的不同路径数量
        // 动态方程：dp[i][j] = dp[i-1][j] + dp[i][j-1]
        // 初始化 dp[i][0] 均为 1，dp[0][j] 均为 1，运行表格如下：
        // 1  1  1  1  1  1  1
        // 1  2  3  4  5  6  7
        // 1  3  6  10 15 21 28
        // 优化：简化为一维 DP，状态转移方程为 dp[j] = dp[j] + dp[j-1]
        // 即：本轮新的 dp[j] = 上一轮 dp[j] + 本轮新的 dp[j-1]
        // 与之前的 dp[i][j] = dp[i-1][j] + dp[i][j-1] 效果相同，节约了存储空间
        vector<int> dp = vector<int>(m, 1);
        
        // 从坐标 (1,1) 开始，m 为列数，n 为行数
        for (int i = 1; i < n; i++) {
            for (int j = 1; j < m; j++) {
                dp[j] += dp[j - 1];
            }
        }
        
        return dp[m - 1];
    }
    
    // 方法二：排列组合。时间复杂度 O(M*N)，空间复杂度 O(1)。
    // Runtime: 4 ms, faster than 74.27% of C++ online submissions for Unique Paths.
    // Memory Usage: 8.3 MB, less than 63.37% of C++ online submissions for Unique Paths.
    int solution2 (int m, int n) {
        // 边界情况
        if (m <= 0 || n <= 0) {
            return 0;
        }
        
        if (m == 1 || n == 1) {
            return 1;
        }
        
        // 共有 N 行 M 列，达到目的地一定需要向右走 M-1 步，向下走 N-1 步
        // 总路径序列为 (M-1)+(N-1) = M+N-2 步，其中挑选出 M-1 步向右（其余自然只能向下）
        // 即求解组合数 C(M+N-2, M-1)，当然该值也等同于 C(M+N-2, N-1)，即挑 N-1 步向下
        // 即求 (M+N-2)! / ((M-1)! * (N-1)!)
        
        // 由题目条件，m 和 n 的值最大可能达到 100，所以阶乘可能会溢出
        return this->combineNumber(m + n - 2, min(m, n) - 1);
    }
    
    // n 个中挑选 m 个做组合
    int combineNumber (int n, int m) {
        double res = 1;
        
        // 为了避免溢出，乘除法交替运行
        for (int i = 0; i < m; i++) {
            res *= n - i;
            res /= m - i;
        }
        
        // 保持精度，四舍五入取最近的整数
        return (int)round(res);
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    int m = 3, n = 2; // 预期结果 3
    int m = 7, n = 3; // 预期结果 28
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->uniquePaths(m, n);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
