from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import session, request, redirect, url_for, jsonify

from config import api_secret_key
from database.users import UserDB
from src.loader import app

app.secret_key = api_secret_key


# Decorator for protecting routes with JWT
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('jwt')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.secret_key, ["HS256", ])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated


@app.get('/api/showCurrentUser')
@auth_required
def index():
    if 'client_id' in session:
        return jsonify({'user': f'{session["client_id"]}'}), 200
    return 'You are not logged in', 403


@app.post('/api/auth/login')
def login():
    client = UserDB.get_user_by_auth(request.form["login"], request.form["password"])
    if client is None:
        return "Wrong auth data", 400

    token = jwt.encode({'id': client["user_id"], 'exp': datetime.now() + timedelta(days=30)},
                       app.secret_key)
    session['jwt'] = token
    session['client_id'] = client["user_id"]
    return redirect(url_for('index'))


@app.get('/api/auth/logout')
@auth_required
def logout():
    session.clear()
    return redirect(url_for('index'))
