# Code_Play

Programming Practice - ACM Algorithm

By [YuweiYin](https://github.com/YuweiYin)

**Algorithm - Data Structure**

> Data structures are nothing different. They are like the bookshelves of your application where you can organize your data. Different data structures will give you different facility and benefits. To properly use the power and accessibility of the data structures you need to know the trade-offs of using one.

## 目录

- 基础结构
    - 数组、链表、栈、队列
    - 指针与对象的实现 (例如用数组实现)
    - 块状链表
- [哈希散列](./hashing.py)
    - 直接寻址表 Direct-Access Table、散列表 Hashing Table
    - 散列表解决碰撞/冲突：链接法 Chaining、开放寻址法 Open Addressing
        - 线性探查 Linear Probing
        - 二次探查 Quadratic Probing
        - 双重散列 Double Hashing
    - 散列函数 Hash Function
        - 除法散列法 Division Hashing
        - 乘法散列法 Multiplication Hashing
        - 全域散列法 Universal Hashing
    - 散列表的动态扩缩 grow / shrink
    - 完全散列 Perfect Hashing、动态完全散列 Dynamic Perfect Hashing
    - 布谷鸟散列 Cuckoo Hashing、布隆过滤器 Bloom Filter
    - 一致性散列 Consistent Hashing (分布式系统的负载均衡)
- 树形结构
    - 二叉树及其各类树遍历算法 (深度/广度)
        - 前序遍历 Preorder Traversal
        - 中序遍历 Inorder Traversal
        - 后序遍历 Postorder Traversal
        - 层序遍历 Level Traversal
    - [二叉排序/搜索树](./binary-search-tree.py) (Binary Sort/Search Tree, BST)
    - [高度平衡二叉搜索树](./avl-tree.py) AVL 树 (Adelson-Velsky-Landis Tree) (Height Balanced Binary Search Tree)
    - [红黑树](./red-black-tree.py) (Red Black Tree, RBT)
        - 红黑树的变种: AA 树
        - 红黑树的扩张: [顺序统计树](./order-statistic-tree.py) (Order Statistic Tree, OST)
        - 红黑树的扩张: [区间树](./interval-tree.py) (Interval Tree)
    - [堆树](./treap.py) (Treap)
    - [伸展树](./splay-tree.py) (Splay Tree)
    - [跳表](./skip-list.py) Skip List
    - 替罪羊树
    - 带权平衡树
    - [B-Tree](./b-tree.py)
        - 2-3 树、B- 树、B+ 树、B\* 树
    - [哈夫曼树](../greedy-algorithm/huffman.py) (Huffman Tree)
    - [van Emde Boas 树](./van-emde-boas-tree.py)
    - k 近邻树、k 维树 (k-dimensional Tree, kd-Tree)
- 区间查询 Range Query
    - [线段树](./segment-tree.py) (Segment Tree, ST)
    - [树状数组](./binary-indexed-tree.py) Fenwick Tree (Binary Indexed Tree, BIT)
    - [区间最值查询](./range-min-max-query.py) Sparse Table (Range Minimum/Maximum Query, RMQ)
    - [最近公共祖先](./lowest-common-ancestor.py) (Lowest Common Ancestors, LCA)
- 堆
    - [二叉堆与优先队列](./heap-priority-queue.py)
    - 双端队列 Deque
    - 可合并堆 Mergeable Heap
        - 左偏堆 Leftist Heap
        - [斐波那契堆](./fibonacci-heap.py)
- 不相交集合 (Disjoint Set)
    - [并查集](./union-find.py) (Union Find)
- [图结构与图算法](../graph-theory)
- 字符串相关 (算法/数据结构)
    - [子串匹配](../other-topics/string-matching)
        - 朴素字符串匹配算法 Naive String Matching
        - Finite Automaton 有限自动机-字符串匹配算法
        - Rabin-Karp 算法
        - KMP 算法 (D.E.Knuth，J.H.Morris and V.R.Pratt)
    - [前缀树/字典树](./string-trie.py) (Trie Tree)、01-字典树
    - 后缀树、后缀数组
    - 后缀自动机 (Suffix Automaton, SAM)
    - AC 自动机 (Aho-Corasick Automaton)
    - 回文串 Palindrome
        - 回文自动机 (Palindromic Automaton, PAM)
        - 回文树 Palindromic Tree
        - 马拉车算法 Manacher's Algorithm
