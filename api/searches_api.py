import json
from flask import request, session
from api.sessions import auth_required
from database.searches import SearchesDB
from src.errors import err
from src.loader import app


@app.get("/api/searches/show")
@auth_required
def show_searches():
    searches = SearchesDB.show_searches(session.get("client_id"))
    if searches == "0xdb": return err.not_found("searches")
    result_map = [
        dict(search_id=search["search_id"], search=";".join([search["link"],
                                                             str(True),
                                                             str(search["properties"]),
                                                             ]), activity=search["activity"],
             created_at=search["created_at"])
        for search in searches
    ]
    return json.dumps(result_map, indent=2), 200


@app.post("/api/searches/add")
@auth_required
def add_search():
    data = json.loads(request.data)
    search_id = SearchesDB.add_search(
        data.get("type"),
        data.get("link"),
        data.get("props"),
        session.get("client_id"))
    if search_id == "0xdb": return err.db_add("searches")
    return json.dumps(search_id), 200


@app.get("/api/searches/changeActivity")
@auth_required
def set_search_activity():
    args = request.args
    act = SearchesDB.change_search_activity(args.get("search_id"), session.get("client_id"))
    if act == "0xdb": return err.db_update("searches")
    if act == "0xperm": return err.perm("set activity", "searches")
    return f"Success: changed to {act}", 200


@app.post("/api/searches/change")
@auth_required
def change_search():
    data = json.loads(request.data)
    changed_search = SearchesDB.change_search(
        data.get("search_id"),
        data.get("search_for"),
        data.get("link"),
        data.get("properties"),
        session.get("client_id")
    )
    if changed_search == "0xdb": return err.db_update("searches")
    if changed_search == "0xperm": return err.perm("change", "searches")
    return json.dumps(changed_search), 200


@app.get("/api/searches/delete")
@auth_required
def delete_search():
    args = request.args
    changed = SearchesDB.delete_search(
        args.get("search_id"),
        session.get("client_id")
    )
    if changed == "0xdb": return err.db_update("searches")
    if changed == "0xperm": return err.perm("change", "searches")
    return json.dumps(changed), 200
