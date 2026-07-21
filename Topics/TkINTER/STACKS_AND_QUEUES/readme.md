## Animation of Stack and Queue Operations

The directory has four files, including the readme.md. The three Python files are:
- stackOps.py: backend class for stack operations
- queueOps.py: backend class for queue operations
- stack_and_queue.py: frontend for animating the stack and queue operations

The environment for the program is discussed earlier in the README.md file in the parent directory one level up. There are two parts each to the animation of stacks and queues. Stack animation controlled by the movement of a rectangular block moving up or down to exhibit push or pop operation. Queue animation is indicated by the block moving from right to left. Enqueue creates a block with an input label, appears to the right of the current rear position, moves left to settle as a new element, and redraws the rear's new position. Dequeue moves the current first block to the left; the block then disappears, and the remaining blocks in the queue are shifted one position to the right. The rear is adjusted. 

We create a few helper functions for making the animation appealing to the user. These functions are:
- Pulsate
- Move_left
- Move_down
- drop_down

  
