import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tasks.db')

def get_db_connection():
    """
    Establece y devuelve una conexion a la base de datos SQLite.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa la base de datos creando la tabla 'tasks' si no existe.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pendiente', -- 'pendiente', 'completada'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"Base de datos '{DATABASE}' inicializada y tabla 'tasks' creada (si no existia).")

if __name__ == '__main__':
    init_db()
