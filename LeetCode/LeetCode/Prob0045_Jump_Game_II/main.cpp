//
//  main.cpp
//  Prob1045_Jump_Game_II
//
//  Created by 阴昱为 on 2019/7/21.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//45. Jump Game II
//
//Given an array of non-negative integers, you are initially positioned at the first index of the array.
//Each element in the array represents your maximum jump length at that position.
//Your goal is to reach the last index in the minimum number of jumps.
//
//数组中的每个元素代表你在该位置可以跳跃的最大长度。
//你的目标是使用最少的跳跃次数到达数组的最后一个位置。
//
//Example:
//    Input: [2,3,1,1,4]
//    Output: 2
//    Explanation: The minimum number of jumps to reach the last index is 2.
//    Jump 1 step from index 0 to 1, then 3 steps to the last index.
//
//Note:
//    You can assume that you can always reach the last index.
//
//说明:
//    假设你总是可以到达数组的最后一个位置。


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
    int jump(vector<int>& nums) {
        return this->solution1(nums);
    }
    
private:
    // 方法一：贪心选择。时间复杂度 O(N^2)，空间复杂度 O(1)。
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 91.27% 的用户
    // 内存消耗 : 10 MB , 在所有 C++ 提交中击败了 92.62% 的用户
    // Runtime: 8 ms, faster than 96.92% of C++ online submissions for Jump Game II.
    // Memory Usage: 10.1 MB, less than 56.43% of C++ online submissions for Jump Game II.
    int solution1 (vector<int>& nums) {
        // 边界情况
        if (nums.empty() || nums.size() <= 1) {
            return 0;
        }
        
        int len = (int)nums.size();
        
        int res = 0;
        
        bool continue_loop = true;
        int cur_index = 0, farthest_index = 0, best_choice = 0;
        
        while (continue_loop) {
            best_choice = farthest_index;
            
            // 贪心选择综合效果最远的点
            for (int i = farthest_index; i >= cur_index; i--) {
                if (i + nums[i] >= len - 1) {
                    // 本次跳跃已可以达到目的地
                    best_choice = i + nums[i];
                    continue_loop = false;
                    break;
                }
                
                if (i + nums[i] > best_choice) {
                    best_choice = i + nums[i];
                }
            }
            
            // cout << "best_choice = " << best_choice << endl;
            
            if (best_choice <= farthest_index) {
                // 最佳跳跃都不能使得前进，则不可能达到目的地
                return -1;
            } else {
                farthest_index = best_choice;
                cur_index ++; // 至少向前要跳一步
                res ++; // 记录这一步
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
//    vector<int> nums = {2, 3, 1, 1, 4}; // 预期结果 2
    vector<int> nums = {2, 3, 1, 1, 4, 2, 3, 1, 1, 4, 2, 3, 1, 1, 4}; // 预期结果
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->jump(nums);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
