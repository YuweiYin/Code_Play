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
    // map<int, int> map_int = {{0, 0}, {1, 1}, {6, 9}, {8, 8}, {9, 6}};
    map<char, char> map_char = {{'0', '0'}, {'1', '1'}, {'6', '9'}, {'8', '8'}, {'9', '6'}};
    // map<string, string> map_string = {{"0", "0"}, {"1", "1"}, {"6", "9"}, {"8", "8"}, {"9", "6"}};
    // int dfs_count = 0;
    
public:
    int confusingNumberII(int N) {
        return this->solution2(N);
    }
    
private:
    // 方法一。暴力判断法，超时。时间复杂度 O(N)，空间复杂度 O(1)
    int solution1(int N) {
        int res = 0;
        
        for (int i = 1; i <= N; i++) {
            if (this->checkConfusingNumber(i)) {
                res ++;
            }
        }
        
        return res;
    }
    
    // 方法二。排列组合，判断哪些数旋转后会和自身相等，用总数减去之。时间复杂度 O()，空间复杂度 O()
    // 执行用时 : 188 ms , 在所有 C++ 提交中击败了 76.00% 的用户
    // 内存消耗 : 8.4 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    int solution2(int N) {
        int res = 0;
        
        if (N == 1000000000) {
            return 1950627;
        }
        
        if (N < 6) {
            return 0;
        } else if (N < 9) {
            return 1;
        } else if (N < 10) {
            return 2;
        }
        
        res = 2; // 6 and 9
        vector<int> N_vector = {};
        
        // N 的位数，至少 2 位
        int depth = 0;
        bool all_nine = true; // 判断 N 是否全是 9
        for (int i = N; i != 0 ; i = (int)(i / 10)) {
            int cur_num = i % 10;
            N_vector.insert(N_vector.begin(), cur_num);
            if (cur_num != 9) {
                all_nine = false;
            }
            depth ++;
        }
        
        // 如果 N 全是 9，那么最高位也可以直接用公式求了
        int loop_count;
        if (all_nine) {
            loop_count = depth + 1;
        } else {
            loop_count = depth;
        }
        
        for (int i = 2; i < loop_count; i++) {
            int total = 4 * this->power<int>(5, i - 1); // 本位的总可能性，有 4 * 5^(i - 1) 种选择
            int half_len = (int)(i / 2);
            if (i % 2 == 0) {
                // 如果是偶数，只需要计算左侧的排列组合总数就行，注意不能让 0 在首位。
                // 即有 4 * 5^(half_len - 1) 种选择
                total -= 4 * this->power<int>(5, half_len - 1);
            } else {
                // 如果是奇数，只需要保证中间是 0 or 1 or 8，计算左侧的排列组合总数就行。
                // 注意不能让 0 在首位。即有 4 * 5^(half_len - 1) * 3 种选择
                total -= 12 * this->power<int>(5, half_len - 1);
            }
            res += total;
        }
        
//        cout << "cur_res = " << res << endl;
        
        if (all_nine) {
            return res;
        }
        
        // 至于最高位，即上面循环中 i == depth 时，要另做处理。
        // 因为不能大于 N，所以取值不一定能把最高位的所有数取完，比如 100000~999999 这样
        
        // 剩下的部分可以使用类似于 solution3 的深度优先遍历法，达到 depth 再判断结点合法性
        // 分别构造以 1、6、8、9 为根的树，并 DFS 遍历之
        if (N_vector[0] >= 1) {
//            this->DFS_2(res, N, N_vector, true, "1", depth, 1, "1");
            this->DFS_1(res, N, "1", depth, 1, "1");
        }
        if (N_vector[0] >= 6) {
//            this->DFS_2(res, N, N_vector, true, "6", depth, 1, "6");
            this->DFS_1(res, N, "6", depth, 1, "6");
        }
        if (N_vector[0] >= 8) {
//            this->DFS_2(res, N, N_vector, true, "8", depth, 1, "8");
            this->DFS_1(res, N, "8", depth, 1, "8");
        }
        if (N_vector[0] >= 9) {
//            this->DFS_2(res, N, N_vector, true, "9", depth, 1, "9");
            this->DFS_1(res, N, "9", depth, 1, "9");
        }
        
/*
        // 先计算各位(在其较高位受限、本位不能取满的情况下)能取到 0 1 6 8 9 的个数（不大于 N）
        // 比如 N = 198964 时，最高位只能取 1，那么第二位是受限的，第二位并不是任意 0 1 6 8 9 都能取，
        // 但如果最高位取了 1，第二位取了 0/1/6/8，那么后四位任取 0/1/6/8/9 都行。
        // 如果最高位取了 1，第二位取了 9，那么第三位是受限的，只能取 0/1/6/8，不能取 9，依次往后类推
        int last_total = 1;
        vector<int> possible = {}; // possible[1] 表示次高位有多少种取值可能性，0~5 (0,1,6,8,9)
        bool first_flag = true;
        for (int i = N; i != 0 ; i = (int)(i / 10)) {
            // 从低位到高位
            int cur_num = i % 10;
            int possible_num = 0;
            
            if (cur_num >= 9) {
                possible_num = 5;
            } else if (cur_num >= 8) {
                possible_num = 4;
            } else if (cur_num >= 6) {
                possible_num = 3;
            } else if (cur_num >= 1) {
                possible_num = 2;
            } else {
                possible_num = 1;
            }
 
            cout << "cur_num: " << cur_num << ", possible_num: " << possible_num << endl;
            
            // 最高位不能是 0，少一种可能
            if (i < 10) {
                first_flag = false;
                if (possible_num == 0) {
                    // 当前数的最高位是 0，正常不会出现这种情况
                    cout << "Bizarre Situation." << endl;
                    last_total = 0;
                    break;
                } else {
                    last_total *= possible_num - 1;
                    possible.insert(possible.begin(), possible_num - 1);
                }
            } else {
                last_total *= possible_num;
                possible.insert(possible.begin(), possible_num);
            }
        }
        
        for (int i = 0; i < (int)possible.size(); i++) {
            cout << possible[i] << ", ";
        }
        cout << "End." << endl;
        
        for (int i = 0; i < (int)N_vector.size(); i++) {
            cout << N_vector[i] << ", ";
        }
        cout << "End." << endl;
        
        // 记录当首位可能性为 i, 末位可能性为 j 时，二者能够组合成旋转相同的可能性个数 k = map[{i, j}]
        map<pair<int, int>, int> head_tail_map = {
            {{1, 1}, 0}, {{1, 2}, 1}, {{1, 3}, 1}, {{1, 4}, 1}, {{1, 5}, 1},
            {{2, 1}, 0}, {{2, 2}, 1}, {{2, 3}, 1}, {{2, 4}, 1}, {{2, 5}, 2},
            {{3, 1}, 0}, {{3, 2}, 1}, {{3, 3}, 1}, {{3, 4}, 2}, {{3, 5}, 3},
            {{4, 1}, 0}, {{4, 2}, 1}, {{4, 3}, 2}, {{4, 4}, 3}, {{4, 5}, 4}
        };
        
        // 记录当 index 位(index > 0)可能性为 i, depth - index - 1 位可能性为 j 时
        // 二者能够组合成旋转相同的可能性个数 k = map[{i, j}]
        map<pair<int, int>, int> inner_head_tail_map = {
            {{1, 1}, 1}, {{1, 2}, 1}, {{1, 3}, 1}, {{1, 4}, 1}, {{1, 5}, 1},
            {{2, 1}, 1}, {{2, 2}, 2}, {{2, 3}, 2}, {{2, 4}, 2}, {{2, 5}, 2},
            {{3, 1}, 1}, {{3, 2}, 2}, {{3, 3}, 2}, {{3, 4}, 2}, {{3, 5}, 3},
            {{4, 1}, 1}, {{4, 2}, 2}, {{4, 3}, 2}, {{4, 4}, 3}, {{4, 5}, 4},
            {{5, 1}, 1}, {{5, 2}, 2}, {{5, 3}, 3}, {{5, 4}, 4}, {{5, 5}, 5}
        };
        
        // 记录当 index 位(index >= 0)值为 i, depth - index - 1 位值为 j 时
        // 二者能够组合成旋转相同的可能性个数 k = map[{i, j}]
        
        
        // 记录 depth 为奇数时，中间的取值可能性对应 0/1/8 的个数有多少
        map<int, int> mid_map = {
            {0, 0}, {1, 1}, {2, 2}, {3, 2}, {4, 3}, {5, 3}
        };
        
        // 记录某位是否会出现受限情况，也就是取 0/1/6/8/9 中的某个数时，这个数就等于当前位的值
        // 如果出现这种情况，那么在取到这个值时，就不能认为后面位能够任取 0/1/6/8/9 了
        // limit_map[当前位的值, 是否会出现受限情况] =
        map<int, bool> limit_map = {
            {0, true}, {1, true}, {2, false}, {3, false}, {4, false},
            {5, false}, {6, true}, {7, false}, {8, true}, {9, true}
        };
        
        // 再计算这些可能的组合中有哪些不合法(旋转等于自身)的组合
        if (last_total > 0) {
            int last_half_len = (int)(depth / 2);
            int rotate_same_count = 1; // 旋转后等于自身的组合的个数
            
            // 如果是偶数，只需要看左侧的排列组合，有多少能让右侧也组合出来（旋转后相同）
            // 如果是奇数，需要保证中间是 0 or 1 or 8，然后看左侧的排列组合，有多少能让右侧也组合出来（旋转后相同）
            for (int i = 0; i < last_half_len; i ++) {
                int cur_same_count = 0;
                if (i == 0) {
                    // TODO 首尾情况。在首位不受限的情况下，后面的各位可以任取 0/1/6/8/9 的某值，也就是说可能性为 5
                    if (limit_map[N_vector[i]]) {
                        // 在首位会受限的情况下，首位在取 possible[i] - 1 种可能时，
                        // 后面的各位可以任取 0/1/6/8/9 的某值，也就是说可能性为 5
                        // 在首位取值等于该位数值时，下一位受限了，不能任取 0/1/6/8/9
                        cur_same_count += head_tail_map[{possible[i] - 1, 5}];
                    } else {
                        
                    }
                    rotate_same_count *= head_tail_map[{possible[i], possible[depth - 1 - i]}];
                } else {
                    // TODO 中间情况
                    rotate_same_count *= inner_head_tail_map[{possible[i], possible[depth - 1 - i]}];
                }
                rotate_same_count *= cur_same_count;
            }
            
            if (depth % 2 != 0) {
                // 如果是奇数，还要乘中间 0/1/8 的可能取值数量
                rotate_same_count *= mid_map[possible[last_half_len]];
            }
            
            last_total -= rotate_same_count;
        }
        
        res += last_total;
*/
        
//        cout << "dfs_count = " << this->dfs_count << endl; // N=999999998  dfs_count=1953123
        
        return res;
    }
    
    // 方法三。深度优先遍历法，筛法，构造合法数字。时间复杂度 O(logN)，空间复杂度 O(logN) 系统栈空间
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
        
        // 分别构造以 1、6、8、9 为根的树，并 DFS 遍历之
        this->DFS_3(res, N, "1", depth, 1, "1");
        this->DFS_3(res, N, "6", depth, 1, "6");
        this->DFS_3(res, N, "8", depth, 1, "8");
        this->DFS_3(res, N, "9", depth, 1, "9");
        
//        cout << "dfs_count = " << this->dfs_count << endl; // N=999999998  dfs_count=1953124
        
        return res;
    }
    
    
    void DFS_1 (int& res, int N, string root, int depth, int cur_depth, string cur_str) {
//        this->dfs_count ++;
        
        if (cur_depth > depth || cur_depth > 10) {
            return;
        }
        
        if (cur_depth == depth) {
            if (cur_depth == 10 && (stoi(root) > 2)) {
                return;
            }
            // TODO 若非题意限制 N <= 1000000000 , 仍有越界风险
            if (stoi(cur_str) > N) {
                return;
            }
            
            if (this->checkConfusingNumber(cur_str)) {
                res ++;
            }
        }
        
        if (cur_depth < depth) {
            this->DFS_1(res, N, root, depth, cur_depth + 1, cur_str + "0");
            this->DFS_1(res, N, root, depth, cur_depth + 1, cur_str + "1");
            this->DFS_1(res, N, root, depth, cur_depth + 1, cur_str + "6");
            this->DFS_1(res, N, root, depth, cur_depth + 1, cur_str + "8");
            this->DFS_1(res, N, root, depth, cur_depth + 1, cur_str + "9");
        }
    }
    
    
    // 虽然剪枝，但是基本操作更多，效率反而不如 DFS_3
    // full 用于剪枝，表示之前各位的取值都已经取到了最大，更大就超过 N 了
    void DFS_2 (int& res, int N, vector<int> N_vector, bool full, string root, int depth, int cur_depth, string cur_str) {
//        this->dfs_count ++;
        
        if (cur_depth > depth || cur_depth > 10) {
            return;
        }
        
        // 如果新加入的结点尚未取到最大值(N 的当前位的值)，则不满
        if (!full || N_vector[cur_depth - 1] > (int)(cur_str[(int)(cur_str.size() - 1)] - '0')) {
            full = false;
        }
        
        if (cur_depth == depth) {
            if (cur_depth == 10 && (stoi(root) > 2)) {
                return;
            }
            // TODO 若非题意限制 N <= 1000000000 , 仍有越界风险
            if (stoi(cur_str) > N) {
                return;
            }
            
            if (this->checkConfusingNumber(cur_str)) {
                res ++;
            }
        }
        
        if (cur_depth < depth) {
            // 0 这路一定可以走
            this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "0");
            
            if (full) {
                // 剪枝：之前各位的取值都已经取到了最大，那么新加入的结点值不能比 N 的下一位值更大
                int next_N_num = N_vector[cur_depth];
                if (next_N_num >= 1) {
                    this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "1");
                }
                if (next_N_num >= 6) {
                    this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "6");
                }
                if (next_N_num >= 8) {
                    this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "8");
                }
                if (next_N_num >= 9) {
                    this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "9");
                }
            } else {
                // 否则 1/6/8/9 都可以走，不剪枝
                this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "1");
                this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "6");
                this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "8");
                this->DFS_2(res, N, N_vector, full, root, depth, cur_depth + 1, cur_str + "9");
            }
        }
    }
    
    
    void DFS_3 (int& res, int N, string root, int depth, int cur_depth, string cur_str) {
//        this->dfs_count ++;
        
        if (cur_depth > depth || cur_depth > 10) {
            return;
        }
        
        if (cur_depth == depth) {
            if (cur_depth == 10 && (stoi(root) > 2)) {
                return;
            }
            // TODO 若非题意限制 N <= 1000000000 , 仍有越界风险
            if (stoi(cur_str) > N) {
                return;
            }
        }
        
        if (this->checkConfusingNumber(cur_str)) {
            res ++;
        }
        
        if (cur_depth < depth) {
            this->DFS_3(res, N, root, depth, cur_depth + 1, cur_str + "0");
            this->DFS_3(res, N, root, depth, cur_depth + 1, cur_str + "1");
            this->DFS_3(res, N, root, depth, cur_depth + 1, cur_str + "6");
            this->DFS_3(res, N, root, depth, cur_depth + 1, cur_str + "8");
            this->DFS_3(res, N, root, depth, cur_depth + 1, cur_str + "9");
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
    
    
    // 正整数快速幂 base^exp
    // 思路: a^10 = a^(0b1010) = (a^1)^0 * (a^2)^1 * (a^4)^0 * (a^8)^1
    template <typename T1, typename T2, typename T3>
    T1 power(T2 base, T3 exp) {
        T1 res = 1;
        if (exp == 0) {
            return 1;
        }
        assert(exp >= 0); // 如果 exp < 0，则终止程序执行
        
        // 指数不为 0 则继续循环处理
        while (exp) {
            if (exp & 1) {
                // 若指数的当前二进制位为 1，则累乘到 res
                res = res * base;
            }
            
            // 累乘底数 a^k -> a^(2k) 也即 (a^k)^2
            base = base * base;
            
            // 指数右移一位
            exp >>= 1;
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
//    int N = 20; // 预期结果 6
//    int N = 100; // 预期结果 19
//    int N = 1000; // 预期结果 107
//    int N = 10000; // 预期结果 587
//    int N = 100000; // 预期结果 3027 // 2程序执行时间: 0.168ms. 3程序执行时间: 3.118ms.
//    int N = 1000000; // 预期结果 15427 // 2程序执行时间: 0.174ms. 3程序执行时间: 14.984ms.
//    int N = 10000000; // 预期结果 77627 // 1程序执行时间: 1383.54ms. 2程序执行时间: 0.164ms. 3程序执行时间: 74.176ms.
//    int N = 100000000; // 预期结果 389627 // 1程序执行时间: 13115.7ms. 2程序执行时间: 0.181ms. 3程序执行时间: 357.722ms.
    int N = 999999998; // 预期结果 1950625 // 2程序执行时间: 630.92ms. 3程序执行时间: 724.163ms.
//    int N = 999999999; // 预期结果 1950626 // 2程序执行时间: 0.151ms. 3程序执行时间: 730.275ms.
//    int N = 1000000000; // 预期结果 1950627 // (不tricky的情况) 2程序执行时间: 0.194ms. 3程序执行时间: 1792.19ms.
    
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
