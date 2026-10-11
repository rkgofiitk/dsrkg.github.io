---
title: AVL Tree Animation
layout: default
---
{% include head-custom.html %}

## AVL Tree Animation.



The Animation folder contains three files for animating AVL tree operations. Before dealing with implementation, let us understand the data structure in sufficient detail. It will facilitate our i[...]
- Single left rotation (LR)
- Single right rotation (RR)
- Double rotation

A Double Rotation is a mix of two single rotation types. The combination could be LR, RR, LL, or RL. Sometimes a right rotation is also called a clockwise rotation, while a left rotation is an anticlockwise rotation.

 | Config I | Config II|
  |:----------:|:----------:|
 | <img src="images/avlLLrotation.png" width="80%" alt-text="Single left rotation"> | <img src="images/avlRRrotation.png" width="80%" alt-text="Single right rotation"> |

Before going further, we define the balance factor (bf) of a node in a binary search tree (BST):
- It is the difference between the heights of a node's left and right subtrees.

The picture above shows two configurations, one of which is a mirror image of the other. We refer to the left half of the image as Config I, and the right half as Config II.  We fix our explanation with respect to Config I.
- Pushes $a$ down along with its left subtree, 
- Pushes $b$ up to $a$'s previous position along with its right subtree,
- Node $a$ retains its right subtree and adopts the left subtree of $b$ as its new right subtree.

Since $b$ loses its previous left child to adopt $a$ as its new left child, the height of the left subtree of $b$ becomes $h$. The previous left child of $b$ is orphaned, and $a$ should adopt it as its right child.

The picture above shows the following:
- The value of $a$ is smaller than $b$, so $a$ with its left subtree contains values less than $b$,
- The each value in the left subtree of $b$ is greater than the value of $a$,
- The height of the left subtree of $b$ is increased to $h$,
- The height of the right subtree of $b$ remains unchanged at $h$
  
Thus, $bf(b) = 0$, in other words, the single left rotation restores balance properties at $a$ and $b$. Unfortunately, the example does not really expose the whole picture. It need not be the case; the balance factor could be positive or negative.

In both Config I, we need just one rotation involving three nodes: $a$, $b$, and the root of $ b$'s right subtree. The tri-node structure for Config I is referred to as a Zig-Zig pattern, while that for Config II is referred to as a Zag-Zag pattern.

The Config I in the figure below represents a tri-node structure $a-b-c$, which requires double rotation on a Zig-Zag configuration.  Config II in the figure represents a Zag-Zig pattern for the tri-node structure.

 | Config I | Config II|
  |:----------:|:----------:|
 | <img src="images/avlLRrotation.png" width="80%" alt-text="Single left rotation"> | <img src="images/avlRLrotation.png" width="80%" alt-text="Single right rotation"> |

A left rotation on $b$ in Config I turns the tri-node into a Zig-Zig configuration. Now, a single right rotation can fix the balance factors as explained by Config II of the previous figure. Similarly, a right rotation about $b$ in Config II yields a Zag-Zag configuration, followed by a single left rotation.

Why is double rotation required at all? The figure below provides an explanation. 

 | Why Double Rotation? |
  |:----------:|
 | <img src="images/need_for_DR.png" width="60%" alt-text="Single left rotation"> |
 
Suppose we apply an LL rotation to the leftmost configuration. The configuration turns into a zig-zig. If we apply an RR rotation to a zig-zag configuration, then it returns the initial zig-zag configuration. So, a single rotation won't rebalance such a structure. 

How does a double rotation solve a rebalancing problem like the one described above? To understand it, consider the example shown below. Focus on the zag-zig pattern. After an LL rotation is applied, the result is a zig-zig pattern, as indicated by the structure in the middle. Now, an RR rotation is applied to the same node position, resulting in a double rotation on the node position. The final structure to the right is a rebalanced tree. 

| LR type Double Rotation |
|:---------------:|
| <img src="images/Double_LR_Rotation.png" width="70%" alt-text="Double LR rotation"> |

A zig-zag pattern that represents a mirror of above configuration found in an unbalance tree is shown in the image below. It also requires a double rotation to rebalance the tree. This double rotation is similar to LR rotation except that the roation orders are reversed. The result is a rebalanced tree as illustrated by the right-most configuration of the tree after performing the rotation.


| RL type Double Rotation |
|:---------------:|
| <img src="images/Double_RL_Rotation.png" width="70%" alt-text="Double RL rotation"> |

We have understood how rotations rebalance the tree when applied to the node postions where balance factors are disturbed. Rotations are applied bottom up along the tree path from the depth-most unbalanced node to the root. One important fact that we did not mention until now is that an AVL tree is a binary search tree (BST). Therefore, insert and delete operations on BSTs are the two mutating operations that disturb the balance factors of nodes in AVL trees. Therefore, rotations are needed only when an insertion or a deletion occurs in an AVL tree.
