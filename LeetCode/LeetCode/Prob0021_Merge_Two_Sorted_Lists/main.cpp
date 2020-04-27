//
//  main.cpp
//  Prob1021_Merge_Two_Sorted_Lists
//
//  Created by 阴昱为 on 2019/6/15.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1021. Merge Two Sorted Lists
//
//Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the nodes of the first two lists.
//
//将两个有序链表合并为一个新的有序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。
//
//Example:
//    Input: 1->2->4, 1->3->4
//    Output: 1->1->2->3->4->4


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
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        return this->solution1(l1, l2);
    }
    
private:
    // 方法一。时间复杂度 O(m+n)，空间复杂度 O(m+n)
    // 可以通过修改 next 指针，改进算法的空间复杂度到 O(1)
    ListNode* solution1(ListNode* l1, ListNode* l2) {
        ListNode* res = NULL;
        
        // 边界条件，如果其中一个链表为空，则返回另一个链表
        if (!l1) {
            return l2;
        }
        
        if (!l2) {
            return l1;
        }
        
        ListNode* ptr1 = l1;
        ListNode* ptr2 = l2;
        
        // 给结果链表头赋初值
        if (ptr1->val <= ptr2->val) {
            // cout << "Init: " << ptr1->val << endl;
            res = new ListNode(ptr1->val);
            ptr1 = ptr1->next;
        } else {
            // cout << "Init: " << ptr2->val << endl;
            res = new ListNode(ptr2->val);
            ptr2 = ptr2->next;
        }
        
        // 记录结果链表头
        ListNode* head = res;
        
        // 在两个链表均不空的情况下，每次把较小数加入结果链表
        while (ptr1 && ptr2) {
            if (ptr1->val <= ptr2->val) {
                // cout << "Add: " << ptr1->val << endl;
                res->next = new ListNode(ptr1->val);
                res = res->next;
                
                ptr1 = ptr1->next;
            } else {
                // cout << "Add: " << ptr2->val << endl;
                res->next = new ListNode(ptr2->val);
                res = res->next;
                
                ptr2 = ptr2->next;
            }
        }
        
        // 处理 l1 链表有剩余结点的情况
        while (ptr1) {
            // cout << "Rest: " << ptr1->val << endl;
            res->next = new ListNode(ptr1->val);
            res = res->next;
            
            ptr1 = ptr1->next;
        }
        
        // 处理 l2 链表有剩余结点的情况
        while (ptr2) {
            // cout << "Rest: " << ptr2->val << endl;
            res->next = new ListNode(ptr2->val);
            res = res->next;
            
            ptr2 = ptr2->next;
        }
        
        // 返回结果链表头
        return head;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    ListNode* l1 = new ListNode(1);
    l1->next = new ListNode(2);
    l1->next->next = new ListNode(4);
    
    ListNode* l2 = new ListNode(1);
    l2->next = new ListNode(3);
    l2->next->next = new ListNode(4);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->mergeTwoLists(l1, l2);
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
