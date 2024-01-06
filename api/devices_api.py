import json
from flask import request, session
from api.sessions import auth_required
from database.devices import DevicesDB
from src.loader import app


@app.get("/api/devices/show")
@auth_required
def show_devices():
    servers = DevicesDB.show_devices(session.get("client_id"))
    return json.dumps(servers, indent=2), 200


@app.post("/api/devices/add")
@auth_required
def add_device():
    data = json.loads(request.data)
    device = DevicesDB.add_device(
        data.get("phone"),
        data.get("desktop"),
        data.get("tablet"),
        session.get("client_id"))
    if device is None:
        return "Wrong data", 400
    return json.dumps(device), 200


@app.get("/api/devices/delete")
@auth_required
def delete_device():
    changed_device = DevicesDB.delete_device(
        session["client_id"],
    )
    if changed_device is None:
        return "Wrong data", 400
    return json.dumps(changed_device), 200


# @app.post("/api/devices/change")
# @auth_required
# def change_device():
#     data = json.loads(request.data)
#     changed_device = DevicesDB.change_device(
#         data.get("record_id"),
#         data.get("phone"),
#         data.get("desktop"),
#         data.get("tablet"), )
#     if changed_device is None:
#         return "Wrong data", 400
#     return json.dumps(changed_device), 200
