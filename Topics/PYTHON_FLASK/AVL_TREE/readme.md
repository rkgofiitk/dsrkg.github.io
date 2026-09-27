## Read Me AVL Tree Animation.

The Animation folder contains three files for animating AVL tree operations. Before dealing with implementation, let us understand the data structure in sufficient detail. It will facilitate our implementation design. We know that the average cost of an operation: insert, delete, or retrieve is O($\log n$) in a binary search tree (BST) with $n$ nodes. However, due to a random sequence of insertions and deletions, the worst-case scenario may produce a completely skewed tree that resembles a linear list of nodes. In this case, any operation may take up to O($n$) time. However, if we always maintain a balanced tree, we can preserve O($\log n$) time per operation. An AVL tree is named after the discoverers Adelson, Velsky, and Landis. It maintains tree balance by defining a single O(1) operation, called rotation. There are three different types of rotations:
- Single left rotation (LR)
- Single right rotation (RR)
- Double rotation

A Double Rotation is a mix of two single rotation types. The combination could be LR, RR, LL, or RL. Sometimes a right rotation is also called a clockwise rotation, while a left rotation is an anticlockwise rotation.  A single rotation involves changing three pointers, as shown in the picture below. 
<p align="center">
  <img src="images/avlLLrotation.png">
</p>
