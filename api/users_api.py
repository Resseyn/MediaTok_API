import json
from flask import request, session
from api.sessions import auth_required
from database.users import UserDB
from src.errors import err
from src.loader import app


@app.get("/api/users/show")
@auth_required
def show_users():
    users = UserDB.show_users()
    if users == "0xdb": return err.not_found("users")
    return json.dumps(users, indent=2), 200


@app.post("/api/users/add")
@auth_required
def add_user():
    data = json.loads(request.data)
    user_id = UserDB.add_user(data["login"], data["password"], data["name"], data["surname"])
    if user_id == "0xp": return err.db_add("users")
    return json.dumps(user_id), 200


@app.post("/api/users/change")
@auth_required
def change_user():
    data = json.loads(request.data)
    changed_user = UserDB.change_user(data["user_id"], data["login"], data["password"], data["name"],
                                      data["surname"])
    if changed_user == "0xu": return err.not_found("users")
    if changed_user == "0xdb": return err.db_update("users")
    return json.dumps(changed_user), 200


@app.get("/api/users/changeActivity")
@auth_required
def set_user_activity():
    args = request.args
    act = UserDB.change_user_activity(args.get("user_id"))
    if act == "0xdb": return err.db_update("users")
    return f"Success: changed to {act}", 200


@app.get("/api/users/delete")
@auth_required
def delete_user():
    args = request.args
    if session["client_id"] == args.get("user_id"):
        return err.create("ебать ты тупой себя удаляешь", "228")
    changed = UserDB.delete_user(args.get("user_id"))
    if changed == "0xdb":
        return err.not_found("users")
    return json.dumps(changed), 200
