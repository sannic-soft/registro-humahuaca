
import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    """Devuelve la conexión SQLite de la solicitud actual."""
    if "db" not in g:
        db_path = Path(current_app.config["DATABASE"])
        db_path.parent.mkdir(parents=True, exist_ok=True)

        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")

        g.db = db

    return g.db


def close_db(error=None):
    """Cierra la conexión al finalizar el contexto de la solicitud."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Crea las tablas definidas en schema.sql si todavía no existen."""
    db_path = Path(current_app.config["DATABASE"])
    schema_path = Path(current_app.root_path) / "schema.sql"

    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema = schema_path.read_text(encoding="utf-8")

    db = sqlite3.connect(db_path)

    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(schema)
        db.commit()
    finally:
        db.close()


def init_app(app):
    """Registra el cierre de conexiones en Flask."""
    app.teardown_appcontext(close_db)


def init_cli(app):
    """Registra el comando explícito para inicializar la base."""
    @app.cli.command("init-db")
    def init_db_command():
        with app.app_context():
            init_db()

        print("Base de datos inicializada correctamente.")
