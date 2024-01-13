import json
from flask import request, session
from api.sessions import auth_required
from database.servers import ServersDB
from src.errors import err
from src.loader import app


@app.get("/api/servers/show")
@auth_required
def show_servers():
    """
    Show servers

    ---
    tags:
      - servers
    responses:
      200:
        description: List of servers
        schema:
          type: array
          items:
            type: object
            properties:
              server_id:
                type: integer
                description: ID of the server
              name:
                type: string
                description: Name of the server
              login_anyd:
                type: string
                description: Login for the anyd service on the server
              password_anyd:
                type: string
                description: Password for the anyd service on the server
              cpu:
                type: string
                description: CPU information of the server
              ram:
                type: string
                description: RAM information of the server
              storage:
                type: string
                description: Storage information of the server
              ip:
                type: string
                description: IP address of the server
              activity:
                type: boolean
                description: Activity status of the server (true for active, false for inactive)
              to_a_specific_proxy:
                type: boolean
                description: Indicates whether the server is linked to a specific proxy
              created_at:
                type: integer
                description: Timestamp of when the server was created
              creator_id:
                type: integer
                description: Creator of the server record ID
            example:
              - server_id: 3
                name: "ServerQuantum"
                login_anyd: "quantumAdmin"
                password_anyd: "quantumPass123"
                cpu: "Intel Core i7"
                ram: "16GB"
                storage: "1TB"
                ip: "192.168.1.1"
                activity: false
                to_a_specific_proxy: false
                created_at: 1704574147
                creator_id: 228
              - server_id: 5
                name: "фаfgfgпф"
                login_anyd: "hf13dmin"
                password_anyd: "umPass123"
                cpu: "Intel Co131re i7"
                ram: "1488B"
                storage: "1131TB"
                ip: "19bfgf1318.1.1"
                activity: true
                to_a_specific_proxy: false
                created_at: 1704574182
                creator_id: 228
              - server_id: 4
                name: "фавфпф"
                login_anyd: "quanagagd13dmin"
                password_anyd: "q13315umPass123"
                cpu: "Intel Co131re i7"
                ram: "1136GB"
                storage: "131TB"
                ip: "192.161318.1.1"
                activity: false
                to_a_specific_proxy: true
                created_at: 1704574165
                creator_id: 228
      404:
        description: Data not found in servers
    """

    servers = ServersDB.show_servers(session.get("client_id"))
    if servers == "0xdb": err.not_found("servers")
    return json.dumps(servers, indent=2), 200


@app.post("/api/servers/add")
@auth_required
def add_server():
    """
    Add a new server

    ---
    tags:
      - servers
    parameters:
      - in: body
        name: server_data
        required: true
        description: JSON object containing server details
        schema:
          type: object
          properties:
            name:
              type: string
              description: Name of the server
            type:
              type: string
              description: Type of the server (Hosting or Anydesc)
            login_anyd:
              type: string
              description: Login for the anyd service on the server. Empty string if type is Hosting
            password_anyd:
              type: string
              description: Password for the anyd service on the server. Empty string if type is Hosting
            cpu:
              type: string
              description: CPU information of the server
            ram:
              type: string
              description: RAM information of the server
            storage:
              type: string
              description: Storage information of the server
            ip:
              type: string
              description: IP address of the server. Empty string if type is Anydesc
            login:
              type: string
              description: Login to host. Empty string if type is Anydesc
            password:
              type: string
              description: password to host. Empty string if type is Anydesc
            activity:
              type: boolean
              description: Activity status of the server (true for active, false for inactive)
          example:
            name: "ServerQuantum"
            type: "Hosting"
            login_anyd: ""
            password_anyd: ""
            cpu: "Intel Core i7"
            ram: "16GB"
            storage: "1TB"
            ip: "192.01.01"
            login: "maestro"
            password: "12r=f21mf1"
            activity: false
    responses:
      200:
        description: Server added successfully
        schema:
          type: object
          properties:
            server_id:
              type: integer
              description: ID of the newly added server
            name:
              type: string
              description: Name of the server
            type:
              type: string
              description: Type of the server (Hosting or Anydesc)
            login_anyd:
              type: string
              description: Login for the anyd service on the server. Empty string if type is Hosting
            password_anyd:
              type: string
              description: Password for the anyd service on the server. Empty string if type is Hosting
            cpu:
              type: string
              description: CPU information of the server
            ram:
              type: string
              description: RAM information of the server
            storage:
              type: string
              description: Storage information of the server
            ip:
              type: string
              description: IP address of the server. Empty string if type is Anydesc
            login:
              type: string
              description: Login to host. Empty string if type is Anydesc
            password:
              type: string
              description: password to host. Empty string if type is Anydesc
            activity:
              type: boolean
              description: Activity status of the server (true for active, false for inactive)
            to_a_specific_proxy:
              type: boolean
              description: Indicates whether the server is linked to a specific proxy
            created_at:
              type: integer
              description: Timestamp of when the server was created
            creator_id:
              type: integer
              description: Creator of the server record ID
          example:
            server_id: 6
            name: "ServerQuantum"
            type: "Hosting"
            login_anyd: ""
            password_anyd: ""
            cpu: "Intel Core i7"
            ram: "16GB"
            storage: "1TB"
            ip: "192.01.01"
            login: "maestro"
            password: "12r=f21mf1"
            activity: false
            to_a_specific_proxy: false
            created_at: 1704633862
            creator_id: 228
      500:
        description: Failed to add data in servers
    """

    data = json.loads(request.data)
    server_id = ServersDB.add_server(
        data.get("name"),
        data.get("type"),
        data.get("login_anyd"),
        data.get("password_anyd"),
        data.get("link"),
        data.get("cpu"),
        data.get("ram"),
        data.get("storage"),
        data.get("ip"),
        data.get("login"),
        data.get("password"),
        data.get("activity"),
        session.get("client_id"))
    if server_id == "0xdb": return err.db_add("servers")
    return json.dumps(server_id), 200


@app.get("/api/servers/changeActivity")
@auth_required
def set_server_activity():
    """
    Change server activity

    ---
    tags:
      - servers
    parameters:
      - in: query
        name: server_id
        type: integer
        required: true
        description: ID of the server to change activity
    responses:
      200:
        description: Server activity changed successfully
        schema:
          type: object
          properties:
            changed_to:
              type: boolean
              description: Indicates the new activity status of the server
          example:
            changed_to: true
      403:
        description: Permission denied to change server activity
      404:
        description: Data not found in servers
    """

    args = request.args
    act = ServersDB.change_server_activity(args.get("server_id"), session.get("client_id"))
    if act == "0xdb": return err.db_update("servers")
    if act == "0xperm": return err.perm("set activity", "servers")
    return json.dumps({"changed_to": act}), 200


@app.get("/api/servers/delete")
@auth_required
def delete_server():
    """
    Delete a server

    ---
    tags:
      - servers
    parameters:
      - in: query
        name: server_id
        type: integer
        required: true
        description: ID of the server to delete
    responses:
      200:
        description: Server deleted successfully
        schema:
          type: object
          properties:
            is_deleted:
              type: boolean
              description: Indicates whether the server was successfully deleted
          example:
            is_deleted: true
      403:
        description: Permission denied to delete server
      404:
        description: Data not found in servers
    """

    args = request.args
    is_deleted = ServersDB.delete_server(
        args.get("server_id"),
        session.get("client_id")
    )
    if is_deleted == "0xdb": return err.db_update("servers")
    if is_deleted == "0xperm": return err.perm("set activity", "servers")
    return json.dumps({"is_deleted": is_deleted}), 200


@app.post("/api/servers/change")
@auth_required
def change_server():
    """
    Change server details

    ---
    tags:
      - servers
    parameters:
      - in: body
        name: server_data
        required: true
        description: JSON object containing server details to be changed
        schema:
          type: object
          properties:
            server_id:
              type: integer
              description: ID of the server to be changed
            name:
              type: string
              description: New name for the server
            type:
              type: string
              description: New type for the server
            login_anyd:
              type: string
              description: New login for the anyd service on the server
            password_anyd:
              type: string
              description: New password for the anyd service on the server
            cpu:
              type: string
              description: New CPU information of the server
            ram:
              type: string
              description: New RAM information of the server
            storage:
              type: string
              description: New storage information of the server
            ip:
              type: string
              description: New IP address of the server
            login:
              type: string
              description: Login to host. Empty string if type is Anydesc
            password:
              type: string
              description: password to host. Empty string if type is Anydesc
            activity:
              type: string
              description: new activity
    responses:
      200:
        description: Server details changed successfully
        schema:
          type: object
          properties:
            server_id:
              type: integer
              description: ID of the server to be changed
            name:
              type: string
              description: New name for the server
            type:
              type: string
              description: New type for the server
            login_anyd:
              type: string
              description: New login for the anyd service on the server
            password_anyd:
              type: string
              description: New password for the anyd service on the server
            cpu:
              type: string
              description: New CPU information of the server
            ram:
              type: string
              description: New RAM information of the server
            storage:
              type: string
              description: New storage information of the server
            ip:
              type: string
              description: New IP address of the server
            login:
              type: string
              description: Login to host. Empty string if type is Anydesc
            password:
              type: string
              description: password to host. Empty string if type is Anydesc
            activity:
              type: string
              description: new activity
            to_a_specific_proxy:
              type: boolean
              description: Indicates whether the server is linked to a specific proxy
            created_at:
              type: integer
              description: Timestamp of when the server was created
            creator_id:
              type: integer
              description: Creator of the server record ID
          example:
            server_id: 1
            name: "ServerQuantum"
            type: "Hosting"
            login_anyd: ""
            password_anyd: ""
            cpu: "Intel Core i7"
            ram: "16GB"
            storage: "1TB"
            ip: "192.01.01"
            login: "maestro"
            password: "12r=f21mf1"
            activity: false
            to_a_specific_proxy: false
            created_at: 1704633862
            creator_id: 228
      403:
        description: Permission denied to change server details
      404:
        description: Data not found in servers
    """

    data = json.loads(request.data)
    changed_server = ServersDB.change_server(
        data.get("server_id"),
        data.get("name"),
        data.get("type"),
        data.get("login_anyd"),
        data.get("password_anyd"),
        data.get("link"),
        data.get("cpu"),
        data.get("ram"),
        data.get("storage"),
        data.get("ip"),
        data.get("login"),
        data.get("password"),
        data.get("activity"),
        session.get("client_id"))
    if changed_server == "0xdb": return err.db_update("servers")
    if changed_server == "0xperm": return err.perm("set activity", "servers")
    return json.dumps(changed_server), 200
