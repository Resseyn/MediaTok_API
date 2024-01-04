
import json

from flask import request, session

from api.sessions import auth_required
from database.searches import SearchesDB
from src.loader import app


@app.get("/api/searches/show")
@auth_required
def show_searches():
    searches = SearchesDB.show_searches(session.get("client_id"))
    return json.dumps(searches, indent=2), 200


@app.post("/api/searches/add")
@auth_required
def add_search():
    args = request.args
    search_id = SearchesDB.add_search(
        args.get("type"),
        request.form["link"],
        request.form["props"],
        session.get("client_id"))
    return json.dumps(search_id), 200


@app.get("/api/searches/changeActivity")
@auth_required
def set_search_activity():
    args = request.args
    act = SearchesDB.change_search_activity(args.get("server_id"))
    return f"Success: changed to {act}", 200
