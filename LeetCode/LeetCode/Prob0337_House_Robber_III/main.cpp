//
//  main.cpp
//  Prob1337_House_Robber_III
//
//  Created by 阴昱为 on 2019/7/11.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//337. House Robber III
//
//The thief has found himself a new place for his thievery again. There is only one entrance to this area, called the "root." Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that "all houses in this place forms a binary tree". It will automatically contact the police if two directly-linked houses were broken into on the same night.
//Determine the maximum amount of money the thief can rob tonight without alerting the police.
//
//在上次打劫完一条街道之后和一圈房屋后，小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为“根”。 除了“根”之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果两个直接相连的房子在同一天晚上被打劫，房屋将自动报警。
//计算在不触动警报的情况下，小偷一晚能够盗取的最高金额。
//
//Example 1:
//    Input: [3,2,3,null,3,null,1]
//
//      3
//     / \
//    2   3
//     \   \
//      3   1
//
//    Output: 7
//    Explanation: Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.
//
//Example 2:
//    Input: [3,4,5,1,3,null,1]
//
//        3
//       / \
//      4   5
//     / \   \
//    1   3   1
//
//    Output: 9
//    Explanation: Maximum amount of money the thief can rob = 4 + 5 = 9.


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
//const int SQRT_MAX_INT32 = (int)sqrt(MAX_INT32);


// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};


class Solution {
private:
    map<TreeNode*, pair<int, int>> dp = {};
    int max_sum = 0;
    
public:
    int rob(TreeNode* root) {
        return this->solution3(root);
    }
    
private:
    // 方法一：深度优先遍历。时间复杂度 O()，空间复杂度 O(1)。
    // 123 / 124 个通过测试用例，在最后一个 case 超出时间限制 TLE
    // 所以需要改成动态规划，处理重叠子问题
    int solution1 (TreeNode* root) {
        // 边界情况
        if (root == NULL) {
            return 0;
        }
        
        if (root->left == NULL && root->right == NULL) {
            return root->val;
        }
        
        // 注：本题可做成带备忘录的自顶向下动态规划，因为有重叠子问题。
        // 不过 DP 表的制作需要考究，比如使用层序遍历的结点数组/链表。
        // 如果可以，最好把 DP 信息作为树结点的附加信息，即如下两个值：
        // 1.考察以它为根的子树，选根的值时的最优解。2.不选根的值时的最优解。
        return this->dfsTree(root, true);
    }
    
    // can_choose_root 为 true 表示当前能选择 root 结点，否则不能
    int dfsTree (TreeNode* root, bool can_choose_root) {
        if (root == NULL) {
            return 0;
        }
        
        // 选择根，则其左右孩子都不能选了
        int choose_root = 0;
        if (can_choose_root) {
            choose_root = root->val + this->dfsTree(root->left, false) + this->dfsTree(root->right, false);
        }
        
        // 不选择根，左右孩子仍可以选
        int not_choose_root = this->dfsTree(root->left, true) + this->dfsTree(root->right, true);
        
        // 在两种选择中挑较大者
        return max(choose_root, not_choose_root);
    }
    
    // 方法二：带备忘录的自顶向下动态规划。时间复杂度 O()，空间复杂度 O(1)。
    // 执行用时 : 36 ms , 在所有 C++ 提交中击败了 67.23% 的用户
    // 内存消耗 : 23.4 MB , 在所有 C++ 提交中击败了 27.53% 的用户
    // Runtime: 28 ms, faster than 41.29% of C++ online submissions for House Robber III.
    // Memory Usage: 23.5 MB, less than 35.19% of C++ online submissions for House Robber III.
    int solution2 (TreeNode* root) {
        // 边界情况
        if (root == NULL) {
            return 0;
        }
        
        if (root->left == NULL && root->right == NULL) {
            return root->val;
        }
        
        // 注：本题可做成带备忘录的自顶向下动态规划，因为有重叠子问题。
        // 不过 DP 表的制作需要考究，比如使用层序遍历的结点数组/链表。
        // 如果可以，最好把 DP 信息作为树结点的附加信息，即如下两个值：
        // 1.考察以它为根的子树，选根的值时的最优解。2.不选根的值时的最优解。
        int res = this->dpTree(root, false); // 根的“父结点”未被选择
        
//        for (auto ite = this->dp.begin(); ite != this->dp.end(); ite++) {
//            cout << ite->first->val << ": ";
//            cout << get<0>(ite->second) << "," << get<1>(ite->second) << endl;
//        }
        
        return res;
    }
    
    // father_select 为 true 表示当前结点 root 的父结点已经被选择了。
    int dpTree (TreeNode* root, bool father_select) {
        if (root == NULL) {
            return 0;
        }
        
        // 若当然结点没有对应的 dp 表项，则先创建并初始化
        if (this->dp.find(root) == this->dp.end()) {
            dp.insert({root, {-1, -1}});
        }
        
        int choose_root = 0; // 选择根的最优解
        int not_choose_root = 0; // 不选择根的最优解
        
        // 计算选择当前结点的情况下，能达到的最优解
        // 选择根，则其左右孩子都不能选了
        if (get<0>(this->dp[root]) < 0) {
            // 若 dp 表当前没有值，则把运算结果给 dp 表
            get<0>(this->dp[root]) = root->val +
                this->dpTree(root->left, true) +
                this->dpTree(root->right, true);
        }
        choose_root = get<0>(this->dp[root]);
        
        // 计算不选当前结点的情况下，能达到的最优解
        // 不选择根，左右孩子仍可以选
        if (get<1>(this->dp[root]) < 0) {
            // 若 dp 表当前没有值，先把运算结果给 dp 表
            get<1>(this->dp[root]) = this->dpTree(root->left, false) +
                this->dpTree(root->right, false);
        }
        not_choose_root = get<1>(this->dp[root]);
        
        // 根据父结点是否被选择的情况，返回父结点的 get<0>(..) 或 get<1>(..)
        if (father_select) {
            // 若父结点被选，则 get<0>(..) 是其左孩子的“不可选最优解”加上右孩子的“不可选最优解”
            return not_choose_root;
        } else {
            // 若父结点未选，则 get<1>(..) 是其左孩子的 max(可选,不可选) 加上右孩子的 max(可选,不可选)
            return max(choose_root, not_choose_root);
        }
    }
    
    // 方法三：时空效率改进的带备忘录的自顶向下动态规划。时间复杂度 O(N)，空间复杂度 O(N), Omega(lg N)。
    // 执行用时 : 16 ms , 在所有 C++ 提交中击败了 99.01% 的用户
    // 内存消耗 : 20.4 MB , 在所有 C++ 提交中击败了 99.08% 的用户
    // Runtime: 16 ms, faster than 88.03% of C++ online submissions for House Robber III.
    // Memory Usage: 20.6 MB, less than 80.83% of C++ online submissions for House Robber III.
    int solution3 (TreeNode* root) {
        // 边界情况
        if (root == NULL) {
            return 0;
        }
        
        if (root->left == NULL && root->right == NULL) {
            return root->val;
        }
        
        int jump_sum = 0; // 不选当前结点的最大收益值
        this->robTree(root, jump_sum);
        
        return this->max_sum;
    }
    
    int robTree (TreeNode* root, int& jump_sum) {
        if(!root) {
            jump_sum = 0;
            return 0;
        }
        
        // 当前结点是叶节点
        if(!root->left && !root->right) {
            jump_sum = 0; // 如果不选当前结点，那收益就是 0
            this->max_sum = max(this->max_sum, root->val);
            return root->val;
        }
        
        int jump_left = 0, jump_right = 0; // jump_left 表示左子树不选择根的最大收益
        int left = this->robTree(root->left, jump_left); // 左子树，选择根的最大收益
        int right = this->robTree(root->right, jump_right); // 右子树，选择根的最大收益
        
        // 保证前面结果计算出来才会算后面的，所以实质还是自底向上的动态规划
        // 并且函数是通过引用的方式调用 jump_sum 的，所以“持久化”了该变量，不至于重复计算
        
        int sum_root = root->val + jump_left + jump_right; // 当前树，选择根的最大收益
        jump_sum = max(left, jump_left) + max(right, jump_right); // 当前树，不选择根的最大收益
        this->max_sum = max(this->max_sum, max(sum_root, jump_sum)); // 更新最大收益
        
        return sum_root; // 返回选择根的最大收益
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果 7
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->right = new TreeNode(3);
    root->right->right = new TreeNode(1);
    
    // 预期结果 9
//    TreeNode* root = new TreeNode(3);
//    root->left = new TreeNode(4);
//    root->right = new TreeNode(5);
//    root->left->left = new TreeNode(1);
//    root->left->right = new TreeNode(3);
//    root->right->right = new TreeNode(1);
    
    // 预期结果 7
//    TreeNode* root = new TreeNode(2);
//    root->left = new TreeNode(1);
//    root->right = new TreeNode(3);
//    root->left->right = new TreeNode(4);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    int ans = solution->rob(root);
    cout << "Answer is " << ans << endl;
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
