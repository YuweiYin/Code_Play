//
//  main.cpp
//  Prob1019_Remove_Nth_Node_From_End_of_List
//
//  Created by 阴昱为 on 2019/6/12.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//19. Remove Nth Node From End of List
//
//Given a linked list, remove the n-th node from the end of list and return its head.
//
//给定一个链表，删除链表的倒数第 n 个节点，并且返回链表的头结点。
//
//Example:
//    Given linked list: 1->2->3->4->5, and n = 2.
//    After removing the second node from the end, the linked list becomes 1->2->3->5.
//Note:
//    Given n will always be valid.
//    给定的 n 保证是有效的。
//Follow up:
//    Could you do this in one pass?
//    你能尝试使用一趟扫描实现吗？


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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        return this->solution1(head, n);
    }
    
private:
    // 方法一：三指针，一趟扫描完成
    ListNode* solution1 (ListNode* head, int n) {
        if (!head || n <= 0) {
            return head;
        }
        
        ListNode* res = head;
        ListNode* ptr_left_pre = head;
        ListNode* ptr_left = head;
        ListNode* ptr_right = head;
        bool move_flag = false;
        
        // 让 ptr_right 先走 n - 1 步
        for (int i = 0; i < n - 1; i++) {
            // 若未移动够 n - 1 步就到尾部了，表示 n 大于链表总长度，该倒数第 n 个元素删除不到
            if (!ptr_right) {
                return head;
            }
            ptr_right = ptr_right->next;
        }
        if (!ptr_right) {
            return head;
        }
        
        // 往后移动
        while (ptr_right->next) {
            if (!move_flag) {
                move_flag = true;
            } else {
                // 从第二次移动开始，ptr_left 的前结点也跟着移动
                ptr_left_pre = ptr_left_pre->next;
            }
            ptr_left = ptr_left->next;
            ptr_right = ptr_right->next;
        }
        
        // 此时 ptr_right 是最后一个结点，ptr_left 是倒数第 n 个结点、需要删除
        // ptr_left_pre 是倒数第 n + 1 个结点
        // 如果链表仅有 n 个结点，此时 ptr_left 和 ptr_left_pre 都为 head、需要删除 head
        if (ptr_left == head) {
            res = head->next;
            delete head;
        } else {
            ptr_left_pre->next = ptr_left->next;
            delete ptr_left;
        }
        
        return res;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    
    start = clock();
    
    // 设置测试数据
    // 预期结果 ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(5);
    
    int n = 2;
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->removeNthFromEnd(head, n);
    if (ans) {
        ListNode* ptr = ans;
        while (ptr) {
            cout << ptr->val << endl;
            ptr = ptr->next;
        }
    } else {
        cout << "No Answer." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
