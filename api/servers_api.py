import json
from flask import request, session
from api.sessions import auth_required
from database.servers import ServersDB
from src.errors import err
from src.loader import app


@app.get("/api/servers/show")
@auth_required
def show_servers():
    servers = ServersDB.show_servers(session.get("client_id"))
    if servers == "0xdb": err.not_found("servers")
    return json.dumps(servers, indent=2), 200


@app.post("/api/servers/add")
@auth_required
def add_server():
    data = json.loads(request.data)
    server_id = ServersDB.add_server(
        data.get("name"),
        data.get("login_anyd"),
        data.get("password_anyd"),
        data.get("cpu"),
        data.get("ram"),
        data.get("storage"),
        data.get("ip"),
        data.get("activity"),
        session.get("client_id"))
    if server_id == "0xdb": return err.db_add("servers")
    return json.dumps(server_id), 200


@app.get("/api/servers/changeActivity")
@auth_required
def set_server_activity():
    args = request.args
    act = ServersDB.change_server_activity(args.get("server_id"), session.get("client_id"))
    if act == "0xdb": return err.db_update("servers")
    if act == "0xperm": return err.perm("set activity", "servers")
    return f"Success: changed to {act}", 200


@app.get("/api/servers/delete")
@auth_required
def delete_server():
    args = request.args
    changed = ServersDB.delete_server(
        args.get("server_id"),
        session.get("client_id")
    )
    if changed == "0xdb": return err.db_update("servers")
    if changed == "0xperm": return err.perm("set activity", "servers")
    return json.dumps(changed), 200


@app.post("/api/servers/change")
@auth_required
def change_server():
    data = json.loads(request.data)
    server_id = ServersDB.change_server(
        data.get("server_id"),
        data.get("name"),
        data.get("login_anyd"),
        data.get("password_anyd"),
        data.get("cpu"),
        data.get("ram"),
        data.get("storage"),
        data.get("ip"),
        session.get("client_id"))
    if server_id == "0xdb": return err.db_update("servers")
    if server_id == "0xperm": return err.perm("set activity", "servers")
    return json.dumps(server_id), 200
