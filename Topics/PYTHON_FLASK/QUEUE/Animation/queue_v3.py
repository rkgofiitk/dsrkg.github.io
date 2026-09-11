from flask import Flask, render_template, jsonify, request
from queueOps import Queue 

app = Flask(__name__)
queue = Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enqueue', methods=['POST'])
def enqueue():
    if queue.is_full():
        return jsonify({
            "queue": queue.to_list(),
            "enqd": "Queue is full - enqueue failed"
            })
    else:
        val = request.json.get('value')
        queue.enqueue(val)
        print(queue.to_list())
        return jsonify({
            "queue": queue.to_list(),
            "enqd": val
            })

@app.route('/dequeue', methods=['POST'])
def dequeue():
    if queue.is_empty():
        print("Dequeue entered ", queue.to_list())
        return jsonify({
            "queue": queue.to_list(),
            "deqd": "Queue is empty - dequeue failed"
            })
    else:
        deqd = queue.dequeue()
        print(queue.to_list(), "deqd = ",deqd)
        return jsonify({
           "queue": queue.to_list(),
           "deqd": deqd
           })

if __name__ == '__main__':
    app.run(debug=True)

