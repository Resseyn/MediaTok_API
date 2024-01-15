import json
from flask import request, session
from api.sessions import auth_required
from database.users import UserDB
from src.errors import err
from src.loader import app


@app.get("/api/users/show")
@auth_required
def show_users():
    """
    Show users

    ---
    tags:
      - users
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: integer
                description: User ID
              login:
                type: string
                description: User login
              password:
                type: string
                description: User password
              name:
                type: string
                description: User first name
              surname:
                type: string
                description: User last name
              activity:
                type: boolean
                description: User activity status
              created_at:
                type: integer
                description: Timestamp of user creation
      404:
        description: No users found
    """

    users = UserDB.show_users()
    if users == "0xdb": return err.not_found("users")
    return json.dumps(users, indent=2), 200


@app.post("/api/users/add")
@auth_required
def add_user():
    """
    Add a new user

    ---
    tags:
      - users
    parameters:
      - in: body
        name: user_data
        required: true
        description: JSON object containing user information for registration
        schema:
          type: object
          properties:
            login:
              type: string
              description: User login
            password:
              type: string
              description: User password
            name:
              type: string
              description: User first name
            surname:
              type: string
              description: User last name
    responses:
      200:
        description: User added successfully
        schema:
          type: object
          properties:
            user_id:
              type: integer
              description: ID of the newly added user
      400:
        description: Login occupied
      500:
        description: User not added (db error)
    """

    data = json.loads(request.data)
    user_id = UserDB.add_user(data["login"], data["password"], data["name"], data["surname"])
    if user_id == "0xp": return err.db_add("users")
    return json.dumps({"user_id":user_id}), 200


@app.post("/api/users/change")
@auth_required
def change_user():
    """
    Change user information

    ---
    tags:
      - users
    parameters:
      - in: body
        name: user
        required: true
        description: User information
        schema:
          type: object
          properties:
            user_id:
              type: integer
              description: User ID
            login:
              type: string
              description: User login
            password:
              type: string
              description: User password
            name:
              type: string
              description: User first name
            surname:
              type: string
              description: User last name
    responses:
      200:
        description: User information updated successfully
        schema:
          type: object
          properties:
            user_id:
              type: integer
              description: User ID
            login:
              type: string
              description: User login
            password:
              type: string
              description: User password
            name:
              type: string
              description: User first name
            surname:
              type: string
              description: User last name
            activity:
              type: boolean
              description: User activity status
            created_at:
              type: integer
              description: Timestamp of user creation
      404:
        description: User not found
      500:
        description: Failed to update user information
    """

    data = json.loads(request.data)
    changed_user = UserDB.change_user(data["user_id"], data["login"], data["password"], data["name"],
                                      data["surname"])
    if changed_user == "0xu": return err.not_found("users")
    if changed_user == "0xdb": return err.db_update("users")
    return json.dumps(changed_user), 200


@app.get("/api/users/changeActivity")
@auth_required
def set_user_activity():
    """
    Change user activity status

    ---
    tags:
      - users
    parameters:
      - in: query
        name: user_id
        type: integer
        required: true
        description: ID of the user to change activity
    responses:
      200:
        description: User activity status changed successfully
        schema:
          type: object
          properties:
            changed_to:
              type: boolean
              description: New user activity status
      404:
        description: User not found
      500:
        description: Failed to update user activity status
    """

    args = request.args
    changed = UserDB.change_user_activity(args.get("user_id"))
    if changed == "0xdb": return err.db_update("users")
    return json.dumps({"changed_to": changed}), 200


@app.get("/api/users/delete")
@auth_required
def delete_user():
    """
    Delete user

    ---
    tags:
      - users
    parameters:
      - in: query
        name: user_id
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      200:
        description: User deleted successfully
        schema:
          type: object
          properties:
            is_deleted:
              type: boolean
              description: Indicates whether the user is deleted
      404:
        description: User not found
      403:
        description: Cannot delete own user
      500:
        description: Failed to delete user
    """

    args = request.args
    if session["client_id"] == args.get("user_id"):
        return err.perm("delete","users")
    is_deleted = UserDB.delete_user(args.get("user_id"))
    if is_deleted == "0xdb":
        return err.not_found("users")
    return json.dumps({"is_deleted":is_deleted}), 200
