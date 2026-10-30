import os
import secrets
from pathlib import Path

from flask import Flask, jsonify

from database import init_app, init_cli

from routes.public import bp as public_bp
from routes.auth import bp as auth_bp
from routes.admin import bp as admin_bp
from routes.owner import bp as owner_bp


def create_app(test_config=None):
    """Crea y configura la aplicación Flask."""

    app = Flask(__name__, instance_relative_config=True)

    # Entorno de ejecución
    production = os.environ.get("APP_ENV") == "production"
    secret_key = os.environ.get("SECRET_KEY")

    if production and not secret_key:
        raise RuntimeError(
            "En producción es obligatorio configurar SECRET_KEY."
        )

    # Configuración principal
    database_path = Path(
        os.environ.get(
            "DATABASE_PATH",
            str(Path(app.instance_path) / "alojamientos.db")
        )
    ).expanduser()

    if not database_path.is_absolute():
        database_path = (Path(app.root_path) / database_path).resolve()

    app.config.from_mapping(
        SECRET_KEY=secret_key or secrets.token_hex(32),
        DATABASE=str(database_path),
        TESTING=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=production,
    )

    # Permite modificar la configuración durante las pruebas.
    if test_config is not None:
        app.config.update(test_config)

    # Conexión con el módulo de base de datos.
    init_app(app)

    # Registra el comando: flask --app app init-db
    init_cli(app)

    # Registro de los módulos de rutas.
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(owner_bp, url_prefix="/propietario")

    # Ruta temporal para comprobar que Flask funciona.
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("APP_ENV") == "development"
    )
