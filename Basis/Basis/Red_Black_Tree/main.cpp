//
//  main.cpp
//  Red_Black_Tree
//
//  Created by 阴昱为 on 2019/6/1.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include <iostream>
#include <time.h>
#include <iterator>
#include <vector>
#include <algorithm>
#include "RBTree.h"
using namespace std;

typedef long long ll;

//const ll MOD = 1e9+7;


int main(int argc, const char * argv[]) {
    // 计时
    clock_t start, finish;
    double prog_duration;
    start = clock();
    
    vector<int> nodes = {10, 40, 30, 60, 90, 70, 20, 50, 80};
    
    // int a[]= {10, 40, 30, 60, 90, 70, 20, 50, 80};
    int check_insert = 0; // 手动设置"插入"动作的检测开关(0，关闭；1，打开)
    int check_remove = 0; // 手动设置"删除"动作的检测开关(0，关闭；1，打开)
    int i;
    // int ilen = (sizeof(a)) / (sizeof(a[0])); // 数据个数
    int ilen = (int)nodes.size(); // 数据个数
    RBTree<int>* tree = new RBTree<int>();
    
    cout << "== 原始数据: ";
    for(i = 0; i < ilen; i++)
        // cout << a[i] <<" ";
        cout << nodes[i] <<" ";
    cout << endl;
    
    for (i = 0; i < ilen; i++) {
        // 通过插入结点的方式构造红黑树（插入过程会自动调整平衡）
        // tree->insert(a[i]);
        tree->insert(nodes[i]);
        
        // 如果设置check_insert=1,逐步测试"添加函数"
        if (check_insert) {
            // cout << "== 添加节点: " << a[i] << endl;
            cout << "== 添加节点: " << nodes[i] << endl;
            cout << "== 树的详细信息: " << endl;
            tree->print();
            cout << endl;
        }
    }
    
    // 遍历
    cout << "== 前序遍历: ";
    tree->preOrder();
    
    cout << "\n== 中序遍历: ";
    tree->inOrder();
    
    cout << "\n== 后序遍历: ";
    tree->postOrder();
    cout << endl;
    
    // 最值
    cout << "== 最小值: " << tree->minimum() << endl;
    cout << "== 最大值: " << tree->maximum() << endl;
    
    // 树的详情
    cout << "== 树的详细信息: " << endl;
    tree->print();
    
    // 如果设置check_remove=1,逐步测试"删除函数"
    if (check_remove) {
        for (i = 0; i < ilen; i++) {
            // tree->remove(a[i]);
            tree->remove(nodes[i]);
            
            // cout << "== 删除节点: " << a[i] << endl;
            cout << "== 删除节点: " << nodes[i] << endl;
            cout << "== 树的详细信息: " << endl;
            tree->print();
            cout << endl;
        }
    }
    
    // 销毁红黑树
    tree->destroy();
    
    // 计时
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序耗时: " << prog_duration << "ms." << endl;
    
    return 0;
}
