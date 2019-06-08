//
//  main.cpp
//  Basis
//
//  Created by 阴昱为 on 2019/5/28.
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

#include <unordered_set>
#include <unordered_map>

// 使用 std 标准命名空间
using namespace std;

// 类型命名
typedef long long ll;
//typedef __int64_t ll;
//#define ll __int64_t
//#define ll long long

// 全局常量
//#define PI acos(-1.0)
const double PI = acos(-1.0);
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;
const ll MOD = 1e9+7;

/*
 模数 MOD 一般选择 1e+7 的主要原因：
 1）减少冲突。
    首先，1e9+7是一个大的数，int32位的最大值为2147483647，所以对于int32位来说1000000007足够大。
    int64位的最大值为2^63-1，对于1000000007来说它的平方不会在int64中溢出所以在大数相乘的时候，
    因为(a∗b)%c=((a%c)∗(b%c))%c，所以相乘时两边都对1000000007取模，再保存在int64里面不会溢出 ｡◕‿◕｡

    其次，1e9+7是一个素数，在模素数p的情况下a*n（a非p的倍数）的循环节长为p,这是减少冲突的一个原因。
    另一方面模素数p的环是无零因子环,也就是说两个非p倍数的数相乘再模p不会是零（如果是0的话,在多个数连乘的情况下会大大增加冲突概率）。
    比如说如果所有的结果都是偶数…你模6就只可能出现0, 2, 4这三种情况…但模5还是可以出现2, 4, 1, 3这四(4=5-1)种情况的…
    hash表如果是用取模的方法也要模一个大素数来减少冲突，出题人也会这样来 希望减少你“蒙对“的概率。

 2）模1e9+7相加不爆int，相乘不爆long long。
 
 3）允许“除法”操作（乘以乘法逆元）
    就是模素数所成的环还是个域，因而允许“除法”操作（乘以乘法逆元）,模非素数就没有这个性质。
    一般来说x的选取只要10^x＋7保证比初始输入数据的范围大就可以了。
    比如有些数据范围小的题为了避免用long long而把模数设定为10007。
    至于为什么要用10^x＋7,大概是因为这种patten多为素数而又比较好记吧。
 
 4）出题人的本意不在高精度
    首先有很多题目的答案是很大的，然而出题人的本意也不是让选手写高精度或者Java，所以势必要让答案落在整型的范围内。
    那么怎么做到这一点呢，对一个很大的素数取模即可(自行思考为什么不是小数)。
    那么如果您学过哈希表的设计的话，应该知道对素数取模的话，能尽可能地避免模数相同的数之间具备公因数，来达到减少冲突的目的。
    那么有个很大的且好记的素数1e9+7(包括它的孪生素数1e9+9)。
 */


#include <iostream>

int main(int argc, const char * argv[]) {
    return 0;
}
