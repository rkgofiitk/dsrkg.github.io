---
title: Heap and its Animation
layout: default
---
{% include head-custom.html %}


## Heap and its Animation

A heap, also known as a priority queue, is a binary tree that satisfies the priority queue property. The elements in a heap are ordered by a partial order relation. A partial order relation is characterized by being reflexive, asymmetric, and transitive. The heap property is specified by the elements held at three nodes: a node and its two children. The property should hold at each node in a heap except for the leaves. Heap does not specify any relationship between the siblings and leaves. It means some pairs of elements are not comparable. There are two types of heaps: Max heap and Min heap:
- Max Heap: The value at a node is greater than the values held by its two child nodes.
- Min Heap: The value at a node is greater than the values held by its two child nodes.

The picture below shows an example of a max heap and a min heap. 

| Max Heap Example | Min Heap Example|
|:----- | :-----|
| <img src="images/max_heap.png"> | <img src="images/min_heap.png:>|

A heap allows two mutating operations:
- Insert: Allows insertion of a new element and restores the heap property.
- DeletMax: This operation works only in a Max Heap, allowing deletion of the maximum element and restoring the heap property after deletion.
- DeletMin: This operation works only in a Min Heap, allowing deletion of the minimum element and restoring the heap property after deletion.

The challenge with insertion and deletion operations is restoring the heap property. A heap is maintained as a complete binary tree. In a complete binary tree, nodes at all levels of the tree are populated except for the last and the level one up. As shown in the examples above, we can see that nodes at levels above $i-1$ are fully populated (each having two children).
  

