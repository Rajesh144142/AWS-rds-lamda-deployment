from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Use environment variables for security
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# CONNECTING SQLALCHEMY TO DATABASE
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username}
    

# CREATE TABLE
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello World"})

# API Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({"users": [i.to_dict() for i in users]})

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"}), 409

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully", "user": new_user.to_dict()}), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# AWS Lambda requires a callable function
# def create_app():
#     return app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

