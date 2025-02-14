from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)




# TELLING FLASK WHERE TO FIND POSTGRESQL DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leomessiten@rdspg172.cpyacgkokb25.ap-south-1.rds.amazonaws.com:5432/postgres'


# CONNECTING SQLALCHEMY TO DATABASE
db = SQLAlchemy(app)



# DEFINING THE MODEL
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username}
    

# CREAT THE TABLE 
with app.app_context():
    db.create_all()
    



# GET 
@app.route('/users', methods=['GET'])
def get_users():
    var = User.query.all()
    return jsonify({"users": [i.to_dict() for i in var]})



# POST
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json

    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"})

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"})

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully", "user": new_user.to_dict()})





# DELETE
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    var = User.query.get(user_id)

    if not var:
        return jsonify({"error": "User not found"})

    db.session.delete(var)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"})




# REUNNING IT
if __name__ == '__main__':
    app.run(debug=True) 