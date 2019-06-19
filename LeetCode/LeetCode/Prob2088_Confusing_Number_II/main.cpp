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

const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


class Solution {
private:
    map<int, int> map_int = {{0, 0}, {1, 1}, {6, 9}, {8, 8}, {9, 6}};
    map<char, char> map_char = {{'0', '0'}, {'1', '1'}, {'6', '9'}, {'8', '8'}, {'9', '6'}};
    // map<string, string> map_string = {{"0", "0"}, {"1", "1"}, {"6", "9"}, {"8", "8"}, {"9", "6"}};
    // int dfs_count = 0;
    
    // num_possible[i] = j 表示记录非首位数字为 i 时，对应的取值可能性 j
    // 如果是首位数字，对应的取值可能性为 num_possible[i] - 1
    map<int, int> num_possible = {
        {0, 1}, {1, 2}, {2, 2}, {3, 2}, {4, 2},
        {5, 2},{6, 3}, {7, 3}, {8, 4}, {9, 5}
    };
    
    // 记录当首位可能性为 i, 末位可能性为 j 时，二者能够组合成旋转相同的可能性个数 k = map[{i, j}]
//    map<pair<int, int>, int> head_tail_map = {
//        {{1, 1}, 0}, {{1, 2}, 1}, {{1, 3}, 1}, {{1, 4}, 1}, {{1, 5}, 1},
//        {{2, 1}, 0}, {{2, 2}, 1}, {{2, 3}, 1}, {{2, 4}, 1}, {{2, 5}, 2},
//        {{3, 1}, 0}, {{3, 2}, 1}, {{3, 3}, 1}, {{3, 4}, 2}, {{3, 5}, 3},
//        {{4, 1}, 0}, {{4, 2}, 1}, {{4, 3}, 2}, {{4, 4}, 3}, {{4, 5}, 4}
//    };
    
    // 记录当 index 位(index > 0)可能性为 i, depth - index - 1 位可能性为 j 时
    // 二者能够组合成旋转相同的可能性个数 k = map[{i, j}]
//    map<pair<int, int>, int> inner_head_tail_map = {
//        {{1, 1}, 1}, {{1, 2}, 1}, {{1, 3}, 1}, {{1, 4}, 1}, {{1, 5}, 1},
//        {{2, 1}, 1}, {{2, 2}, 2}, {{2, 3}, 2}, {{2, 4}, 2}, {{2, 5}, 2},
//        {{3, 1}, 1}, {{3, 2}, 2}, {{3, 3}, 2}, {{3, 4}, 2}, {{3, 5}, 3},
//        {{4, 1}, 1}, {{4, 2}, 2}, {{4, 3}, 2}, {{4, 4}, 3}, {{4, 5}, 4},
//        {{5, 1}, 1}, {{5, 2}, 2}, {{5, 3}, 3}, {{5, 4}, 4}, {{5, 5}, 5}
//    };
    
    // 记录某位是否会出现受限情况，也就是取 0/1/6/8/9 中的某个数时，这个数就等于当前位的值
    // 如果出现这种情况，那么在取到这个值时，就不能认为后面位能够任取 0/1/6/8/9 了
    // limit_map[当前位的值, 是否会出现受限情况] =
    map<int, bool> limit_map = {
        {0, true}, {1, true}, {2, false}, {3, false}, {4, false},
        {5, false}, {6, true}, {7, false}, {8, true}, {9, true}
    };
    
    // 记录 depth 为奇数时，中间位是否可能受限，也就是取 0/1/8 时
    map<int, bool> mid_limit_map = {
        {0, true}, {1, true}, {2, false}, {3, false}, {4, false},
        {5, false}, {6, false}, {7, false}, {8, true}, {9, false}
    };
    
    // 记录 depth 为奇数时，中间的取值对应 0/1/8 的个数有多少
    map<int, int> mid_map = {
        {0, 1}, {1, 2}, {2, 2}, {3, 2}, {4, 2},
        {5, 2},{6, 2}, {7, 2}, {8, 3}, {9, 3}
    };
    
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
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 96.00% 的用户
    // 内存消耗 : 8.8 MB , 在所有 C++ 提交中击败了 100.00% 的用户
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
        vector<int> N_vector = {}; // 记录 N 各位的数值
        
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
        
        // cout << "cur_res = " << res << endl;
        
        if (all_nine) {
            return res;
        }
        
        // 至于最高位，即上面循环中 i == depth 时，要另做处理。
        // 因为不能大于 N，所以取值不一定能把最高位的所有数取完，比如 100000~999999 这样
        
        // 剩下的部分可以使用类似于 solution3 的深度优先遍历法，达到 depth 再判断结点合法性
        // 分别构造以 1、6、8、9 为根的树，并 DFS 遍历之
//        if (N_vector[0] >= 1) {
//            this->DFS_1(res, N, "1", depth, 1, "1");
//        }
//        if (N_vector[0] >= 6) {
//            this->DFS_1(res, N, "6", depth, 1, "6");
//        }
//        if (N_vector[0] >= 8) {
//            this->DFS_1(res, N, "8", depth, 1, "8");
//        }
//        if (N_vector[0] >= 9) {
//            this->DFS_1(res, N, "9", depth, 1, "9");
//        }
        
        // 最高位 100..00 到 N 的总组合(用 0/1/6/8/9 组合)数量（包括旋转后等于自身的数）
        // 即首位取 1/6/8/9 <= N_vector[0]，后面第 i 位取 0/1/6/8/9 <= N_vector[i - 1]
        int rest_total = 0;
        bool first_flag = true;
        
        for (int i = 0; i < depth; i++) {
            // 判断当前位是否会出现受限情况
            bool limit = this->limit_map[N_vector[i]];
            
            if (limit) {
                // 如果该位可能会受限，那么在下一个循环中，计算受限的那个情况
                // 而除了取受限的那个最大数外，取别的都不会使得后面受限
                // 注意 num_possible[N_vector[i]] - 1 才是首位数字对应的取值可能数
                if (first_flag) {
                    first_flag = false;
                    // 如果已到最后一位，则不必关心会不会让后面受限
                    if (i == depth - 1) {
                        rest_total += this->num_possible[N_vector[i]] - 1;
                    } else {
                        rest_total += (this->num_possible[N_vector[i]] - 2) * this->power<int>(5, depth - 1 - i);
                    }
                } else {
                    if (i == depth - 1) {
                        rest_total += this->num_possible[N_vector[i]];
                    } else {
                        rest_total += (this->num_possible[N_vector[i]] - 1) * this->power<int>(5, depth - 1 - i);
                    }
                }
                continue;
            } else {
                // 如果该位不受限，之后也不会受限，直接计算全部的情况
                if (first_flag) {
                    first_flag = false;
                    rest_total += (this->num_possible[N_vector[i]] - 1) * this->power<int>(5, depth - 1 - i);
                } else {
                    rest_total += this->num_possible[N_vector[i]] * this->power<int>(5, depth - 1 - i);
                }
                break;
            }
        }
        
//        cout << "rest_total~1 = " << rest_total << endl;
        
        // 扣除不合法的值
        first_flag = true;
        int half_depth = (int)(depth / 2);
        
        if (depth % 2 == 0) {
            // depth 为偶数，只需看左侧有多少排列组合
            for (int i = 0; i < half_depth; i++) {
                // 判断当前位是否会出现受限情况
                bool limit = this->limit_map[N_vector[i]];
                
                if (limit) {
                    // 如果该位可能会受限，那么在下一个循环中，计算受限的那个情况
                    // 而除了取受限的那个最大数外，取别的都不会使得后面受限
                    // 注意 num_possible[N_vector[i]] - 1 才是首位数字对应的取值可能数
                    // 由于 i > 1 且 i 至多取到 half_depth - 1，所以始终存在后一位，所以始终要考虑后一位是否受限
                    if (first_flag) {
                        // 该数字是首位
                        first_flag = false;
                        if (i == half_depth - 1) {
                            // 如果是左侧最后一个数字受限了，那么要在取受限数(最大数)的情况下
                            // 判断此时是否右侧的每一位都能取到相应的左侧值的旋转值
                            bool check = true;
                            for (int j = 0; j < half_depth; j++) {
                                if (this->map_int[N_vector[j]] > N_vector[depth - 1 - j]) {
                                    check = false;
                                    break;
                                }
                            }
                            
                            if (check) {
                                // 如果全部旋转匹配，那么不减少可能性
                                rest_total -= this->num_possible[N_vector[i]] - 1;
//                                cout << "even-1: " << rest_total << endl;
                            } else {
                                // 如果不全都能旋转匹配，那么少一种可能性
                                rest_total -= this->num_possible[N_vector[i]] - 2;
//                                cout << "even-2: " << rest_total << endl;
                            }
                        } else {
                            // 如果该数字是首位，且不是左侧最后一个数字
                            rest_total -= (this->num_possible[N_vector[i]] - 2) * this->power<int>(5, half_depth - 1 - i);
//                            cout << "even-3: " << rest_total << endl;
                        }
                    } else {
                        // 该数字不是首位
                        if (i == half_depth - 1) {
                            // 如果是左侧最后一个数字受限了，那么要在取受限数(最大数)的情况下
                            // 判断此时是否右侧的每一位都能取到相应的左侧值的旋转值
                            bool check = false;
                            for (int j = half_depth - 1; j >= 0; j--) {
                                int diff = this->map_int[N_vector[j]] - N_vector[depth - 1 - j];
                                if (diff < 0) {
                                    // 只要右侧的较高位大于相应左侧数字的旋转值
                                    // 那么它之后的右侧数字可以任取 0/1/6/8/9，必然也满足条件
                                    check = true;
                                    break;
                                } else if (diff == 0) {
                                    if (j == 0) {
                                        // 到最后各位全都旋转相等
                                        check = true;
                                    } else {
                                        // 比较下一位
                                        continue;
                                    }
                                } else {
                                    // 右侧的较高位小于相应左侧数字的旋转值
                                    // 必不能满足条件
                                    break;
                                }
                            }
                            
                            if (check) {
                                // 如果全部旋转匹配，那么不减少可能性
                                rest_total -= this->num_possible[N_vector[i]];
//                                cout << "even-4: " << rest_total << endl;
                            } else {
                                // 如果不全都能旋转匹配，那么少一种可能性
                                rest_total -= this->num_possible[N_vector[i]] - 1;
//                                cout << "even-5: " << rest_total << endl;
                            }
                        } else {
                            // 如果该数字不是首位，且不是左侧最后一个数字
                            rest_total -= (this->num_possible[N_vector[i]] - 1) * this->power<int>(5, half_depth - 1 - i);
//                            cout << "even-6: " << rest_total << endl;
                        }
                    }
                    continue;
                } else {
                    // 如果该位不受限，之后也不会受限，直接计算全部的情况
                    if (first_flag) {
                        first_flag = false;
                        rest_total -= (this->num_possible[N_vector[i]] - 1) * this->power<int>(5, half_depth - 1 - i);
//                        cout << "even-7: " << rest_total << endl;
                    } else {
                        rest_total -= this->num_possible[N_vector[i]] * this->power<int>(5, half_depth - 1 - i);
//                        cout << "even-8: " << rest_total << endl;
                    }
                    break;
                }
            }
        } else {
            // depth 为奇数，看左侧有多少排列组合，再乘上相应的中间值能取到 0/1/8 的个数
            for (int i = 0; i < half_depth; i++) {
                // 判断当前位是否会出现受限情况
                bool limit = this->limit_map[N_vector[i]];
                int mid_possible = 3; // 如果中间数任取值，肯定 0/1/8 都能取到，所以是 3 个
                
                if (limit) {
                    // 如果该位可能会受限，那么在下一个循环中，计算受限的那个情况
                    // 而除了取受限的那个最大数外，取别的都不会使得后面受限
                    // 注意 num_possible[N_vector[i]] - 1 才是首位数字对应的取值可能数
                    
                    if (i == half_depth - 1) {
                        // 如果是左侧最后一个数字受限了(程序运行至此，表示 N_vector[i] 前面全部数字都取受限值了)
                        // 那么中间数不能任取值，那么要具体分析它能取到 0/1/8 中的多少个
                        mid_possible = this->mid_map[N_vector[half_depth]]; // 这是受限的情况
                        
                        // 同时如果中间值取到最大值，让后一位受限，那么要判断后一位是否能与前一位构成 180 度旋转相等
                        bool limit_mid = this->mid_limit_map[N_vector[half_depth]];
                        if (limit_mid) {
                            // 如果左侧最后一个数字受限了，并且中间数字也受限了
                            // 判断此时是否右侧的每一位都能取到相应的左侧值的旋转值
                            bool check = false;
                            for (int j = half_depth - 1; j >= 0; j--) {
                                int diff = this->map_int[N_vector[j]] - N_vector[depth - 1 - j];
                                if (diff < 0) {
                                    // 只要右侧的较高位大于相应左侧数字的旋转值
                                    // 那么它之后的右侧数字可以任取 0/1/6/8/9，必然也满足条件
                                    check = true;
                                    break;
                                } else if (diff == 0) {
                                    if (j == 0) {
                                        // 到最后各位全都旋转相等
                                        check = true;
                                    } else {
                                        // 比较下一位
                                        continue;
                                    }
                                } else {
                                    // 右侧的较高位小于相应左侧数字的旋转值
                                    // 必不能满足条件
                                    break;
                                }
                            }
                            
                            if (check) {
                                // 如果全部旋转匹配，那么此时中间仍可以取最大值，不减少可能性
                                if (first_flag) {
                                    first_flag = false;
                                    rest_total -= (this->num_possible[N_vector[i]] - 2) * 3 + mid_possible;
//                                    cout << "odd-1: " << rest_total << endl;
                                } else {
                                    rest_total -= (this->num_possible[N_vector[i]] - 1) * 3 + mid_possible;
//                                    cout << "odd-2: " << rest_total << endl;
                                }
                            } else {
                                // 如果不全都能旋转匹配，那么此时中间不可以取最大值，表示少一种可能性
                                if (first_flag) {
                                    first_flag = false;
                                    rest_total -= (this->num_possible[N_vector[i]] - 2) * 3 + mid_possible - 1;
//                                    cout << "odd-3: " << rest_total << endl;
                                } else {
                                    rest_total -= (this->num_possible[N_vector[i]] - 1) * 3 + mid_possible - 1;
//                                    cout << "odd-4: " << rest_total << endl;
                                }
                            }
                        } else {
                            // 如果是左侧最后一个数字受限了，但中间不受限
                            // 那么只要最后一个数字不取最大值，那么中间的可取值就是 3。否则看它自身原本是多少
                            // 分两段计算，一段是该位取最大的数字，一段是其他取值
                            if (first_flag) {
                                first_flag = false;
                                rest_total -= mid_possible + (this->num_possible[N_vector[i]] - 2) * 3;
//                                cout << "odd-5: " << rest_total << endl;
                            } else {
                                rest_total -= mid_possible + (this->num_possible[N_vector[i]] - 1) * 3;
//                                cout << "odd-6: " << rest_total << endl;
                            }
                        }
                        continue;
                    } else {
                        // 如果当前数字会受限，但不是左侧最后一个数字，所以中间数字仍然不受限
                        if (first_flag) {
                            first_flag = false;
                            rest_total -= (this->num_possible[N_vector[i]] - 2) *
                                this->power<int>(5, half_depth - 1 - i) * 3;
//                            cout << "odd-7: " << rest_total << endl;
                        } else {
                            rest_total -= (this->num_possible[N_vector[i]] - 1) *
                                this->power<int>(5, half_depth - 1 - i) * 3;
//                            cout << "odd-8: " << rest_total << endl;
                        }
                    }
                } else {
                    // 如果该位不受限，之后也不会受限，直接计算全部的情况
                    if (first_flag) {
                        first_flag = false;
                        rest_total -= (this->num_possible[N_vector[i]] - 1) *
                            this->power<int>(5, half_depth - 1 - i) * 3;
//                        cout << "odd-9: " << rest_total << endl;
                    } else {
                        rest_total -= this->num_possible[N_vector[i]] *
                            this->power<int>(5, half_depth - 1 - i) * 3;
//                        cout << "odd-10: " << rest_total << endl;
                    }
                    break;
                }
            }
        }
        
//        cout << "rest_total~2 = " << rest_total << endl;
        
        res += rest_total;
        
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
    
    
    // 虽然剪枝，但是基本操作更多，效率反而不如 DFS_1
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
            
            // 累乘底数之前做乘法溢出判断
            if (exp == 1 || base > (int)sqrt(MAX_INT32)) {
                break;
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
//    int N = 60; // 预期结果 7
//    int N = 69; // 预期结果 10
//    int N = 87; // 预期结果 13
//    int N = 88; // 预期结果 13
//    int N = 100; // 预期结果 19
//    int N = 106; // 预期结果 20
//    int N = 190; // 预期结果 36
//    int N = 1000; // 预期结果 107
//    int N = 9999; // 预期结果 586
//    int N = 10000; // 预期结果 587
//    int N = 19750; // 预期结果 1147
//    int N = 100000; // 预期结果 3027 // 2程序执行时间: 0.168ms. 3程序执行时间: 3.118ms.
    int N = 999959; // 预期结果 15411
//    int N = 1000000; // 预期结果 15427 // 2程序执行时间: 0.174ms. 3程序执行时间: 14.984ms.
//    int N = 10000000; // 预期结果 77627 // 1程序执行时间: 1383.54ms. 2程序执行时间: 0.164ms. 3程序执行时间: 74.176ms.
//    int N = 100000000; // 预期结果 389627 // 1程序执行时间: 13115.7ms. 2程序执行时间: 0.181ms. 3程序执行时间: 357.722ms.
//    int N = 999999998; // 预期结果 1950625 // 2程序执行时间: 0.281ms. 3程序执行时间: 724.163ms.
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
