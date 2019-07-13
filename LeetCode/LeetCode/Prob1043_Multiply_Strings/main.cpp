//
//  main.cpp
//  Prob1043_Multiply_Strings
//
//  Created by 阴昱为 on 2019/7/12.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//43. Multiply Strings
//
//Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2, also represented as a string.
//
//给定两个以字符串形式表示的非负整数 num1 和 num2，返回 num1 和 num2 的乘积，它们的乘积也表示为字符串形式。
//
//Example 1:
//    Input: num1 = "2", num2 = "3"
//    Output: "6"
//
//Example 2:
//    Input: num1 = "123", num2 = "456"
//    Output: "56088"
//
//Note:
//    The length of both num1 and num2 is < 110.
//    Both num1 and num2 contain only digits 0-9.
//    Both num1 and num2 do not contain any leading zero, except the number 0 itself.
//    You must not use any built-in BigInteger library or convert the inputs to integer directly.
//
//说明：
//    num1 和 num2 的长度小于110。
//    num1 和 num2 只包含数字 0-9。
//    num1 和 num2 均不以零开头，除非是数字 0 本身。
//    不能使用任何标准库的大数类型（比如 BigInteger）或直接将输入转换为整数来处理。


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
//const int MOD = 1000000007; // 1e9+7 与 1e9+9 为孪生素数

//const int MAX_INT32 = 0x7fffffff;
//const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;
//const double SQRT_MAX_INT32 = sqrt(MAX_INT32);


class Solution {
public:
    // 快速数论变换 NTT (Number Theoretic Transform)
    // 和 FFT 一样，NTT 也用来加速多项式乘法，NTT 最大的优点是可以取模
    // 原根为 3 的常用模数有 469762049, 998244353, 1004535809
    // 998244353 = ((7 * 17) << 23) + 1
    // 二进制表示为 111011100000000000000000000001
    // 是两个数的平方和 998244353 = 3943^2 + 31348^2
    // 是勾股数之一 998244353^2 = 247210328^2 + 967149855^2
    static const int MOD = 998244353;
    
    string multiply(string num1, string num2) {
        return this->solution2(num1, num2);
    }
    
private:
    // 方法一：模拟乘法。时间复杂度 O(MN), 空间复杂度 O(M+N), N=num1.size M=num2.size
    // 执行用时 : 24 ms , 在所有 C++ 提交中击败了 27.76% 的用户
    // 内存消耗 : 10.8 MB , 在所有 C++ 提交中击败了 31.96% 的用户
    // Runtime: 16 ms, faster than 28.97% of C++ online submissions for Multiply Strings.
    // Memory Usage: 10.8 MB, less than 24.01% of C++ online submissions for Multiply Strings.
    string solution1 (string num1, string num2) {
        // 边界条件
        if (num1.empty() || num2.empty()) {
            return "0";
        }
        
        // 已知条件：num1 和 num2 只包含数字 0-9，且均不以零开头（除非是数字 0 本身）
        if (num1 == "0" || num2 == "0") {
            return "0";
        }
        
        // 已知条件：num1 和 num2 是非负整数
        if (num1 == "1") {
            return num2;
        }
        
        if (num2 == "1") {
            return num1;
        }
        
        
        if (num1.size() < num2.size()) {
            // 让长串为 num1，短串为 num2
            this->swapString(num1, num2);
        } else if (num1.size() == num2.size() && num1 < num2) {
            // 让较大串为 num1，较小串为 num2
            this->swapString(num1, num2);
        }
        
        // 反转两串，让低位在前
        reverse(num1.begin(), num1.end());
        reverse(num2.begin(), num2.end());
        
        string res = "0";
        string cur_mul = "1";
        string base = "";
        
        // 模拟竖式相乘相加
        for (int i = 0; i < num2.size(); i++) {
            cur_mul = this->multiplyTwoStringNumber(num1, (int)(num2[i]) - 48);
            cur_mul = base + cur_mul;
            
            this->addTwoStringNumber(res, cur_mul);
            
            base += "0";
        }
        
        // 反转结果串，让高位在前
        reverse(res.begin(), res.end());
        
        return res;
    }
    
    // 串和某个一位数相乘
    string multiplyTwoStringNumber (string& num1, int num2) {
        string res = "";
        
        int cur_mul = 0;
        int carry = 0;
        
        for (int i = 0; i < num1.size(); i++) {
            // 保证 res 的位数够多
            if (i >= res.size()) {
                res.append("0");
            }
            
            cur_mul = ((int)num1[i] - 48) * num2 + carry;
            
            if (cur_mul >= 10) {
                carry = cur_mul / 10;
                cur_mul %= 10;
            } else {
                carry = 0;
            }
            
            res[i] = (char)(cur_mul + 48);
        }
        
        // 末尾还有进位的情况
        if (carry > 0) {
            res += to_string(carry);
        }
        
        return res;
    }
    
    // 两串相加
    void addTwoStringNumber (string& res, string& addition) {
        int cur_sum = 0;
        int carry = 0;
        
        for (int i = 0; i < addition.size(); i++) {
            // 保证 res 的位数够多
            if (i >= res.size()) {
                res.append("0");
            }
            
            cur_sum = (int)res[i] - 48 + (int)addition[i] - 48 + carry;
            
            if (cur_sum >= 10) {
                carry = 1;
                cur_sum -= 10;
            } else {
                carry = 0;
            }
            
            res[i] = (char)(cur_sum + 48);
        }
        
        // 末尾还有进位的情况
        if (carry == 1) {
            res += "1";
        }
    }
    
    // 交换两个串
    void swapString (string& num1, string& num2) {
        string temp = num1;
        num1 = num2;
        num2 = temp;
    }
    
    // 方法二：模拟乘法，用 NTT 加速乘法。时间复杂度 O(N lg N), 空间复杂度 O(M+N), N=num1.size M=num2.size
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 94.30% 的用户
    // 内存消耗 : 9 MB , 在所有 C++ 提交中击败了 84.14% 的用户
    // Runtime: 4 ms, faster than 96.40% of C++ online submissions for Multiply Strings.
    // Memory Usage: 9.3 MB, less than 33.92% of C++ online submissions for Multiply Strings.
    string solution2 (string num1, string num2) {
        vector<int> A, B;
        
        // 反转 num1
        reverse(num1.begin(), num1.end());
        // 用向量存储各位数字
        A.resize(num1.size());
        for (size_t i = 0; i < A.size(); i++) {
            A[i] = num1[i] - '0';
        }
        
        // 反转 num2
        reverse(num2.begin(), num2.end());
        // 用向量存储各位数字
        B.resize(num2.size());
        for (size_t i = 0; i < B.size(); i++) {
            B[i] = num2[i] - '0';
        }
        
        // 向量数字相乘，结果在 A 中
        this->polyMultiply(A, B);
        
        // 把向量 A 转为字符串
        string str = "";
        int cur_num = 0;
        int carry = 0;
        for (size_t i = 0; i < A.size(); i++) {
            cur_num = A[i] % 10;
            carry = A[i] / 10;
            
            str += cur_num + '0';
            
            if (carry > 0 && i + 1 >= A.size()) {
                // 如果 A 长度不够，则末尾补进位值
                A.push_back(carry);
            } else if (carry > 0) {
                // 否则直接修改该位的值
                A[i + 1] += carry;
            }
        }
        
        // 去掉字符串末尾的 '0' 字符
        while (*str.rbegin() == '0') {
            str.pop_back();
        }
        
        if (str == "") {
            return "0";
        }
        
        // 反转回来
        reverse(str.begin(), str.end());
        
        return str;
    }
    
    // 向量相乘
    void polyMultiply(vector<int>& A, vector<int>& B) {
        int len = (int)(A.size() + B.size() - 1);
        int n = 1;
        
        // n 增大到比 len 更大的 2 的某次幂
        while (n <= len) {
            n <<= 1;
        }
        
        // 修改 A 和 B 的向量大小
        A.resize(n);
        B.resize(n);
        
        // 对 A 和 B 分别做 FFT
        this->fastFourierTransform(A);
        this->fastFourierTransform(B);
        
        // A 和 B 各位对应相乘
        for (size_t i = 0; i < n; i++) {
            A[i] = 1LL * A[i] * B[i] % MOD;
        }
        
        // 对乘积结果做 FFT
        this->fastFourierTransform(A, -1);
        
        // 重置 A 的向量大小
        A.resize(len);
    }
    
    // FFT 优化求点值
    void fastFourierTransform(vector<int>& A, int d = 1) {
        static vector<int> rev;
        
        if (rev.size() != A.size()) {
            rev.resize(A.size());
            rev[0] = 0;
            
            for (size_t i = 1; i < A.size(); ++i) {
                rev[i] = (rev[i >> 1] >> 1) | ((i & 1) * ((int)A.size() >> 1));
            }
        }
        
        for (size_t i = 0; i < A.size(); ++i) {
            if (i < rev[i]) {
                swap(A[i], A[rev[i]]);
            }
        }
        
        for (size_t i = 1; i < A.size(); i <<= 1) {
            int wn = this->quickIntPower(3, (MOD - 1) / (i << 1));
            
            for (size_t j = 0; j < A.size(); j += (i << 1)) {
                int w = 1;
                
                for (size_t k = 0; k < i; ++k) {
                    int x = A[j + k];
                    int y = 1LL * w * A[i + j + k] % MOD;
                    
                    A[j + k] = (x + y) % MOD;
                    A[i + j + k] = (x - y + MOD) % MOD;
                    
                    w = 1LL * w * wn % MOD;
                }
            }
        }
        
        if (d == -1) {
            reverse(A.begin() + 1, A.end());
            int inv = this->quickIntPower((int)A.size(), MOD - 2);
            
            for (size_t i = 0; i < A.size(); i++) {
                A[i] = 1LL * A[i] * inv % MOD;
            }
        }
    }
    
    // 正整数快速幂
    int quickIntPower(int a, int b) {
        int ans = 1;
        
        while (b) {
            if (b & 1) {
                ans = 1LL * ans * a % MOD;
            }
            
            a = 1LL * a * a % MOD;
            b >>= 1;
        }
        
        return ans;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string num1 = "2", num2 = "3"; // 预期结果 6
//    string num1 = "123", num2 = "456"; // 预期结果 56088
//    string num1 = "12345", num2 = "12345"; // 预期结果 152399025
//    string num1 = "0", num2 = "0"; // 预期结果 0
    
    // 预期结果 1524157875323883675049535156256668194500533455762536198787501905199875019052100
    string num1 = "1234567890123456789012345678901234567890", num2 = "1234567890123456789012345678901234567890";
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->multiply(num1, num2);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
