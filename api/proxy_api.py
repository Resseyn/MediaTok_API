import json
from flask import request, session
from api.sessions import auth_required
from database.proxy import ProxyDB
from src.errors import err
from src.loader import app


@app.get("/api/proxy/show")
@auth_required
def show_proxies():
    servers = ProxyDB.show_proxies(session.get("client_id"))
    if servers == "0xdb": return err.not_found("servers")
    return json.dumps(servers, indent=2), 200


@app.post("/api/proxy/add")
@auth_required
def add_proxy():
    data = json.loads(request.data)
    server_id = ProxyDB.add_proxy(
        data.get("server_id"),
        data.get("address"),
        session.get("client_id"))
    if server_id == "0xc": return err.create("Too many proxies!", 400)
    if server_id == "0xdb": return err.db_add("proxy")
    return json.dumps(server_id), 201


@app.get("/api/proxy/changeActivity")
@auth_required
def change_proxy_activity():
    args = request.args
    act = ProxyDB.change_proxy_activity(args.get("proxy_id"), session.get("client_id"))
    if act == "0xdb": return err.not_found("proxy")
    if act == "0xc": return err.create("Too many active proxies!", 400)
    return f"Success: changed to {act}", 200


@app.post("/api/proxy/change")
@auth_required
def change_proxy_address():
    data = json.loads(request.data)
    new_proxy = ProxyDB.change_proxy(data["proxy_id"], data.get("address"), session.get("client_id"))
    if new_proxy == "0xdb": return err.not_found("proxy")
    if new_proxy == "0xperm": return err.perm("change", "proxy")
    return json.dumps(new_proxy), 200


@app.get("/api/proxy/delete")
@auth_required
def delete_proxy():
    args = request.args
    changed = ProxyDB.delete_proxy(args.get("proxy_id"), session.get("client_id"))
    if changed == "0xdb": return err.not_found("proxy")
    if changed == "0xperm": return err.perm("delete", "proxy")
    return json.dumps(changed), 200
