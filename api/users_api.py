import json

from flask import request, session

from api.sessions import auth_required
from database.users import user_db
from src.loader import app


@app.get("/api/users/show")
@auth_required
def show_users():
    users = user_db.show_users(session["user_id"])
    return json.dumps(users, indent=2), 200

@app.post("/api/users/add")
@auth_required
def add_user():
    user_id = user_db.add_user(request.form["login"],
                    request.form["password"],
                    request.form["name"],
                    request.form["surname"],
                    session["user_id"])

    return json.dumps(user_id), 200

@app.get("/api/users/changeActivity")
@auth_required
def set_user_activity():
    args = request.args
    user_db.change_user_activity(args.get("user_id"))
    return "Success", 200


