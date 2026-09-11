from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sort_class import SortVisualizer

import random


app = Flask(__name__)
CORS(app)


def generate_random_array(size=10, max_value=400):
    return [random.randint(50, max_value) for _ in range(size)]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bubble-sort')
def bubble_sort():
    size = int(request.args.get('size', 10))
    arr = generate_random_array(size)
    sorter = SortVisualizer(arr.copy())
    steps, final = sorter.bubble_sort()
    return jsonify({
        "steps": steps, 
        "array": arr
        })

@app.route('/insertion-sort')
def insertion_sort():
    size = int(request.args.get('size', 10))
    arr = generate_random_array(size)
    sorter = SortVisualizer(arr.copy())
    steps, final = sorter.insertion_sort()

    return jsonify({
        "steps": steps, 
        "array": arr 
    })

@app.route('/merge-sort')
def merge_sort():
    size = int(request.args.get('size', 10))
    arr = generate_random_array(size)
    sorter = SortVisualizer(arr.copy())
    steps, final = sorter.run_merge_sort()
    return jsonify({
        "steps": steps, 
        "array": arr 
        })

@app.route("/quick-sort")
def quick_sort():
    size = int(request.args.get("size", 10))
    data = generate_random_array(size)

    sorter = SortVisualizer(data.copy())
    sorter.quick_sort_step(0, size-1)

    return jsonify({
        "array": data,            # original unsorted array
        "steps": sorter.steps     # recorded snapshots
    })


@app.route("/heap-sort")
def heap_sort():
    size = int(request.args.get("size", 10))
    data = generate_random_array(size)
    sorter = SortVisualizer(data.copy())
    sorter.heap_sort_step()
    return jsonify({
        "array": data,          # original unsorted input
        "steps": sorter.steps   # snapshots for animation
    })

@app.route("/bucket-sort")
def bucket_sort():
    size = int(request.args.get("size", 10))
    data = generate_random_array(size)
    sorter = SortVisualizer(data.copy())
    sorter.bucket_sort_step()
    return jsonify({
        "array": data,          # original unsorted input
        "steps": sorter.steps   # snapshots for animation
    })




if __name__ == "__main__":
    app.run(debug=True)


