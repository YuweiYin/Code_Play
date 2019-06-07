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
        return (int)sqrt(n);
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    int n = 666;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->bulbSwitch(n) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
