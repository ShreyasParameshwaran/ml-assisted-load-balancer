from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


data_store = {}

@app.route('/')
def time_display():
    current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    return f'Current time is {current_time}'


@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data_store)

@app.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = data_store.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    item_id = request.json.get('id')
    name = request.json.get('name')
    if item_id and name:
        data_store[item_id] = {'id': item_id, 'name': name}
        return jsonify(data_store[item_id]), 201
    else:
        return jsonify({"error": "Invalid data"}), 400


@app.route('/time', methods=['POST'])
def get_current_time():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({"current_time": current_time})

@app.route('/predict', methods=['POST'])
def predictor():
    input_data = request.json.get('datetime')
    try:
        input_datetime = datetime.strptime(input_data, '%Y-%m-%d %H:%M:%S')
        return jsonify({"predictor": input_data})
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400



if __name__ == '__main__':
    app.run(debug=True)
