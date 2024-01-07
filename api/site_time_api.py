import json

from flask import request, session

from api.sessions import auth_required
from database.site_time import SiteTimeDB
from src.errors import err
from src.loader import app


@app.get("/api/site_time/show")
@auth_required
def show_times():
    """
    Show site time configurations

    ---
    tags:
      - site_time

    responses:
      200:
        description: Site time configurations retrieved successfully
        schema:
          type: object
          properties:
            emulation_of_inactivity_min:
              type: integer
              description: Minimum duration for the emulation of user inactivity (minutes)
            emulation_of_inactivity_max:
              type: integer
              description: Maximum duration for the emulation of user inactivity (minutes)
            make_transitions:
              type: boolean
              description: Indicates whether transitions between articles are enabled (true or false)
            emulation_of_inactivity_between_articles_min:
              type: integer
              description: Minimum duration for the emulation of inactivity between articles (minutes)
            emulation_of_inactivity_between_articles_max:
              type: integer
              description: Maximum duration for the emulation of inactivity between articles (minutes)
            number_of_transitions_min:
              type: integer
              description: Minimum number of transitions between articles
            number_of_transitions_max:
              type: integer
              description: Maximum number of transitions between articles
            creator_id:
              type: integer
              description: Creator of the site time record ID
          example:
            emulation_of_inactivity_min: 15
            emulation_of_inactivity_max: 25
            make_transitions: false
            emulation_of_inactivity_between_articles_min: 10
            emulation_of_inactivity_between_articles_max: 15
            number_of_transitions_min: 4
            number_of_transitions_max: 6
            creator_id: 228
      404:
        description: Data not found in site_time
    """

    site_time_curr = SiteTimeDB.show_times(session.get("client_id"))
    if site_time_curr == "0xst": return err.create("Not configured", 404)
    if site_time_curr == "0xdb": return err.not_found("times")
    return json.dumps(site_time_curr, indent=2), 200


@app.post("/api/site_time/add")
@auth_required
def add_time():
    """
    Add site time configurations

    ---
    tags:
      - site_time
    parameters:
      - in: body
        name: site_time_data
        required: true
        description: JSON object containing site time configurations to be added
        schema:
          type: object
          properties:
            emulation_of_inactivity:
              type: string
              description: Range for the emulation of user inactivity in the format "min-max"
            make_transitions:
              type: boolean
              description: Indicates whether transitions between articles are enabled (true or false)
            emulation_of_inactivity_between_articles:
              type: string
              description: Range for the emulation of inactivity between articles in the format "min-max"
            number_of_transitions:
              type: string
              description: Range for the number of transitions between articles in the format "min-max"
    responses:
      200:
        description: Site time configurations added successfully
        schema:
          type: object
          properties:
            emulation_of_inactivity_min:
              type: string
              description: Minimum duration for the emulation of user inactivity (minutes)
            emulation_of_inactivity_max:
              type: string
              description: Maximum duration for the emulation of user inactivity (minutes)
            make_transitions:
              type: boolean
              description: Indicates whether transitions between articles are enabled (true or false)
            emulation_of_inactivity_between_articles_min:
              type: string
              description: Minimum duration for the emulation of inactivity between articles (minutes)
            emulation_of_inactivity_between_articles_max:
              type: string
              description: Maximum duration for the emulation of inactivity between articles (minutes)
            number_of_transitions_min:
              type: string
              description: Minimum number of transitions between articles
            number_of_transitions_max:
              type: string
              description: Maximum number of transitions between articles
            creator_id:
              type: integer
              description: Creator of the site time record ID
          example:
            emulation_of_inactivity_min: "5"
            emulation_of_inactivity_max: "6"
            make_transitions: true
            emulation_of_inactivity_between_articles_min: "7"
            emulation_of_inactivity_between_articles_max: "8"
            number_of_transitions_min: "9"
            number_of_transitions_max: "10"
            creator_id: 228
      404:
        description: Data not found in site_time
    """

    data = json.loads(request.data)
    emul = data["emulation_of_inactivity"].split("-")
    emul_between_art = data["emulation_of_inactivity_between_articles"].split("-")
    number_of_transactions = data["number_of_transitions"].split("-")
    new_time = SiteTimeDB.add_time(
        emul[0],
        emul[1],
        data["make_transitions"],
        emul_between_art[0],
        emul_between_art[1],
        number_of_transactions[0],
        number_of_transactions[1],
        session.get("client_id"))
    if new_time == "0xdb": return err.not_found("times")
    return json.dumps(new_time), 200

#
# @app.post("/api/site_time/change")
# @auth_required
# def change_times():
#     data = json.loads(request.data)
#     emul = data["emulation_of_inactivity"].split("-")
#     emul_between_art = data["emulation_of_inactivity"].split("-")
#     number_of_transactions = data["emulation_of_inactivity"].split("-")
#     try:
#         changed_time = SiteTimeDB.change_times(
#             session["client_id"],
#             emul[0],
#             emul[1],
#             data["make_transitions"],
#             emul_between_art[0],
#             emul_between_art[1],
#             number_of_transactions[0],
#             number_of_transactions[1])
#     except:
#         return "Invalid data", 400
#     return json.dumps(changed_time), 200
