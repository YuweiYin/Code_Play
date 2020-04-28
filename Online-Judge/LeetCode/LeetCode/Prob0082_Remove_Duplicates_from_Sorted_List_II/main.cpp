//
//  main.cpp
//  Prob1082_Remove_Duplicates_from_Sorted_List_II
//
//  Created by 阴昱为 on 2019/8/6.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//82. Remove Duplicates from Sorted List II
//
//Given a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list.
//
//给定一个排序链表，删除所有含有重复数字的节点，只保留原始链表中 没有重复出现 的数字。
//
//Example 1:
//    Input: 1->2->3->3->4->4->5
//    Output: 1->2->5
//
//Example 2:
//    Input: 1->1->1->2->3
//    Output: 2->3


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
    ListNode* deleteDuplicates(ListNode* head) {
        return this->solution1(head);
    }
    
private:
    // 方法一。快慢双指针。时间复杂度 O(N)，空间复杂度 O(1)。N = list.size
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 85.44% 的用户
    // 内存消耗 : 9 MB , 在所有 C++ 提交中击败了 69.95% 的用户
    // Runtime: 8 ms, faster than 85.23% of C++ online submissions for Remove Duplicates from Sorted List II.
    // Memory Usage: 9 MB, less than 99.01% of C++ online submissions for Remove Duplicates from Sorted List II.
    ListNode* solution1 (ListNode* head) {
        // 边界情况
        if (head == NULL || head->next == NULL) {
            return head;
        }
        
        if (head->next->next == NULL) {
            if (head->val == head->next->val) {
                return NULL;
            } else {
                return head;
            }
        }
        
        ListNode* fast = head->next; // 快指针
        ListNode* slow = head; // 慢指针
        ListNode* slow_left = new ListNode(INT_MIN); // 慢指针的左结点
        slow_left->next = head;
        
        while (fast != NULL && fast->next != NULL) {
            if (fast->val != slow->val) {
                // 不重复（已知链表已排序）
                if (slow->next != fast) {
                    // 表示 slow->val 重复了，需要跳过重复部分
                    if (slow == head) {
                        // 若此时慢指针是链头，则需要移动链头
                        head = fast;
                    }
                    slow = fast;
                    slow_left->next = slow;
                    fast = fast->next;
                } else {
                    // 快慢指针均前进
                    slow_left = slow_left->next;
                    slow = slow->next;
                    fast = fast->next;
                }
            } else {
                // 重复了，只让快指针向前进
                fast = fast->next;
            }
        }
        
        // 末尾情况
        if (fast != NULL && fast->val == slow->val) {
            if (slow_left->next == head) {
                return NULL; // 所有值全相同
            } else {
                slow_left->next = NULL;
            }
        } else {
            if (slow->next != fast) {
                // 表示 slow->val 重复了，需要跳过重复部分
                if (slow == head) {
                    // 若此时慢指针是链头，则需要移动链头
                    head = fast;
                }
                slow_left->next = fast;
            } else {
                // 否则表示
            }
        }
        
        return head;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    ListNode* head = new ListNode(1); // 预期结果 4
    head->next = new ListNode(1);
    head->next->next = new ListNode(2);
    head->next->next->next = new ListNode(2);
    head->next->next->next->next = new ListNode(4);
    head->next->next->next->next->next = new ListNode(5);
    head->next->next->next->next->next->next = new ListNode(5);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->deleteDuplicates(head);
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
