//
//  main.cpp
//  Prob1002_Add_Two_Numbers
//
//  Created by 阴昱为 on 2019/5/28.
//  Copyright © 2019 阴昱为. All rights reserved.
//


//2. Add Two Numbers
//
//You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

//You may assume the two numbers do not contain any leading zero, except the number 0 itself.
//
//给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
//你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。
//
//Example:
//Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
//Output: 7 -> 0 -> 8
//Explanation: 342 + 465 = 807.


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


// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode *result = NULL;
        
        if (l1 == NULL && l2 == NULL) {
            return result;
        }
        
        ListNode *ptr1 = l1;
        ListNode *ptr2 = l2;
        ListNode *head = NULL; // 头结点指针
        int carry = 0; // 进位
        int addition = 0; // 当前加和
        int first_flag = true; // 头结点标志
        
        // 结束条件：链表 l1 和链表 l2 均已遍历结束，并且没有进位
        while (!(ptr1 == NULL && ptr2 == NULL && carry == 0)) {
            // 本轮加和
            addition = carry;
            if (ptr1 != NULL) {
                addition += ptr1->val;
                ptr1 = ptr1->next;
            }
            if (ptr2 != NULL) {
                addition += ptr2->val;
                ptr2 = ptr2->next;
            }
            
            // 判断是否进位
            if (addition >= 10) {
                addition -= 10;
                carry = 1;
            } else {
                carry = 0;
            }
            
            // 创建新结点，记录本轮结果
            ListNode *new_node = new ListNode(addition);
            if (first_flag) {
                // 如果是第一次，则记录头结点位置
                first_flag = false;
                
                result = new_node;
                head = result;
            } else {
                result->next = new_node;
                result = result->next;
            }
        }
        
        return head;
    }
};


int main(int argc, const char * argv[]) {
    // 设置测试数据
    ListNode *number1 = new ListNode(2);
    number1->next = new ListNode(4);
    number1->next->next = new ListNode(5);
    number1->next->next->next = new ListNode(7);
    
    ListNode *number2 = new ListNode(5);
    number2->next = new ListNode(6);
    number2->next->next = new ListNode(4);
    
    // 调用解决方案，获得处理结果
    Solution *solution = new Solution();
    ListNode *result = solution->addTwoNumbers(number1, number2);
    
    // 输出展示结果
    for (ListNode *ptr = result; ptr != NULL; ptr = ptr->next) {
        cout << "result: " << ptr->val << endl;
    }
    
    return 0;
}
