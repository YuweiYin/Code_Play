//
//  main.cpp
//  Prob1086_Partition_List
//
//  Created by 阴昱为 on 2019/8/7.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//86. Partition List
//
//Given a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.
//You should preserve the original relative order of the nodes in each of the two partitions.
//
//给定一个链表和一个特定值 x，对链表进行分隔，使得所有小于 x 的节点都在大于或等于 x 的节点之前。
//你应当保留两个分区中每个节点的初始相对位置。
//
//Example:
//    Input: head = 1->4->3->2->5->2, x = 3
//    Output: 1->2->2->4->3->5


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


// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};


class Solution {
public:
    ListNode* partition(ListNode* head, int x) {
        return this->solution1(head, x);
    }
    
private:
    // 方法一。快慢双指针。时间复杂度 O(N)，空间复杂度 O(1)。N = list.size
    // 执行用时 : 4 ms , 在所有 C++ 提交中击败了 99.60% 的用户
    // 内存消耗 : 8.5 MB , 在所有 C++ 提交中击败了 88.49% 的用户
    // Runtime: 4 ms, faster than 97.38% of C++ online submissions for Partition List.
    // Memory Usage: 8.7 MB, less than 73.77% of C++ online submissions for Partition List.
    ListNode* solution1 (ListNode* head, int x) {
        // 边界情况
        if (head == NULL || head->next == NULL) {
            return head;
        }
        
        ListNode* new_head = new ListNode(INT_MIN); // 头部哑结点
        new_head->next = head;
        
        ListNode* fast = head; // 快指针
        ListNode* slow = new_head; // 慢指针
        ListNode* fast_left = new_head; // 快指针的前一个结点
        
        while (fast != NULL) {
            if (fast->val < x) {
                // 把 fast 指向的结点链接到 slow 结点后面
                if (slow->next == fast) {
                    slow = slow->next;
                    fast = fast->next;
                    fast_left = fast_left->next;
                } else {
                    fast_left->next = fast->next;
                    fast->next = slow->next;
                    slow->next = fast;
                    
                    fast = fast_left->next;
                    slow = slow->next;
                }
            } else {
                fast = fast->next;
                fast_left = fast_left->next;
            }
            
            // this->displayList(head);
        }
        
        return new_head->next;
    }
    
    void displayList (ListNode* head) {
        if (head == NULL) {
            cout << "List is empty." << endl;
        } else {
            while (head != NULL) {
                cout << head->val << ", ";
                head = head->next;
            }
            cout << "End." << endl;
        }
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    ListNode* head = new ListNode(1);
    head->next = new ListNode(4);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(2);
    head->next->next->next->next = new ListNode(5);
    head->next->next->next->next->next = new ListNode(2);
    int x = 3; // 预期结果 1->2->2->4->3->5
    
//    ListNode* head = new ListNode(2);
//    head->next = new ListNode(1);
//    int x = 2; // 预期结果 1->2
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->partition(head, x);
    if (ans == NULL) {
        cout << "Answer is empty." << endl;
    } else {
        while (ans != NULL) {
            cout << ans->val << ", ";
            ans = ans->next;
        }
        cout << "End." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
