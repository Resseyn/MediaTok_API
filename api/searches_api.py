import json
from flask import request, session
from api.sessions import auth_required
from database.searches import SearchesDB
from src.loader import app

@app.get("/api/searches/show")
@auth_required
def show_searches():
    searches = SearchesDB.show_searches(session.get("client_id"))
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
    args = request.args
    data = json.loads(request.data)
    search_id = SearchesDB.add_search(
        args.get("type"),
        data.get("link"),
        data.get("props"),
        session.get("client_id"))
    return json.dumps(search_id), 200

@app.get("/api/searches/changeActivity")
@auth_required
def set_search_activity():
    args = request.args
    act = SearchesDB.change_search_activity(args.get("search_id"))
    return f"Success: changed to {act}", 200

@app.get("/api/searches/delete")
@auth_required
def delete_search():
    args = request.args
    changed = SearchesDB.delete_search(
        args.get("search_id"),
    )
    if changed is None:
        return "Wrong data", 400
    return json.dumps(changed), 200
