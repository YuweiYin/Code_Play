//
//  main.cpp
//  Prob1071_Simplify_Path
//
//  Created by 阴昱为 on 2019/7/30.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//71. Simplify Path
//
//Given an absolute path for a file (Unix-style), simplify it. Or in other words, convert it to the canonical path.
//In a UNIX-style file system, a period . refers to the current directory. Furthermore, a double period .. moves the directory up a level. For more information, see: Absolute path vs relative path in Linux/Unix
//Note that the returned canonical path must always begin with a slash /, and there must be only a single slash / between two directory names. The last directory name (if it exists) must not end with a trailing /. Also, the canonical path must be the shortest string representing the absolute path.
//
//以 Unix 风格给出一个文件的绝对路径，你需要简化它。或者换句话说，将其转换为规范路径。
//在 Unix 风格的文件系统中，一个点（.）表示当前目录本身；此外，两个点 （..） 表示将目录切换到上一级（指向父目录）；两者都可以是复杂相对路径的组成部分。更多信息请参阅：Linux / Unix中的绝对路径 vs 相对路径
//请注意，返回的规范路径必须始终以斜杠 / 开头，并且两个目录名之间必须只有一个斜杠 /。最后一个目录名（如果存在）不能以 / 结尾。此外，规范路径必须是表示绝对路径的最短字符串。
//
//Example 1:
//    Input: "/home/"
//    Output: "/home"
//    Explanation: Note that there is no trailing slash after the last directory name.
//
//Example 2:
//    Input: "/../"
//    Output: "/"
//    Explanation: Going one level up from the root directory is a no-op, as the root level is the highest level you can go.
//
//Example 3:
//    Input: "/home//foo/"
//    Output: "/home/foo"
//    Explanation: In the canonical path, multiple consecutive slashes are replaced by a single one.
//
//Example 4:
//    Input: "/a/./b/../../c/"
//    Output: "/c"
//
//Example 5:
//    Input: "/a/../../b/../c//.//"
//    Output: "/c"
//
//Example 6:
//    Input: "/a//b////c/d//././/.."
//    Output: "/a/b/c"


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


class Solution {
public:
    string simplifyPath(string path) {
        return this->solution1(path);
    }
    
private:
    // 方法一。按规律简化路径。时间复杂度 O(N)，空间复杂度 O(1)。N = path.size
    // 执行用时 : 8 ms , 在所有 C++ 提交中击败了 93.96% 的用户
    // 内存消耗 : 8.9 MB , 在所有 C++ 提交中击败了 100.00% 的用户
    // Runtime: 4 ms, faster than 97.91% of C++ online submissions for Simplify Path.
    // Memory Usage: 8.9 MB, less than 100.00% of C++ online submissions for Simplify Path.
    string solution1 (string& path) {
        if (path.empty()) {
            return "";
        }
        
        // 根据题意：都用 "/" 开头
        auto p_begin = path.begin();
        int index = 0;
        
//        cout << "1: " << path << endl;
        
        // 把 "//" 改为 "/"
        while (index < (int)path.size() - 1) {
            if (path[index] == '/' && path[index + 1] == '/') {
                path.erase(p_begin + index); // "//" -> "/"
            } else {
                index ++;
            }
        }
        
//        cout << "2: " << path << endl;
        
        index = 0;
        // 把 "/./" 改为 "/"
        while (index < (int)path.size() - 2) {
            if (path[index] == '/' && path[index + 1] == '.' && path[index + 2] == '/') {
                path.erase(p_begin + index, p_begin + index + 2); // "/./" -> "/"
            } else {
                index ++;
            }
        }
        if (path == "/../" || path == "/.." || path == "/." || path == "/") {
            return "/";
        } else {
            if (path.size() >= 2 && path[path.size() - 2] == '/' && path[path.size() - 1] == '.') {
                path.erase(path.end() - 2, path.end()); // 末尾 "x/." -> "x"
            }
        }
        
//        cout << "3: " << path << endl;
        
        index = 0;
        int last_slash = 0; // 上一个斜线
        // 把 "x/y/../" 改为 "x/"，即删除 "y/../"，监测点为 y 后面的 "/"
        while (index < (int)path.size() - 3) {
            if (path[index] == '/' && path[index + 1] == '.'
                && path[index + 2] == '.' && path[index + 3] == '/') {
                if (index == 0) {
                    path.erase(p_begin + 1, p_begin + 4); // 首部 "/../" -> "/"
                }  else {
                    last_slash = (int)path.rfind('/', index - 1); // 找到上一个斜线
                    path.erase(p_begin + last_slash + 1, p_begin + index + 4); // "x/y/../" -> "x/"
                    index = last_slash;
                }
            } else {
                index ++;
            }
        }
        
//        cout << "4: " << path << endl;
        
        if (path == "/../" || path == "/.." || path == "/." || path == "/") {
            return "/";
        }
        if (path.size() >= 3 && path[path.size() - 3] == '/'
            && path[path.size() - 2] == '.' && path[path.size() - 1] == '.') {
            last_slash = (int)path.rfind('/', (int)path.size() - 4); // 找到倒数第二个斜线
            path.erase(p_begin + last_slash + 1, path.end()); // 末尾 "x/y/.." -> "x"
        }
        
//        cout << "5: " << path << endl;
        
        while (path.size() > 1 && path[path.size() - 1] == '/') {
            path.erase(path.end() - 1);
        }
        
//        cout << "6: " << path << endl;
        
        return path;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
//    string path = "/home/"; // 预期结果 "/home"
//    string path = "/..."; // 预期结果 "/..."
//    string path = "/../"; // 预期结果 "/"
//    string path = "/.."; // 预期结果 "/"
//    string path = "/."; // 预期结果 "/"
//    string path = "/"; // 预期结果 "/"
//    string path = "/home//foo/"; // 预期结果 "/home/foo"
//    string path = "/a/./b/../../c/"; // 预期结果 "/c"
//    string path = "/a/../../b/../c//.//"; // 预期结果 "/c"
//    string path = "/a//b////c/d//././/.."; // 预期结果 "/a/b/c"
//    string path = "/a//b////c/d//././/.."; // 预期结果 "/a/b/c"
    string path = "/hzx/.././BVHm/../././..//"; // 预期结果 "/"
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    string ans = solution->simplifyPath(path);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
