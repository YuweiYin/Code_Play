//
//  main.cpp
//  Prob1025_Reverse_Nodes_in_k-Group
//
//  Created by 阴昱为 on 2019/6/20.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1025. Reverse Nodes in k-Group
//
//Given a linked list, reverse the nodes of a linked list k at a time and return its modified list.
//k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes in the end should remain as it is.
//
//给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。
//k 是一个正整数，它的值小于或等于链表的长度。
//如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。
//
//Example:
//    Given this linked list: 1->2->3->4->5
//    For k = 2, you should return: 2->1->4->3->5
//    For k = 3, you should return: 3->2->1->4->5
//
//Note:
//    Only constant extra memory is allowed.
//    You may not alter the values in the list's nodes, only nodes itself may be changed.
//说明 :
//    你的算法只能使用常数的额外空间。
//    你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。


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
    ListNode* reverseKGroup(ListNode* head, int k) {
        return this->solution1(head, k);
    }
    
private:
    // 方法一。直接遍历、改变链接方式。时间复杂度 O(N)，空间复杂度 O(1)
    // Runtime: 16 ms, faster than 98.61% of C++ online submissions for Reverse Nodes in k-Group.
    // Memory Usage: 9.6 MB, less than 90.49% of C++ online submissions for Reverse Nodes in k-Group.
    ListNode* solution1(ListNode* head, int k) {
        if (!head || !head->next || k <= 1) {
            return head;
        }
        
        // 设置头结点
        ListNode* head_node = new ListNode(MIN_INT32);
        head_node->next = head;
        
        // 初始化链接方式 pre->left->right->...->after
        ListNode* pre = head_node; // pre 是子链表第一个结点的前一个结点
        ListNode* after = head; // after 是子链表最后一个结点的后一个结点
        
        ListNode* left = head;
        ListNode* right = head;
        ListNode* temp = head;
        
        // k (k >= 3)个结点的子链表中，pre->首结点->中间结点->尾结点->after
        // 尾结点、中间结点、首结点之间的链接，只需要把后者的 next 指向前者就行
        // 还需要把 pre 的 next 指向尾结点，首结点的 next 指向 after
        // 之后，pre 移动到原首结点的位置(即新子链表的最末)，after 则往后找 k 个结点
        while (after) {
            // after 向右先走 k - 1 步
            for (int i = 0; i < k - 1; i++) {
                if (after) {
                    after = after->next;
                } else {
                    break;
                }
            }
            
            // after 走不到 k - 1 步，表示当前剩余不足 k 个结点了，结束循环
            if (!after) {
                break;
            }
            
            after = after->next; // after 位于子链表最后一个结点的后一个结点
            
            // right 先向后移动一步
            if (right->next) {
                right = right->next;
            } else {
                break;
            }
            
            // 逐对改变中间结点的链接方式，让后者的 next 指向前者
            while (right != after) {
                temp = right->next;
                right->next = left;
                
                left = right;
                right = temp;
            }
            
            // 改变子链表头尾结点的链接方式
            // 此时为 pre->node_1<->node_2<-...<-node_k  after->
            // left 在 node_k 位置，right 在 after 位置
            pre->next->next = after;
            temp = pre->next; // 记录这时的 pre->next，它是反转后的子链表的最后一个结点，也即是下一个子链表首结点的前驱结点
            pre->next = left;
            
            // 为下一循环做好准备
            pre = temp;
            left = after;
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
    head->next->next->next->next = new ListNode(5);
    
//    int k = 2; // 预期结果 2->1->4->3->5
    int k = 3; // 预期结果 3->2->1->4->5
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->reverseKGroup(head, k);
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
