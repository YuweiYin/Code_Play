//
//  main.cpp
//  FindMinimum
//
//  Created by 阴昱为 on 2019/8/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//二维矩阵找极小值点(应用：ML中梯度下降找局部全局最优解)
//题目描述：
//    给定一个不包含重复元素的N行M列二维矩阵，求矩阵的极小值。极小值的定义如下：若一个值是极小值，四连通方向上的的不越界的邻居都比它大。
//Example1:
//    Input:
//    Output:
//Example2:
//    Input:
//    Output:


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


class Pos {
    int x, y;
    int value;
    
    Pos(int x, int y, int value) {
        this.x = x;
        this.y = y;
        this.value = value;
    }
};

    
class Solution {
private:
    int[][] a;
    Random r = new Random();
    int dir[][] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
public:
    // 解决方案入口函数
    string FindMatrixMinimum(string str) {
        return this->solution1(str);
    }
    
private:
    // 方法一。。时间复杂度 O(), Omega(), 空间复杂度 O()
    string solution1(string str) {
        for (int t = 0; t < 100; t++) {
            generate();
            Pos p = good(0, 0, a.length, a[0].length, new Pos(-1, -1, Integer.MAX_VALUE));
            for (int i = 0; i < a.length; i++) {
                for (int j = 0; j < a[i].length; j++) {
                    System.out.printf(String.format("%4d", a[i][j]));
                }
                System.out.println();
            }
            System.out.println(p.x + " " + p.y + " " + p.value);
            if (!isMinimum(p.x, p.y)) {
                throw new RuntimeException("error");
            }
        }
        
        return this->result;
    }
    
    void generate() {
        int rows = r.nextInt(10) + 5;
        int cols = r.nextInt(10) + 5;
        a = new int[rows][cols];
        int b[] = new int[rows * cols];
        for (int i = 0; i < b.length; i++) b[i] = i;
        for (int i = 0; i < b.length; i++) {
            int next = r.nextInt(b.length - i) + i;
            int temp = b[i];
            b[i] = b[next];
            b[next] = temp;
        }
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                a[i][j] = b[i * cols + j];
            }
        }
    }
    
    boolean legal(int x, int y) {
        return x >= 0 && y >= 0 && x < a.length && y < a[0].length;
    }
    
    int dir[][] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
    boolean isMinimum(int i, int j) {
        for (int k = 0; k < dir.length; k++) {
            int x = i + dir[k][0];
            int y = j + dir[k][1];
            if (legal(x, y)) {
                if (a[x][y] < a[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }

    Pos good(int fx, int fy, int tx, int ty, Pos min) {
        if (fx + 1 == tx && fy + 1 == ty) return new Pos(fx, fy, a[fx][fy]);
        if (tx - fx < ty - fy) {//二分长轴
            int my = (ty + fy) >> 1;
            for (int i = fx; i < tx; i++) {
                if (a[i][my] < min.value) {
                    min.x = i;
                    min.y = my;
                    min.value = a[i][my];
                }
            }
            int minx = min.x, miny = min.y;
            for (int i = 0; i < dir.length; i++) {
                int x = minx + dir[i][0], y = miny + dir[i][1];
                if (legal(x, y) && a[x][y] < min.value) {
                    min.x = x;
                    min.y = y;
                    min.value = a[x][y];
                }
            }
            if (min.y >= my) {
                return good(fx, my, tx, ty, min);
            } else {
                return good(fx, fy, tx, my, min);
            }
        } else {
            int mx = (tx + fx) >> 1;
            for (int i = fy; i < ty; i++) {
                if (a[mx][i] < min.value) {
                    min.x = mx;
                    min.y = i;
                    min.value = a[mx][i];
                }
            }
            int minx = min.x, miny = min.y;
            for (int i = 0; i < dir.length; i++) {
                int x = minx + dir[i][0];
                int y = miny + dir[i][1];
                if (legal(x, y) && a[x][y] < min.value) {
                    min.x = x;
                    min.y = y;
                    min.value = a[x][y];
                }
            }
            if (min.x >= mx) {
                return good(mx, fy, tx, ty, min);
            } else {
                return good(fx, fy, mx, ty, min);
            }
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // Case  预期结果
    

    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->FindMatrixMinimum(str);
    if (!ans.empty()) {
        cout << ans << endl;
    } else {
        cout << "Answer is Empty." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
