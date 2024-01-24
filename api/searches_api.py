import json
from flask import request
from api.sessions import auth_required
from database.searches import SearchesDB
from src.errors import err
from src.loader import app


@app.get("/api/searches/show")
@auth_required
def show_searches(jwt=None):
    """
    Show searches

    ---
    tags:
      - searches
    responses:
      200:
        description: List of searches
        schema:
          type: array
          items:
            type: object
            properties:
              search_id:
                type: integer
                description: ID of the search
              search:
                type: string
                description: Search details in the format "<link>;True;<properties>"
              activity:
                type: boolean
                description: Activity status of the search (true for active, false for inactive)
              created_at:
                type: integer
                description: Timestamp of when the search was created
            example:
              - search_id: 1
                search: "<link_1234>;True;<properties_1488>"
                type: "Google"
                activity: true
                created_at: 1704571530
              - search_id: 3
                search: "<li4542241;True;<35ops13411"
                type: "Google"
                activity: true
                created_at: 1704572256
              - search_id: 4
                search: "<li4hghgdshds1;True;True"
                type: "Google"
                activity: false
                created_at: 1704572266
      404:
        description: Data not found in searches
    """

    searches = SearchesDB.show_searches()
    if searches == "0xdb": return err.not_found("searches")
    result_map = [
        dict(search_id=search["search_id"], type=search["search_for"], search=";".join([search["link"],
                                                             str(True),
                                                             str(search["properties"]),
                                                             ]), activity=search["activity"],
             created_at=search["created_at"])
        for search in searches
    ]
    return json.dumps(result_map, indent=2), 200


@app.post("/api/searches/add")
@auth_required
def add_search(jwt=None):
    """
    Add a new search

    ---
    tags:
      - searches
    parameters:
      - in: body
        name: search_data
        required: true
        description: JSON object containing search details
        schema:
          type: object
          properties:
            type:
              type: string
              description: Type of the search
            link:
              type: string
              description: Link associated with the search
            props:
              type: boolean
              description: Properties of the search
          example:
            type: "Google"
            link: "<link_1234>;True;<properties_1488>"
            props: True
    responses:
      200:
        description: Search added successfully
        schema:
          type: object
          properties:
            search_id:
              type: integer
              description: ID of the newly added search
          example:
            search_id: 2
      500:
        description: Failed to add data in searches
    """

    data = json.loads(request.data)
    search_id = SearchesDB.add_search(
        data.get("type"),
        data.get("link"),
        data.get("props"),
        jwt.get("client_id"))
    if search_id == "0xdb": return err.db_add("searches")
    return json.dumps(search_id), 200


@app.get("/api/searches/changeActivity")
@auth_required
def set_search_activity(jwt=None):
    """
    Change search activity

    ---
    tags:
      - searches
    parameters:
      - in: query
        name: search_id
        type: integer
        required: true
        description: ID of the search to change activity
    responses:
      200:
        description: Search activity changed successfully
        schema:
          type: object
          properties:
            changed_to:
              type: boolean
              description: Indicates the new activity status
          example:
            changed_to: true
      403:
        description: Permission denied to set activity for search
      500:
        description: Failed to update data in searches
    """

    args = request.args
    act = SearchesDB.change_search_activity(args.get("search_id"))
    if act == "0xdb": return err.db_update("searches")
    if act == "0xperm": return err.perm("set activity", "searches")
    return json.dumps({"changed_to":act}), 200


@app.post("/api/searches/change")
@auth_required
def change_search(jwt=None):
    """
    Change search details

    ---
    tags:
      - searches
    parameters:
      - in: body
        name: search_data
        required: true
        description: JSON object containing search details to be changed
        schema:
          type: object
          properties:
            search_id:
              type: string
              description: ID of the search to be changed
            search_for:
              type: string
              description: New search_for value
            link:
              type: string
              description: New link value
            properties:
              type: string
              description: New properties value
          example:
            search_id: "1"
            search_for: "<search_for_coke>"
            link: "<link_1234>"
            properties: "<properties_1488>"
    responses:
      200:
        description: Search details changed successfully
        schema:
          type: object
          properties:
            search_id:
              type: string
              description: ID of the changed search
            search_for:
              type: string
              description: New search_for value
            link:
              type: string
              description: New link value
            properties:
              type: string
              description: New properties value
            list_seti:
              type: boolean
              description: Indicates whether the search is part of list_seti
            activity:
              type: boolean
              description: Activity status of the search (true for active, false for inactive)
            created_at:
              type: integer
              description: Timestamp of when the search was created
            creator_id:
              type: integer
              description: Creator of the search record ID
          example:
            search_id: "1"
            search_for: "<search_for_coke>"
            link: "<link_1234>"
            properties: "<properties_1488>"
            list_seti: true
            activity: true
            created_at: 1704571530
            creator_id: 228
      403:
        description: Permission denied to change search
      404:
        description: Data not found in searches
    """

    data = json.loads(request.data)
    changed_search = SearchesDB.change_search(
        data.get("search_id"),
        data.get("search_for"),
        data.get("link"),
        data.get("properties")
    )
    if changed_search == "0xdb": return err.db_update("searches")
    if changed_search == "0xperm": return err.perm("change", "searches")
    return json.dumps(changed_search), 200


@app.get("/api/searches/delete")
@auth_required
def delete_search(jwt=None):
    """
    Delete a search

    ---
    tags:
      - searches
    parameters:
      - in: query
        name: search_id
        type: integer
        required: true
        description: ID of the search to delete
    responses:
      200:
        description: Search deleted successfully
        schema:
          type: object
          properties:
            is_deleted:
              type: boolean
              description: Indicates whether the search was successfully deleted
          example:
            is_deleted: true
      403:
        description: Permission denied to delete search
      404:
        description: Data not found in searches
    """

    args = request.args
    is_deleted = SearchesDB.delete_search(
        args.get("search_id")
    )
    if is_deleted == "0xdb": return err.db_update("searches")
    if is_deleted == "0xperm": return err.perm("change", "searches")
    return json.dumps({"is_deleted":is_deleted}), 200
