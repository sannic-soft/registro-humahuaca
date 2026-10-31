from functools import wraps

from flask import session, flash, redirect, url_for


def login_required(view):
    """Exige que exista una sesión de usuario."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if not session.get("usuario_id"):
            flash("Debes iniciar sesión para continuar.", "error")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


def roles_required(*roles):
    """Exige que el usuario tenga uno de los roles permitidos."""

    def decorator(view):

        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if not session.get("usuario_id"):
                flash("Debes iniciar sesión para continuar.", "error")
                return redirect(url_for("auth.login"))

            if session.get("usuario_rol") not in roles:
                flash("No tienes permiso para acceder.", "error")
                return redirect(url_for("public.index"))

            return view(*args, **kwargs)

        return wrapped_view

    return decorator
