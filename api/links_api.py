import json
from flask import request
from api.sessions import auth_required
from database.links import LinksDB
from src.errors import err
from src.loader import app


@app.get("/api/links/show")
@auth_required
def show_links(jwt=None):
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
    links = LinksDB.show_links(jwt.get('client_id'))
    if links == "0xdb": return err.not_found("links")

    return json.dumps(links, indent=2), 200


@app.post("/api/links/add")
@auth_required
def add_link(jwt=None):
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
        data.get("traffic"),
        jwt.get('client_id'))
    if link_id == "0xdb":
        return err.db_add("links")
    return json.dumps(link_id), 201


@app.get("/api/links/changeActivity")
@auth_required
def set_link_activity(jwt=None):
    """
    Change link activity
    ---
    tags:
      - links
    parameters:
      - in: query
        name: link_id
        type: integer
        required: true
        description: ID of the link to change link activity
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
    args = request.args
    act = LinksDB.change_link_activity(args.get("link_id"), jwt.get('client_id'))
    if act == "0xperm":
        return err.perm("set activity", "links")
    if act == "0xdb":
        return err.db_add("links")
    return json.dumps({"changed_to":act}), 200


@app.get("/api/links/delete")
@auth_required
def delete_link(jwt=None):
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
        description: ID of the link to delete link
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
    args = request.args
    is_deleted = LinksDB.delete_link(
        args.get("link_id"), jwt.get("client_id")
    )
    if is_deleted == "0xdb":
        return err.db_update("links")
    if is_deleted == "0xperm":
        return err.perm("delete", "links")
    return json.dumps({"deleted":is_deleted}), 200


@app.post("/api/links/change")
@auth_required
def change_link(jwt=None):
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
        data.get("traffic"),
        jwt.get("client_id"))
    if link_id == "0xperm":
        return err.perm("change", "links")
    return json.dumps(data), 201
