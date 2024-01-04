import json

from flask import request, session

from api.sessions import auth_required
from database.proxy import ProxyDB
from src.loader import app


@app.get("/api/proxy/show")
@auth_required
def show_servers():
    servers = ProxyDB.show_proxies(session.get("client_id"))
    return json.dumps(servers, indent=2), 200


@app.post("/api/proxy/add")
@auth_required
def add_server():
    server_id = ProxyDB.add_proxy(
        request.form["name"],
        request.form["login"],
        request.form["password"],
        session.get("client_id"))
    return json.dumps(server_id), 200
