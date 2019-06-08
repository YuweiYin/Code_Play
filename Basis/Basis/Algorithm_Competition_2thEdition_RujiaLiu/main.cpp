//
//  main.cpp
//  Algorithm_Competition_2thEdition_RujiaLiu
//
//  Created by 阴昱为 on 2019/6/6.
//  Copyright © 2019 阴昱为. All rights reserved.
//

// 设置系统栈深度
#pragma comment(linker, "/STACK:1024000000,1024000000")

// 引入头文件
#include <iostream>
#include <iomanip>
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
//const double PI = acos(-1.0);
//const double EPS = 1e-14;
//const ll MAX = 1ll<<55;
//const double INF = ~0u>>1;
//const int MOD = 1000000007;
//const ll MOD = 1e9+7;

class Solution {
private:
    // 类似 LeetCode 319 灯泡开关
    int Program3_2_Page39 () {
        int n, k;
        cin >> n >> k;
        
        vector<bool> light = vector<bool>(n, false);
        
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= k; j++) {
                if (i % j == 0) {
                    light[i] = !light[i];
                }
            }
        }
        
        bool first = true;
        for (int i = 1; i <= n; i++) {
            if (light[i]) {
                if (first) {
                    first = false;
                    cout << i;
                } else {
                    cout << " " << i;
                }
            }
        }
        cout << endl;
        
        return 0;
    }
    
    int Program3_3_Page40 () {
        int n;
        cin >> n;
        
        vector<vector<int>> matrix = vector<vector<int>>(n, vector<int>(n, 0));
        
        int direction = 0, mod = 4; // 0 down, 1 left, 2 up, 3 right (mod 4)
        int i = 0, j = n - 1, num = 1;
        
        while (num <= n * n) {
            matrix[i][j] = num++;
            if (direction == 0) {
                i ++; // down
                if (i >= n || matrix[i][j] > 0) { // 短路运算符，不会越界
                    i --; // back
                    j --; // left
                    direction = (direction + 1) % mod;
                }
            } else if (direction == 1) {
                j --; // left
                if (j < 0 || matrix[i][j] > 0) {
                    j ++; // back
                    i --; // up
                    direction = (direction + 1) % mod;
                }
            } else if (direction == 2) {
                i --; // up
                if (i < 0 || matrix[i][j] > 0) {
                    i ++; // back
                    j ++; // right
                    direction = (direction + 1) % mod;
                }
            } else {
                j ++; // right
                if (j >= n || matrix[i][j] > 0) {
                    j --; // back
                    i ++; // down
                    direction = (direction + 1) % mod;
                }
            }
        }
        
        for (i = 0; i < n; i++) {
            for (j = 0; j < n - 1; j++) {
                cout << matrix[i][j] << " ";
            }
            cout << matrix[i][j] << endl;
        }
        
        return 0;
    }
    
    int Program3_4_Page43 () {
        int count = 0;
        char s[20], buf[99];
        scanf("%s", s);
        for (int abc = 100; abc <= 999; abc++) {
            for (int de = 10; de <= 99; de++) {
                int x = abc * (de % 10);
                int y = abc * (de / 10);
                int z = abc * de;
                sprintf(buf, "%d%d%d%d%d", abc, de, x, y, z);
                bool ok = true;
                for (int i = 0; i < (int)strlen(buf); i++) {
                    if (strchr(s, buf[i]) == NULL) {
                        ok = false;
                    }
                }
                
                if (ok) {
                    printf("<%d>\n", ++count);
                    printf("%5d\nX%4d\n-----\n%5d\n%4d\n-----\n%5d\n\n", abc, de, x, y, z);
                }
            }
        }
        printf("The number of solutions = %d\n", count);
        
        return 0;
    }
    
    // Tex Quotes, UVa 272
    int Program3_5_Page45 () {
        char ch = '\0';
        bool flag = true;
        
        while ((ch = getchar()) != EOF) {
            if (ch == '\"') {
                printf("%s", flag ? "``" : "\'\'");
                flag = !flag;
            } else {
                printf("%c", ch);
            }
        }
        
        return 0;
    }
    
    // WERTYU, UVa 10082
    int Program3_6_Page47 () {
        // 使用常量数组
        char s[] = "`1234567890-=QWERTYUIOP[]\\ASDFGHJKL;'ZXCVBNM,./";
        char ch = '\0';
        int s_len = (int)strlen(s);
        const int shift = 1;
        
        while ((ch = getchar()) != EOF) {
            int i = 0;
            // 找到 s[i] == ch 时的下标 i
            while (i < s_len && s[i] && s[i] != ch) {
                i ++;
            }
            
            if (s[i] && s[i] == ch) {
                // 左移输出
                int pre_index = i - shift;
                if (pre_index < 0) {
                    pre_index += s_len;
                }
                printf("%c", s[pre_index]);
            } else {
                putchar(ch);
            }
        }
        
        return 0;
    }
    
    // Palindromes, UVa 401
    int Program3_7_Page48 () {
        // 使用常量数组
        // 镜像串, 对应的字符:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789
        const char* rev = "A   3  HIL JM O   2TUVWXY51SE Z  8 ";
        // 00 普通串, 01 普通回文串, 10 普通镜像串, 11 镜像回文串
        const char* msg[] = {"not a palindrome", "a regular palindrome",
            "a mirrored string", "a mirrored palindrome"};
        char s[30];
        
        while (scanf("%s", s) == 1) {
            int s_len = (int)strlen(s);
            int palin = 1, mirro = 1;
            // 遍历一半长度
            for (int i = 0; i < (s_len + 1) / 2; i++) {
                // 先判断是否不满足回文串要求
                if (s[i] != s[s_len - 1 - i]) {
                    palin = 0;
                }
                
                // 再判断是否不满足镜像串要求
                if (isalpha(s[i])) {
                    // s[i] 是字母
                    if (rev[s[i] - 'A'] != s[s_len - 1 - i]) {
                        mirro = 0;
                    }
                } else if (isdigit(s[i])) {
                    // s[i] 是数字，+25 而不是 +26 是因为本题不考虑数字 0
                    if (rev[s[i] - '0' + 25] != s[s_len - 1 - i]) {
                        mirro = 0;
                    }
                } else {
                    mirro = 0;
                }
            }
            printf("%s -- is %s.\n\n", s, msg[(mirro * 2) + palin]);
        }
        
        return 0;
    }

public:
    int MainSolution () {
        this->Program3_2_Page39();
        return 0;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    clock_t start, finish;
    double prog_duration;
    start = clock();
    
    Solution *solution = new Solution();
    solution->MainSolution();
    
    // 计时
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
