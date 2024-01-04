import json

from flask import request, session

from api.sessions import auth_required
from database.servers import ServersDB
from src.loader import app


@app.get("/api/smart_mode/show")
@auth_required
def show_servers():
    servers = ServersDB.show_servers(session.get("client_id"))
    return json.dumps(servers, indent=2), 200

@app.post("/api/smart_mode/add")
@auth_required
def add_server():
    server_id = ServersDB.add_server(
        request.form["name"],
        request.form["login"],
        request.form["password"],
        request.form["cpu"],
        request.form["ram"],
        request.form["storage"],
        request.form["ip"],
        request.form["activity"],
        session.get("client_id"))
    return json.dumps(server_id), 200

@app.get("/api/smart_mode/change")
@auth_required
def set_server_activity():
    args = request.args
    act = ServersDB.change_server_activity(args.get("server_id"))
    return f"Success: changed to {act}", 200


