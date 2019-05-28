//
//  main.cpp
//  Sqrt_Newton_Method
//
//  Created by 阴昱为 on 2019/5/28.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
#include <cmath>
//#include <math.h>
using namespace std;

const double EPS = 1e-10;

class Solution {
public:
    // 计算 double 型数的正平方根
    double mySqrtDouble(double x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            // 牛顿-拉弗森方法求解平方根，梯度下降 Gradient Descent
            // 要求 x = sqrt(n)，即求 f(x) = x^2 - k 的根。
            // 构造 x_n+1 = x_n + alpha * f(x_n)，如果 f(x) 收敛，
            // 那么通过迭代求解，能使 x_n 趋近于根，alpha 的绝对值越大，变化速度越快。
            
            // f(x) 收敛的充分条件：若 f 二阶可导，那么在待求的零点 x 周围存在一个区域，
            // 只要起始点 x_0 位于这个邻近区域内，那么牛顿-拉弗森方法必定收敛。
            // 可以证明，求平方根时使用的 f(x) = x^2 - k 是收敛的，
            // 梯度 grad = f'(x)，令 alpha = -1 / grad，有 x_n+1 = x_n - f(x_n) / f'(x_n)
            // 对于求平方根问题，f'(x_n) = 2 * x_n，所以 x_n+1 = x_n - (x_n^2 - k) / (2 * x_n)
            // 为了简化计算过程，等式化简为 x_n+1 = (x_n  + k / x_n) / 2
            
            // 梯度下降法的问题：梯度为 0 达到驻点、在根两边震荡、离根越来越远。
            // 不过在求平方根时不会有上述问题。
            
            double res = 1; // 迭代计算平方根 x_n+1
            double last = 0; // 记录上一轮的计算值 x_n
            int max_loop = 100; // 设置最大迭代计算次数
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            return res;
        }
    }
    
    // 获得某整数的正平方根的整数部分
    int mySqrtInt(int x) {
        if (x < 0) {
            return -1;
        } else if (x == 0) {
            return 0;
        } else {
            double res = 1; // 迭代计算平方根
            double last = 0; // 记录上一轮的计算值
            int max_loop = 100; // 设置最大迭代计算次数
            
            // 循环结束条件：本轮计算值与上轮计算值极度相近
            while (fabs(res - last) > EPS && max_loop > 0) {
                last = res;
                res = (last + x / last) / 2;
                max_loop --;
            }
            
            // 只返回整数部分
            return int(res);
        }
    }
};


int main(int argc, const char * argv[]) {
    // 设置测试数据
    int num1 = 20;
    double num2 = 20.0;
    double num3 = 25.0;
    double num4 = 25.1;
    
    // 调用解决方案，计算结果
    Solution *solution = new Solution();

    // 输出运行结果
    cout << solution->mySqrtInt(num1) << '\t'
        << solution->mySqrtDouble(num2) << '\n'
        << solution->mySqrtDouble(num3) << '\t'
        << solution->mySqrtDouble(num4) << endl;
    
    return 0;
}
