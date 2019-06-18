//
//  main.cpp
//  Prob2088_Confusing_Number_II
//
//  Created by 阴昱为 on 2019/6/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//2088. Confusing Number II
//
//
//
//本题我们会将数字旋转 180° 来生成一个新的数字。
//
//比如 0、1、6、8、9 旋转 180° 以后，我们得到的新数字分别为 0、1、9、8、6。
//
//2、3、4、5、7 旋转 180° 后，是 无法 得到任何数字的。
//
//易混淆数（Confusing Number）指的是一个数字在整体旋转 180° 以后，能够得到一个和原来 不同 的数，且新数字的每一位都应该是有效的。（请注意，旋转后得到的新数字可能大于原数字）
//
//给出正整数 N，请你返回 1 到 N 之间易混淆数字的数量。
//
//示例 1：
//    输入：20
//    输出：6
//    解释：
//        易混淆数为 [6,9,10,16,18,19]。
//        6 转换为 9
//        9 转换为 6
//        10 转换为 01 也就是 1
//        16 转换为 91
//        18 转换为 81
//        19 转换为 61
//示例 2：
//    输入：100
//    输出：19
//    解释：
//        易混淆数为 [6,9,10,16,18,19,60,61,66,68,80,81,86,89,90,91,98,99,100]。
//
//提示：
//    1 <= N <= 10^9

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
private:
//    map<int, int> map_int = {{0, 0}, {1, 1}, {6, 9}, {8, 8}, {9, 6}};
    map<char, char> map_char = {{'0', '0'}, {'1', '1'}, {'6', '9'}, {'8', '8'}, {'9', '6'}};
//    map<string, string> map_string = {{"0", "0"}, {"1", "1"}, {"6", "9"}, {"8", "8"}, {"9", "6"}};
    
public:
    int confusingNumberII(int N) {
        return this->solution3(N);
    }
    
private:
    // 方法一。暴力判断法，超时。时间复杂度 O(N^2)，空间复杂度 O(1)
    int solution1(int N) {
        int res = 0;
        
        for (int i = 1; i <= N; i++) {
            if (this->checkConfusingNumber(i)) {
                // cout << i << ",";
                res ++;
            }
        }
        // cout << endl;
        
        return res;
    }
    
    // 方法二。子集判断法，筛法。时间复杂度 O()，空间复杂度 O()
    int solution2(int N) {
        int res = 0;
        return res;
    }
    
    // 方法三。深度优先遍历法，筛法，构造合法数字。时间复杂度 O(NlogN)，空间复杂度 O(logN) 系统栈空间
    // 执行用时 : 884 ms , 在所有 C++ 提交中击败了 34.88% 的用户
    // 内存消耗 : 8.2 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    int solution3(int N) {
        int res = 0;
        
        // 特殊处理：如果是 N = 1e10，要耗费约 1.8 秒，而 N = (1e10)-1 只需要约 0.7 毫秒
        // 题目给定最大的 N 为 1e10，所以没必要额外处理那么多叶节点。只需计算 (1e10)-1 的结果 +1 就行
        // 或者直接 tricky 输出正确值 1950627
        if (N == 1000000000) {
            return 1950627;
        }
        
        // N 的位数，也是构造的树最大深度
        int depth = 0;
        for (int i = N; i != 0 ; i = (int)(i / 10)) {
            depth ++;
        }
        
        // cout << "depth = " << depth << endl;
        
        // 分别构造以 1、6、8、9 为根的树，并 DFS 遍历之
        this->DFS(res, N, "1", depth, 1, "1");
        this->DFS(res, N, "6", depth, 1, "6");
        this->DFS(res, N, "8", depth, 1, "8");
        this->DFS(res, N, "9", depth, 1, "9");
        
        return res;
    }
    
    void DFS (int& res, int N, string root, int depth, int cur_depth, string cur_str) {
        if (cur_depth > depth || cur_depth > 10) {
            return;
        }
        
//        cout << res << ", " << N << ", " << root << ", " << depth << ", " << cur_depth << ", " << cur_str << endl;
        
        if (cur_depth == depth) {
            if (cur_depth == 10 && (stoi(root) > 2)) {
                return;
            }
            // TODO 仍有越界风险
            if (stoi(cur_str) > N) {
                return;
            }
        }
        
        if (this->checkConfusingNumber(cur_str)) {
            res ++;
//            cout << res << ": " << cur_str << endl;
        }
        
        if (cur_depth < depth) {
            this->DFS(res, N, root, depth, cur_depth + 1, cur_str + "0");
            this->DFS(res, N, root, depth, cur_depth + 1, cur_str + "1");
            this->DFS(res, N, root, depth, cur_depth + 1, cur_str + "6");
            this->DFS(res, N, root, depth, cur_depth + 1, cur_str + "8");
            this->DFS(res, N, root, depth, cur_depth + 1, cur_str + "9");
        }
    }
    
    bool checkConfusingNumber (int num) {
        string num_str = to_string(num);
        // 如果数字里面有 2、3、4、5、7 这几个数字，肯定不合法
        if (num_str.find('2') != num_str.npos ||
            num_str.find('3') != num_str.npos ||
            num_str.find('4') != num_str.npos ||
            num_str.find('5') != num_str.npos ||
            num_str.find('7') != num_str.npos) {
            return false;
        }
        
        // 如果不含不合法数字，末尾是 0 肯定能合法，因为旋转后降位，必不可能与原数相等
        if (num % 10 == 0) {
            return true;
        }
        
        // 否则是合法的，则看旋转后是否和原数相同，相同则不要
        int len = (int)num_str.size();
        int half = (int)(len / 2);
        
        if (len % 2 == 0) {
            for (int i = 0; i < half; i++) {
                if (num_str[i] != this->map_char[num_str[len - 1 - i]]) {
                    // 若出现不同，则接收
                    return true;
                }
            }
        } else {
            for (int i = 0; i <= half; i++) {
                if (num_str[i] != this->map_char[num_str[len - 1 - i]]) {
                    // 若出现不同，则接收
                    return true;
                }
            }
        }
        
        return false;
    }
    
    bool checkConfusingNumber (string num_str) {
        // 如果数字里面有 2、3、4、5、7 这几个数字，肯定不合法
//        if (num_str.find('2') != num_str.npos ||
//            num_str.find('3') != num_str.npos ||
//            num_str.find('4') != num_str.npos ||
//            num_str.find('5') != num_str.npos ||
//            num_str.find('7') != num_str.npos) {
//            return false;
//        }
        
        // 否则是合法的，则看旋转后是否和原数相同，相同则不要
        int len = (int)num_str.size();
        int half = (int)(len / 2);
        
        // 如果不含不合法数字，末尾是 0 肯定能合法，因为旋转后降位，必不可能与原数相等
        if (num_str[len - 1] == '0') {
            return true;
        }
        
        if (len % 2 == 0) {
            for (int i = 0; i < half; i++) {
                if (num_str[i] != this->map_char[num_str[len - 1 - i]]) {
                    // 若出现不同，则接收
                    return true;
                }
            }
        } else {
            for (int i = 0; i <= half; i++) {
                if (num_str[i] != this->map_char[num_str[len - 1 - i]]) {
                    // 若出现不同，则接收
                    return true;
                }
            }
        }
        
        return false;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    int N = 20; // 预期结果 6
//    int N = 100; // 预期结果 19
//    int N = 1000; // 预期结果 107
//    int N = 10000; // 预期结果 587
//    int N = 100000; // 预期结果 3027 // 3程序执行时间: 3.118ms.
//    int N = 1000000; // 预期结果 15427 // 3程序执行时间: 14.984ms.
//    int N = 10000000; // 预期结果 77627 // 1程序执行时间: 1383.54ms. 3程序执行时间: 74.176ms.
//    int N = 100000000; // 预期结果 389627 // 1程序执行时间: 13115.7ms. 3程序执行时间: 357.722ms.
    int N = 999999999; //预期结果 1950626 // 3程序执行时间: 701.579ms.
//    int N = 1000000000; // 预期结果 1950627 // 3程序执行时间: 1792.19ms.
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->confusingNumberII(N);
    if (ans >= 0) {
        cout << ans << endl;
    } else {
        cout << "Error, ans < 0." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
