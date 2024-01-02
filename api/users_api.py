from scr.loader import app
from database.postgres import cur
@app.get("/api/users/show")
def show_users():
    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    return [user.to_json() for user in users]

