import json
from flask import request, session
from api.sessions import auth_required
from database.servers import ServersDB
from src.loader import app

@app.get("/api/servers/show")
@auth_required
def show_servers():
    servers = ServersDB.show_servers(session.get("client_id"))
    return json.dumps(servers, indent=2), 200

@app.post("/api/servers/add")
@auth_required
def add_server():
    data = json.loads(request.data)
    server_id = ServersDB.add_server(
        data.get("name"),
        data.get("login"),
        data.get("password"),
        data.get("cpu"),
        data.get("ram"),
        data.get("storage"),
        data.get("ip"),
        data.get("activity"),
        session.get("client_id"))
    return json.dumps(server_id), 200

@app.get("/api/servers/changeActivity")
@auth_required
def set_server_activity():
    args = request.args
    act = ServersDB.change_server_activity(args.get("server_id"))
    return f"Success: changed to {act}", 200

@app.get("/api/servers/delete")
@auth_required
def delete_server():
    args = request.args
    changed = ServersDB.delete_server(
        args.get("server_id"),
    )
    if changed is None:
        return "Wrong data", 400
    return json.dumps(changed), 200
