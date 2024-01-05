import json

from flask import request, session

from api.sessions import auth_required
from database.proxy import ProxyDB
from src.loader import app


@app.get("/api/proxy/show")
@auth_required
def show_proxies():
    servers = ProxyDB.show_proxies(session.get("client_id"))
    return json.dumps(servers, indent=2), 200


@app.post("/api/proxy/add")
@auth_required
def add_proxy():
    args = request.args
    server_id = ProxyDB.add_proxy(
        args.get("server_id"),
        request.form["address"],
        session.get("client_id"))
    if server_id is None:
        return "Too many proxies to server!", 400
    return json.dumps(server_id), 200

@app.get("/api/proxy/changeActivity")
@auth_required
def change_proxy_activity():
    args = request.args
    act = ProxyDB.change_proxy_activity(args.get("proxy_id"))
    if act is None:
        return "Unknown proxy_id!", 400
    return f"Success: changed to {act}", 200


@app.post("/api/proxy/change")
@auth_required
def change_proxy_address():
    request_data = json.loads(request.data)
    new_proxy = ProxyDB.change_proxy(request_data["proxy_id"],request_data["address"])
    if new_proxy is None:
        return "Unknown proxy_id!", 400
    return json.dumps(new_proxy), 200


@app.get("/api/proxy/delete")
@auth_required
def delete_proxy():
    args = request.args
    changed = ProxyDB.delete_proxy(
        args.get("proxy_id"),
    )
    if changed is None:
        return "Wrong data", 400
    return json.dumps(changed), 200