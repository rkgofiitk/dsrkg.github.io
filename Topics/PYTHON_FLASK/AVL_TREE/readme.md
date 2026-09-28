## Read Me AVL Tree Animation.



The Animation folder contains three files for animating AVL tree operations. Before dealing with implementation, let us understand the data structure in sufficient detail. It will facilitate our implementation design. We know that the average cost of an operation: insert, delete, or retrieve is O($\log n$) in a binary search tree (BST) with $n$ nodes. However, due to a random sequence of insertions and deletions, the worst-case scenario may produce a completely skewed tree that resembles a linear list of nodes. In this case, any operation may take up to O($n$) time. However, if we always maintain a balanced tree, we can preserve O($\log n$) time per operation. An AVL tree is named after the discoverers Adelson, Velsky, and Landis. It maintains tree balance by defining a single O(1) operation, called rotation. There are three different types of rotations:
- Single left rotation (LR)
- Single right rotation (RR)
- Double rotation

A Double Rotation is a mix of two single rotation types. The combination could be LR, RR, LL, or RL. Sometimes a right rotation is also called a clockwise rotation, while a left rotation is an anticlockwise rotation.  A single rotation involves changing three pointers, as shown in the picture below. 

 | Config I | Config II|
  |:----------:|:----------:|
 | <img src="images/avlLLrotation.png" width="80%" alt-text="Single left rotation"> | <img src="images/avlRRrotation.png" width="80%" alt-text="Single right rotation"> |



 



Before going further, we define the balance factor (bf) of a node in a binary search tree (BST):
- It is the difference between the heights of a node's left and right subtrees.

The above picture shows two different configurations, one of which is a mirror image of the other. We refer to the left half of the image as Config I, and the right half as Config II.  We fix our explanation with reference to Config I. It will be valid for Config II, with left and right switched. For example, in the figure above, the height of node $a$'s right subtree is $h+1$ while the height of its left subtree is $h-1$. Ignoring the sign of the difference for the moment, we represent the balance factor of $bf(a)=h+1-(h-1)=2$. Similarly, $bf(b)=1$. Since the right subtree of $a$ is taller than the left subtree, we apply a single anticlockwise or left rotation at $a$ involving three nodes, $a$, $b$, and the left child of $b$. The result of the rotation is shown on the right half of the figure. The operation pushes 
- Pushes $a$ down along with its left subtree, 
- Pushes $b$ up to $a$'s previous position along with its right subtree,
- Node $a$ retains its right subtree and adopts the left subtree of $b$ as its new right subtree.

Since $b$ loses its previous left child to adopt $a$ as its new left child, the height of the left subtree of $b$ becomes $h$. The previous left child of $b$ is orphaned, and $a$ should adopt it as its new right child. The second change in configuration  The BST property is retained by the change, because: 
- The value of $a$ is smaller than $b$, so $a$ with its left subtree contains values less than $b$,
- The each value in the left subtree of $b$ is greater than the value of $a$,
- The height of the left subtree of $b$ is increased to $h$,
- The height of the right subtree of $b$ remains unchanged at $h$
  
Thus, $bf(b) = 0$, in other words, the single left rotation restores balance properties at $a$ and $b$. Unfortunately, the example does not really expose the whole picture. It need not be the case; the violation of the balance property may affect many nodes along tree paths, up to the leaves. Therefore, we need to apply rotations up the tree until the root. The maximum number of rotations could equal the length of the tree path. Since we keep the tree balanced by applying the rotations, no path can have a length exceeding O($\log n$).
In both Config I and Config II, the nodes that make the tree unbalanced are characterized as Zig-Zig pattern, i.e., either left-left direction or right-right direction 
