//
//  main.cpp
//  Prob1599_Minimum_Index_Sum_of_Two_Lists
//
//  Created by 阴昱为 on 2019/6/22.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1599. Minimum Index Sum of Two Lists
//
//Suppose Andy and Doris want to choose a restaurant for dinner, and they both have a list of favorite restaurants represented by strings.
//You need to help them find out their common interest with the least list index sum. If there is a choice tie between answers, output all of them with no order requirement. You could assume there always exists an answer.
//
//假设Andy和Doris想在晚餐时选择一家餐厅，并且他们都有一个表示最喜爱餐厅的列表，每个餐厅的名字用字符串表示。
//你需要帮助他们用最少的索引和找出他们共同喜爱的餐厅。 如果答案不止一个，则输出所有答案并且不考虑顺序。 你可以假设总是存在一个答案。
//
//Example 1:
//    Input:
//    ["Shogun", "Tapioca Express", "Burger King", "KFC"]
//    ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"]
//    Output: ["Shogun"]
//    Explanation: The only restaurant they both like is "Shogun".
//Example 2:
//    Input:
//    ["Shogun", "Tapioca Express", "Burger King", "KFC"]
//    ["KFC", "Shogun", "Burger King"]
//    Output: ["Shogun"]
//    Explanation: The restaurant they both like and have the least index sum is "Shogun" with index sum 1 (0+1).
//Note:
//    The length of both lists will be in the range of [1, 1000].
//    The length of strings in both lists will be in the range of [1, 30].
//    The index is starting from 0 to the list length minus 1.
//    No duplicates in both lists.
//提示:
//    两个列表的长度范围都在 [1, 1000]内。
//    两个列表中的字符串的长度将在[1，30]的范围内。
//    下标从0开始，到列表的长度减1。
//    两个列表都没有重复的元素。


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
public:
    vector<string> findRestaurant(vector<string>& list1, vector<string>& list2) {
        return this->solution1(list1, list2);
    }
    
private:
    // 方法一。哈希法。
    // 时间复杂度 O(N)，空间复杂度 O(N)
    vector<string> solution1(vector<string>& list1, vector<string>& list2) {
        if (list1.empty() || list2.empty()) {
            return {};
        }
        
        vector<string> res = {};
        
        int min_index_sum = MAX_INT32;
        map<string, pair<bool, int>> dict = {}; // 记录某餐厅是否被共同喜爱、下标和
        
        // 前提：两个列表各自都没有重复元素，否则要先去重
        for (int i = 0; i < (int)list1.size(); i++) {
            dict.insert({list1[i], {false, i}});
        }
        
        for (int i = 0; i < (int)list2.size(); i++) {
            if (dict.find(list2[i]) != dict.end()) {
                get<0>(dict[list2[i]]) = true;
                get<1>(dict[list2[i]]) += i;
                if (get<1>(dict[list2[i]]) < min_index_sum) {
                    min_index_sum = get<1>(dict[list2[i]]);
                }
            }
        }
        
        // 取出所有下标和极小的共同餐厅
        for (auto ite = dict.begin(); ite != dict.end(); ite++) {
            if (get<0>(ite->second) && get<1>(ite->second) == min_index_sum) {
                res.emplace_back(ite->first);
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
    // 预期结果 ["Shogun"]
    vector<string> list1 = {"Shogun", "Tapioca Express", "Burger King", "KFC"};
    vector<string> list2 = {"KFC", "Shogun", "Burger King"};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    vector<string> ans = solution->findRestaurant(list1, list2);
    if (!ans.empty()) {
        for (int i = 0; i < (int)ans.size(); i++) {
            cout << ans[i] << ", ";
        }
        cout << "End." << endl;
    } else {
        cout << "Answer is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
