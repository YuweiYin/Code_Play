//
//  main.cpp
//  Prob1024_Swap_Nodes_in_Pairs
//
//  Created by 阴昱为 on 2019/6/20.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1024. Swap Nodes in Pairs
//
//Given a linked list, swap every two adjacent nodes and return its head.
//You may not modify the values in the list's nodes, only nodes itself may be changed.
//
//给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。
//你不能只是单纯地改变节点内部的值，而是需要实际地进行节点交换。
//
//Example:
//    Given 1->2->3->4, you should return the list as 2->1->4->3.


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
const int MIN_INT32 = -0x80000000;
//const ll MAX_INT32 = 2147483647;
//const ll MIN_INT32 = -2147483648;


// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};


class Solution {
public:
    ListNode* swapPairs(ListNode* head) {
        return this->solution1(head);
    }
    
private:
    // 方法一。直接遍历、改变链接方式。时间复杂度 O(N)，空间复杂度 O(1)
    ListNode* solution1(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }
        
        // 设置头结点
        ListNode* head_node = new ListNode(MIN_INT32);
        head_node->next = head;
        
        // 初始化链接方式 pre->left->right
        ListNode* pre = head_node;
        ListNode* left = head;
        ListNode* right = head->next;
        
        while (right) {
            // 改变链接方式，从 pre->left->right 改为 pre->right->left
            pre->next = right;
            left->next = right->next;
            right->next = left;
            
            right = left->next; // right 移动到下一个结点处
            if (right && right->next) {
                // 如果后面还剩至少两个非空结点，则继续执行循环
                // 重新形成 pre->left->right 的链接方式
                pre = left;
                left = right;
                right = right->next;
            } else {
                // 如果到头了，或者后面只剩一个结点了，结束循环
                break;
            }
        }
        
        // 返回结果链表头
        return head_node->next;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->swapPairs(head);
    if (ans) {
        while (ans) {
            cout << ans->val << "->";
            ans = ans->next;
        }
        cout << "End." << endl;
    } else {
        cout << "No Answer." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
