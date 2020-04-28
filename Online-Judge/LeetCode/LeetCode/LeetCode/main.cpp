//
//  main.cpp
//  LeetCode
//
//  Created by 阴昱为 on 2019/5/27.
//  Copyright © 2019 阴昱为. All rights reserved.
//

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
    vector<int> method(vector<int>& testData) {
        vector<int> result{};
        
        // TODO coding...
        result = testData;
        
        return result;
    }
};


int main(int argc, const char * argv[]) {
    // 设置测试数据
    vector<int> testData{1, 2, 3};
    
    // 调用解决方案，获得处理结果
    Solution *solution = new Solution();
    vector<int> result = solution->method(testData);
    
    // 输出展示结果
    for (vector<int>::iterator ite = result.begin(); ite != result.end(); ite++) {
        cout << *ite << endl;
    }
    
    return 0;
}
