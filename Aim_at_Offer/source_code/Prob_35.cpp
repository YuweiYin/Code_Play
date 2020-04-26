/*
序号：35
题目：数组中的逆序对

题目描述：
在数组中的两个数字，如果前面一个数字大于后面的数字，
则这两个数字组成一个逆序对。输入一个数组,求出这个数组中的逆序对的总数P。
并将P对1000000007取模的结果输出。即输出P%1000000007

输入描述：
题目保证输入的数组中没有的相同的数字

数据范围：
    对于%50的数据,size<=10^4
    对于%75的数据,size<=10^5
    对于%100的数据,size<=2*10^5

示例：
    输入：
    1,2,3,4,5,6,7,0
    输出：
    7

时间限制：2秒 空间限制：32768K
本题知识点：数组，时间空间效率的平衡
*/

#include <iostream>
#include <vector>
using namespace std;


class Solution {
public:
    int InversePairs(vector<int> data) {
        if(data.size() <= 1) {
            // 如果少于等于 1 个元素，直接返回 0
            return 0;
        }
        
        // 深复制原数组
        int* copy = new int[data.size()];
        
        // 初始化该数组，该数组作为存放临时排序的结果，最后要将排序的结果复制到原数组中
        for(int i = 0; i < data.size(); i++) {
            copy[i] = 0;
        }
        
        // 二路归并排序
        int count = this->MergeSort2Way(data, copy, 0, data.size() - 1);

        // 删除临时数组
        delete[] copy;
        
        return count;
    }

    // 二路归并排序
    int MergeSort2Way(vector<int>& data, int* copy, int start, int end) {
        if(start >= end) {
            copy[start] = data[start];
            return 0;
        }
        
        // 拆分数组
        int mid = (end + start) / 2;
        
        // 分别计算左边部分和右边部分
        int left = this->MergeSort2Way(data, copy, start, mid) % 1000000007;
        int right = this->MergeSort2Way(data, copy, mid + 1, end) % 1000000007;
        
        int i = mid; // 左数组的尾下标
        int j = end; // 右数组的尾下标
        int index = end; // 辅助数组 copy 下标，从尾部走起
        int count = 0;
        
        while(i >= start && j >= mid + 1) {
            // 此时出现逆序对情况
            if(data[i] > data[j]) {
                copy[index--] = data[i--];
                
                // 累积逆序对数目
                count += j - mid;
                
                // 根据题意，限定数值范围
                if(count >= 1000000007)
                    count %= 1000000007;
            }
            else {
                copy[index--] = data[j--];
            }
        }
        
        // 把左数组剩下的元素加进辅助数组 copy 中
        for(; i >= start; --i) {
            copy[index--] = data[i];
        }
        
        // 把右数组剩下的元素加进辅助数组 copy 中
        for(; j >= mid + 1; --j) {
            copy[index--] = data[j];
        }
        
        // 此时辅助数组是有序的，用它替换原数组的相应部分
        for(int i = start; i <= end; i++) {
            data[i] = copy[i];
        }
        
        // 返回最终的结果
        return (count + left + right) % 1000000007;
    }
};


int main(int argc, const char * argv[]) {
    Solution solution = Solution();
    
    // int array[8] = {1, 2, 3, 4, 5, 6, 7, 0}; // 7
    // int array[8] = {1, 8, 3, 4, 5, 6, 7, 0}; // 12
    int array[100] = {
         364, 637, 341, 406, 747, 995, 234, 971, 571,
         219, 993, 407, 416, 366, 315, 301, 601, 650, 418,
         355, 460, 505, 360, 965, 516, 648, 727, 667, 465,
         849, 455, 181, 486, 149, 588, 233, 144, 174, 557,
         67, 746, 550, 474, 162, 268, 142, 463, 221, 882,
         576, 604, 739, 288, 569, 256, 936, 275, 401, 497,
         82, 935, 983, 583, 523, 697, 478, 147, 795, 380,
         973, 958, 115, 773, 870, 259, 655, 446, 863, 735,
         784, 3, 671, 433, 630, 425, 930, 64, 266, 235, 187,
         284, 665, 874, 80, 45, 848, 38, 811, 267, 575
    }; // 2519
    
    vector<int> data(array, array + 100);
    
    cout << solution.InversePairs(data) << endl;
    
    return 0;
}
