import json
from flask import request, session
from api.sessions import auth_required
from database.links import LinksDB
from src.errors import err
from src.loader import app


@app.get("/api/links/show")
@auth_required
def show_links():
    links = LinksDB.show_links(session.get("client_id"))
    if links == "0xdb": return err.not_found("links")
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
    if link_id == "0xdb":
        return err.db_add("links")
    return json.dumps(link_id), 201


@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity():
    args = request.args
    act = LinksDB.change_link_activity(args.get("link_id"), session.get("client_id"))
    if act == "0xperm":
        return err.perm("set activity", "links")
    if act == "0xdb":
        return err.db_add("links")
    return f"Success: changed to {act}", 200


@app.get("/api/links/delete")
@auth_required
def delete_link():
    args = request.args
    is_deleted = LinksDB.delete_link(
        args.get("link_id"), session.get("client_id")
    )
    if is_deleted == "0xdb":
        return err.db_update("links")
    if is_deleted == "0xperm":
        return err.perm("delete", "links")
    return json.dumps(is_deleted), 200


@app.post("/api/links/change")
@auth_required
def change_link():
    data = json.loads(request.data)
    link_id = LinksDB.change_link(
        data.get("link_id"),
        data.get("link"),
        data.get("leads_to_post"),
        data.get("spec_links"),
        data.get("link_time"),
        data.get("traffic"),
        session.get("client_id"))
    if link_id == "0xperm":
        return err.perm("change", "links")
    return json.dumps(data), 201
