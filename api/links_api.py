import json

from flask import request, session

from api.sessions import auth_required
from database.links import LinksDB
from src.loader import app


@app.get("/api/links/show")
@auth_required
def show_links():
    links = LinksDB.show_links(session.get("client_id"))
    result_map = [
        dict(link_id=link["link_id"], link=";".join([link["link"],
                                                     str(link["leads_to_post"]),
                                                     str(link["to_a_specific_link"]),
                                                     link["spec_links"],
                                                     str(link["time"]),
                                                     str(link["traffic"]), ]), activity=link["activity"],
             created_at=link["created_at"])
        for link in links
    ]
    return json.dumps(result_map, indent=2), 200


@app.post("/api/links/add")
@auth_required
def add_link():
    # format_link = request.form["link"]
    # parsed_link = format_link.split(";")
    # link_id = LinksDB.add_link(
    #     parsed_link[0],
    #     parsed_link[1],
    #     parsed_link[3],
    #     parsed_link[4],
    #     parsed_link[5],
    #     session.get("client_id"))
    # return json.dumps(link_id), 200
    link_id = LinksDB.add_link(
        request.form["link"],
        request.form["leads_to_post"],
        request.form["spec_links"],
        request.form["link_time"],
        request.form["traffic"],
        session.get("client_id"))
    return json.dumps(link_id), 200


@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity():
    args = request.args
    act = LinksDB.change_link_activity(args.get("link_id"))
    return f"Success: changed to {act}", 200

@app.get("/api/links/delete")
@auth_required
def delete_link():
    args = request.args
    changed = LinksDB.delete_link(
        args.get("link_id"),
    )
    if changed is None:
        return "Wrong data", 400
    return json.dumps(changed), 200
@app.post("/api/links/change")
@auth_required
def change_link():
    args = request.args
    try:
        link_id = LinksDB.change_link(
            args.get("link_id"),
            request.form["link"],
            request.form["leads_to_post"],
            request.form["spec_links"],
            request.form["link_time"],
            request.form["traffic"],
            session.get("client_id"))
        if link_id is None:
            return "Wrong data", 400
    except:
        return "Wrong data", 400
    return json.dumps(link_id), 200
