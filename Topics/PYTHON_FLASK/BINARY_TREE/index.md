---
title: Binary Tree Animation
layout: default
---
{% include head-custom.html %}

## Binary Tree Animation

### General Tree Terminology

We borrow terminology from a family tree to describe relationships between the nodes in a tree. The terminology is valid for generic tree structures. A tree consists of a collection of nodes. A node is a non-divisible unit of information (a record) in a large data structure, such as a linked list. It may contain links (pointers) to other nodes. One node is designated as the root of the tree. The remaining nodes are classified either as <b>leaves</b> or <b>internal nodes</b>.  Formally, a tree represents a hierarchical structure defined recursively as follows:

<strong>Definition: </strong> A tree $T$ can be empty, or may consist of
- One special node $r$ called the root.
- A set of trees $k$ trees $T_1, T_2, \ldots, T_k$ (possibly empty) with roots $r_1, r_2, \ldots, r_k$ respectively.

The trees $T_1, T_2, \ldots, T_k$ are called subtrees of $T$. The roots $r_1, r_2, \ldots, r_k$ of subtrees are called children of $r$, and the node $r$ contains pointers to reach each of its children. The nodes in a tree $T$ are, thus, accessible through its root $r$. 

To explore a tree, we always start from the root. Starting from the root, we can reach a leaf node by selecting a child pointer at each internal node on the way. The sequence of nodes from the root to a leaf is called <b>tree path</b>. No tree path can extend beyond a leaf, since the node has null pointers for its children. Any non-empty subsequence of a sequence of a tree path defines a subpath that is also a tree path. There is a similarity between a linked list and a tree path. A linked list cannot extend beyond its last node that has a null pointer for its next field. Similarly, a tree path cannot extend beyond a leaf that contains no child pointer. Every pair of nodes on a tree path is related by an <b>ancestor-descendant</b> relationship. The node closer to the root is an ancestor of the node farther from the root; the latter is called a descendant of the former node. The nodes that do not share the same tree path from a root to a leaf are unrelated by the ancestor-descendant relation. The nodes with the same parent are called <b>siblings</b>. The node where a subtree begins is called the root of the subtree. We will return to elaborate on the terminology later in our text.

### Binary Tree

A Binary Tree is a restricted class of trees for which $k$ is at most 2. An internal node in a binary tree has at least one child and at most 2 children, while a leaf node has no children. The two subtrees of the root in a Binary Tree are known as the left and right subtrees. A link to the left child of a node is called the <b>left branch</b>, and the link to a right child is called the <b>right branch</b>. If a binary tree is left-skewed or right-skewed, it resembles a linear list. Similarly, if the left or right child links of the internal nodes are absent, the binary tree resembles a linked list. The configurations of a binary tree representing a linked list are shown in the figure below. The reader may notice that any  tree where each internal node has one child resembles a linked list.

<div align="center">
 
| Config I | Config II | Config III |
|:----------:|:-----------:|:------------:|
| <img src="images/left_skewed_binary_tree.png" width="60%"> | <img src="images/right_skewed_binary_tree.png" width="60%" > |  <img src="images/skewed_binary_tree.png" width="60%"> |

</div>

### Traversals of a Binary Tree

How do we process data represented as a binary tree? We will consider each node that only stores one unit of data. However, in practice, it will depend on the nature of the requirements for solving a problem at hand. The fundamental operation involved in processing a binary tree data structure is a traversal. The traversal is essentially a <b>walk</b> around the branches of a Binary Tree starting from the root. The figure below illustrates a walk around a binary tree.

<div align="center">
 
| Walk around a binary tree |
|:----------:|
| <img src="images/walk_binary_tree.png" width="60%"> 

</div>

So, a traversal is a process of:
- Systematically visiting each node three times,
- Processing the data represented by the visited node

Depending on the instance of the visit during traversal, we distinguish three traversal mechanisms.
- <b>Preorder</b> that lists the nodes in the order they are visited for the first time. For the example shown above, the preorder list is: 1, 2, 3, 5, 8, 9, 6, 10.
- <b>Inorder</b> that lists the nodes in the order they are visited for the second time. For the example shown above, the inorder list is: 2, 1, 8, 5, 9, 3, 6, 10
- <b>Postorder</b> that lists the nodes in the order they are visited for the last time. For the example shown above, the postorder list is: 2, 8, 9, 5, 10, 6, 3, 1

An alternative way to define traversals is to do so recursively, using a tree's hierarchical relationship with its subtrees. Suppose $r$ denotes the root (of a subtree), $L$, and $R$ its left and right subtrees, respectively. Then the order of visiting the nodes in different traversals is specified recursively as follows:
- <b>Preorder</b>: $r\ L\ R$
- <b>Preorder</b>: $L\ r\ R$
- <b>Preorder</b>: $L\ R\ r$

 ### Implementation 

Implementing operations of a Binary Tree is much simpler than those of a linked list. The idea implementation is limited to the traversals. Insertion, deletion, or search operations are quite relevant here, because unless there is a superposition of a partial ordering on elements belonging to left and right subtrees, it will not be possible to implement mutating operations on a Binary Tree. The implementation of a Binary Tree here is controlled by a random decision to add a new node as a left or right child of an existing node. However, there is still an ambiguity concerning how to choose the new node's position. Therefore, we construct the tree level by level. To summarize, the implementation process is as follows.

- 

