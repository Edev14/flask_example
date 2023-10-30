import sys
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/')

def with_auth():
    if "user_id" in session: return True
    return False

@bp.route('/users', methods=['GET'])
def get_all_users():
    db = get_db()
    users = db.query(User).all()
    users_data = [{ "id": user.id, "username": user.username, "email": user.email } for user in users]
    return jsonify(users_data)

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user =  db.query(User).filter(User.id == user_id).one()

    if user: return jsonify({ "id": user.id, "username": user.username, "email": user.email })
    else: return jsonify({"message": "User not found"}), 404

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    db = get_db()
    user = db.query(User).filter(User.id == user_id).one()

    if user:
        session.clear()
        return jsonify({"message": "User deleted"})
    
    else: return jsonify({"message": "User not found"}), 404

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    db = get_db()
    try:
        new_user = User(username = data['username'], email = data['email'], password = data['password'])
        db.add(new_user)
        db.commit()
    except:
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify(message = 'Signup failed'), 500

    session.clear()
    session['user_id'] = new_user.id
    session['loggedIn'] = True
    return jsonify(id = new_user.id)

@bp.route('/restricted', methods=['GET'])
def restricted():

    if with_auth(): return jsonify("Restricted Area: Logged in users only...")
    return jsonify("Not logged in..."), 401

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])
        return jsonify(message = 'Incorrect credentials'), 400
    
    if user.verify_password(data['password']) == False: return jsonify(message = 'Incorrect credentials'), 400
    
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True
    return jsonify(id = user.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    session.clear()
    return '', 204