import json

from flask import request

from api.sessions import auth_required
from database.smart_mode import SmartModeDB
from src.errors import err
from src.loader import app


@app.get("/api/smart_mode/show")
@auth_required
def show_mode(jwt=None):
    """
    Show smart mode configurations

    ---
    tags:
      - smart_mode
    responses:
      200:
        description: Smart mode configurations retrieved successfully
        schema:
          type: object
          properties:
            toggle:
              type: boolean
              description: Indicates whether the smart mode is enabled or disabled (true or false)
            sleep_time:
              type: string
              description: Sleep time duration in milliseconds
            promotion_time_and_percentage:
              type: string
              description: Range for promotion time and percentage in the format "time-percentage"
            update_time:
              type: integer
              description: Update time interval in minutes
            creator_id:
              type: integer
              description: Creator of the smart mode record ID
          example:
            toggle: true
            sleep_time: "10000"
            promotion_time_and_percentage: "22-8"
            update_time: 2
            creator_id: 228
      404:
        description: Data not found in smart_modes
    """

    servers = SmartModeDB.show_smart_mode(jwt.get('client_id'))
    if servers == "0xst": return err.create("Not configured", 400)
    if servers == "0xdb": return err.not_found("smart_modes")
    return json.dumps(servers, indent=2), 200


@app.post("/api/smart_mode/add")
@auth_required
def add_mode(jwt=None):
    """
    Add smart mode configurations

    ---
    tags:
      - smart_mode
    parameters:
      - in: body
        name: smart_mode_data
        required: true
        description: JSON object containing smart mode configurations to be added
        schema:
          type: object
          properties:
            toggle:
              type: boolean
              description: Indicates whether the smart mode is enabled or disabled (true or false)
            sleep_time:
              type: string
              description: Sleep time duration in milliseconds
            promotion_time_and_percentage:
              type: string
              description: Time and percentage configuration for promotions in the format "time1:percentage1;time2:percentage2;..."
    responses:
      200:
        description: Smart mode configurations added successfully
        schema:
          type: object
          properties:
            toggle:
              type: boolean
              description: Indicates whether the smart mode is enabled or disabled (true or false)
            sleep_time:
              type: string
              description: Sleep time duration in milliseconds
            promotion_time_and_percentage:
              type: string
              description: Time and percentage configuration for promotions in the format "time1:percentage1;time2:percentage2;..."
            update_time:
              type: integer
              description: Update time interval in minutes
            creator_id:
              type: integer
              description: Creator of the smart mode record ID
          example:
            toggle: true
            sleep_time: "60000"
            promotion_time_and_percentage: "0:30;3:50;6:90;9:100;12:100;15:100;18:100;21:80»"
            update_time: 17
            creator_id: 228
      404:
        description: Data not found in smart_modes
    """

    data = json.loads(request.data)
    server_id = SmartModeDB.add_property(
        data["toggle"],
        data["sleep_time"],
        data["promotion_time_and_percentage"],
        jwt.get('client_id'))
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
