//
//  main.cpp
//  Prob1023_Merge_k_Sorted_Lists
//
//  Created by 阴昱为 on 2019/6/15.
//  Copyright © 2019 阴昱为. All rights reserved.
//

//1023. Merge k Sorted Lists
//
//Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.
//
//合并 k 个排序链表，返回合并后的排序链表。请分析和描述算法的复杂度。
//
//Example:
//    Input:
//    [
//      1->4->5,
//      1->3->4,
//      2->6
//    ]
//    Output: 1->1->2->3->4->4->5->6


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
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        return this->solution2(lists);
    }
    
private:
    // 方法一。暴力法。时间复杂度 O(NlogN)，空间复杂度 O(N)
    // 遍历 lists 存储所有的 val 值，然后排序，然后生成新链表
    ListNode* solution1(vector<ListNode*>& lists) {
        // 清除空链表
        for (auto ite = lists.begin(); ite < lists.end(); ite++) {
            if (!(*ite)) {
                lists.erase(ite);
                ite --;
            }
        }
        
        if (lists.empty()) {
            return NULL;
        }
        
        // 遍历第一遍，存储 val 值
        vector<int> value = {};
        for (int i = 0; i < (int)lists.size(); i++) {
            while (lists[i]) {
                value.push_back(lists[i]->val);
                lists[i] = lists[i]->next;
            }
        }
        
        // 向量排序
        sort(value.begin(), value.end());
        
        // 构造结果链表
        ListNode* res = new ListNode(MIN_INT32);
        ListNode* head = res;
        for (int i = 0; i < (int)value.size(); i++) {
            res->next = new ListNode(value[i]);
            res = res->next;
        }
        
        // 返回结果链表头
        return head->next;
    }
    
    // 方法二。分治法，二路归并排序，两两合并链表(链表总数为k)。
    // 时间复杂度 O(Nlogk)，空间复杂度 O(N)或O(1)
    ListNode* solution2(vector<ListNode*>& lists) {
        // 清除空链表
        for (auto ite = lists.begin(); ite < lists.end(); ite++) {
            if (!(*ite)) {
                lists.erase(ite);
                ite --;
            }
        }
        
        if (lists.empty()) {
            return NULL;
        }
        
        int lists_len = (int)lists.size();
        int interval = 1; // 合并的间隔，1->2->4->8->...
        
        while (interval < lists_len) {
            // 简单解释二路归并排序过程：假设 lists_len 等于 5
            // 第一轮 while 循环结束后，新 lists[0] 存储原 lists[0] 和 lists[1] 的合并链表
            // 新 lists[2] 存储原 lists[2] 和 lists[3] 的合并链表，lists[4] 不变
            // 第二轮 while 循环结束后，新 lists[0] 存储上一轮 lists[0] 和 lists[2] 的合并链表
            // lists[4] 仍然没有与之结合的链表，所以仍然不变
            // 第三轮，interval == 4，新 lists[0] 存储 lists[0] 与 lists[4] 的合并链表，即最终解
            for (int i = 0; i < (lists_len - interval); i += interval * 2) {
                // cout << "i=" << i << ", i + interval=" << i + interval << endl;
                lists[i] = this->mergeSort(lists[i], lists[i + interval]);
            }
            interval *= 2;
        }
        
        // 返回结果链表头
        return lists[0];
    }
    
    // 合并排序两个有序链表
    ListNode* mergeSort (ListNode* l1, ListNode* l2) {
        ListNode* head = new ListNode(MIN_INT32);
        ListNode* res = head;
        ListNode* ptr1 = l1;
        ListNode* ptr2 = l2;
        
        // 此处使用链接的方式构造结果链表，不增加空间消耗，但会破坏原链表结构
        while (ptr1 && ptr2) {
            if (ptr1->val <= ptr2->val) {
                res->next = ptr1;
                ptr1 = ptr1->next;
            } else {
                res->next = ptr2;
                ptr2 = ptr2->next;
            }
            res = res->next;
        }
        
        // 把 l1 或 l2 的剩余部分直接链接到 res 尾部
        if (ptr1) {
            res->next = ptr1;
        } else {
            res->next = ptr2;
        }
        
        // 返回头结点
        return head->next;
    }
    
    // 方法三：逐一比较 k 个链表的头结点，谁最小就让它加入结果结点
    // 时间复杂度 O(kN)，空间复杂度 O(N)
    
    // 方法四：优先队列
    // 时间复杂度 O(Nlogk)，空间复杂度 O(N)
    
    // 方法三：逐一两两合并链表
    // 时间复杂度 O(kN)，空间复杂度 O(N)或O(1)
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    ListNode* l1 = new ListNode(1);
    l1->next = new ListNode(4);
    l1->next->next = new ListNode(5);
    
    ListNode* l2 = new ListNode(1);
    l2->next = new ListNode(3);
    l2->next->next = new ListNode(4);
    
    ListNode* l3 = new ListNode(2);
    l3->next = new ListNode(6);
    
    ListNode* l4 = NULL;
    
    ListNode* l5 = new ListNode(4);
    l5->next = new ListNode(7);
    l5->next->next = new ListNode(9);
    
    ListNode* l6 = new ListNode(3);
    l6->next = new ListNode(6);
    l6->next->next = new ListNode(8);
    
    vector<ListNode*> lists = {l1, l2 ,l3, l4, l5, l6};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    ListNode* ans = solution->mergeKLists(lists);
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
