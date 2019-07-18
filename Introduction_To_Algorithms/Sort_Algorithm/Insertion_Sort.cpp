//
//  Insertion_Sort.cpp
//  Sort_Algorithm
//
//  Created by 阴昱为 on 2019/7/18.
//  Copyright © 2019 阴昱为. All rights reserved.
//

#include "Insertion_Sort.hpp"

class InsertionSort {
public:
    template <typename T>
    void insertionSort (vector<T>& nums) {
        for (size_t i = 1; i < nums.size(); i++) {
            T key = nums[i];
            
            size_t j = i - 1;
            while (j >= 0 && nums[j] > key) {
                nums[j + 1] = nums[j];
                j --;
            }
            
            nums[j + 1] = key;
        }
    }
};
