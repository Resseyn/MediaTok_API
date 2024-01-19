import json
from flask import request
from api.sessions import auth_required
from database.devices import DevicesDB
from src.loader import app
from src.errors import err


@app.get("/api/devices/show")
@auth_required
def show_devices(jwt=None):
    """
    Show devices
    ---
    tags:
      - devices
    responses:
      200:
        description: Current devices settings
        schema:
          type: object
          properties:
            phone:
              type: integer
              description: Percentage of phone
            desktop:
              type: integer
              description: Percentage of phone+desktop
            tablet:
              type: integer
              description: Percentage of phone+desktop+tablet (always = 100)
            creator_id:
              type: integer
              description: Creator of devices record id
      400:
        description: Devices is not configured
      404:
        description: Database error
    """
    servers = DevicesDB.show_devices(jwt.get("client_id"))
    if servers == "0xst":
        return err.create("Not configured",400)
    if servers == "0xdb":
        return err.not_found("devices")
    return json.dumps(servers, indent=2), 200


@app.post("/api/devices/add")
@auth_required
def add_device(jwt=None):
    """
Add a new device
---
tags:
  - devices
parameters:
  - in: body
    name: device
    required: true
    description: |
      Device information in the format "phone;desktop;tablet", example: "30;70;100"
    schema:
      type: object
      properties:
        device:
          type: string
responses:
  200:
    description: Device added successfully
    schema:
      type: object
      properties:
        phone:
          type: integer
          description: Percentage of phone
        desktop:
          type: integer
          description: Percentage of phone+desktop
        tablet:
          type: integer
          description: Percentage of phone+desktop+tablet (always = 100)
        creator_id:
          type: integer
          description: Creator of devices record id
  400:
    description: Device not added (db error)

    """
    data = json.loads(request.data)
    phone, desktop, tablet = list(map(int, data.get("device").split(";")))
    device = DevicesDB.add_device(
        phone, desktop, tablet,
        jwt.get("client_id"))
    if device == "0xn":
        return err.create("Invalid input", 400)
    if device == "0xdb":
        return err.not_found("devices")
    return json.dumps(device), 200


@app.get("/api/devices/delete")
@auth_required
def delete_device(jwt=None):
    """
    Delete a device
    ---
    tags:
      - devices
    responses:
      200:
        description: Device deleted successfully
        schema:
          type: object
          properties:
            deleted:
              type: boolean
              description: Indicates whether the device was successfully deleted
          example:
            deleted: true
      404:
        description: Data not found in devices
    """
    deleted_device = DevicesDB.delete_device(
        jwt.get("client_id"),
    )
    if deleted_device == "0xdb":
        return err.not_found("devices")
    return json.dumps({"deleted":deleted_device}), 200

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
