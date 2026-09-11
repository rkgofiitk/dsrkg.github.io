class SortVisualizer:
    def __init__(self, arr):
        self.arr = arr
        self.steps = []

    def record_step(self, highlights=None, pivot=None):
        # highlights is a list of indices being compared/swapped
        self.steps.append({
            "array": self.arr.copy(),
            "highlights": highlights or [],
            "pivot": pivot if pivot is not None else None
        })

    # ---------------- Bubble Sort ----------------
    def bubble_sort(self):
        self.steps = []
        n = len(self.arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                #if self.arr[j] > self.arr[j + 1]:
                #    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                self.record_step(highlights=[j, j+1])

                #self.record_step()
        return self.steps, self.arr

    # ---------------- Insertion Sort ----------------
    def insertion_sort(self):
        self.steps = []
        for i in range(1, len(self.arr)):
            key = self.arr[i]
            j = i - 1

            while j >= 0 and self.arr[j] > key:
                self.arr[j + 1] = self.arr[j]
                j -= 1
                self.record_step(highlights=[j, j+1])
            self.arr[j + 1] = key
            self.record_step()
        return self.steps, self.arr

    # ---------------- Merge Sort ----------------
    def merge(self, temp, left, mid, right):
        i, j, k = left, mid + 1, left

        while i <= mid and j <= right:
            if self.arr[i] <= self.arr[j]:
                temp[k] = self.arr[i]
                i += 1
            else:
                temp[k] = self.arr[j]
                j += 1
            k += 1

        while i <= mid:
# inside merge loop
            temp[k] = self.arr[i]
            self.record_step(highlights=[i, j])
            i += 1
            k += 1

        while j <= right:
            temp[k] = self.arr[j]
            j += 1
            k += 1

        for idx in range(left, right + 1):
            self.arr[idx] = temp[idx]

        self.record_step()

    def merge_sort(self, temp, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(temp, left, mid)
            self.merge_sort(temp, mid + 1, right)
            self.merge(temp, left, mid, right)

    def run_merge_sort(self):
        self.steps = []
        temp = [0] * len(self.arr)
        self.merge_sort(temp, 0, len(self.arr) - 1)
        return self.steps, self.arr

    #---------------------------------------
    #   QUICK sort
    #---------------------------------------

    # Quick sort function partition


    def partition(self, low, high):
        i = low - 1
        pivot_value = self.arr[high]

        # Record pivot selection
        self.record_step(pivot=high)

        for j in range(low, high):
            if self.arr[j] <= pivot_value:
                i += 1
                # Swap
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                # Record swap step with highlights
                self.record_step(highlights=[i, j], pivot=high)

        # Final pivot placement
        self.arr[i+1], self.arr[high] = self.arr[high], self.arr[i+1]
        self.record_step(highlights=[i+1, high], pivot=i+1)

        return i+1 

    # high  --> Ending index
    def quick_sort_step(self,low,high):

        self.record_step(highlights=[], pivot=None)

        #  auxiliary stack
        size = high - low + 1
        stack = [0] * (size)
 
        top = -1
 
        top = top + 1
        stack[top] = low
        top = top + 1
        stack[top] = high
 
        # Keep popping from stack while is not empty
        while top >= 0:
 
            # Pop high and low
            high = stack[top]
            top = top - 1
            low = stack[top]
            top = top - 1
 
            # sorted array
            p = self.partition( low, high )

            # push left side to stack
            if p-1 > low:
                top = top + 1
                stack[top] = low
                top = top + 1
                stack[top] = p - 1

            #  push right side to stack
            if p+1 < high:
                top = top + 1
                stack[top] = p + 1
                top = top + 1
                stack[top] = high
 
        #self.add_label("Quick sort is complete")
        # push final cleanup snapshot
        self.record_step(highlights=[], pivot=None)
        return 


    # ---------------- Heap Sort ----------------
    def buildHeap(self):
        # Build max heap
        for k in range((len(self.arr) - 2) // 2, -1, -1):
            self.heapify(len(self.arr), k)
        return self.arr

    def heapify(self, heapSize, k):
        done = False
        while not done:
            largest = k
            l = 2 * k + 1
            r = 2 * k + 2

            if l < heapSize and self.arr[l] > self.arr[largest]:
                largest = l
            if r < heapSize and self.arr[r] > self.arr[largest]:
                largest = r

            if largest != k:
                # swap
                self.arr[k], self.arr[largest] = self.arr[largest], self.arr[k]
                # record swap indices
                self.record_step(highlights=[k, largest], pivot=None)
                k = largest
            else:
                done = True

    def heap_sort_step(self):
        # record initial unsorted state
        self.record_step(highlights=[], pivot=None)

        self.buildHeap()
        heapSize = len(self.arr)

        for i in range(len(self.arr) - 1, 0, -1):
            # swap root with last element
            self.arr[0], self.arr[heapSize - 1] = self.arr[heapSize - 1], self.arr[0]
            self.record_step(highlights=[0, heapSize - 1], pivot=None)

            heapSize -= 1
            self.heapify(heapSize, 0)

        # final cleanup snapshot
        self.record_step(highlights=[], pivot=None)

        return self.arr

    # ------- BUCKET SORT ------------------ 

    def bucket_insertion_sort(self, bucket):
        # Standard insertion sort with step recording
        for i in range(1, len(bucket)):
            temp = bucket[i]
            j = i - 1
            while j >= 0 and temp < bucket[j]:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = temp

            # Record snapshot of the whole array, highlighting indices in this bucket
            # We need to rebuild self.data to reflect current buckets
            self.arr = []
            for b in self.buckets:
                self.arr.extend(b)
            self.record_step(highlights=[j+1, i], pivot=None)

        return bucket




    # Distributes input into 5 (fiexed) different buckets 
    def bucket_sort_step(self):
        self.record_step(highlights=[], pivot=None)  # initial unsorted state

        result = []
        no_of_buckets = 5
        self.buckets = [[] for _ in range(no_of_buckets)]
        max_elem, min_elem = max(self.arr), min(self.arr)

        bucket_size = (max_elem - min_elem) / no_of_buckets

        # Distribute elements into buckets
        for element in self.arr:
            index = int((element - min_elem) / bucket_size)
            if element == max_elem:
                index -= 1
            self.buckets[index].append(element)

        # Sort each bucket and concatenate
        result = []
        for bucket in self.buckets:
            sorted_bucket = self.bucket_insertion_sort(bucket)
            result.extend(sorted_bucket)
            self.arr = result.copy()
            self.record_step(highlights=list(range(len(result))), pivot=None)

        self.arr = result

        # Final cleanup snapshot
        self.record_step(highlights=[], pivot=None)

        return self.arr



   
