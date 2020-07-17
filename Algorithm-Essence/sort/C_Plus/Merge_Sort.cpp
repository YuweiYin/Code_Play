//
//  Merge_Sort.cpp
//  Sort_Algorithm
//
//  Created by 阴昱为 on 2019/7/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include "Merge_Sort.hpp"

template <typename T>
class MergeSort {
private:
//    const T INFNITY = ~0u >> 1;
//    const T NEGATIVE_INFNITY = ~0u;
    
public:
    void mergeSort (vector<T>& nums, int p, int r, bool reverse = false, bool (*cmp)(T, T) = increasingOrder) {
        if (p < r) {
            int q = (p + r) / 2;
            this->mergeSort(nums, p, q, reverse, cmp);
            this->mergeSort(nums, q + 1, r, reverse, cmp);
            this->merge(nums, p, q, r, reverse, cmp);
        }
    }
    
private:
    void merge (vector<T>& nums, int p, int q, int r, bool reverse = false, bool (*cmp)(T, T) = increasingOrder) {
        // nums[p..q] and nums[q+1..r] have already been sorted
        int n1 = q - p + 1; // left subsequence size
        int n2 = r - q; // right subsequence size
        
        // Create new sequences to store the sorted subsequences
        vector<T> L(n1);
        vector<T> R(n2);
        
        int i = 0, j = 0;
        
        while (i < n1) {
            L[i] = nums[p + i]; // Store nums[p..q] into L
            i ++;
        }
        
        while (j < n2) {
            R[j] = nums[q + 1 + j]; // Store nums[q+1..r] into R
            j ++;
        }
        
        // Set sentinel to avoid sequence-end check
//        if (reverse) {
//            L[n1] = this->NEGATIVE_INFNITY;
//            R[n2] = this->NEGATIVE_INFNITY;
//        } else {
//            L[n1] = this->INFNITY;
//            R[n2] = this->INFNITY;
//        }
        
        i = j = 0;
        int k = p;
        if (reverse) {
            // Decreasing order
            while (k <= r && i < n1 && j < n2) {
                // Choose the bigger one to modify nums[p..r]
                if ((*cmp)(R[j], L[i])) {
                    nums[k++] = L[i++];
                } else {
                    nums[k++] = R[j++];
                }
            }
            
            while (k <= r && i < n1) {
                nums[k++] = L[i++];
            }
            
            while (k <= r && j < n2) {
                nums[k++] = R[j++];
            }
        } else {
            // Increasing order
            while (k <= r && i < n1 && j < n2) {
                // Choose the smaller one to modify nums[p..r]
                if ((*cmp)(L[i], R[j])) {
                    nums[k++] = L[i++];
                } else {
                    nums[k++] = R[j++];
                }
            }
            
            while (k <= r && i < n1) {
                nums[k++] = L[i++];
            }
            
            while (k <= r && j < n2) {
                nums[k++] = R[j++];
            }
        }
    }
    
    static bool increasingOrder (T a, T b) {
        return a < b;
    }
};
