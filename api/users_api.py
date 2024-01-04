import json

from flask import request, session

from api.sessions import auth_required
from database.users import UserDB
from src.loader import app


@app.get("/api/users/show")
@auth_required
def show_users():
    users = UserDB.show_users()
    return json.dumps(users, indent=2), 200

@app.post("/api/users/add")
@auth_required
def add_user():
    user_id = UserDB.add_user(request.form["login"],
                    request.form["password"],
                    request.form["name"],
                    request.form["surname"])
    if user_id == None:
        return "This login is present!"
    return json.dumps(user_id), 200

@app.get("/api/users/changeActivity")
@auth_required
def set_user_activity():
    args = request.args
    act = UserDB.change_user_activity(args.get("user_id"))
    return f"Success: changed to {act}", 200


