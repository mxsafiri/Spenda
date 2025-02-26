from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///splitwise.db'
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(amount=data['amount'], description=data['description'], user_id=data['user_id'])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully!'}), 201

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{'amount': exp.amount, 'description': exp.description} for exp in expenses])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
