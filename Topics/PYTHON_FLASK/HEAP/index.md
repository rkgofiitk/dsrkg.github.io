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
| <img src="images/max_heap.png"> | <img src="images/min_heap.png">|

A heap allows two mutating operations:
- Insert: Allows insertion of a new element and restores the heap property.
- DeletMax: This operation works only in a Max Heap, allowing deletion of the maximum element and restoring the heap property after deletion.
- DeletMin: This operation works only in a Min Heap, allowing deletion of the minimum element and restoring the heap property after deletion.

Creating and maintaining a heap poses two basic challenges:
- Building a heap from a given set of elements.
- Restoring the heap property after an insertion or a deletion.
  
A heap is maintained as a complete binary tree. In a complete binary tree, nodes at all levels of the tree are fully populated except for the last and the level one up. As shown in the examples above, nodes at levels above $i-1$ are fully populated (each with two children). The technique for constructing the heap will differ depending on whether we build it from the beginning or the end of the array. 

- If we start at the beginning of the array, then we compare the next two elements by adding from the top. Continue the addition of the next 4 elements again from the top, and in general, the last $n/2^i$ elements starting at the top at step $i$. Essentially, it builds the heap level by level from the top down.
- If we start from the end, then $n/2$ elements from the end are already heaps of size 1 each at the bottom-most level. Next, consider $n/2$ elements by merging each element with 2 adjacent heaps of the bottom-most level. Continue building the heap bottom-up, merging pairs of adjacent heaps with the next incoming element from the remaining unprocessed array. 

The question is which of the two techniques above for building a heap is more efficient?

The answer to the question is, surprisingly, the bottom-up technique. Let us reiterate how the bottom-up technique progresses:
- First building $n/2$ heaps of size 1, it does not require any compare-and-swap (CAS).
- Next, merging 2 adjacent heaps of size 1 from $n/2$ heaps into $n/4$ heaps of size 3 each, adding a new element to each, which requires $n/2$ CAS operations.
- Repeat the process of merging heaps by adding new elements from the unprocessed portion of the array until we finish with a single heap of size $n$.

Except for the starting step, each merging step requires twice as many CAS operations as the immediately preceding step. So, the cost of building a heap using bottom-up construction is given by the following expression:

$0 * (n/2) + 1 * (n/4) + 2 * (n/8) + \ldots + (\log n * 1) = \sum_{1}^{h} i * \frac{n}{2^{i+1}} = \sum_{1}^{h} \frac{in}{2^{i+1}}$

Let us try to obtain an upper bound for the above expression. 

$\sum_{1}{h} \frac{in}{2^{i+1}} = \frac{n}{4}\sum_{1}^{h} \frac{i}{2^{i-1}} < \frac{n}{4}\sum_0^\infty ix^{i-1}$,

where $x = 1/2$.


  

