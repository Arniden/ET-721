from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# in-memory database (just a dictionary)
items = {}
next_id = 1   # counter so ids never repeat, even after a delete

# home route
@app.route('/')
def home():
    return render_template('index.html')

# CREATE an item
@app.route('/items', methods=["POST"])
def create_item():
    global next_id
    # read the JSON data sent by the client
    data = request.get_json()

    # generate a new unique id for the new item
    item_id = str(next_id)
    next_id += 1

    items[item_id] = data
    return jsonify({"id": item_id, "item": data}), 201

# READ all items
@app.route('/items', methods=["GET"])
def get_items():
    return jsonify(items)

# READ, UPDATE, DELETE a single item
@app.route('/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    item = items.get(item_id)

    if not item:
        return render_template('error.html', message="Item not found."), 404

    # READ
    if request.method == "GET":
        return jsonify(item)

    # UPDATE
    elif request.method == "PUT":
        data = request.get_json()
        if not data:
            return render_template('error.html', message="Invalid input."), 400

        items[item_id] = data
        return render_template('update.html', item_id=item_id, item=data)

    # DELETE
    elif request.method == "DELETE":
        deleted_item = items.pop(item_id)
        return render_template('delete.html', item_id=item_id, deleted_item=deleted_item)

if __name__ == "__main__":
    app.run(debug=True)