//
//  main.cpp
//  Prob1445_Add_Two_Numbers_II
//
//  Created by 阴昱为 on 2019/6/21.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1445. Add Two Numbers II
//
//You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.
//You may assume the two numbers do not contain any leading zero, except the number 0 itself.
//
//Follow up:
//    What if you cannot modify the input lists? In other words, reversing the lists is not allowed.
//
//给定两个非空链表来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储单个数字。将这两数相加会返回一个新的链表。
//你可以假设除了数字 0 之外，这两个数字都不会以零开头。
//
//进阶:
//    如果输入链表不能修改该如何处理？换句话说，你不能对列表中的节点进行翻转。
//
//Example:
//    Input: (7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
//    Output: 7 -> 8 -> 0 -> 7


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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        return this->solution1(l1, l2);
    }
    
private:
    // 方法一。向量模拟栈，修改长链表的各结点值。
    // 时间复杂度 O(N)，空间复杂度 O(N)
    // 执行用时 : 44 ms , 在所有 C++ 提交中击败了 73.07% 的用户
    // 内存消耗 : 11.5 MB , 在所有 C++ 提交中击败了 93.06% 的用户
    // Runtime: 28 ms, faster than 75.42% of C++ online submissions for Add Two Numbers II.
    // Memory Usage: 11.3 MB, less than 66.26% of C++ online submissions for Add Two Numbers II.
    ListNode* solution1(ListNode* l1, ListNode* l2) {
        ListNode* res = new ListNode(0);
        
        if (!l1 && !l2) {
            return res;
        }
        
        if (!l1 && l2 != NULL) {
            return l2;
        }
        
        if (!l2 && l1 != NULL) {
            return l1;
        }
        
        ListNode* ptr_1 = l1;
        ListNode* ptr_2 = l2;
        
        // 直接用 vector 模拟栈，只移动下标、不做 pop 操作，比栈快
        vector<ListNode*> num_1 = {};
        vector<ListNode*> num_2 = {};
        
        while (ptr_1) {
            num_1.emplace_back(ptr_1);
            ptr_1 = ptr_1->next;
        }
        
        while (ptr_2) {
            num_2.emplace_back(ptr_2);
            ptr_2 = ptr_2->next;
        }
        
        int len_1 = (int)num_1.size();
        int len_2 = (int)num_2.size();
        
        int i, j;
        
        if (len_1 >= len_2) {
            for (i = len_1 - 1, j = len_2 - 1; i >= 0 && j >= 0; i--, j--) {
                // 相加，值赋给较长的链表
                num_1[i]->val += num_2[j]->val;
                
                // 进位情况
                if (num_1[i]->val >= 10) {
                    num_1[i]->val -= 10;
                    
                    if (i > 0) {
                        num_1[i - 1]->val += 1;
                    } else {
                        // 如果长列表到头了，还有进位，则需增加头结点
                        ListNode* head = new ListNode(1);
                        head->next = num_1[0];
                        return head;
                    }
                }
            }
            
            for (; i >= 0; i--) {
                // 进位情况
                if (num_1[i]->val >= 10) {
                    num_1[i]->val -= 10;
                    
                    if (i > 0) {
                        num_1[i - 1]->val += 1;
                    } else {
                        // 如果长列表到头了，还有进位，则需增加头结点
                        ListNode* head = new ListNode(1);
                        head->next = num_1[0];
                        return head;
                    }
                }
            }
            
            res = num_1[0];
        } else {
            for (i = len_1 - 1, j = len_2 - 1; i >= 0 && j >= 0; i--, j--) {
                // 相加，值赋给较长的链表
                num_2[j]->val += num_1[i]->val;
                
                // 进位情况
                if (num_2[j]->val >= 10) {
                    num_2[j]->val -= 10;
                    
                    if (j > 0) {
                        num_2[j - 1]->val += 1;
                    } else {
                        // 如果长列表到头了，还有进位，则需增加头结点
                        ListNode* head = new ListNode(1);
                        head->next = num_2[0];
                        return head;
                    }
                }
            }
            
            for (; j >= 0; j--) {
                // 进位情况
                if (num_2[j]->val >= 10) {
                    num_2[j]->val -= 10;
                    
                    if (j > 0) {
                        num_2[j - 1]->val += 1;
                    } else {
                        // 如果长列表到头了，还有进位，则需增加头结点
                        ListNode* head = new ListNode(1);
                        head->next = num_2[0];
                        return head;
                    }
                }
            }
            
            res = num_2[0];
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
    // 预期结果 8
    ListNode* l1 = new ListNode(9);
//    l1->next = new ListNode(4);
//    l1->next->next = new ListNode(4);
//    l1->next->next->next = new ListNode(3);
    
    ListNode* l2 = new ListNode(9);
    l2->next = new ListNode(9);
    l2->next->next = new ListNode(9);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->addTwoNumbers(l1, l2);
    if (ans) {
        while (ans) {
            cout << ans->val << "->";
            ans = ans->next;
        }
        cout << "End." << endl;
    } else {
        cout << "Answer is Null." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
