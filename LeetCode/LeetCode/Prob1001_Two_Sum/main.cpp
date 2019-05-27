//
//  main.cpp
//  Prob1001_Two_Sum
//
//  Created by 阴昱为 on 2019/5/27.
//  Copyright © 2019 阴昱为. All rights reserved.
//

// 设置系统栈深度
#pragma comment(linker, "/STACK:1024000000,1024000000")

// 引入头文件
#include<iostream>
#include<cstdio>
#include<cstring>
#include<cmath>

#include<math.h>
#include<time.h>

#include<algorithm>
#include<string>
#include<vector>
#include<list>
#include<stack>
#include<queue>
#include<map>
#include<set>
#include<bitset>

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


class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result{};
        map<int, int> hashmap;
        
        for (int i = 0; i < nums.size(); i++) {
            // 计算当前元素值与目标值的差值
            int diff = target - nums[i];
            
            // 如果哈希表中已有该差值对应的元素坐标，则返回之
            if (hashmap.find(diff) != hashmap.end()) {
                return vector<int> {hashmap[diff], i};
            }
            
            // 否则将键值对(当前元素值, 当前元素坐标)存储进哈希表
            hashmap[nums[i]] = i;
        }
        
        return result;
    }
};


int main(int argc, const char * argv[]) {
    // 设置测试数据
    vector<int> nums{2, 7, 11, 15};
    int target = 9;
    
    // 调用解决方案，获得处理结果
    Solution *solution = new Solution();
    vector<int> result = solution->twoSum(nums, target);
    
    // 输出展示结果
    for (vector<int>::iterator ite = result.begin(); ite != result.end(); ite++) {
        cout << *ite << endl;
    }
    
    return 0;
}
