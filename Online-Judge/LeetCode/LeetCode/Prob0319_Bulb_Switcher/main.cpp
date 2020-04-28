//
//  main.cpp
//  Prob1319_Bulb_Switcher
//
//  Created by 阴昱为 on 2019/6/7.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//319. Bulb Switcher
//
//There are n bulbs that are initially off. You first turn on all the bulbs. Then, you turn off every second bulb. On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the i-th round, you toggle every i bulb. For the n-th round, you only toggle the last bulb. Find how many bulbs are on after n rounds.

//初始时有 n 个灯泡关闭。 第 1 轮，你打开所有的灯泡。 第 2 轮，每两个灯泡你关闭一次。 第 3 轮，每三个灯泡切换一次开关（如果关闭则开启，如果开启则关闭）。第 i 轮，每 i 个灯泡切换一次开关。 对于第 n 轮，你只切换最后一个灯泡的开关。 找出 n 轮后有多少个亮着的灯泡。
//
//Example:
//  Input: 3
//  Output: 1
//  Explanation:
//      At first, the three bulbs are [off, off, off].
//      After first round, the three bulbs are [on, on, on].
//      After second round, the three bulbs are [on, off, on].
//      After third round, the three bulbs are [on, off, off].
//  So you should return 1, because there is only one bulb is on.

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
const double EPS = 1e-6;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


class Solution {
public:
    int bulbSwitch(int n) {
        return this->solution2(n);
    }

private:
    // 暴力法：超时
    int solution1 (int n) {
        int count = 0;
        
        vector<bool> light = vector<bool>(n, false);
        
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                // 整除则切换灯泡状态
                if (i % j == 0) {
                    light[i] = !light[i];
                }
            }
        }
        
        // 统计最终亮灯的灯泡数量
        for (int i = 1; i <= n; i++) {
            if (light[i]) {
                count ++;
            }
        }
        
        return count;
    }
    
    // 巧妙解法：
    // 用 i 表示灯泡序号，如果 i 是素数，那么该灯泡总要被按两次，因为 i = 1 * i
    // 如果 i 不是素数，且不是完全平方数，那么该灯泡总要被按偶数次
    // 只有 i 是完全平方数时，该灯泡会被按奇数次，最终状态是亮的
    // 所以只需要统计小于等于 n 的完全平方数个数，也就是 (int)floor(sqrt(n)) 了
    int solution2 (int n) {
        // return (int)sqrt(n);
        return this->mySqrtInt(n);
    }
    
    // 计算 double 型数的正平方根
    double mySqrtDouble(double x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            // 牛顿-拉弗森方法求解平方根，梯度下降 Gradient Descent
            // 要求 x = sqrt(n)，即求 f(x) = x^2 - k 的根。
            // 构造 x_n+1 = x_n + alpha * f(x_n)，如果 f(x) 收敛，
            // 那么通过迭代求解，能使 x_n 趋近于根，alpha 的绝对值越大，变化速度越快。
            
            // f(x) 收敛的充分条件：若 f 二阶可导，那么在待求的零点 x 周围存在一个区域，
            // 只要起始点 x_0 位于这个邻近区域内，那么牛顿-拉弗森方法必定收敛。
            // 可以证明，求平方根时使用的 f(x) = x^2 - k 是收敛的，
            // 梯度 grad = f'(x)，令 alpha = -1 / grad，有 x_n+1 = x_n - f(x_n) / f'(x_n)
            // 对于求平方根问题，f'(x_n) = 2 * x_n，所以 x_n+1 = x_n - (x_n^2 - k) / (2 * x_n)
            // 为了简化计算过程，等式化简为 x_n+1 = (x_n  + k / x_n) / 2
            
            // 梯度下降法的问题：梯度为 0 达到驻点、在根两边震荡、离根越来越远。
            // 不过在求平方根时不会有上述问题。
            
            double res = 1; // 迭代计算平方根 x_n+1
            double last = 0; // 记录上一轮的计算值 x_n
            int max_loop = 100; // 设置最大迭代计算次数
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            return res;
        }
    }
    
    // 获得某整数的正平方根的整数部分
    int mySqrtInt(int x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            double res = 1; // 迭代计算平方根
            double last = 0; // 记录上一轮的计算值
            int max_loop = 100; // 设置最大迭代计算次数
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            // 只返回整数部分
            return int(res);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    int n = 99999;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->bulbSwitch(n) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
