//
//  main.cpp
//  FindMinimum
//
//  Created by 阴昱为 on 2019/8/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//二维矩阵找极小值点 (应用：ML中梯度下降找局部全局最优解)
//题目描述：
//    给定一个不包含重复元素的 M * N 二维矩阵，求矩阵的极小值点。
//    极小值点的定义如下：若一个点的值是极小值，四个连通方向上的的不越界的相邻点值都比它大。


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
#include <random>

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
public:
    int x, y;
    int value;
    
    Pos(int x, int y, int value) {
        this->x = x;
        this->y = y;
        this->value = value;
    }
};


class Solution {
private:
    vector<vector<int>> matrix;
    vector<vector<int>> direction = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
public:
    // 解决方案入口函数
    void FindMatrixMinimum() {
        this->solution1();
    }
    
private:
    // 方法一。矩阵二分法。时间复杂度 O(), Omega(), 空间复杂度 O()
    // M * N 矩阵
    void solution1() {
        const int TEST_LOOP = 100; // 测试循环次数
        for (int t = 0; t < TEST_LOOP; t++) {
            this->generateRandomMatrix();
            
            int rows = (int)this->matrix.size();
            if (rows <= 0) {
                throw "error";
                return;
            }
            int cols = (int)this->matrix[0].size();
            
            Pos min = Pos(-1, -1, INT_MAX);
            Pos res = this->binarySearchMatrix(0, 0, rows, cols, min);
            
            if (!this->isMinimum(res.x, res.y)) {
                cout << "No Minimum in Matrix" << endl;
            } else {
                cout << "Minimum: position=(" << res.x << "," << res.y << ")  value=" << res.value << endl;
            }
        }
    }
    
    
    // 产生随机大小和乱序数值的矩阵 this->matrix
    void generateRandomMatrix() {
        // 5~15 * 5~15 的矩阵
        int rows = rand() % 11 + 5;
        int cols = rand() % 11 + 5;
        
        this->matrix = vector<vector<int>>(rows, vector<int>(cols));
        
        // 产生一维数组
        int num = rows * cols;
        vector<int> vec(num);
        for (int i = 0; i < num; i++) {
            vec[i] = i;
        }
        
        // shuffle 数组，即两两随机交换
        for (int i = 0; i < num; i++) {
            int next = rand() % (num - i) + i;
            
            int temp = vec[i];
            vec[i] = vec[next];
            vec[next] = temp;
        }
        
        // 把数组值赋给矩阵
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                this->matrix[i][j] = vec[i * cols + j];
            }
        }
        
        // 展示矩阵
//        for (int i = 0; i < rows; i++) {
//            for (int j = 0; j < cols; j++) {
//                cout << setiosflags(ios::left) << setw(5) << this->matrix[i][j];
//            }
//            cout << endl;
//        }
    }
    
    
    // 判断是否为非越界的矩阵下标
    bool isLegalIndex(int x, int y) {
        return x >= 0 && y >= 0 && x < (int)matrix.size() && y < (int)(matrix[0].size());
    }
    
    
    // 判断点 (i, j) 是否为极小值点
    bool isMinimum(int i, int j) {
        for (int k = 0; k < (int)this->direction.size(); k++) {
            // 考察点 (i, j) 四个方向的点 (x, y)
            int x = i + this->direction[k][0];
            int y = j + this->direction[k][1];
            
            // 如果点 (x, y) 为不越界点，并且点 (x, y) 比点 (i, j) 更小
            if (this->isLegalIndex(x, y) && this->matrix[x][y] < this->matrix[i][j]) {
                // 则点 (i, j) 不是极小值点
                return false;
            }
        }
        
        // 点 (i, j) 四个方向的点的值都比它大，则它是极小值点
        return true;
    }
    
    
    Pos binarySearchMatrix(int x_start, int y_start, int x_end, int y_end, Pos min) {
        // base case
        if (x_start + 1 == x_end && y_start + 1 == y_end) {
            return Pos(x_start, y_start, this->matrix[x_start][y_start]);
        }
        
        // 二分长轴
        if (x_end - x_start < y_end - y_start) {
            // y 方向更长，则以 y 方向的垂直平分线 来二分当前矩阵
            int y_mid = (y_end + y_start) >> 1;
            for (int i = x_start; i < x_end; i++) { // 时间复杂度 O(x_end - x_start)
                // 固定 y 方向中点，扫描 x 方向，找到值比 min 值小的点
                if (matrix[i][y_mid] < min.value) {
                    min.x = i;
                    min.y = y_mid;
                    min.value = matrix[i][y_mid];
                }
            }
            // 此时的 min，要么比之前的 min 值更小，要么扫描方向上的所有点都大于 min
            
            // 查看此时 min 点的周围四个点，如果周围点的值更小，则更新 min
            int x_min = min.x, y_min = min.y; // 记录下此时 min 的坐标
            for (int i = 0; i < (int)direction.size(); i++) { // 时间复杂度 O(1)
                int x = x_min + direction[i][0];
                int y = y_min + direction[i][1];
                
                if (this->isLegalIndex(x, y) && this->matrix[x][y] < min.value) {
                    min.x = x;
                    min.y = y;
                    min.value = this->matrix[x][y];
                }
            }
            // 此时的 min，要么比之前的 min 值更小，要么仍是原 min，意味着该 min 是极小值点
            if (min.x == x_min && min.y == y_min) {
                return min;
            }
            
            // 判断找到的 min 位于二分矩阵的哪一侧（左 or 右）
            if (min.y >= y_mid) {
                // 若找到的 min 在右侧或是线上，则递归地在右侧找 min
                return this->binarySearchMatrix(x_start, y_mid, x_end, y_end, min);
            } else {
                // 否则递归地在左侧找 min
                return this->binarySearchMatrix(x_start, y_start, x_end, y_mid, min);
            }
        } else {
            // x 方向更长，写法是对称的
            int x_mid = (x_end + x_start) >> 1;
            for (int i = y_start; i < y_end; i++) {
                if (this->matrix[x_mid][i] < min.value) {
                    min.x = x_mid;
                    min.y = i;
                    min.value = this->matrix[x_mid][i];
                }
            }
            
            int minx = min.x, miny = min.y;
            for (int i = 0; i < (int)direction.size(); i++) {
                int x = minx + direction[i][0];
                int y = miny + direction[i][1];
                if (this->isLegalIndex(x, y) && this->matrix[x][y] < min.value) {
                    min.x = x;
                    min.y = y;
                    min.value = this->matrix[x][y];
                }
            }
            
            if (min.x >= x_mid) {
                return this->binarySearchMatrix(x_mid, y_start, x_end, y_end, min);
            } else {
                return this->binarySearchMatrix(x_start, y_start, x_mid, y_end, min);
            }
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->FindMatrixMinimum();
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
