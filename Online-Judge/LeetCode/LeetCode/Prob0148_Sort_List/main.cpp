//
//  main.cpp
//  Prob1148_Sort_List
//
//  Created by 阴昱为 on 2019/6/15.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1148. Sort List
//
//Sort a linked list in O(n log n) time using constant space complexity.
//
//在 O(n log n) 时间复杂度和常数级空间复杂度下，对链表进行排序。
//
//Example 1:
//    Input: 4->2->1->3
//    Output: 1->2->3->4
//
//Example 2:
//    Input: -1->5->3->4->0
//    Output: -1->0->3->4->5


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
    ListNode* sortList(ListNode* head) {
        return this->solution1(head);
    }
    
private:
    // 方法一。分治法，二路归并排序。时间复杂度 O(NlogN)，空间复杂度 O(1)
    ListNode* solution1(ListNode* head) {
        if (!head) {
            return NULL;
        }
        
        if (!head->next) {
            return head;
        }
        
        // 用一快一慢指针移动，找到中间位置
        ListNode* fast = head->next;
        ListNode* slow = head;
        
        while (fast && fast->next) {
            fast = fast->next->next;
            slow = slow->next;
        }
        
        // 从中间位置切开原链表为两部分
        ListNode* mid = slow->next;
        slow ->next = NULL;
        
        // 切分至最细，即满足 !head 或 !head->next
        ListNode* left = this->solution1(head);
        ListNode* right = this->solution1(mid);
        
        // 分而治之，返回合并结果
        return this->mergeSort(left, right);
    }
    
    ListNode* mergeSort (ListNode* l1, ListNode* l2) {
        ListNode* head = new ListNode(MIN_INT32);
        ListNode* res = head;
        
        // 此处使用链接的方式构造结果链表，不增加空间消耗，但会破坏原链表结构
        while (l1 && l2) {
            if (l1->val <= l2->val) {
                res->next = l1;
                l1 = l1->next;
            } else {
                res->next = l2;
                l2 = l2->next;
            }
            res = res->next;
        }
        
        // 把 l1 或 l2 的剩余部分直接链接到 res 尾部
        if (l1) {
            res->next = l1;
        } else {
            res->next = l2;
        }
        
        // 返回头结点
        return head->next;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    ListNode* head = new ListNode(-1);
    head->next = new ListNode(5);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(0);
    head->next->next->next->next->next = new ListNode(-3);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->sortList(head);
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
