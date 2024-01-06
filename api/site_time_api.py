import json

from flask import request, session

from api.sessions import auth_required
from database.site_time import SiteTimeDB
from src.loader import app


@app.get("/api/site_time/show")
@auth_required
def show_times():
    servers = SiteTimeDB.show_times(session.get("client_id"))
    return json.dumps(servers, indent=2), 200


@app.post("/api/site_time/add")
@auth_required
def add_time():
    data = json.loads(request.data)
    emul = data["emulation_of_inactivity"].split("-")
    emul_between_art = data["emulation_of_inactivity_between_articles"].split("-")
    number_of_transactions = data["number_of_transitions"].split("-")
    try:
        new_time = SiteTimeDB.add_time(
            emul[0],
            emul[1],
            data["make_transitions"],
            emul_between_art[0],
            emul_between_art[1],
            number_of_transactions[0],
            number_of_transactions[1],
            session.get("client_id"))
    except:
        return "Invalid data", 400
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
