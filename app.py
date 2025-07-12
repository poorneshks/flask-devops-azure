from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Load DB URL from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define DB model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="PostgreSQL connected!"), 200

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    if not data or 'name' not in data:
        return jsonify(error="Missing name"), 400

    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()

    # Fetch all names from DB
    users = User.query.all()
    all_names = [user.name for user in users]

    return jsonify(message="Data stored in DB", all_data=all_names), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create table if not exists
    app.run(host='0.0.0.0', port=5000)
