import json
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import session, request, redirect, url_for, jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from config import api_secret_key
from database.users import UserDB
from src.loader import app

app.secret_key = api_secret_key
#app.config["JWT_SECRET_KEY"] = api_secret_key

# Decorator for protecting routes with JWT
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        print(request.headers)
        if token is None:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            kwargs["jwt"] = jwt.decode(token.split(" ")[1], app.secret_key, ["HS256", ])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated


# @app.get('/api/showCurrentUser')
# @auth_required
# def index():
#     if 'client_id' in session:
#         return jsonify({'user': f'{session["client_id"]}'}), 200
#     return 'You are not logged in', 403
#

@app.post('/api/auth/login')
def login():
    """
    Login

    ---
    tags:
      - login
    parameters:
      - in: body
        name: auth_Data
        required: true
        description: JSON object containing server details
        schema:
          type: object
          properties:
            login:
              type: string
              description: Your login
            password:
              type: string
              description: Your password
    responses:
      200:
        description: Succesfully logged in
      400:
        description: Wrong login or password
    """
    data = json.loads(request.data)
    client = UserDB.get_user_by_auth(data["login"], data["password"])
    if client is None:
        return jsonify({'message': "Wrong auth data"}), 400

    acsstoken = jwt.encode({'client_id': client["user_id"], 'exp': datetime.now() + timedelta(days=30)},
                       app.secret_key)
    access_token = create_access_token(identity={"id": client["user_id"]}, fresh=True)
    refresh_token = create_refresh_token(client["user_id"])
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

@app.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # jti = get_jwt()["jti"]
        # BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@app.get('/api/auth/logout')
@auth_required
def logout(jwt=None):
    request.cookies.clear()
    return jsonify({'message': "Success"}), 200
