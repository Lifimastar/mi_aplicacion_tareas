from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, init_db

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route("/")
def home():
    """
    Muestra la lista de todas las tareas.
    """
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)