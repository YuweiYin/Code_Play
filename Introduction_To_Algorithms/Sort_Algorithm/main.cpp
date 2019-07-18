//
//  main.cpp
//  Sort_Algorithm
//
//  Created by 阴昱为 on 2019/7/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include "Header.h"
#include "Insertion_Sort.cpp"
#include "Merge_Sort.cpp"

class Solution {
public:
    void sortVector (vector<int>& nums) {
        this->solution2(nums);
    }
    
private:
    // 方法一：插入排序。时间复杂度 Theta(N^2)，空间复杂度 O(1)。N = nums.size
    void solution1 (vector<int>& nums) {
        InsertionSort<int>* i_sort = new InsertionSort<int>();
        i_sort->insertionSort(nums); // default: increasing order
//        i_sort->insertionSort(nums, false, increasingOrder); // increasing order
//        i_sort->insertionSort(nums, true, increasingOrder); // decreasing order
//        i_sort->insertionSort(nums, true, decreasingOrder); // increasing order
    }
    
    // 方法一：归并排序。时间复杂度 Theta(N lg N)，空间复杂度 O(N)。N = nums.size
    // 可以通过对 merge 过程的优化，不使用辅助数组，以使得空间复杂度降为 O(1) 或者 O(lg N) 因为递归栈
    void solution2 (vector<int>& nums) {
        MergeSort<int>* m_sort = new MergeSort<int>();
        m_sort->mergeSort(nums, 0, (int)nums.size() - 1); // default: increasing order
//        m_sort->mergeSort(nums, 0, (int)nums.size() - 1, false, increasingOrder); // increasing order
//        m_sort->mergeSort(nums, 0, (int)nums.size() - 1, true, increasingOrder); // decreasing order
//        m_sort->mergeSort(nums, 0, (int)nums.size() - 1, true, decreasingOrder); // increasing order
    }
    
    static bool increasingOrder (int a, int b) {
        return a < b;
    }
    
    static bool decreasingOrder (int a, int b) {
        return a > b;
    }
};


int main(int argc, const char * argv[]) {
    // 计时
    time_t start, finish;
    double prog_duration;
    start = clock();
    
    // 设置测试数据
    // 预期结果 {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    vector<int> nums = {5, 3, 8, 2, 6, 7, 1, 0, 9, 4};
    
    // 调用解决方案，获得处理结果，并输出展示结果
    Solution *solution = new Solution();
    solution->sortVector(nums);
    if (nums.empty()) {
        cout << "Answer is empty." << endl;
    } else {
        cout << "Answer is: " << endl;
        for (auto ite = nums.begin(); ite != nums.end(); ite++) {
            cout << *ite << ", ";
        }
        cout << "End." << endl;
    }
    
    
    // 程序执行时间
    finish = clock();
    prog_duration = (double)(finish - start) * 1000 / CLOCKS_PER_SEC;
    cout << "程序执行时间: " << prog_duration << "ms." << endl;
    
    return 0;
}
