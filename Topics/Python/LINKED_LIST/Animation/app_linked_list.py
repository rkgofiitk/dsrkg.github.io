from flask import Flask, render_template, jsonify, request
from linkedList import LinkedList

app = Flask(__name__)
linked_list = LinkedList()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_node():
    if linked_list.length() < 8: 
        val = request.json.get('value')
        linked_list.insert(val)
        return jsonify(linked_list.get_list_data())
    else:
        return jsonify(None) 

@app.route('/append', methods=['POST'])
def append_node():
    if linked_list.length() < 8: 
        val = request.json.get('value')
        linked_list.append(val)
        linked_list.print_list_data() 
        return jsonify(linked_list.get_list_data())
    else:
        return jsonify(None) 

@app.route('/delete', methods=['POST'])
def delete_node():
    if linked_list.is_empty():
        e_str =  "Attempt to delete from empty list!!" 
        return jsonify({
            "error": e_str
            })
    val = request.json.get('value')
    success = linked_list.delete(val)
    #linked_list.print_list_data() 
    if success:  
        return jsonify(linked_list.get_list_data())
    else:
        e_str = "Deletion unsuccessful - " + str(val) + " is not in the list" 
        return jsonify({
               "error" : e_str 
            })

@app.route('/insertAfter', methods=['POST'])
def insert_node():
    if linked_list.length() < 8:  
        data = request.get_json()
        val1 = data.get("value1") 
        val2 = data.get("value2") 
        linked_list.print_list_data() 
        linked_list.insert_after(val1, val2)
        linked_list.print_list_data() 
        return jsonify(linked_list.get_list_data())
    else:
        return jsonify(None) 

@app.route('/reverse', methods=['POST'])
def reverse_list():
    linked_list.reverse()
    return jsonify({"operation": "reverse", "result": linked_list.get_list_data()})

@app.route('/sort', methods=['POST'])
def sort_list():
    linked_list.sort()
    return jsonify({"operation": "sort", "result": linked_list.get_list_data()})

@app.route('/print', methods=['POST'])
def print_list():
    return jsonify({"operation": "print", "result": linked_list.get_list_data()})

@app.route('/transform', methods=['POST'])
def transform_list():
    data = request.get_json(force=True)
    print("Received JSON:", data)

    if not data or "operation" not in data:
        return jsonify({"error": "Missing operation"}), 400

    op = data["operation"]

    if op == "print":
        result = linked_list.get_list_data()
    elif op == "reverse":
        linked_list.reverse()
        result = linked_list.get_list_data()
    elif op == "sort":
        linked_list.sort()
        result = linked_list.get_list_data()
    else:
        return jsonify({"error": f"Unknown operation '{op}'"}), 400

    return jsonify({"operation": op, "result": result})

if __name__ == '__main__':
    app.run(debug=True)

