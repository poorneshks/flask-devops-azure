from flask import Flask, request, jsonify

app = Flask(__name__)
data_store = []

@app.route('/', methods=['GET'])
def home():
    return jsonify(message="✅ Flask app is running! Use /health or /submit"), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="✅ UP - PostgreSQL ready!"), 200

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    if not data or 'name' not in data:
        return jsonify(error="Missing 'name'"), 400

    data_store.append(data['name'])
    return jsonify(message="Data received", all_data=data_store), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
