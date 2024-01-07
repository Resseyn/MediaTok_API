import json
from flask import request, session
from api.sessions import auth_required
from database.links import LinksDB
from src.errors import err
from src.loader import app


@app.get("/api/links/show")
@auth_required
def show_links():
    """
    Show links
    ---
    tags:
      - links
    responses:
      200:
        description: List of links
        schema:
          type: array
          items:
            type: object
            properties:
              link_id:
                type: string
                description: ID of the link
              link:
                type: string
                description: Details of the link
              leads_to_post:
                type: boolean
                description: Leads to a post
              to_a_specific_link:
                type: boolean
                description: Leads to a specific link
              spec_links:
                type: string
                description: Specific links associated with the link
              link_time:
                type: string
                description: Time associated with the link
              traffic:
                type: string
                description: Traffic associated with the link
          example:
            - link_id: "2"
              link: "link3.xxx"
              leads_to_post: true
              to_a_specific_link: true
              spec_links: "ok.ru"
              link_time: "122138"
              traffic: "939"
            - link_id: "2"
              link: "link.xxx"
              leads_to_post: true
              to_a_specific_link: true
              spec_links: "vk.com"
              link_time: "1313138"
              traffic: "5429"
      404:
        description: Data not found in links
    """
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
    """
    Add a new link
    ---
    tags:
      - links
    parameters:
      - in: body
        name: link_data
        required: true
        description: JSON object containing link details
        schema:
          type: object
          properties:
            link:
              type: string
              description: The link URL
            leads_to_post:
              type: boolean
              description: Indicates if the link leads to a post
            to_a_specific_link:
              type: boolean
              description: Indicates if the link leads to a specific link
            spec_links:
              type: string
              description: Specific links associated with the link
            link_time:
              type: string
              description: Time associated with the link
            traffic:
              type: string
              description: Traffic associated with the link
          example:
            link: "link182.uk"
            leads_to_post: false
            to_a_specific_link: false
            spec_links: ""
            link_time: "77"
            traffic: "13"
    responses:
      201:
        description: Link added successfully
        schema:
          type: object
          properties:
            link_id:
              type: integer
              description: ID of the newly added link
          example:
            link_id: 4
      500:
        description: Failed to add data in links
    """
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
    return json.dumps({"link_id":link_id}), 201


@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity():
    """
    Change link activity
    ---
    tags:
      - links
    parameters:
      - in: body
        name: link_data
        required: true
        description: JSON object containing link_id
        schema:
          type: object
          properties:
            link_id:
              type: integer
              description: ID of the link to change activity
          example:
            link_id: 1
    responses:
      200:
        description: Link activity changed successfully
        schema:
          type: object
          properties:
            changed_to:
              type: boolean
              description: Indicates the new activity status
          example:
            changed_to: true
      403:
        description: Permission denied to set activity in links
      500:
        description: Failed to add data in links
    """
    args = json.loads(request.data)
    act = LinksDB.change_link_activity(args.get("link_id"), session.get("client_id"))
    if act == "0xperm":
        return err.perm("set activity", "links")
    if act == "0xdb":
        return err.db_add("links")
    return json.dumps({"changed_to":act}), 200


@app.get("/api/links/delete")
@auth_required
def delete_link():
    """
    Delete a link
    ---
    tags:
      - links
    parameters:
      - in: query
        name: link_id
        type: integer
        required: true
        description: ID of the link to be deleted
    responses:
      200:
        description: Link deleted successfully
        schema:
          type: object
          properties:
            deleted:
              type: boolean
              description: Indicates whether the link was successfully deleted
          example:
            deleted: true
      403:
        description: Permission denied to delete links
      500:
        description: Failed to update data in links
    """
    args = json.loads(request.data)
    is_deleted = LinksDB.delete_link(
        args.get("link_id"), session.get("client_id")
    )
    if is_deleted == "0xdb":
        return err.db_update("links")
    if is_deleted == "0xperm":
        return err.perm("delete", "links")
    return json.dumps({"deleted":is_deleted}), 200


@app.post("/api/links/change")
@auth_required
def change_link():
    """
    Change a link
    ---
    tags:
      - links
    parameters:
      - in: body
        name: link_data
        required: true
        description: JSON object containing link details
        schema:
          type: object
          properties:
            link_id:
              type: string
              description: ID of the link to be changed
            link:
              type: string
              description: The new link URL
            leads_to_post:
              type: boolean
              description: Indicates if the link leads to a post
            to_a_specific_link:
              type: boolean
              description: Indicates if the link leads to a specific link
            spec_links:
              type: string
              description: Specific links associated with the link
            link_time:
              type: string
              description: Time associated with the link
            traffic:
              type: string
              description: Traffic associated with the link
          example:
            link_id: "2"
            link: "changed.xxx"
            leads_to_post: true
            to_a_specific_link: true
            spec_links: "youtube.com/watch?v=dQw4w9WgXcQ"
            link_time: "1313138"
            traffic: "5429"
    responses:
      201:
        description: Link changed successfully
        schema:
          type: object
          properties:
            link_id:
              type: string
              description: ID of the changed link
            link:
              type: string
              description: The changed link URL
            leads_to_post:
              type: boolean
              description: Indicates if the link leads to a post
            to_a_specific_link:
              type: boolean
              description: Indicates if the link leads to a specific link
            spec_links:
              type: string
              description: Specific links associated with the link
            link_time:
              type: string
              description: Time associated with the link
            traffic:
              type: string
              description: Traffic associated with the link
          example:
            link_id: "2"
            link: "changed.xxx"
            leads_to_post: true
            to_a_specific_link: true
            spec_links: "youtube.com/watch?v=dQw4w9WgXcQ"
            link_time: "1313138"
            traffic: "5429"
      403:
        description: Permission denied to change links
    """
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
