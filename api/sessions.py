from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import session, request, redirect, url_for, jsonify

from src.loader import app
from config import api_secret_key

app.secret_key = api_secret_key

# Decorator for protecting routes with JWT
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('jwt')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.secret_key, ["HS256",])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated


@app.get('/api/showCurrentUser')
@auth_required
def index():
    if 'user_id' in session:
        return jsonify({'user': f'{session["user_id"]}'}), 200
    return 'You are not logged in'


# @app.post('/api/auth/register')
# def register():
#     cur.execute(f"SELECT * FROM users WHERE email = {request.form["email"]}")
#     users = cur.fetchall()
#     if len(users) != 0:
#         return jsonify({'message': 'This email has been registered!'}), 200
#     else:
#         cur.execute(f"INSERT INTO users (email, username, password) VALUES ({request.form["email"]},"
#                     f"{request.form["username"]},"
#                     f"{request.form["password"]})")
#
#     return jsonify({'message': 'Successful registration'}) , 200


@app.post('/api/auth/login')
def login():
    # cur.execute(
    #     f"SELECT * FROM users WHERE email = {request.form["login"]} "
    #     f"OR username = {request.form["login"]} "
    #     f"AND password = {request.form["password"]};")
    # user = cur.fetchall()
    user = {
        "id":1,
        "email": "massib796@gmail.com",
        "username": "Resseyn",
        "password": 12345678
    }

    # if len(user) == 0:
    #     return "Incorrect data", 400

    # token = jwt.encode({'user': user[0].username, 'exp': datetime.now() + datetime.timedelta(day=30)},
    #                        app.secret_key)
    token = jwt.encode({'id': user["id"], 'exp': datetime.now() + timedelta(days=30)},
                           app.secret_key)
    session['jwt'] = token
    #session['user_id'] = user[0]["id"]
    session['user_id'] = user["id"]
    return redirect(url_for('index'))

@app.get('/api/auth/logout')
@auth_required
def logout():
    # remove the username from the session if it's there
    # session.pop('user_id', None)
    # session.pop('jwt', None)
    session.clear()
    return redirect(url_for('index'))

