import json
from flask import request
from api.sessions import auth_required
from database.proxy import ProxyDB
from src.errors import err
from src.loader import app


@app.get("/api/proxy/show")
@auth_required
def show_proxies(jwt=None):
    """
    Show proxies

    ---
    tags:
      - proxies
    responses:
      200:
        description: List of proxies
        schema:
          type: array
          items:
            type: object
            properties:
              proxy_id:
                type: integer
                description: ID of the proxy
              server_id:
                type: integer
                description: ID of the associated server
              name:
                type: string
                description: name of the proxy
              address:
                type: string
                description: Address of the proxy
              status:
                type: boolean
                description: Status of the proxy (true for active, false for inactive)
              creator_id:
                type: integer
                description: Creator of the proxy record ID
              created_at:
                type: integer
                description: time of creation
            example:
              - proxy_id: 3
                server_id: 4
                name: "gru proxy"
                address: "1935153.18080"
                status: true
                creator_id: 228
                created_at: 0
              - proxy_id: 1
                server_id: 4
                name: "dark proxy"
                address: "192.168.1.1:8080"
                status: false
                creator_id: 228
                created_at: 0
      404:
        description: Data not found in proxies
    """

    servers = ProxyDB.show_proxies()
    if servers == "0xdb": return err.not_found("servers")
    return json.dumps(servers, indent=2), 200


@app.post("/api/proxy/add")
@auth_required
def add_proxy(jwt=None):
    """
    Add a new proxy

    ---
    tags:
      - proxies
    parameters:
      - in: body
        name: proxy_data
        required: true
        description: JSON object containing proxy details
        schema:
          type: object
          properties:
            server_id:
              type: integer
              description: ID of the associated server
            name:
              type: string
              description: name of the proxy
            address:
              type: string
              description: Address of the new proxy
          example:
            server_id: 4
            name: "gru proxy"
            address: "192.168.1.2:8080"
    responses:
      201:
        description: Proxy added successfully
        schema:
          type: object
          properties:
            proxy_id:
              type: integer
              description: ID of the newly added proxy
          example:
            proxy_id: 7
      400:
        description: Too many proxies! (Client error)
      500:
        description: Failed to add data in proxies
    """

    data = json.loads(request.data)
    proxy_id = ProxyDB.add_proxy(
        data.get("server_id"),
        data.get("name"),
        data.get("address"),
        data.get("city"),
        jwt.get("client_id"))
    if proxy_id == "0xc": return err.create("Too many proxies!", 400)
    if proxy_id == "0xdb": return err.db_add("proxy")
    return json.dumps(proxy_id), 201


@app.get("/api/proxy/changeActivity")
@auth_required
def change_proxy_activity(jwt=None):
    """
    Change proxy activity

    ---
    tags:
      - proxies
    parameters:
      - in: query
        name: proxy_id
        type: integer
        required: true
        description: ID of the proxy to change activity
    responses:
      200:
        description: Proxy activity changed successfully
        schema:
          type: object
          properties:
            changed_to:
              type: boolean
              description: Indicates the new activity status
          example:
            changed_to: true
      400:
        description: Too many active proxies! (More than 3 for one server)
      404:
        description: Data not found in proxies
    """

    args = request.args
    act = ProxyDB.change_proxy_activity(args.get("proxy_id"), jwt.get("client_id"))
    if act == "0xdb": return err.not_found("proxy")
    if act == "0xc": return err.create("Too many active proxies!", 400)
    return json.dumps({"changed_to":act}), 200


@app.post("/api/proxy/change")
@auth_required
def change_proxy_address(jwt=None):
    """
    Change proxy details

    ---
    tags:
      - proxies
    parameters:
      - in: body
        name: proxy_data
        required: true
        description: JSON object containing proxy details to be changed
        schema:
          type: object
          properties:
            proxy_id:
              type: integer
              description: ID of the proxy to be changed
            name:
              type: string
              description: name of the proxy
            address:
              type: string
              description: New address for the proxy
            status:
              type: string
              description: New status for the proxy
          example:
            proxy_id: 7
            address: "new.address.com"
    responses:
      200:
        description: Proxy details changed successfully
        schema:
          type: object
          properties:
            proxy_id:
              type: integer
              description: ID of the changed proxy
            server_id:
              type: integer
              description: ID of the associated server
            name:
              type: string
              description: name of the proxy
            address:
              type: string
              description: New address of the proxy
            status:
              type: boolean
              description: Status of the proxy (true for active, false for inactive)
            creator_id:
              type: integer
              description: Creator of the proxy record ID
          example:
            proxy_id: 7
            server_id: 1
            name: "dsdsds"
            address: "new.address.com"
            status: true
            creator_id: 228
      403:
        description: Permission denied to change proxy
      404:
        description: Data not found in proxies
    """

    data = json.loads(request.data)
    new_proxy = ProxyDB.change_proxy(data["proxy_id"], data.get("name"), data.get("address"),data.get("city"),data.get("status"), jwt.get("client_id"))
    if new_proxy == "0xdb": return err.not_found("proxy")
    if new_proxy == "0xperm": return err.perm("change", "proxy")
    return json.dumps(new_proxy), 200


@app.get("/api/proxy/delete")
@auth_required
def delete_proxy(jwt=None):
    """
    Delete a proxy

    ---
    tags:
      - proxies
    parameters:
      - in: query
        name: proxy_id
        type: integer
        required: true
        description: ID of the proxy to delete
    responses:
      200:
        description: Proxy deleted successfully
        schema:
          type: object
          properties:
            is_deleted:
              type: boolean
              description: Indicates whether the proxy was successfully deleted
          example:
            is_deleted: true
      403:
        description: Permission denied to delete proxy
      404:
        description: Data not found in proxy
    """

    args = request.args
    is_deleted = ProxyDB.delete_proxy(args.get("proxy_id"))
    if is_deleted == "0xdb": return err.not_found("proxy")
    if is_deleted == "0xperm": return err.perm("delete", "proxy")
    return json.dumps({"is_deleted":is_deleted}), 200
