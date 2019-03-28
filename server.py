from datetime import timedelta
from flask import Flask, request, jsonify, session, app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from random import randint


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.secret_key = str(randint(0, 1000))


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


class User(db.Model):
    card_number = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True)
    full_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    mobile_number = db.Column(db.Integer)
    pin = db.Column(db.Integer)
    card_balance = db.Column(db.Integer)

    def __init__(self, card_number, employee_id, full_name, email, mobile_number, pin):
        self.card_number = card_number
        self.employee_id = employee_id
        self.full_name = full_name
        self.email = email
        self.mobile_number = mobile_number
        self.pin = pin
        self.card_balance = 0


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose.
        fields = ('full_name',
                  'employee_id',
                  'email',
                  'mobile_number',
                  'card_number',
                  'card_balance')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Endpoint to create new user.
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

    return 'Welcome {}! Your current card balance is &#163;{}.'\
        .format(new_user.full_name, new_user.card_balance)


# Endpoint to show all users. This endpoint is primarily used for
# testing that data has been correctly added to the database,
# which is why it returns the JSON payload and not a message.
@app.route("/user/all", methods=["GET"])
def get_all():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# Endpoint to get a single user.
@app.route("/user/<card_number>", methods=["GET"])
def get_user(card_number):
    user = User.query.get(card_number)
    if user:
        return 'Welcome back {}! Your current card balance is &#163;{}.'\
            .format(user.full_name, user.card_balance)
    else:
        return 'No card found for that number in the system. Please register your card.'


# Endpoint to update user. This endpoint is currently
# limited to topping up the user's card.
@app.route("/user/<card_number>", methods=["PUT"])
def update_user(card_number):
    user = User.query.get(card_number)
    top_up = request.json['card_balance']

    user.card_balance += top_up

    db.session.commit()
    return 'Your card balance is now &#163;{}.'.format(user.card_balance)


# Endpoint to delete user.
@app.route("/user/<card_number>", methods=["DELETE"])
def delete_user(card_number):
    user = User.query.get(card_number)
    db.session.delete(user)
    db.session.commit()

    return 'Your account for card number {} has been deleted.'\
        .format(user.card_number)


if __name__ == '__main__':
    app.run(debug=True)