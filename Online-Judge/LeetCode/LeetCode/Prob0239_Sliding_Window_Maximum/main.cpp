//
//  main.cpp
//  Prob1239_Sliding_Window_Maximum
//
//  Created by 阴昱为 on 2019/8/5.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//239. Sliding Window Maximum
//
//Given an array nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position. Return the max sliding window.
//
//给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。
//返回滑动窗口中的最大值。
//
//Example:
//    Input: nums = [1,3,-1,-3,5,3,6,7], and k = 3
//    Output: [3,3,5,5,6,7]
//    Explanation:
//
//    Window position                Max
//    ---------------               -----
//    [1  3  -1] -3  5  3  6  7       3
//    1 [3  -1  -3] 5  3  6  7       3
//    1  3 [-1  -3  5] 3  6  7       5
//    1  3  -1 [-3  5  3] 6  7       5
//    1  3  -1  -3 [5  3  6] 7       6
//    1  3  -1  -3  5 [3  6  7]      7

//Note:
//    You may assume k is always valid, 1 ≤ k ≤ input array's size for non-empty array.
//
//Follow up:
//    Could you solve it in linear time?
//
//提示：
//    你可以假设 k 总是有效的，在输入数组不为空的情况下，1 ≤ k ≤ 输入数组的大小。
//
//进阶：
//    你能在线性时间复杂度内解决此题吗？


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
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        return this->solution1(nums, k);
    }
    
private:
    // 方法一。动态规划。时间复杂度 O(N)，空间复杂度 O(1)。N = nums.size
    // 执行用时 : 76 ms , 在所有 C++ 提交中击败了 92.19% 的用户
    // 内存消耗 : 13.1 MB , 在所有 C++ 提交中击败了 42.06% 的用户
    // Runtime: 48 ms, faster than 99.03% of C++ online submissions for Sliding Window Maximum.
    // Memory Usage: 13.2 MB, less than 65.00% of C++ online submissions for Sliding Window Maximum.
    vector<int> solution1 (vector<int>& nums, int k) {
        // 边界情况
        if (k <= 0 || nums.empty()) {
            return {};
        }
        
        if (k == 1) {
            return nums;
        }
        
        int len = (int)nums.size();
        
        // 如果窗口大小超过数组，则用查找最末顺序统计量的方法在 O(lg N) 时间内找出最大值
        if (k >= len) {
            return {this->selectOrderStatistic(nums, len, 0, len - 1)};
        }
        
        // 将输入数组分割成有 k 个元素的块，若 n % k != 0，则最后一块的元素个数较少些
        // 记录从某块的最左坐标至坐标 i 的最大值
        vector<int> left(len, INT_MIN);
        left[0] = nums[0];
        
        // 记录从某块的最右坐标至坐标 i 的最大值
        vector<int> right(len, INT_MIN);
        right[len - 1] = nums[len - 1];
        
        for (int i = 1; i < len; i++) {
            // 从块的左到右
            if (i % k == 0) {
                left[i] = nums[i]; // 此时 i 是块的起始坐标
            } else {
                left[i] = max(left[i - 1], nums[i]);
            }
            
            // 从块的右到左
            int j = len - i - 1;
            if ((j + 1) % k == 0) {
                right[j] = nums[j]; // 此时 i 是块的末尾坐标
            } else {
                right[j] = max(right[j + 1], nums[j]);
            }
        }
        
        // 两数组一起可以提供两个块内元素的全部信息，考虑从下标 i 到下标 j的滑动窗口
        vector<int> res(len - k + 1, INT_MIN);
        for (int i = 0; i < len - k + 1; i++) {
            res[i] = max(left[i + k - 1], right[i]);
        }
        
        return res;
    }
    
    void exchange (vector<int>& nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    // 快排随机划分，返回最终的主元位置
    int randomizedPartition (vector<int>& nums, int l, int r) {
        // 随机交换某个下标为 l..r 的数到末尾 r 处
        this->exchange(nums, rand()%(r - l) + l, r);
        
        // 随机交换某个下标为 l..r 的数到末尾 r 处
        this->exchange(nums, rand()%(r - l) + l, r);
        
        // 快排的划分，主元 pivot 为 nums[r]
        int i = l - 1;
        for (int j = l; j < r; j++) {
            if (nums[j] <= nums[r]) {
                this->exchange(nums, ++i, j);
            }
        }
        
        // 把主元放在划分点位置
        i++;
        this->exchange(nums, i, r);
        
        return i;
    }
    
    // 在 nums 向量的坐标 l..r 间，查找第 k 小的数（第 k 个顺序统计量）
    int selectOrderStatistic(vector<int>& nums, int k, int l, int r) {
        if (l == r) {
            return nums[l];
        }
        
        int q = this->randomizedPartition(nums, l, r);
        int less = q - l + 1; // A[l..q] 中的元素个数，也就是比 num[q] 更小的元素个数
        
        if (k == less) {
            // 命中，num[q] 即为第 k 顺序统计量（数组中第 k 小的数）
            return nums[q];
        } else if (k < less) {
            // k 比 less 更小，需要在左子数组中继续递归查找第 k 小的数
            return selectOrderStatistic(nums, k, l, q - 1);
        } else {
            // k 比 less 更大，需要在右子数组中继续递归查找第 k - less 小的数
            return selectOrderStatistic(nums, k - less, q + 1, r);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    vector<int> nums = {1, 3, -1, -3, 5, 3, 6, 7};
    int k = 3; // 预期结果 [3,3,5,5,6,7]
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<int> ans = solution->maxSlidingWindow(nums, k);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        for (int i = 0; i < ans.size(); i++) {
            cout << ans[i] << ", ";
        }
        cout << "End." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
