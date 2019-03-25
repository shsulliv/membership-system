from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    card_number = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True)
    full_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    mobile_number = db.Column(db.Integer)
    pin = db.Column(db.Integer)

    def __init__(self, card_number, employee_id, full_name, email, mobile_number, pin):
        self.card_number = card_number
        self.employee_id = employee_id
        self.full_name = full_name
        self.email = email
        self.mobile_number = mobile_number
        self.pin = pin


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose.
        fields = ('full_name', 'employee_id', 'email', 'mobile_number', 'card_number')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Endpoint to create new user
@app.route("/user/new", methods=["POST"])
def add_user():
    card_number = request.json['card_number']
    employee_id = request.json['employee_id']
    full_name = request.json['full_name']
    email = request.json['email']
    mobile_number = request.json['mobile_number']
    pin = request.json['pin']

    new_user = User(card_number, employee_id, full_name, email, mobile_number, pin)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Endpoint to show all users.
@app.route("/user/all", methods=["GET"])
def get_all():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# Endpoint to get a single user by card_number.
@app.route("/user/<card_number>", methods=["GET"])
def get_user(card_number):
    user = User.query.get(card_number)
    return user_schema.jsonify(user)


# Endpoint to update use.
@app.route("/user/<card_number>", methods=["PUT"])
def user_update(card_number):
    user = User.query.get(card_number)
    employee_id = request.json['employee_id']
    full_name = request.json['full_name']
    email = request.json['email']
    mobile_number = request.json['mobile_number']

    user.employee_id = employee_id
    user.full_name = full_name
    user.email = email
    user.mobile_number = mobile_number

    db.session.commit()
    return user_schema.jsonify(user)


# Endpoint to delete user.
@app.route("/user/<card_number>", methods=["DELETE"])
def user_delete(card_number):
    user = User.query.get(card_number)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)