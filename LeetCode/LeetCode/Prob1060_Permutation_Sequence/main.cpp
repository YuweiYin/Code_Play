//
//  main.cpp
//  Prob1060_Permutation_Sequence
//
//  Created by 阴昱为 on 2019/6/26.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//60. Permutation Sequence
//
//The set [1,2,3,...,n] contains a total of n! unique permutations.
//给出集合 [1,2,3,…,n]，其所有元素共有 n! 种排列。
//By listing and labeling all of the permutations in order, we get the following sequence for n = 3:
//按大小顺序列出所有排列情况，并一一标记，当 n = 3 时, 所有排列如下：
//    "123"
//    "132"
//    "213"
//    "231"
//    "312"
//    "321"
//Given n and k, return the kth permutation sequence.
//给定 n 和 k，返回第 k 个排列。
//
//Note:
//    Given n will be between 1 and 9 inclusive.
//    Given k will be between 1 and n! inclusive.
//说明：
//    给定 n 的范围是 [1, 9]。
//    给定 k 的范围是[1,  n!]。
//
//Example 1:
//    Input: n = 3, k = 3
//    Output: "213"
//
//Example 2:
//    Input: n = 4, k = 9
//    Output: "2314"


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
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
private:
    string res = "";
    bool end_recersion = false;
    
public:
    string getPermutation(int n, int k) {
        return this->solution1(n, k);
    }
    
private:
    // 方法一：排列组合法。时间复杂度 O(N)，空间复杂度 O(N)
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 92.73% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 77.80% 的用户
    // Runtime: 0 ms, faster than 100.00% of C++ online submissions for Permutation Sequence.
    // Memory Usage: 8.3 MB, less than 37.11% of C++ online submissions for Permutation Sequence.
    string solution1 (int n, int k) {
        // 边界情况
        if (n <= 0 || k <= 0 || n > 12) { // n > 12 ，阶乘溢出 MAX_INT32
            return "";
        }
        
        if (n == 1) {
            return "1";
        }
        
        int fact_n = this->factorial(n);
        if (k > fact_n) {
            k %= fact_n;
        }
        
        // 初始排列
        string ans = "";
        string origin = "";
        for (int i = 1; i <= n; i++) {
            origin += to_string(i);
        }
        
        for (int i = 1; i <= n; i++) {
            // k 等于 1，表示当前剩余数字最小序的排列，就是要找的那个排列了
            if (k == 1) {
                // 直接逐个加进来
                for (int j = 0; j < (int)origin.size(); j++) {
                    ans += origin[j];
                }
                break;
            }
            
            // 一个 fact 表示固定当前位为某个数字后，剩余数字能组成的排列数量
            int fact = this->factorial(n - i);
            
            // divide 表示 k 中右多少个完整的 fact
            int divide = k / fact;
            
            // mod 表示减去这些完整的 fact 之后，剩余几个数字。也就是下一轮循环的 k 值
            int mod =  k % fact;
            // cout << "fact:" << fact << ", divide:" << divide << ", mod:" << mod << endl;
            
            if (mod == 0) {
                // 如果 mod 为 0，需要留一个 fact 给 k
                // 因为当下一轮 k 值为 0 ，则表示正在找目标排列的下一个排列，找过头了
                ans += origin[divide - 1]; // 加入该数字
                origin.erase(origin.begin() + divide - 1); // 原数组中删除该数字
                k = fact; // k 赋新值
                // cout << "1-> ans:" << ans << ", k:" << k << endl;
            } else {
                // 如果 mod 不为 0，把余数 mod 留给 k，在原数组 origin 中挑选第 divide 个数字加入 ans
                ans += origin[divide];
                origin.erase(origin.begin() + divide);
                k = mod;
                // cout << "2-> ans:" << ans << ", k:" << k << endl;
            }
        }
        
        return ans;
    }
    
    // 阶乘 n!
    int factorial (int n) {
        if (n <= 1) {
            return 1;
        }
        
        // 12! = 479 001 600 < MAX_INT32
        // 13! = 6 227 020 800 > MAX_INT32
        if (n > 12) {
            return 0; // Overflow
        }
        
        int res = 1;
        
        for (int i = 2; i <= n; i++) {
            res *= i;
        }
        
        return res;
    }
    

    // 方法二：TODO 回溯法，剪枝。时间复杂度 O()，空间复杂度 O()
    string solution2 (int n, int k) {
        // 边界情况
        if (n <= 0 || k <= 0 || n > 12) { // n > 12 ，阶乘溢出 MAX_INT32
            return "";
        }
        
        if (n == 1) {
            return "1";
        }
        
        int fact_n = this->factorial(n);
        if (k > fact_n) {
            k %= fact_n;
        }
        
        // 先排序，方便找到重复元素，剪枝
        // 初始排列
        string nums = "";
        for (int i = 1; i <= n; i++) {
            nums += to_string(i);
        }
        
        // 记录某数字是否已经被选择过
        vector<bool> selected = vector<bool>(n, false);
        string cur_num = "";
        
        this->backtrack(nums, n, 0, cur_num, selected, k);
        
        return this->res;
    }
    
    // TODO 回溯法
    void backtrack (string& nums, int n, int depth, string& cur_num, vector<bool>& selected, int& k) {
        if (end_recersion) {
            return; // 结束结束结束～
        }
        
        if (depth >= n) {
            k --;
            if (k == 0) {
                this->res = cur_num;
                this->end_recersion = true;
            }
            return;
        }
        
        for (int i = 0; i < n; i++) {
            if (end_recersion) {
                return; // 结束结束结束～
            }
            
            // 当前数字未使用过，则选择它
            if (!selected[i]) {
                // 如果当前数字和前一个数相等，并且前一个数已经使用过了，那么不选它(两个相同分支只进一个)
                if (i > 0 && nums[i] == nums[i - 1] && selected[i - 1]) {
                    continue;
                }
                
                // 前进，把 i 元素加进来
                // this->mySwap(nums[i], nums[cur_len]);
                cur_num.push_back(nums[i]);
                selected[i] = true;
                
                // 深度向下执行，长度加一
                this->backtrack(nums, n, depth + 1, cur_num, selected, k);
                if (end_recersion) {
                    return; // 结束结束结束～
                }
                
                // 回溯，弹出 i 元素
                // this->mySwap(nums[i], nums[cur_len]);
                cur_num.erase(cur_num.end() - 1);
                selected[i] = false;
            }
        }
    }
    
    // 方法三：库函数。时间复杂度 O(k)，空间复杂度 O(1)
    // 执行用时 : 864 ms , 在所有 C++ 提交中击败了 5.09% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 79.10% 的用户
    // Runtime: 340 ms, faster than 9.41% of C++ online submissions for Permutation Sequence.
    // Memory Usage: 8.3 MB, less than 37.72% of C++ online submissions for Permutation Sequence.
    string solution3 (int n, int k) {
        // 边界情况
        if (n <= 0 || k <= 0 || n > 12) { // n > 12 ，阶乘溢出 MAX_INT32
            return "";
        }
        
        if (n == 1) {
            return "1";
        }
        
        int fact_n = this->factorial(n);
        if (k > fact_n) {
            k %= fact_n;
        }
        
        // 初始排列
        string ans = "";
        for (int i = 1; i <= n; i++) {
            ans += to_string(i);
        }
        
        // 计数，往后找 k-1 个排列，找到的排列直接放在 ans 里
        int count = 1;
        while (count < k && next_permutation(ans.begin(), ans.end())) {
            count ++;
        }
        
        // 返回 ans，即为第 k 个排列
        return ans;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
//    int n = 3, k = 3; // 预期结果 "213"
    int n = 4, k = 9; // 预期结果 "2314"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans =solution->getPermutation(n, k);
    if (!ans.empty()) {
        cout << ans << endl;
    } else {
        cout << "Answer is empty." << endl;
    }
    
//    for (int i = 1; i <= k; i++) {
//        cout << solution->getPermutation(n, i) << endl;
//    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
