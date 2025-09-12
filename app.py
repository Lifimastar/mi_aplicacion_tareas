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

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    """
    Marca una tarea como completada.
    """
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status = 'completada' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Tarea {task_id} marcada como completada.")
    return redirect(url_for('home'))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """
    Elimina una tarea de la base de datos.
    """
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Tarea {task_id} eliminada.")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)