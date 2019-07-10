//
//  main.cpp
//  Prob1174_Dungeon_Game
//
//  Created by 阴昱为 on 2019/7/10.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//174. Dungeon Game
//
//The demons had captured the princess (P) and imprisoned her in the bottom-right corner of a dungeon. The dungeon consists of M x N rooms laid out in a 2D grid. Our valiant knight (K) was initially positioned in the top-left room and must fight his way through the dungeon to rescue the princess.
//
//The knight has an initial health point represented by a positive integer. If at any point his health point drops to 0 or below, he dies immediately.
//
//Some of the rooms are guarded by demons, so the knight loses health (negative integers) upon entering these rooms; other rooms are either empty (0's) or contain magic orbs that increase the knight's health (positive integers).
//In order to reach the princess as quickly as possible, the knight decides to move only rightward or downward in each step.
//Write a function to determine the knight's minimum initial health so that he is able to rescue the princess.
//
//一些恶魔抓住了公主（P）并将她关在了地下城的右下角。地下城是由 M x N 个房间组成的二维网格。我们英勇的骑士（K）最初被安置在左上角的房间里，他必须穿过地下城并通过对抗恶魔来拯救公主。
//骑士的初始健康点数为一个正整数。如果他的健康点数在某一时刻降至 0 或以下，他会立即死亡。
//有些房间由恶魔守卫，因此骑士在进入这些房间时会失去健康点数（若房间里的值为负整数，则表示骑士将损失健康点数）；其他房间要么是空的（房间里的值为 0），要么包含增加骑士健康点数的魔法球（若房间里的值为正整数，则表示骑士将增加健康点数）。
//为了尽快到达公主，骑士决定每次只向右或向下移动一步。
//编写一个函数来计算确保骑士能够拯救到公主所需的最低初始健康点数。
//
//For example, given the dungeon below, the initial health of the knight must be at least 7 if he follows the optimal path RIGHT-> RIGHT -> DOWN -> DOWN.
//例如，考虑到如下布局的地下城，如果骑士遵循最佳路径 右 -> 右 -> 下 -> 下，则骑士的初始健康点数至少为 7。
//
//-2(K)  -3    3
//-5     -10   1
//10     30    -5(p)
//
//Note:
//    The knight's health has no upper bound.
//    Any room can contain threats or power-ups, even the first room the knight enters and the bottom-right room where the princess is imprisoned.
//说明:
//    骑士的健康点数没有上限。
//    任何房间都可能对骑士的健康点数造成威胁，也可能增加骑士的健康点数，包括骑士进入的左上角房间以及公主被监禁的右下角房间。


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
const int negative_infinity = -0x40000000;


class Solution {
public:
    int calculateMinimumHP(vector<vector<int>>& dungeon) {
        return this->solution1(dungeon);
    }
    
private:
    // 方法一：动态规划。时间复杂度 O(M*N)，空间复杂度 O(M)。
    // TODO 36 / 45 个通过测试用例 [[1,-3,3],[0,-2,0],[-3,-3,-3]] 预期结果 3
    int solution1 (vector<vector<int>>& dungeon) {
        // 边界情况
        if (dungeon.empty() || dungeon[0].empty()) {
            return 0;
        }
        
        int row = (int)dungeon.size();
        int col = (int)dungeon[0].size();
        
        if (row == 1 && col == 1) {
            if (dungeon[0][0] <= 0) {
                return 1 - dungeon[0][0];
            } else {
                return 1;
            }
        }
        
        // dp(i,j) 表示在经过房间 (i,j) 的惩罚/奖励后，(剩余生命值, 曾透支生命值点数)
        vector<pair<int, int>> dp(col, {negative_infinity, negative_infinity});
        int left_0, left_1, up_0, up_1;
        
        dp[0] = {0, 0}; // 令 dp(0,0) = 0，方便查看生命透支情况
        // 自顶向下动态规划，经过一个房间后，惩罚则扣血量，奖励则增血量
        // 然后判断当前血量是否比“曾透支生命值点数”还低，如果是，则更新后者
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                // 状态转移
                if (j == 0) {
                    // 在最左侧，没有 dp[j - 1]，只看上面路径累加本结点的代价
                    get<0>(dp[j]) = get<0>(dp[j]) + dungeon[i][j];
                    if (get<0>(dp[j]) < get<1>(dp[j])) {
                        get<1>(dp[j]) = get<0>(dp[j]);
                    }
                } else {
                    // 分别计算从左边路径 dp[j - 1] 和上面路径 dp[j] 来的代价
                    left_0 = get<0>(dp[j - 1]) + dungeon[i][j];
                    left_1 = get<1>(dp[j - 1]);
                    if (left_0 < left_1) {
                        left_1 = left_0;
                    }

                    up_0 = get<0>(dp[j]) + dungeon[i][j];
                    up_1 = get<1>(dp[j]);
                    if (up_0 < up_1) {
                        up_1 = up_0;
                    }

                    // 选择经过本房间后，“曾透支生命值点数”较少的那个
                    if (left_1 > up_1) {
                        get<0>(dp[j]) = left_0;
                        get<1>(dp[j]) = left_1;
                    } else if (left_1 < up_1) {
                        get<0>(dp[j]) = up_0;
                        get<1>(dp[j]) = up_1;
                    } else {
                        // 如果“曾透支生命值点数”相等，选择当前剩余血量更多的那个
                        if (left_0 > up_0) {
                            get<0>(dp[j]) = left_0;
                            get<1>(dp[j]) = left_1;
                        } else {
                            get<0>(dp[j]) = up_0;
                            get<1>(dp[j]) = up_1;
                        }
                    }
                }
                cout << "(" << get<0>(dp[j]) << "," << get<1>(dp[j]) << ")  ";
            }
            cout << endl;
        }
        
//        dp[col - 1] = {0, 0};
//        // 自底向上动态规划，经过一个房间后，惩罚则扣血量，奖励则增血量
//        // 然后判断当前血量是否比“曾透支生命值点数”还低，如果是，则更新后者
//        for (int i = row - 1; i >= 0; i--) {
//            for (int j = col - 1; j >= 0; j--) {
//                // 状态转移
//                if (j == col - 1) {
//                    // 在最右侧，没有 dp[j + 1]，只看上面路径累加本结点的代价
//                    get<0>(dp[j]) = get<0>(dp[j]) + dungeon[i][j];
//                    if (get<0>(dp[j]) < get<1>(dp[j])) {
//                        get<1>(dp[j]) = get<0>(dp[j]);
//                    }
//                } else {
//                    // 分别计算从右边路径 dp[j + 1] 和下面路径 dp[j] 来的代价
//                    left_0 = get<0>(dp[j + 1]) + dungeon[i][j];
//                    left_1 = get<1>(dp[j + 1]);
//                    if (left_0 < left_1) {
//                        left_1 = left_0;
//                    }
//
//                    up_0 = get<0>(dp[j]) + dungeon[i][j];
//                    up_1 = get<1>(dp[j]);
//                    if (up_0 < up_1) {
//                        up_1 = up_0;
//                    }
//
//                    // 选择经过本房间后，“曾透支生命值点数”较少的那个
//                    if (left_1 > up_1) {
//                        get<0>(dp[j]) = left_0;
//                        get<1>(dp[j]) = left_1;
//                    } else {
//                        get<0>(dp[j]) = up_0;
//                        get<1>(dp[j]) = up_1;
//                    }
//                }
//                cout << "(" << get<0>(dp[j]) << "," << get<1>(dp[j]) << ")  ";
//            }
//            cout << endl;
//        }
        
        // 保证比“曾透支生命值点数”多 1 点血即可
        if (get<1>(dp[col - 1]) <= 0) {
            return 1 - get<1>(dp[col - 1]);
        } else {
            return 1;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    vector<vector<int>> dungeon = {
//        {-2, -3, 3},
//        {-5, -10, 1},
//        {10, 30, -5}
//    }; // 预期结果 7
    
//    vector<vector<int>> dungeon = {
//        {1, -3, 3},
//        {0, -2, 0},
//        {-3, -3, -3}
//    }; // 预期结果 3
    
    vector<vector<int>> dungeon = {
        {1, -3, 3, -1},
        {0, -2, 0, -1}, // 改为 2 纬 dp，遇到上或者左为 0 ，则考察 0 的比较它的左和上，因为 0 相当于快速通道
        {-3, -3, -3, -3}
    }; // 预期结果 4
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->calculateMinimumHP(dungeon);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
