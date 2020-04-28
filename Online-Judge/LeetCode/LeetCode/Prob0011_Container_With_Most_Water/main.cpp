//
//  main.cpp
//  Prob1011_Container_With_Most_Water
//
//  Created by 阴昱为 on 2019/6/4.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//11. Container With Most Water
//
//Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a container, such that the container contains the most water.
//Note: You may not slant the container and n is at least 2.

//给定 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点 (i, ai) 。在坐标内画 n 条垂直线，垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0)。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。
//说明：你不能倾斜容器，且 n 的值至少为 2。
//
//Example:
//  Input: [1,8,6,2,5,4,8,3,7]
//  Output: 49

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
    int maxArea(vector<int>& height) {
        return this->solution1(height);
    }
    
    // 方法一：双指针游走。时间复杂度 O(n), 空间复杂度 O(1)
    int solution1 (vector<int>& height) {
        int max_area = 0; // 面积最大值
        int left = 0; // 左指针
        int right = (int)height.size() - 1; // 右指针
        
        // 遍历一遍
        while (left < right) {
            // 计算当前面积
            int cur_area = min(height[left], height[right]) * (right - left);
            
            // 判断是否需要更新最大值
            if (cur_area > max_area) {
                max_area = cur_area;
            }
            
            if (height[left] < height[right]) {
                // 如果左指针的高度是短板，则移动左指针
                left ++;
            } else {
                // 否则移动右指针
                right --;
            }
        }
        
        return max_area;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    vector<int> height{1, 8, 6, 2, 5, 4, 8, 3, 7};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    cout << solution->maxArea(height) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
