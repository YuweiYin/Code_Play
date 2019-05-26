//
//  main.cpp
//  1_Minimum_Depth_of_Binary_Tree
//
//  Created by 阴昱为 on 2019/5/26.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
using namespace std;

/*
 *  Minimum Depth of Binary Tree
 *
 *  Description:
 *      Given a binary tree, find its minimum depth.
 *      The minimum depth is the number of nodes along the shortest path
 *      from the root node down to the nearest leaf node.
 *
 *  Time Limit: 1 second
 *  Space Limit: 32768 KB
 *
 *  Knowledge: Tree
 */


class TreeNode {
public:
    TreeNode() {
        val = 0;
        left = NULL;
        right = NULL;
    }
    TreeNode(int val) {
        this->val = val;
        left = NULL;
        right = NULL;
    }
private:
    int val;
    TreeNode *left;
    TreeNode *right;
};


class Solution {
public:
    Solution() {
        shortest_depth = 9999;
        current_depth = 0;
    }
    int run(TreeNode *root) {
        // 到达叶节点
        if (!root) {
            if (this->current_depth < this->shortest_depth) {
                this->shortest_depth = this->current_depth
            }
            current_depth -= 1;
            return
        }
        
        if ((this->current_depth + 1) > this->shortest_depth) {
            current_depth -= 1;
            return
        }
        
        current_depth += 1;
        
        this->run(root->left);
        current_depth -= 1;
        
        this->run(root->right);
        current_depth -= 1;
        
        return
    }
public:
    int shortest_depth;
    int current_depth;
};


int main(int argc, const char * argv[]) {
    TreeNode *root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->rgiht = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->left->right = new TreeNode(7);
    
    Solution *solution = new Solution();
    
    solution->run(root);
    
    cout << solution->shortest_depth;
    
    return 0;
}
