from scr.loader import app
from database.postgres import cur
@app.get("/api/users/show")
def show_users():
    cur.execute("SELECT * FROM users")

    records = cur.fetchall()

