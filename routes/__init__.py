from functools import wraps

from flask import session, flash, redirect, url_for

from database import get_db


def _actualizar_sesion_usuario():
    """Verifica que la cuenta exista y esté activa, y actualiza sus datos."""

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return False

    usuario = get_db().execute(
        """
        SELECT id, nombre, rol, activo
        FROM usuarios
        WHERE id = ?
        """,
        (usuario_id,)
    ).fetchone()

    if usuario is None or not usuario["activo"]:
        session.clear()
        return False

    session["usuario_id"] = usuario["id"]
    session["usuario_nombre"] = usuario["nombre"]
    session["usuario_rol"] = usuario["rol"]

    return True


def login_required(view):
    """Exige que exista una sesión válida de usuario."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if not _actualizar_sesion_usuario():
            flash("Debes iniciar sesión para continuar.", "error")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


def roles_required(*roles):
    """Exige que el usuario tenga uno de los roles permitidos."""

    def decorator(view):

        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if not _actualizar_sesion_usuario():
                flash("Debes iniciar sesión para continuar.", "error")
                return redirect(url_for("auth.login"))

            if session.get("usuario_rol") not in roles:
                flash("No tienes permiso para acceder.", "error")
                return redirect(url_for("public.index"))

            return view(*args, **kwargs)

        return wrapped_view

    return decorator
