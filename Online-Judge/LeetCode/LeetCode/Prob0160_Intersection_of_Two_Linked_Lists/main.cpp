//
//  main.cpp
//  Prob1160_Intersection_of_Two_Linked_Lists
//
//  Created by 阴昱为 on 2019/6/21.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1160. Intersection of Two Linked Lists
//
//Write a program to find the node at which the intersection of two singly linked lists begins.
//For example, the following two linked lists:
//A:     a1->a2\
//              c1->c2->c3
//B: b1->b2->b3/
//begin to intersect at node c1.
//
//编写一个程序，找到两个单链表相交的起始节点。
//如下面的两个链表：
//A:     a1->a2\
//              c1->c2->c3
//B: b1->b2->b3/
//在节点 c1 开始相交。
//
//Example 1:
//A:    4->1\
//           8->4->5
//B: 5->0->1/
//    Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,0,1,8,4,5], skipA = 2, skipB = 3
//    Output: Reference of the node with value = 8
//    Input Explanation: The intersected node's value is 8 (note that this must not be 0 if the two lists intersect). From the head of A, it reads as [4,1,8,4,5]. From the head of B, it reads as [5,0,1,8,4,5]. There are 2 nodes before the intersected node in A; There are 3 nodes before the intersected node in B.
//
//Example 2:
//A: 0->9->1\
//           2->4
//B:       3/
//    Input: intersectVal = 2, listA = [0,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
//    Output: Reference of the node with value = 2
//    Input Explanation: The intersected node's value is 2 (note that this must not be 0 if the two lists intersect). From the head of A, it reads as [0,9,1,2,4]. From the head of B, it reads as [3,2,4]. There are 3 nodes before the intersected node in A; There are 1 node before the intersected node in B.
//
//Example 3:
//A: 2->6->4
//
//B:    1->5
//    Input: intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
//    Output: null
//    Input Explanation: From the head of A, it reads as [2,6,4]. From the head of B, it reads as [1,5]. Since the two lists do not intersect, intersectVal must be 0, while skipA and skipB can be arbitrary values.
//    Explanation: The two lists do not intersect, so return null.
//
//Notes:
//    If the two linked lists have no intersection at all, return null.
//    The linked lists must retain their original structure after the function returns.
//    You may assume there are no cycles anywhere in the entire linked structure.
//    Your code should preferably run in O(n) time and use only O(1) memory.
//注意：
//    如果两个链表没有交点，返回 null.
//    在返回结果后，两个链表仍须保持原有的结构。
//    可假定整个链表结构中没有循环。
//    程序尽量满足 O(n) 时间复杂度，且仅用 O(1) 内存。


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
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        return this->solution2(headA, headB);
    }
    
private:
    // 方法一。各自遍历一遍求得长度差，第二轮遍历长链表先走，然后齐头并进找到相同结点。
    // 时间复杂度 O(N)，空间复杂度 O(1)
    // 执行用时 : 64 ms , 在所有 C++ 提交中击败了 90.30% 的用户
    // 内存消耗 : 16.8 MB , 在所有 C++ 提交中击败了 17.98% 的用户
    // Runtime: 48 ms, faster than 91.15% of C++ online submissions for Intersection of Two Linked Lists.
    // Memory Usage: 16.7 MB, less than 73.81% of C++ online submissions for Intersection of Two Linked Lists.
    ListNode* solution1(ListNode *headA, ListNode *headB) {
        // 某结点为空，必无交点
        if (!headA || !headB) {
            return NULL;
        }
        // 二者都仅有一个结点，若该结点不相等，则无交点
        if (!headA->next && !headB->next) {
            return headA == headB ? headA : NULL;
        }
        
        ListNode* res = NULL;
        
        ListNode* ptr_A = headA;
        ListNode* ptr_B = headB;
        int len_A = 0;
        int len_B = 0;
        
        // 1. 各自遍历一遍求得长度差
        while (ptr_A) {
            len_A ++;
            ptr_A = ptr_A->next;
        }
        
        while (ptr_B) {
            len_B ++;
            ptr_B = ptr_B->next;
        }
        
        ptr_A = headA;
        ptr_B = headB;
        int diff = abs(len_A - len_B);
        
        // 2. 第二轮遍历长链表先走
        if (len_A > len_B) {
            for (int i = 0; i < diff; i++) {
                if (ptr_A) {
                    ptr_A = ptr_A->next;
                } else {
                    return NULL; // 异常
                }
            }
        } else if (len_A < len_B) {
            for (int i = 0; i < diff; i++) {
                if (ptr_B) {
                    ptr_B = ptr_B->next;
                } else {
                    return NULL; // 异常
                }
            }
        }
        
        // 3. 齐头并进找到相同结点
        while (ptr_A && ptr_B) {
            if (ptr_A == ptr_B) {
                return ptr_A;
            }
            
            ptr_A = ptr_A->next;
            ptr_B = ptr_B->next;
        }
        
        return res;
    }
    
    // 方法二。各自遍历，到末尾则从另一链表头继续前进，直到遇到相同结点，或者第二次到尾(return NULL)。
    // 因为如果有交点，那么第二遍遍历时，二者走相同的结点个数就能到交点处。
    // len_A = x1+y, len_B = x2+y.  x1+y+x2 == x2+y+x1
    // 时间复杂度 O(N)，空间复杂度 O(1)
    // Runtime: 52 ms, faster than 80.04% of C++ online submissions for Intersection of Two Linked Lists.
    // Memory Usage: 16.8 MB, less than 29.94% of C++ online submissions for Intersection of Two Linked Lists.
    ListNode* solution2(ListNode *headA, ListNode *headB) {
        // 某结点为空，必无交点
        if (!headA || !headB) {
            return NULL;
        }
        // 二者都仅有一个结点，若该结点不相等，则无交点
        if (!headA->next && !headB->next) {
            return headA == headB ? headA : NULL;
        }
        
        ListNode* res = NULL;
        
        ListNode* ptr_A = headA;
        ListNode* ptr_B = headB;
        
        bool reach_tail_A = true; // false 表示第一次到达末尾
        bool reach_tail_B = true;
        
        // 各自遍历，到末尾则从另一链表头继续前进，直到遇到相同结点，或者第二次到尾(return NULL)。
        while (ptr_A && ptr_B) {
            if (ptr_A == ptr_B) {
                return ptr_A;
            }
            
            if (ptr_A->next) {
                ptr_A = ptr_A->next;
            } else {
                if (reach_tail_A) {
                    reach_tail_A = false;
                    ptr_A = headB;
                } else {
                    return NULL;
                }
            }
            
            if (ptr_B->next) {
                ptr_B = ptr_B->next;
            } else {
                if (reach_tail_B) {
                    reach_tail_B = false;
                    ptr_B = headA;
                } else {
                    return NULL;
                }
            }
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
    ListNode* headA = new ListNode(4);
    headA->next = new ListNode(1);
    
    ListNode* headB = new ListNode(5);
    headB->next = new ListNode(0);
    headB->next->next = new ListNode(1);
    
    headB->next->next->next = headA->next->next = new ListNode(8);
    headB->next->next->next->next = headA->next->next->next = new ListNode(4);
    headB->next->next->next->next->next = headA->next->next->next->next = new ListNode(5);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->getIntersectionNode(headA, headB);
    if (ans) {
        cout << ans->val << endl;
    } else {
        cout << "Null." << endl;
    }
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
