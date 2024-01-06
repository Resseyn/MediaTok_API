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
    data = json.loads(request.data)
    link_id = LinksDB.add_link(
        data.get("link"),
        data.get("leads_to_post"),
        data.get("spec_links"),
        data.get("link_time"),
        data.get("traffic"),
        session.get("client_id"))
    return json.dumps(link_id), 200


@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity():
    args = request.args
    act = LinksDB.change_link_activity(args.get("link_id"),session.get("client_id"))
    if act is not None:
        return f"Success: changed to {act}", 200
    elif act == "Permission error":
        return f"No permission to change", 403
    else:
        return f"Error changing link activity",400


@app.get("/api/links/delete")
@auth_required
def delete_link():
    args = request.args
    changed = LinksDB.delete_link(
        args.get("link_id"),session.get("client_id")
    )
    if changed is None:
        return "Wrong data", 400
    if changed == "Permission error":
        return "No permission to delete", 403
    return json.dumps(changed), 200


@app.post("/api/links/change")
@auth_required
def change_link():
    try:
        data = json.loads(request.data)
        link_id = LinksDB.change_link(
            data.get("link_id"),
            data.get("link"),
            data.get("leads_to_post"),
            data.get("spec_links"),
            data.get("link_time"),
            data.get("traffic"),
            session.get("client_id"))
        if link_id is None:
            return "Wrong data", 400
    except:
        return "Wrong data", 400
    return json.dumps(link_id), 200
