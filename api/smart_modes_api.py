import json
import time

from flask import request, session

from api.sessions import auth_required
from database.smart_mode import SmartModeDB
from src.loader import app


@app.get("/api/smart_mode/show")
@auth_required
def show_mode():
    servers = SmartModeDB.show_servers(session.get("client_id"))
    return json.dumps(servers, indent=2), 200

@app.post("/api/smart_mode/add")
@auth_required
def add_mode():
    server_id = SmartModeDB.add_property(
        request.form["toggle"],
        request.form["sleep_time"],
        request.form["promotion_time_and_percentage"],
        session.get("client_id"))
    return json.dumps(server_id), 200

@app.get("/api/smart_mode/change")
@auth_required
def change_mode():
    server_id = SmartModeDB.change_smart_mode_property(
        request.form["toggle"],
        request.form["sleep_time"],
        request.form["promotion_time_and_percentage"],
        time.time(),
        session.get("client_id"))
    return json.dumps(server_id),200
