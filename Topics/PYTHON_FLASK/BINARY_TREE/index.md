---
title: Binary Tree Animation
layout: default
---
{% include head-custom.html %}

## Binary Tree Animation

A binary tree is the simplest non-linear data structure. Each tree node has two pointers, rather than one, as in a linked list. The two pointers are separately identified as the left and right children. If a binary tree is left-skewed or right-skewed, it represents a linear list. Similarly, if the left or right child link of each node is absent, then the binary tree also represents a linked list. The configurations of a binary tree representing a linked list are shown in the figure below.

| Config I | Config II | Config III |
|----------|-----------|------------|
| <img src="image/left_skew_BT.png"> | <img src="image/righy_skew_BT.png"> |  <img src="image/both_skew_BT.png"> |

The focus here is on one fundamental operation of a binary tree data structure. How do we process data represented as a binary tree? We require a way to navigate or traverse a binary tree. The traversal should 
- Systematically visit each node exactly once
- Process the data represented by the visited node

There are three systematic traversal mechanisms:
- Preorder
- Inorder
- Postorder


