import json

from flask import request, session

from api.sessions import auth_required
from database.devices import DevicesDB, Device
from src.loader import app


@app.get("/api/devices/show")
@auth_required
def show_devices():
    servers = DevicesDB.show_devices(session.get("client_id"))
    return json.dumps(servers, indent=2), 200


@app.post("/api/devices/add")
@auth_required
def add_device():
    device = DevicesDB.add_device(
        request.form["phone"],
        request.form["desktop"],
        request.form["tablet"],
        session.get("client_id"))
    if device is None:
        return "Wrong data", 400
    return json.dumps(device), 200


@app.get("/api/devices/change")
@auth_required
def change_device():
    args = request.args
    changed_device = DevicesDB.change_device(
        args.get("record_id"),
        request.form["phone"],
        request.form["desktop"],
        request.form["tablet"]
    )
    if changed_device is None:
        return "Wrong data"
    return json.dumps(changed_device), 200
