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
    data = json.loads(request.data)
    user_id = UserDB.add_user(data["login"], data["password"], data["name"], data["surname"])
    if user_id is None:
        return "This login is present!", 400
    return json.dumps(user_id), 200

@app.get("/api/users/changeActivity")
@auth_required
def set_user_activity():
    args = request.args
    act = UserDB.change_user_activity(args.get("user_id"))
    return f"Success: changed to {act}", 200

@app.get("/api/users/delete")
@auth_required
def delete_user():
    args = request.args
    if session["user_id"] != args.get("user_id"):
        return "Wrong data", 400
    changed = UserDB.delete_user(args.get("user_id"))
    if changed is None:
        return "Wrong data", 400
    return json.dumps(changed), 200
