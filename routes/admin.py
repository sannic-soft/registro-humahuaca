import sqlite3

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from database import get_db
from routes import roles_required
from routes.auth import validar_csrf


bp = Blueprint("admin", __name__)


@bp.route("/")
@roles_required("admin")
def dashboard():
    db = get_db()

    cantidad_alojamientos = db.execute(
        "SELECT COUNT(*) FROM alojamientos"
    ).fetchone()[0]

    cantidad_publicados = db.execute(
        """
        SELECT COUNT(*)
        FROM alojamientos
        WHERE estado = 'publicado'
        """
    ).fetchone()[0]

    cantidad_pendientes = db.execute(
        """
        SELECT COUNT(*)
        FROM alojamientos
        WHERE estado = 'pendiente'
        """
    ).fetchone()[0]

    cantidad_anuncios = db.execute(
        """
        SELECT COUNT(*)
        FROM anuncios
        WHERE activo = 1
        """
    ).fetchone()[0]

    cantidad_usuarios = db.execute(
        "SELECT COUNT(*) FROM usuarios"
    ).fetchone()[0]

    return render_template(
        "admin/dashboard.html",
        cantidad_alojamientos=cantidad_alojamientos,
        cantidad_publicados=cantidad_publicados,
        cantidad_pendientes=cantidad_pendientes,
        cantidad_anuncios=cantidad_anuncios,
        cantidad_usuarios=cantidad_usuarios
    )


@bp.route("/alojamientos", methods=("GET", "POST"))
@roles_required("admin")
def alojamientos():
    db = get_db()

    if request.method == "POST":

        if not validar_csrf():
            flash("La solicitud no es válida. Intentá nuevamente.", "error")
            return redirect(url_for("admin.alojamientos"))

        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "").strip()
        direccion = request.form.get("direccion", "").strip()
        capacidad = request.form.get("capacidad", "").strip()
        telefono = request.form.get("telefono", "").strip()
        servicios = request.form.get("servicios", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre or not tipo or not direccion:
            flash("Completá los campos obligatorios.", "error")
            return redirect(url_for("admin.alojamientos"))

        try:
            capacidad = int(capacidad)

            if capacidad < 1 or capacidad > 1000:
                raise ValueError

        except ValueError:
            flash("La capacidad debe ser un número entre 1 y 1000.", "error")
            return redirect(url_for("admin.alojamientos"))

        propietario_id = session.get("usuario_id")

        try:
            db.execute(
                """
                INSERT INTO alojamientos (
                    propietario_id,
                    nombre,
                    tipo,
                    descripcion,
                    capacidad,
                    direccion_referencia,
                    telefono,
                    servicios,
                    estado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pendiente')
                """,
                (
                    propietario_id,
                    nombre,
                    tipo,
                    descripcion,
                    capacidad,
                    direccion,
                    telefono,
                    servicios
                )
            )

            db.commit()
            flash("Alojamiento registrado correctamente.", "success")

        except sqlite3.Error:
            db.rollback()
            flash("No se pudo guardar el alojamiento.", "error")

        return redirect(url_for("admin.alojamientos"))

    alojamientos = db.execute(
        """
        SELECT
            a.id,
            a.nombre,
            a.tipo,
            a.estado,
            a.capacidad,
            u.nombre AS propietario_nombre,
            u.email AS propietario_email
        FROM alojamientos AS a
        JOIN usuarios AS u
            ON a.propietario_id = u.id
        ORDER BY a.creado_en DESC
        """
    ).fetchall()

    return render_template(
        "admin/alojamientos.html",
        alojamientos=alojamientos
    )


@bp.route(
    "/alojamientos/<int:alojamiento_id>/estado",
    methods=("POST",)
)
@roles_required("admin")
def cambiar_estado_alojamiento(alojamiento_id):

    if not validar_csrf():
        flash("La solicitud no es válida.", "error")
        return redirect(url_for("admin.alojamientos"))

    nuevo_estado = request.form.get("estado", "").strip()

    estados_permitidos = (
        "borrador",
        "pendiente",
        "publicado",
        "suspendido"
    )

    if nuevo_estado not in estados_permitidos:
        flash("El estado seleccionado no es válido.", "error")
        return redirect(url_for("admin.alojamientos"))

    db = get_db()

    alojamiento = db.execute(
        "SELECT id FROM alojamientos WHERE id = ?",
        (alojamiento_id,)
    ).fetchone()

    if alojamiento is None:
        flash("El alojamiento no existe.", "error")
        return redirect(url_for("admin.alojamientos"))

    db.execute(
        """
        UPDATE alojamientos
        SET estado = ?
        WHERE id = ?
        """,
        (nuevo_estado, alojamiento_id)
    )

    db.commit()

    flash(
        "Estado actualizado correctamente.",
        category="alojamiento"
    )

    return redirect(
        url_for(
            "admin.alojamientos",
            actualizado=alojamiento_id
        )
        + f"#alojamiento-{alojamiento_id}"
    )
