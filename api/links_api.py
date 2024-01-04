import json

from flask import request, session

from api.sessions import auth_required
from database.links import LinksDB
from src.loader import app


@app.get("/api/links/show")
@auth_required
def show_links():
    links = LinksDB.show_links(session.get("client_id"))
    return json.dumps(links, indent=2), 200

@app.post("/api/links/add")
@auth_required
def add_link():
    format_link = request.form["link"]
    parsed_link = format_link.split(";")
    link_id = LinksDB.add_link(
                    parsed_link[0],
                    parsed_link[1],
                    parsed_link[3],
                    parsed_link[4],
                    parsed_link[5],
                    session.get("client_id"))
    return json.dumps(link_id), 200

@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity():
    args = request.args
    act = LinksDB.change_link_activity(args.get("link_id"))
    return f"Success: changed to {act}", 200


