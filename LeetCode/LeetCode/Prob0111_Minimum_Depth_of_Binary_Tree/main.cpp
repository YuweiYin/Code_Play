//
//  main.cpp
//  Prob1111_Minimum_Depth_of_Binary_Tree
//
//  Created by 阴昱为 on 2019/6/5.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//111. Minimum Depth of Binary Tree
//
//Given a binary tree, find its minimum depth.
//The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
//Note: A leaf is a node with no children.

//给定一个二叉树，找出其最小深度。
//最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
//说明: 叶子节点是指没有子节点的节点。
//
//Example:
//  Given binary tree [3,9,20,null,null,15,7],
//    3
//   / \
//  9  20
//    /  \
//   15   7
//  return its minimum depth = 2.

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


// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

class Solution {
public:
    int minDepth (TreeNode* root) {
        return this->solution1(root);
    }
    
    int solution1 (TreeNode* root) {
        // 根为空，则层数为 0
        if (root == NULL) {
            return 0;
        }
        
        // 根无子女，则层数为 1
        if (root->left == NULL && root->right == NULL) {
            return 1;
        }
        
        int depth = 0; // 层数，最终结果
        
        queue<TreeNode*> node_queue{}; // 宽度优先搜索，结点队列
        node_queue.push(root); // 把根结点加入队列
        
        // 若队列不空，则继续搜索
        while (!node_queue.empty()) {
            int len_queue = (int)node_queue.size();
            depth ++;
            
            for (int i = 0; i < len_queue; i++) {
                TreeNode* cur = node_queue.front();
                node_queue.pop();
                
                // 如果当前结点没有子女结点，则输出层数
                if (cur->left == NULL && cur->right == NULL) {
                    return depth;
                }
                
                // 否则，如果左孩子存在，则把左孩子加入队列
                if (cur->left != NULL) {
                    node_queue.push(cur->left);
                }
                
                // 如果右孩子存在，则把右孩子加入队列
                if (cur->right != NULL) {
                    node_queue.push(cur->right);
                }
            }
        }
        
        return depth;
    }
    
    // 前序遍历输出树结构
    int PreOrderRetrival (TreeNode* root) {
        if (!root) {
            return -1;
        }
        
        cout << root->val << endl;
        
        if (root->left) {
            this->PreOrderRetrival(root->left);
        }
        
        if (root->right) {
            this->PreOrderRetrival(root->right);
        }
        
        return 0;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据 {3, 9, 20, null, null, 15, 7}
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(9);
    root->right = new TreeNode(20);
    root->right->left = new TreeNode(15);
    root->right->right = new TreeNode(7);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    // solution->PreOrderRetrival(root);
    cout << solution->minDepth(root) << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
