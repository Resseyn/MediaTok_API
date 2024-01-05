import json

from flask import request, session

from api.sessions import auth_required
from database.site_time import SiteTime, SiteTimeDB
from src.loader import app


@app.get("/api/site_time/show")
@auth_required
def show_times():
    servers = SiteTimeDB.show_times(session.get("client_id"))
    return json.dumps(servers, indent=2), 200
# TODO:необработанные ошибка апи


@app.post("/api/site_time/add")
@auth_required
def add_time():
    new_time = SiteTimeDB.add_time(
        request.form["emulation_of_inactivity_min"],
        request.form["emulation_of_inactivity_max"],
        request.form["make_transitions"],
        request.form["emulation_of_inactivity_between_articles_min"],
        request.form["emulation_of_inactivity_between_articles_max"],
        request.form["number_of_transitions_min"],
        request.form["number_of_transitions_max"],
        session.get("client_id"))
    return json.dumps(new_time)


@app.get("/api/site_time/change")
@auth_required
def change_times():
    changed_time = SiteTimeDB.change_times(
        request.form['time_id'],
        request.form['emulation_of_inactivity_min'],
        request.form['emulation_of_inactivity_max'],
        request.form['make_transitions'],
        request.form['emulation_of_inactivity_between_articles_min'],
        request.form['emulation_of_inactivity_between_articles_max'],
        request.form['number_of_transitions_min'],
        request.form['number_of_transitions_max']
    )

    return json.dumps(changed_time),200
