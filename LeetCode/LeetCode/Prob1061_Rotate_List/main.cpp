//
//  main.cpp
//  Prob1061_Rotate_List
//
//  Created by 阴昱为 on 2019/7/26.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//61. Rotate List
//
//Given a linked list, rotate the list to the right by k places, where k is non-negative.
//
//给定一个链表，旋转链表，将链表每个节点向右移动 k 个位置，其中 k 是非负数。
//
//Example 1:
//    Input: 1->2->3->4->5->NULL, k = 2
//    Output: 4->5->1->2->3->NULL
//    Explanation:
//        rotate 1 steps to the right: 5->1->2->3->4->NULL
//        rotate 2 steps to the right: 4->5->1->2->3->NULL
//
//Example 2:
//    Input: 0->1->2->NULL, k = 4
//    Output: 2->0->1->NULL
//    Explanation:
//        rotate 1 steps to the right: 2->0->1->NULL
//        rotate 2 steps to the right: 1->2->0->NULL
//        rotate 3 steps to the right: 0->1->2->NULL
//        rotate 4 steps to the right: 2->0->1->NULL


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


// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};


class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        return this->solution1(head, k);
    }
    
private:
    // 方法一。时间复杂度 O(N)，空间复杂度 O(N)。N = list_size
    // 执行用时 : 12 ms , 在所有 C++ 提交中击败了 88.12% 的用户
    // 内存消耗 : 8.7 MB , 在所有 C++ 提交中击败了 98.92% 的用户
    // Runtime: 4 ms, faster than 98.91% of C++ online submissions for Rotate List.
    // Memory Usage: 9 MB, less than 45.73% of C++ online submissions for Rotate List.
    ListNode* solution1 (ListNode* head, int k) {
        // 边界情况
        if (k <= 0) {
            return head;
        }
        
        if (!head || !head->next) {
            return head;
        }
        
        ListNode* end = head;
        ListNode* new_end = head;
        ListNode* new_start = head->next;
        int len = 1;
        
        // ptr 走到末尾，并记录链表长度
        while (end->next) {
            len ++;
            end = end->next;
        }
        
        // 避免循环右移、做无用功
        if (len <= k) {
            k %= len;
        }
        
        if (k == 0) {
            return head;
        }
        
        k = len - k;
        
        // 指针移动到相应位置
        for (int i = 1; i < k; i++) {
            new_start = new_start->next;
            new_end = new_end->next;
        }
        
        // 重新链接 next 指针
        end->next = head;
        new_end->next = NULL;
        
        return new_start;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果
    // 4->5->1->2->3->NULL
    int k = 2;
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(5);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->rotateRight(head, k);
    if (!ans) {
        cout << "Answer is empty." << endl;
    } else {
        while (ans) {
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
