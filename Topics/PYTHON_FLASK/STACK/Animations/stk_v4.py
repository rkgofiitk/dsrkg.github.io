from flask import Flask, render_template, jsonify, request
from stackOps import Stack

app = Flask(__name__)
stack = Stack()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/push_data", methods=['POST'])
def push_data():
    if stack.is_full():
        return jsonify({
            "stack": stack.print(),
            "pushed": "Stack is full - push failed"
            })
    else:
        val = request.json.get('value')
        stack.push(val)
        return jsonify({
            "stack": stack.print(),
            "pushed":val})

@app.route("/pop_data", methods=['POST'])
def pop_data():
    if not stack.is_empty():
        popped = stack.pop()
        return jsonify({
            "stack": stack.print(),   # current stack as list
            "popped": popped          # the item removed
        })
    else:
        return jsonify({
            "stack": stack.print(),   # current stack as list
            "popped": "Stack is empty - pop failed" # not removed 
        })

if __name__ == '__main__':
    app.run(debug=True)

