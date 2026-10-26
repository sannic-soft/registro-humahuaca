import os
import secrets
from pathlib import Path

from flask import (
    Flask, abort, flash, redirect, render_template,
    request, session, url_for
)

from database import get_db, init_app


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, instance_relative_config=True)
app.config["DATABASE"] = str(BASE_DIR / "instance" / "alojamientos.db")
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "solo-desarrollo-cambiar-antes-de-publicar"
)

init_app(app)


@app.before_request
def protect_forms():
    if request.method == "POST":
        token = session.get("_csrf_token")
        submitted = request.form.get("_csrf_token", "")

        if not token or not secrets.compare_digest(token, submitted):
            abort(400, description="Token de formulario inválido.")


@app.context_processor
def inject_csrf_token():
    def csrf_token():
        if "_csrf_token" not in session:
            session["_csrf_token"] = secrets.token_urlsafe(32)
        return session["_csrf_token"]

    return {"csrf_token": csrf_token}


@app.route("/")
def index():
    db = get_db()

    anuncios = db.execute(
        """
        SELECT id, titulo, contenido, creado_en
        FROM anuncios
        WHERE activo = 1
        ORDER BY id DESC
        LIMIT 5
        """
    ).fetchall()

    alojamientos = db.execute(
        """
        SELECT id, nombre, tipo, direccion, descripcion,
               capacidad, telefono, servicios
        FROM alojamientos
        WHERE activo = 1
        ORDER BY id DESC
        LIMIT 6
        """
    ).fetchall()

    return render_template(
        "index.html",
        anuncios=anuncios,
        alojamientos=alojamientos
    )


@app.route("/alojamientos")
def alojamientos():
    db = get_db()
    termino = request.args.get("q", "").strip()

    consulta = """
        SELECT id, nombre, tipo, direccion, descripcion,
               capacidad, telefono, servicios
        FROM alojamientos
        WHERE activo = 1
    """
    parametros = []

    if termino:
        consulta += """
            AND (
                nombre LIKE ?
                OR tipo LIKE ?
                OR direccion LIKE ?
                OR servicios LIKE ?
            )
        """
        patron = "%" + termino + "%"
        parametros.extend([patron, patron, patron, patron])

    consulta += " ORDER BY nombre COLLATE NOCASE"

    resultados = db.execute(consulta, parametros).fetchall()

    return render_template(
        "alojamientos.html",
        alojamientos=resultados,
        termino=termino
    )


@app.route("/alojamientos/<int:alojamiento_id>")
def alojamiento_detalle(alojamiento_id):
    db = get_db()

    alojamiento = db.execute(
        """
        SELECT id, nombre, tipo, direccion, descripcion,
               capacidad, telefono, servicios
        FROM alojamientos
        WHERE id = ? AND activo = 1
        """,
        (alojamiento_id,)
    ).fetchone()

    if alojamiento is None:
        abort(404)

    return render_template(
        "alojamiento_detalle.html",
        alojamiento=alojamiento
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        password_configurada = os.environ.get("ADMIN_PASSWORD")

        if not password_configurada:
            flash(
                "Falta configurar la variable ADMIN_PASSWORD.",
                "error"
            )
        elif secrets.compare_digest(
            request.form.get("password", ""),
            password_configurada
        ):
            session.clear()
            session["admin"] = True
            session["_csrf_token"] = secrets.token_urlsafe(32)
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Contraseña incorrecta.", "error")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.before_request
def require_admin_for_admin_routes():
    if request.endpoint and request.endpoint.startswith("admin_"):
        if not session.get("admin"):
            return redirect(url_for("login"))


@app.route("/admin")
def admin_dashboard():
    db = get_db()

    cantidad_alojamientos = db.execute(
        "SELECT COUNT(*) FROM alojamientos WHERE activo = 1"
    ).fetchone()[0]

    cantidad_anuncios = db.execute(
        "SELECT COUNT(*) FROM anuncios WHERE activo = 1"
    ).fetchone()[0]

    return render_template(
        "admin/dashboard.html",
        cantidad_alojamientos=cantidad_alojamientos,
        cantidad_anuncios=cantidad_anuncios
    )


@app.route("/admin/alojamientos", methods=["GET", "POST"])
def admin_alojamientos():
    db = get_db()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "").strip()
        direccion = request.form.get("direccion", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        servicios = request.form.get("servicios", "").strip()

        try:
            capacidad = int(request.form.get("capacidad", "1"))
        except ValueError:
            capacidad = 0

        if not nombre or not tipo or not direccion or capacidad < 1:
            flash(
                "Completá nombre, tipo, dirección y una capacidad válida.",
                "error"
            )
        else:
            db.execute(
                """
                INSERT INTO alojamientos
                (nombre, tipo, direccion, descripcion,
                 capacidad, telefono, servicios)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nombre, tipo, direccion, descripcion,
                    capacidad, telefono, servicios
                )
            )
            db.commit()
            flash("Alojamiento agregado correctamente.", "success")
            return redirect(url_for("admin_alojamientos"))

    resultados = db.execute(
        "SELECT * FROM alojamientos ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "admin/alojamientos.html",
        alojamientos=resultados
    )


@app.route("/admin/alojamientos/<int:alojamiento_id>/estado", methods=["POST"])
def admin_estado_alojamiento(alojamiento_id):
    db = get_db()

    db.execute(
        """
        UPDATE alojamientos
        SET activo = CASE WHEN activo = 1 THEN 0 ELSE 1 END
        WHERE id = ?
        """,
        (alojamiento_id,)
    )
    db.commit()

    flash("Estado del alojamiento actualizado.", "success")
    return redirect(url_for("admin_alojamientos"))


@app.route("/admin/anuncios", methods=["GET", "POST"])
def admin_anuncios():
    db = get_db()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        contenido = request.form.get("contenido", "").strip()

        if not titulo or not contenido:
            flash("Completá el título y el contenido.", "error")
        else:
            db.execute(
                """
                INSERT INTO anuncios (titulo, contenido)
                VALUES (?, ?)
                """,
                (titulo, contenido)
            )
            db.commit()
            flash("Anuncio publicado correctamente.", "success")
            return redirect(url_for("admin_anuncios"))

    resultados = db.execute(
        "SELECT * FROM anuncios ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "admin/anuncios.html",
        anuncios=resultados
    )


@app.route("/admin/anuncios/<int:anuncio_id>/estado", methods=["POST"])
def admin_estado_anuncio(anuncio_id):
    db = get_db()

    db.execute(
        """
        UPDATE anuncios
        SET activo = CASE WHEN activo = 1 THEN 0 ELSE 1 END
        WHERE id = ?
        """,
        (anuncio_id,)
    )
    db.commit()

    flash("Estado del anuncio actualizado.", "success")
    return redirect(url_for("admin_anuncios"))


if __name__ == "__main__":
    app.run(debug=True)
