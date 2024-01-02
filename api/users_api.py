import json

from flask import request

from api.sessions import auth_required
from database.users import user_db
from src.loader import app


@app.get("/api/users/show")
@auth_required
def show_users():
    user = user_db.get_user_by_id(2)

    return user.toJSON()

@app.get("/api/users/add")
@auth_required
def add_user():
    # cur.execute("SELECT * FROM users")
    #
    # users = cur.fetchall()
    users = [{"id": 1, "name": "stst"}, {"id": 1, "name": "stst"}, {"id": 1, "name": "stst"}]

    return json.dumps(users)

@app.get("/api/users/changeActivity")
@auth_required
def set_user_activity():
    args = request.args #TODO: from query get id and current activity and change from db
    # cur.execute("SELECT * FROM users")
    #
    # users = cur.fetchall()
    users = [{"id": 1, "name": "stst"}, {"id": 1, "name": "stst"}, {"id": 1, "name": "stst"}]

    return json.dumps(users)


