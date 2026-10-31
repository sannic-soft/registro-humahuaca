
import hmac
import re
import secrets

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from database import get_db


bp = Blueprint("auth", __name__)


@bp.app_template_global()
def csrf_token():
    """Genera o recupera el token CSRF de la sesión."""
    token = session.get("_csrf_token")

    if token is None:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token

    return token


def validar_csrf():
    """Comprueba que el formulario tenga un token CSRF válido."""
    token_formulario = request.form.get("_csrf_token", "")
    token_sesion = session.get("_csrf_token", "")

    return bool(
        token_formulario
        and token_sesion
        and hmac.compare_digest(token_formulario, token_sesion)
    )


@bp.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        if not validar_csrf():
            flash("La solicitud no es válida. Intentá nuevamente.", "error")
            return redirect(url_for("auth.registro"))

        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirmacion = request.form.get("confirmacion", "")

        if not nombre or not email or not password or not confirmacion:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("auth.registro"))

        if len(nombre) > 100:
            flash("El nombre no puede superar los 100 caracteres.", "error")
            return redirect(url_for("auth.registro"))

        if len(email) > 254 or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
        ):
            flash("Ingresá un correo electrónico válido.", "error")
            return redirect(url_for("auth.registro"))

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            return redirect(url_for("auth.registro"))

        if password != confirmacion:
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("auth.registro"))

        password_hash = generate_password_hash(password)

        db = get_db()

        try:
            db.execute(
                """
                INSERT INTO usuarios (nombre, email, password_hash, rol)
                VALUES (?, ?, ?, 'usuario')
                """,
                (nombre, email, password_hash),
            )

            db.commit()

        except Exception as error:
            db.rollback()

            if "UNIQUE constraint failed: usuarios.email" in str(error):
                flash("Ese correo electrónico ya está registrado.", "error")
            else:
                flash("No se pudo crear la cuenta. Intentá nuevamente.", "error")

            return redirect(url_for("auth.registro"))

        flash("Tu cuenta fue creada correctamente. Ya podés iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        if not validar_csrf():
            flash("La solicitud no es válida. Intentá nuevamente.", "error")
            return redirect(url_for("auth.login"))

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Completá el correo y la contraseña.", "error")
            return redirect(url_for("auth.login"))

        db = get_db()

        usuario = db.execute(
            """
            SELECT id, nombre, email, password_hash, rol, activo
            FROM usuarios
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

        if usuario is None or not check_password_hash(
            usuario["password_hash"], password
        ):
            flash("Correo o contraseña incorrectos.", "error")
            return redirect(url_for("auth.login"))

        if not usuario["activo"]:
            flash("Esta cuenta se encuentra desactivada.", "error")
            return redirect(url_for("auth.login"))

        # Evitar reutilizar datos de una sesión anterior.
        session.clear()

        # Guardar únicamente los datos necesarios.
        session["usuario_id"] = usuario["id"]
        session["usuario_nombre"] = usuario["nombre"]
        session["usuario_rol"] = usuario["rol"]

        flash("Iniciaste sesión correctamente.", "success")

        return redirect(url_for("public.index"))

    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():

    if not validar_csrf():
        flash("La solicitud no es válida.", "error")
        return redirect(url_for("public.index"))

    session.clear()

    flash("Cerraste sesión correctamente.", "success")

    return redirect(url_for("public.index"))
