//
//  main.cpp
//  Prob1147_Insertion_Sort_List
//
//  Created by 阴昱为 on 2019/6/16.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1147. Insertion Sort List
//
//Sort a linked list using insertion sort.
//A graphical example of insertion sort. The partial sorted list (black) initially contains only the first element in the list.
//With each iteration one element (red) is removed from the input data and inserted in-place into the sorted list
//
//Algorithm of Insertion Sort:
//    1. Insertion sort iterates, consuming one input element each repetition, and growing a sorted output list.
//    2. At each iteration, insertion sort removes one element from the input data, finds the location it belongs within the sorted list, and inserts it there.
//    3. It repeats until no input elements remain.
//
//对链表进行插入排序。
//插入排序的动画演示如上。从第一个元素开始，该链表可以被认为已经部分排序（用黑色表示）。
//每次迭代时，从输入数据中移除一个元素（用红色表示），并原地将其插入到已排好序的链表中。
//
//插入排序算法：
//    1. 插入排序是迭代的，每次只移动一个元素，直到所有元素可以形成一个有序的输出列表。
//    2. 每次迭代中，插入排序只从输入数据中移除一个待排序的元素，找到它在序列中适当的位置，并将其插入。
//    3. 重复直到所有输入数据插入完为止。
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
    ListNode* insertionSortList(ListNode* head) {
        return this->solution1(head);
    }
    
private:
    // 方法一。插入排序，时间复杂度 O(N^2)，空间复杂度 O(N)
    ListNode* solution1(ListNode* head) {
        if (!head || !head->next) {
            return head;
        }
        
        // ListNode* res_head = head;
        ListNode* ptr1 = head; // 主遍历指针
        ListNode* ptr2 = head; // 寻找 key 应该插入的位置
        ListNode* pre = head; // 指向 ptr2 的前一个结点
        
        // ptr1 每一次比较的 key
        while (ptr1->next) {
            // 如果是升序，则继续找，直到找到不满足排序的结点 ptr1->next
            if (ptr1->val <= ptr1->next->val) {
                ptr1 = ptr1->next;
                continue;
            }
            
            // 此时 ptr1 的值比 ptr1->next 的值更大，则以 ptr1->next 为 key，插入
            // 此时 ptr2 指向链头，从 ptr2 开始为 key 找合适的插入位置
            if (ptr2 && ptr1->next->val <= ptr2->val) {
                // 找到了该插入的位置，把 ptr1->next 结点放到 ptr2 前面
                ListNode* temp = ptr1->next;
                ptr1->next = temp->next; // 让 ptr1 的 next 跳过原 ptr1->next 指向原 ptr1->next->next
                temp->next = ptr2; // 让原 ptr1 的 next 指向 ptr2
                
                if (ptr2 == head) {
                    // 如果 ptr2 原本是 head 链头，则修改链头为 temp（原 ptr1->next）
                    // pre 本身是指向 head 的，所以 pre 也 = temp 了，表示 pre 仍指向 ptr2 的前一结点
                    head = temp;
                } else {
                    // pre 原本作为 ptr2 的前一结点，其 next 指向 temp（原 ptr1->next），就把 ptr1->next 放在 ptr2 前了
                    pre->next = temp;
                }
                
                // ptr2 再次指向链头
                ptr2 = head;
            } else {
                // 否则 ptr1->next 更大，ptr1->next 不该插入到 ptr2 前
                // 因此需要向后移动 ptr2，直到满足 ptr2 的值大于 ptr1->next
                // ptr2 往后移动，pre 指向 ptr2 的前一个结点
                pre = ptr2;
                ptr2 = ptr2->next;
                continue;
            }
        }
        
        return head;
    }
    
    // 方法二。分治法，二路归并排序。时间复杂度 O(NlogN)，空间复杂度 O(1)
    ListNode* solution2(ListNode* head) {
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
    // 预期结果 -1->0->3->4->5
    ListNode* head = new ListNode(-1);
    head->next = new ListNode(5);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);
    head->next->next->next->next = new ListNode(0);
    
//    ListNode* head = new ListNode(1);
//    head->next = new ListNode(1);
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->insertionSortList(head);
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
