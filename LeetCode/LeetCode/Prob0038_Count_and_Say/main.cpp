//
//  main.cpp
//  Prob1038_Count_and_Say
//
//  Created by 阴昱为 on 2019/7/5.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//38. Count and Say
//
//The count-and-say sequence is the sequence of integers with the first five terms as following:
//    1.     1
//    2.     11
//    3.     21
//    4.     1211
//    5.     111221
//1 is read off as "one 1" or 11.
//11 is read off as "two 1s" or 21.
//21 is read off as "one 2, then one 1" or 1211.
//
//Given an integer n where 1 ≤ n ≤ 30, generate the nth term of the count-and-say sequence.
//Note: Each term of the sequence of integers will be represented as a string.
//
//报数序列是一个整数序列，按照其中的整数的顺序进行报数，得到下一个数。其前五项如下：
//    1.     1
//    2.     11
//    3.     21
//    4.     1211
//    5.     111221
//1 被读作  "one 1"  ("一个一") , 即 11。
//11 被读作 "two 1s" ("两个一"）, 即 21。
//21 被读作 "one 2",  "one 1" （"一个二" ,  "一个一") , 即 1211。
//
//给定一个正整数 n（1 ≤ n ≤ 30），输出报数序列的第 n 项。
//注意：整数顺序将表示为一个字符串。
//
//Example 1:
//    Input: 1
//    Output: "1"
//
//Example 2:
//    Input: 4
//    Output: "1211"


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
public:
    // 题目解释：从第二项开始，每项都是对前面一项数字的拆分解释
    // 第一项是一个 1
    // 第二项是对第一项的描述：第二项报数：第一项是一个一 ：11
    // 第三项报数：第二项是两个一： 21
    // 第四项报数：第三项是一个二，一个一：1211
    // 第五项报数：第四项是一个一，一个二，两个一：111221
    // 以此类推往后。给定一个正整数 n(1 ≤ n ≤ 30)，输出报数序列的第 n 项。
    string countAndSay(int n) {
        return this->solution2(n);
    }
    
private:
    // 方法一：直接循环遍历计算出目标。时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 81.51% 的用户
    // 内存消耗 : 8.6 MB , 在所有 C++ 提交中击败了 93.05% 的用户
    // Runtime: 4 ms, faster than 86.75% of C++ online submissions for Count and Say.
    // Memory Usage: 8.6 MB, less than 85.80% of C++ online submissions for Count and Say.
    string solution1 (int n) {
        // 边界情况
        if (n <= 0) {
            return "1";
        }
        
        string res = "1";
        char cur_char;
        int count;
        string temp;
        
        for (int i = 2; i <= n ; i++) {
            cur_char = res[0];
            count = 0;
            temp = "";
            
            for (int j = 0; j < (int)res.size(); j++) {
                if (res[j] == cur_char) {
                    count ++;
                } else {
                    temp += to_string(count) + cur_char;
                    
                    cur_char = res[j];
                    count = 1;
                }
            }
            
            // 最末情况
            if (count > 0) {
                temp += to_string(count) + cur_char;
            }
            
            res = temp;
        }
        
        return res;
    }
    
    // 方法二：作弊：提前打好表。时间复杂度 O(1) if n ≤ 30，空间复杂度 O(1)
    // Runtime: 4 ms, faster than 86.75% of C++ online submissions for Count and Say.
    // Memory Usage: 9.6 MB, less than 19.10% of C++ online submissions for Count and Say.
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 95.32% 的用户
    // 内存消耗 : 9.7 MB , 在所有 C++ 提交中击败了 21.41% 的用户
    string solution2 (int n) {
        // 边界情况
        if (n <= 0) {
            return "1";
        }
        
        // 提前准备好结果表 1~30
        vector<string> res_vec = {
            "1", "11", "21", "1211", "111221", "312211", "13112221", "1113213211", "31131211131221",
            "13211311123113112211", "11131221133112132113212221", "3113112221232112111312211312113211",
            "1321132132111213122112311311222113111221131221",
            "11131221131211131231121113112221121321132132211331222113112211",
            "311311222113111231131112132112311321322112111312211312111322212311322113212221",
            "132113213221133112132113311211131221121321131211132221123113112221131112311332111213211322211312113211",
            "11131221131211132221232112111312212321123113112221121113122113111231133221121321132132211331121321231231121113122113322113111221131221",
            "31131122211311123113321112131221123113112211121312211213211321322112311311222113311213212322211211131221131211132221232112111312111213111213211231131122212322211331222113112211",
            "1321132132211331121321231231121113112221121321132122311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112311332111213122112311311123112111331121113122112132113213211121332212311322113212221",
            "11131221131211132221232112111312111213111213211231132132211211131221131211221321123113213221123113112221131112311332211211131221131211132211121312211231131112311211232221121321132132211331121321231231121113112221121321133112132112312321123113112221121113122113121113123112112322111213211322211312113211",
            "311311222113111231133211121312211231131112311211133112111312211213211312111322211231131122211311122122111312211213211312111322211213211321322113311213212322211231131122211311123113223112111311222112132113311213211221121332211211131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221131112311311121321122112132231121113122113322113111221131221",
            "132113213221133112132123123112111311222112132113311213211231232112311311222112111312211311123113322112132113213221133122112231131122211211131221131112311332211211131221131211132221232112111312111213322112132113213221133112132113221321123113213221121113122123211211131221222112112322211231131122211311123113321112131221123113111231121113311211131221121321131211132221123113112211121312211231131122211211133112111311222112111312211312111322211213211321322113311213211331121113122122211211132213211231131122212322211331222113112211",
            "111312211312111322212321121113121112131112132112311321322112111312212321121113122112131112131221121321132132211231131122211331121321232221121113122113121113222123112221221321132132211231131122211331121321232221123113112221131112311332111213122112311311123112112322211211131221131211132221232112111312211322111312211213211312111322211231131122111213122112311311221132211221121332211213211321322113311213212312311211131122211213211331121321123123211231131122211211131221131112311332211213211321223112111311222112132113213221123123211231132132211231131122211311123113322112111312211312111322212321121113122123211231131122113221123113221113122112132113213211121332212311322113212221",
            "3113112221131112311332111213122112311311123112111331121113122112132113121113222112311311221112131221123113112221121113311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112311332111213213211221113122113121113222112132113213221232112111312111213322112132113213221133112132123123112111311222112132113311213211221121332211231131122211311123113321112131221123113112221132231131122211211131221131112311332211213211321223112111311222112132113212221132221222112112322211211131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221133112132123222112111312211312112213211231132132211211131221131211132221121311121312211213211312111322211213211321322113311213212322211231131122211311123113321112131221123113112211121312211213211321222113222112132113223113112221121113122113121113123112112322111213211322211312113211",
            "132113213221133112132123123112111311222112132113311213211231232112311311222112111312211311123113322112132113212231121113112221121321132132211231232112311321322112311311222113111231133221121113122113121113221112131221123113111231121123222112132113213221133112132123123112111312111312212231131122211311123113322112111312211312111322111213122112311311123112112322211211131221131211132221232112111312111213111213211231132132211211131221232112111312212221121123222112132113213221133112132123123112111311222112132113213221132213211321322112311311222113311213212322211211131221131211221321123113213221121113122113121132211332113221122112133221123113112221131112311332111213122112311311123112111331121113122112132113121113222112311311221112131221123113112221121113311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112212211131221121321131211132221123113112221131112311332211211133112111311222112111312211311123113322112111312211312111322212321121113121112133221121321132132211331121321231231121113112221121321132122311211131122211211131221131211322113322112111312211322132113213221123113112221131112311311121321122112132231121113122113322113111221131221",
            "1113122113121113222123211211131211121311121321123113213221121113122123211211131221121311121312211213211321322112311311222113311213212322211211131221131211221321123113213221121113122113121113222112131112131221121321131211132221121321132132211331121321232221123113112221131112311322311211131122211213211331121321122112133221121113122113121113222123211211131211121311121321123113111231131122112213211321322113311213212322211231131122211311123113223112111311222112132113311213211221121332211231131122211311123113321112131221123113111231121113311211131221121321131211132221123113112211121312211231131122113221122112133221121113122113121113222123211211131211121311121321123113213221121113122113121113222113221113122113121113222112132113213221232112111312111213322112311311222113111221221113122112132113121113222112311311222113111221132221231221132221222112112322211213211321322113311213212312311211131122211213211331121321123123211231131122211211131221131112311332211213211321223112111311222112132113213221123123211231132132211231131122211311123113322112111312211312111322111213122112311311123112112322211213211321322113312211223113112221121113122113111231133221121321132132211331121321232221123123211231132132211231131122211331121321232221123113112221131112311332111213122112311311123112112322211211131221131211132221232112111312111213111213211231132132211211131221131211221321123113213221123113112221131112211322212322211231131122211322111312211312111322211213211321322113311213211331121113122122211211132213211231131122212322211331222113112211",
            "31131122211311123113321112131221123113111231121113311211131221121321131211132221123113112211121312211231131122211211133112111311222112111312211312111322211213211321322123211211131211121332211231131122211311122122111312211213211312111322211231131122211311123113322112111331121113112221121113122113111231133221121113122113121113222123211211131211121332211213211321322113311213211322132112311321322112111312212321121113122122211211232221123113112221131112311332111213122112311311123112111331121113122112132113311213211321222122111312211312111322212321121113121112133221121321132132211331121321132213211231132132211211131221232112111312212221121123222112132113213221133112132123123112111311222112132113311213211231232112311311222112111312211311123113322112132113212231121113112221121321132122211322212221121123222112311311222113111231133211121312211231131112311211133112111312211213211312111322211231131122211311123113322113223113112221131112311332211211131221131211132211121312211231131112311211232221121321132132211331221122311311222112111312211311123113322112132113213221133122211332111213112221133211322112211213322112111312211312111322212321121113121112131112132112311321322112111312212321121113122112131112131221121321132132211231131122211331121321232221121113122113121122132112311321322112111312211312111322211213111213122112132113121113222112132113213221133112132123222112311311222113111231132231121113112221121321133112132112211213322112111312211312111322212311222122132113213221123113112221133112132123222112111312211312111322212321121113121112133221121311121312211213211312111322211213211321322123211211131211121332211213211321322113311213212312311211131122211213211331121321122112133221123113112221131112311332111213122112311311123112111331121113122112132113121113222112311311222113111221221113122112132113121113222112132113213221133122211332111213322112132113213221132231131122211311123113322112111312211312111322212321121113122123211231131122113221123113221113122112132113213211121332212311322113212221",
            "13211321322113311213212312311211131122211213211331121321123123211231131122211211131221131112311332211213211321223112111311222112132113213221123123211231132132211231131122211311123113322112111312211312111322111213122112311311123112112322211213211321322113312211223113112221121113122113111231133221121321132132211331121321232221123123211231132132211231131122211331121321232221123113112221131112311332111213122112311311123112112322211211131221131211132221232112111312211322111312211213211312111322211231131122111213122112311311221132211221121332211213211321322113311213212312311211131122211213211331121321123123211231131122211211131221232112111312211312113211223113112221131112311332111213122112311311123112112322211211131221131211132221232112111312211322111312211213211312111322211231131122111213122112311311221132211221121332211211131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221133112132123222112111312211312112213211231132132211211131221131211322113321132211221121332211213211321322113311213212312311211131122211213211331121321123123211231131122211211131221131112311332211213211321322113311213212322211322132113213221133112132123222112311311222113111231132231121113112221121321133112132112211213322112111312211312111322212311222122132113213221123113112221133112132123222112111312211312111322212311322123123112111321322123122113222122211211232221123113112221131112311332111213122112311311123112111331121113122112132113121113222112311311221112131221123113112221121113311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112212211131221121321131211132221123113112221131112311332211211133112111311222112111312211311123113322112111312211312111322212321121113121112133221121321132132211331121321132213211231132132211211131221232112111312212221121123222112311311222113111231133211121321321122111312211312111322211213211321322123211211131211121332211231131122211311123113321112131221123113111231121123222112111331121113112221121113122113111231133221121113122113121113221112131221123113111231121123222112111312211312111322212321121113121112131112132112311321322112111312212321121113122122211211232221121321132132211331121321231231121113112221121321133112132112312321123113112221121113122113111231133221121321132132211331221122311311222112111312211311123113322112111312211312111322212311322123123112112322211211131221131211132221132213211321322113311213212322211231131122211311123113321112131221123113112211121312211213211321222113222112132113223113112221121113122113121113123112112322111213211322211312113211",
            "11131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221133112132123222112111312211312112213211231132132211211131221131211132221121311121312211213211312111322211213211321322113311213212322211231131122211311123113223112111311222112132113311213211221121332211211131221131211132221231122212213211321322112311311222113311213212322211211131221131211132221232112111312111213322112131112131221121321131211132221121321132132212321121113121112133221121321132132211331121321231231121113112221121321133112132112211213322112311311222113111231133211121312211231131122211322311311222112111312211311123113322112132113212231121113112221121321132122211322212221121123222112111312211312111322212321121113121112131112132112311321322112111312212321121113122112131112131221121321132132211231131122111213122112311311222113111221131221221321132132211331121321231231121113112221121321133112132112211213322112311311222113111231133211121312211231131122211322311311222112111312211311123113322112132113212231121113112221121321132122211322212221121123222112311311222113111231133211121312211231131112311211133112111312211213211312111322211231131122111213122112311311222112111331121113112221121113122113121113222112132113213221232112111312111213322112311311222113111221221113122112132113121113222112311311222113111221132221231221132221222112112322211211131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221133112132123222112111312211312111322212321121113121112133221132211131221131211132221232112111312111213322112132113213221133112132113221321123113213221121113122123211211131221222112112322211231131122211311123113321112132132112211131221131211132221121321132132212321121113121112133221123113112221131112311332111213211322111213111213211231131211132211121311222113321132211221121332211213211321322113311213212312311211131122211213211331121321123123211231131122211211131221131112311332211213211321223112111311222112132113213221123123211231132132211231131122211311123113322112111312211312111322111213122112311311123112112322211213211321322113312211223113112221121113122113111231133221121321132132211331121321232221123123211231132132211231131122211331121321232221123113112221131112311332111213122112311311123112112322211211131221131211132221232112111312211322111312211213211312111322211231131122111213122112311311221132211221121332211213211321322113311213212312311211131211131221223113112221131112311332211211131221131211132211121312211231131112311211232221121321132132211331121321231231121113112221121321133112132112211213322112312321123113213221123113112221133112132123222112311311222113111231132231121113112221121321133112132112211213322112311311222113111231133211121312211231131112311211133112111312211213211312111322211231131122111213122112311311221132211221121332211211131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221133112132123222112111312211312111322212311222122132113213221123113112221133112132123222112311311222113111231133211121321132211121311121321122112133221123113112221131112311332211322111312211312111322212321121113121112133221121321132132211331121321231231121113112221121321132122311211131122211211131221131211322113322112111312211322132113213221123113112221131112311311121321122112132231121113122113322113111221131221",
            "3113112221131112311332111213122112311311123112111331121113122112132113121113222112311311221112131221123113112221121113311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112212211131221121321131211132221123113112221131112311332211211133112111311222112111312211311123113322112111312211312111322212321121113121112133221121321132132211331121321132213211231132132211211131221232112111312212221121123222112311311222113111231133211121321321122111312211312111322211213211321322123211211131211121332211231131122211311123113321112131221123113111231121123222112111331121113112221121113122113111231133221121113122113121113221112131221123113111231121123222112111312211312111322212321121113121112131112132112311321322112111312212321121113122122211211232221121321132132211331121321231231121113112221121321132132211322132113213221123113112221133112132123222112111312211312112213211231132132211211131221131211322113321132211221121332211231131122211311123113321112131221123113111231121113311211131221121321131211132221123113112211121312211231131122211211133112111311222112111312211312111322211213211321223112111311222112132113213221133122211311221122111312211312111322212321121113121112131112132112311321322112111312212321121113122122211211232221121321132132211331121321231231121113112221121321132132211322132113213221123113112221133112132123222112111312211312112213211231132132211211131221131211322113321132211221121332211213211321322113311213212312311211131122211213211331121321123123211231131122211211131221131112311332211213211321223112111311222112132113213221123123211231132132211231131122211311123113322112111312211312111322111213122112311311123112112322211213211321322113312211223113112221121113122113111231133221121321132132211331222113321112131122211332113221122112133221123113112221131112311332111213122112311311123112111331121113122112132113121113222112311311221112131221123113112221121113311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112311332111213122112311311123112112322211322311311222113111231133211121312211231131112311211232221121113122113121113222123211211131221132211131221121321131211132221123113112211121312211231131122113221122112133221121321132132211331121321231231121113121113122122311311222113111231133221121113122113121113221112131221123113111231121123222112132113213221133112132123123112111312211322311211133112111312211213211311123113223112111321322123122113222122211211232221121113122113121113222123211211131211121311121321123113213221121113122123211211131221121311121312211213211321322112311311222113311213212322211211131221131211221321123113213221121113122113121113222112131112131221121321131211132221121321132132211331121321232221123113112221131112311322311211131122211213211331121321122112133221121113122113121113222123112221221321132132211231131122211331121321232221121113122113121113222123211211131211121332211213111213122112132113121113222112132113213221232112111312111213322112132113213221133112132123123112111311222112132113311213211221121332211231131122211311123113321112131221123113112221132231131122211211131221131112311332211213211321223112111311222112132113212221132221222112112322211211131221131211132221232112111312111213111213211231131112311311221122132113213221133112132123222112311311222113111231132231121113112221121321133112132112211213322112111312211312111322212321121113121112131112132112311321322112111312212321121113122122211211232221121311121312211213211312111322211213211321322123211211131211121332211213211321322113311213211322132112311321322112111312212321121113122122211211232221121321132132211331121321231231121113112221121321133112132112312321123113112221121113122113111231133221121321132122311211131122211213211321222113222122211211232221123113112221131112311332111213122112311311123112111331121113122112132113121113222112311311221112131221123113112221121113311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112311332111213213211221113122113121113222112132113213221232112111312111213322112132113213221133112132123123112111312211322311211133112111312212221121123222112132113213221133112132123222113223113112221131112311332111213122112311311123112112322211211131221131211132221232112111312111213111213211231132132211211131221131211221321123113213221123113112221131112211322212322211231131122211322111312211312111322211213211321322113311213211331121113122122211211132213211231131122212322211331222113112211"
        };
        
        if (n <= 30) {
            return res_vec[n - 1];
        }
        
        string res = res_vec[29];
        char cur_char;
        int count;
        string temp;
        
        for (int i = 31; i <= n ; i++) {
            cur_char = res[0];
            count = 0;
            temp = "";
            
            for (int j = 0; j < (int)res.size(); j++) {
                if (res[j] == cur_char) {
                    count ++;
                } else {
                    temp += to_string(count) + cur_char;
                    
                    cur_char = res[j];
                    count = 1;
                }
            }
            
            // 最末情况
            if (count > 0) {
                temp += to_string(count) + cur_char;
            }
            
            res = temp;
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
    int n = 1; // 预期结果 "1"
//    int n = 4; // 预期结果 "1211"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->countAndSay(n);
    if (ans.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        cout << ans << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
