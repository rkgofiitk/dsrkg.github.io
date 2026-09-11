from flask import Flask, request, jsonify, render_template
from sort_class import SortVisualizer

import random
import time

app = Flask(__name__)

# Measuring raw time for sort
def measure_raw(method_name, array):
    sorter = SortVisualizer(array.copy())
    start = time.perf_counter()
    if method_name == "bubble":
        sorter.bubble_sort()
    elif method_name == "merge":
        sorter.run_merge_sort()
    elif method_name == "quick":
        sorter.quick_sort_step(0, len(array) - 1)
    elif method_name == "bucket":
        sorter.bucket_sort_step()
    end = time.perf_counter()
    elasped = (end - start) * 10e6 # Use 10e9 for nanoseconds
    return elasped

# Measuring sorting time including the front-end display 
def timed_sort(sort_func, array):
    start = time.perf_counter()
    steps = sort_func(array)
    end = time.perf_counter()
    elapsed = (end - start) * 10e6 # Use 10e9 for nanoseconds
    return steps, elapsed

# Generating random values in [100, 400] for sorting
def generate_random_array(size=10, max_value=400):
    return [random.randint(100, max_value) for _ in range(size)]

@app.route('/')
def index():
    return render_template('race_index.html')


@app.route("/race")
def race():
    size = int(request.args.get("size", 10))
    arr = generate_random_array(size)

    # Bubble sort
    bubble_sorter = SortVisualizer(arr.copy())
    start = time.perf_counter()
    bubble_steps, bubble_final = bubble_sorter.bubble_sort()
    bubble_time = time.perf_counter() - start
    bubble_raw = measure_raw(SortVisualizer(arr.copy()).bubble_sort, arr)

    # Merge sort
    merge_sorter = SortVisualizer(arr.copy())
    start = time.perf_counter()
    merge_steps, merge_final = merge_sorter.run_merge_sort()
    merge_time = time.perf_counter() - start
    merge_raw = measure_raw(SortVisualizer(arr.copy()).run_merge_sort, arr)

    # Quick sort
    quick_sorter = SortVisualizer(arr.copy())
    start = time.perf_counter()
    quick_sorter.quick_sort_step(0, size - 1)
    quick_steps = quick_sorter.steps
    quick_final = quick_sorter.arr
    quick_time = time.perf_counter() - start
    quick_raw = measure_raw(lambda a: SortVisualizer(a).quick_sort_step(0, len(a)-1), arr)



    # Bucket sort
    bucket_sorter = SortVisualizer(arr.copy())
    start = time.perf_counter()
    bucket_sorter.bucket_sort_step()
    bucket_steps = bucket_sorter.steps
    bucket_final = bucket_sorter.arr
    bucket_time = time.perf_counter() - start
    bucket_raw = measure_raw(lambda a: SortVisualizer(a).bucket_sort_step(), arr)

    return jsonify({
        "array": arr,
        "bubble": {"steps": bubble_steps, "final": bubble_final,
                   "time": bubble_time, "raw_time_ms": bubble_raw},
        "merge": {"steps": merge_steps, "final": merge_final,
                   "time": bubble_time, "raw_time_ms": merge_raw},
        "quick": {"steps": quick_steps, "final": quick_final,
                   "time": quick_time, "raw_time_ms": quick_raw},
        "bucket": {"steps": bucket_steps, "final": bucket_final,
                   "time": bucket_time, "raw_time_ms": bucket_raw},
    })

    
if __name__ == "__main__":
    app.run(debug=True)


