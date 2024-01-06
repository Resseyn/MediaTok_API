import json

from flask import request, session

from api.sessions import auth_required
from database.smart_mode import SmartModeDB
from src.errors import err
from src.loader import app


@app.get("/api/smart_mode/show")
@auth_required
def show_mode():
    servers = SmartModeDB.show_smart_mode(session.get("client_id"))
    if servers == "0xst": return err.create("Not configured",404)
    if servers == "0xdb": return err.not_found("smart_modes")
    return json.dumps(servers, indent=2), 200


@app.post("/api/smart_mode/add")
@auth_required
def add_mode():
    data = json.loads(request.data)
    server_id = SmartModeDB.add_property(
        data["toggle"],
        data["sleep_time"],
        data["promotion_time_and_percentage"],
        session.get("client_id"))
    if server_id == "0xdb": return err.db_update("smart_modes")
    return json.dumps(server_id), 200

#
# @app.post("/api/smart_mode/change")
# @auth_required
# def change_mode():
#     data = json.loads(request.data)
#     server_id = SmartModeDB.change_smart_mode_property(
#         data["toggle"],
#         data["sleep_time"],
#         data["promotion_time_and_percentage"],
#         session.get("client_id"))
#     return json.dumps(server_id), 200
