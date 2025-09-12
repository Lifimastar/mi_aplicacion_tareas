from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, init_db

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route("/", methods=('GET', 'POST'))
def home():
    """
    Muestra la lista de todas las tareas y maneja la creacion de nuevas tareas.
    """
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')

        if not title:
            print("Error! El titulo de la tarea es obligatoria.")
        else:
            conn.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
            conn.commit()
            print(f"Tarea '{title}' anadida.")
            return redirect(url_for('home'))

    tasks = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)