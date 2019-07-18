//
//  Insertion_Sort.cpp
//  Sort_Algorithm
//
//  Created by 阴昱为 on 2019/7/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include "Insertion_Sort.hpp"

template <typename T>
class InsertionSort {
public:
    void insertionSort (vector<T>& nums, bool reverse = false, bool (*cmp)(T, T) = increasingOrder) {
        if (reverse) {
            // Decreasing order
            for (int i = 1; i < nums.size(); i++) {
                T key = nums[i];
                // Insert key into the sorted sequence nums[0..i-1]
                
                int j = i - 1;
                // Find a proper index for key to insert
                while (j >= 0 && (*cmp)(nums[j], key)) {
                    nums[j + 1] = nums[j];
                    j --;
                }

                nums[j + 1] = key;
            }
        } else {
            // Increasing order
            for (int i = 1; i < nums.size(); i++) {
                T key = nums[i];
                // Insert key into the sorted sequence nums[0..i-1]
                
                int j = i - 1;
                // Find a proper index for key to insert
                while (j >= 0 && (*cmp)(key, nums[j])) {
                    nums[j + 1] = nums[j];
                    j --;
                }
                
                nums[j + 1] = key;
            }
        }
    }
    
private:
    static bool increasingOrder (T a, T b) {
        return a < b;
    }
};
