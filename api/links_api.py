import json

from flask import request, session

from api.sessions import auth_required
from database.links import LinksDB
from src.loader import app


@app.get("/api/links/show")
@auth_required
def show_links():
    links = LinksDB.show_links()
    return json.dumps(links, indent=2), 200

@app.post("/api/links/add")
@auth_required
def add_link():
    format_link = request.form["link"]
    link_id = LinksDB.add_link(
                    request.form["link"],
                    request.form["login"],
                    request.form["password"],
                    request.form["cpu"],)
    return json.dumps(link_id), 200

@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity():
    args = request.args
    act = LinksDB.change_link_activity(args.get("link_id"))
    return f"Success: changed to {act}", 200


