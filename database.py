import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        db_path = current_app.config["DATABASE"]

        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db_path = Path(current_app.config["DATABASE"])
    db_path.parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(db_path)

    try:
        schema_path = Path(current_app.root_path) / "schema.sql"
        schema = schema_path.read_text(encoding="utf-8")
        db.executescript(schema)
        db.commit()
    finally:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()
