//
//  main.cpp
//  Prob1143_Reorder_List
//
//  Created by 阴昱为 on 2019/6/21.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1143. Reorder List
//
//Given a singly linked list L: L0→L1→…→Ln-1→Ln,
//reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…
//You may not modify the values in the list's nodes, only nodes itself may be changed.
//
//给定一个单链表 L：L0→L1→…→Ln-1→Ln ，
//将其重新排列后变为： L0→Ln→L1→Ln-1→L2→Ln-2→…
//你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。
//
//Example 1:
//    Given 1->2->3->4, reorder it to 1->4->2->3.
//
//Example 2:
//    Given 1->2->3->4->5, reorder it to 1->5->2->4->3.


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
    void reorderList(ListNode* head) {
        this->solution2(head);
    }
    
private:
    // 方法一。一遍扫描，用向量记录每个结点的指针，在向量中改变结点链接结构。
    // 时间复杂度 O(N)，空间复杂度 O(N)
    // Runtime: 48 ms, faster than 88.53% of C++ online submissions for Reorder List.
    // Memory Usage: 13.2 MB, less than 13.10% of C++ online submissions for Reorder List.
    void solution1(ListNode* head) {
        // 结点数目小于等于 2，不用重排
        if (!head || !head->next || !head->next->next) {
            return;
        }
        
        vector<ListNode*> node_vec = {};
        ListNode* ptr = head;
        
        while (ptr) {
            node_vec.emplace_back(ptr);
            ptr = ptr->next;
        }
        
        int len = (int)node_vec.size();
        int mid = (int)(len / 2);
        
        // 把 node_vec[i] 链接到 node_vec[len - 1 - i] 的后面
        for (int i = len - 1; i > mid; i--) {
            node_vec[i]->next = node_vec[len - 1 - i]->next;
            node_vec[len - 1 - i]->next = node_vec[i];
        }
        
        // 最终 node_vec[mid] 是末尾结点
        node_vec[mid]->next= NULL;
        
        return;
    }
    
    // 方法二：一遍扫描，反转后半部分链表，然后合并前后两个子链表。
    // 时间复杂度 O(N)，空间复杂度 O(1)
    // Runtime: 48 ms, faster than 88.53% of C++ online submissions for Reorder List.
    // Memory Usage: 12.1 MB, less than 74.25% of C++ online submissions for Reorder List.
    void solution2 (ListNode* head) {
        // 1. 快慢双指针，将链表分成两段
        // 2. 将链表后半段进行反转
        // 3. 交替合并两段链表
        
        // 结点数目小于等于 2，不用重排
        if (!head || !head->next || !head->next->next) {
            return;
        }
        
        ListNode* fast = head;
        ListNode* slow = head;
        
        // 快慢双指针，将链表分成两段
        while (fast->next) {
            fast = fast->next;
            if (fast->next) {
                fast = fast->next;
            } else {
                break;
            }
            slow = slow->next;
        }
        
        // cout << slow->val << ", " << fast->val << endl;
        
        // 此时 slow 位于中间结点，是右半部分子链表首结点的前驱结点，也是最终链表的尾部
        // 反转右侧链表。slow->next == fast 表示右侧只有一个结点，无需反转
        ListNode* left = slow->next;
        ListNode* right = slow->next;
        ListNode* right_next;
        
        if (slow->next && slow->next != fast) {
            right = right->next;

            while (right) {
                right_next = right->next; // 记录下一个结点位置
                
                right->next = left; // 反转链接

                left = right; // 向后移动
                right = right_next;
            }
        }
        
        slow->next->next = NULL;
        slow->next = NULL;
        
        // 此时分成了两个子链表，左侧 head->..->slow->NULL，右侧 left->..->NULL
        // 合并两个链表。最终链表以 slow 结尾
        ListNode* first = head; // 左侧
        ListNode* first_next = head;
        ListNode* second = left; // 右侧
        ListNode* second_next = left;
        
        while (second && first) {
            first_next = first->next; // 记录下一个结点位置
            second_next = second->next;
            
            second->next = first_next; // 修改链接方式
            first->next = second;
            
            first = first_next; // 向后移动
            second = second_next;
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
    head->next = new ListNode(2);
    head->next->next = new ListNode(3); // 预期结果 1->3->2
    head->next->next->next = new ListNode(4); // 预期结果 1->4->2->3
    head->next->next->next->next = new ListNode(5); // 预期结果 1->5->2->4->3
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->reorderList(head);
    if (head) {
        while (head) {
            cout << head->val << "->";
            head = head->next;
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
