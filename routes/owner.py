import sqlite3

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort
)

from database import get_db
from routes import roles_required
from routes.auth import validar_csrf


bp = Blueprint("owner", __name__)


@bp.route("/", methods=("GET", "POST"))
@roles_required("propietario")
def dashboard():
    """Muestra y gestiona los alojamientos del propietario autenticado."""

    db = get_db()

    if request.method == "POST":

        if not validar_csrf():
            flash("La solicitud no es válida. Intentá nuevamente.", "error")
            return redirect(url_for("owner.dashboard"))

        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "").strip()
        direccion = request.form.get("direccion", "").strip()
        capacidad = request.form.get("capacidad", "").strip()
        telefono = request.form.get("telefono", "").strip()
        servicios = request.form.get("servicios", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre or not tipo or not direccion:
            flash("Completá los campos obligatorios.", "error")
            return redirect(url_for("owner.dashboard"))
        tipos_validos = {
            "Hotel",
            "Hostería",
            "Hostel",
            "Cabaña",
            "Casa o departamento",
            "Habitación",
            "Otro"
        }

        if tipo not in tipos_validos:
            flash("Seleccioná un tipo de alojamiento válido.", "error")
            return redirect(url_for("owner.dashboard"))

        if len(nombre) > 150 or len(direccion) > 250:
            flash("El nombre o la dirección superan la longitud permitida.", "error")
            return redirect(url_for("owner.dashboard"))

        if len(telefono) > 40 or len(servicios) > 2000:
            flash("El teléfono o los servicios superan la longitud permitida.", "error")
            return redirect(url_for("owner.dashboard"))

        if len(descripcion) > 5000:
            flash("La descripción no puede superar los 5000 caracteres.", "error")
            return redirect(url_for("owner.dashboard"))

        try:
            capacidad = int(capacidad)

            if capacidad < 1 or capacidad > 1000:
                raise ValueError

        except ValueError:
            flash("La capacidad debe ser un número entre 1 y 1000.", "error")
            return redirect(url_for("owner.dashboard"))

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
                    session["usuario_id"],
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
            flash(
                "El alojamiento fue registrado y quedó pendiente de revisión.",
                "success"
            )

        except sqlite3.Error:
            db.rollback()
            flash("No se pudo guardar el alojamiento.", "error")

        return redirect(url_for("owner.dashboard"))

    alojamientos = db.execute(
        """
        SELECT
            id,
            nombre,
            tipo,
            estado,
            capacidad,
            direccion_referencia,
            creado_en
        FROM alojamientos
        WHERE propietario_id = ?
        ORDER BY creado_en DESC
        """,
        (session["usuario_id"],)
    ).fetchall()

    return render_template(
        "owner/dashboard.html",
        alojamientos=alojamientos
    )

@bp.route("/alojamientos/<int:alojamiento_id>/editar", methods=("GET", "POST"))
@roles_required("propietario")
def editar_alojamiento(alojamiento_id):
    """Permite editar únicamente los alojamientos del propietario autenticado."""

    db = get_db()

    alojamiento = db.execute(
        """
        SELECT
            id,
            nombre,
            tipo,
            descripcion,
            capacidad,
            direccion_referencia,
            telefono,
            servicios,
            estado
        FROM alojamientos
        WHERE id = ? AND propietario_id = ?
        """,
        (alojamiento_id, session["usuario_id"])
    ).fetchone()

    if alojamiento is None:
        abort(404)

    if request.method == "POST":

        if not validar_csrf():
            flash("La solicitud no es válida. Intentá nuevamente.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "").strip()
        direccion = request.form.get("direccion", "").strip()
        capacidad = request.form.get("capacidad", "").strip()
        telefono = request.form.get("telefono", "").strip()
        servicios = request.form.get("servicios", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        tipos_validos = {
            "Hotel",
            "Hostería",
            "Hostel",
            "Cabaña",
            "Casa o departamento",
            "Habitación",
            "Otro"
        }

        if not nombre or not tipo or not direccion:
            flash("Completá los campos obligatorios.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        if tipo not in tipos_validos:
            flash("Seleccioná un tipo de alojamiento válido.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        if len(nombre) > 150 or len(direccion) > 250:
            flash("El nombre o la dirección superan la longitud permitida.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        if len(telefono) > 40 or len(servicios) > 2000:
            flash("El teléfono o los servicios superan la longitud permitida.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        if len(descripcion) > 5000:
            flash("La descripción no puede superar los 5000 caracteres.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        try:
            capacidad = int(capacidad)

            if capacidad < 1 or capacidad > 1000:
                raise ValueError

        except ValueError:
            flash("La capacidad debe ser un número entre 1 y 1000.", "error")
            return redirect(
                url_for("owner.editar_alojamiento", alojamiento_id=alojamiento_id)
            )

        try:
            db.execute(
                """
                UPDATE alojamientos
                SET
                    nombre = ?,
                    tipo = ?,
                    descripcion = ?,
                    capacidad = ?,
                    direccion_referencia = ?,
                    telefono = ?,
                    servicios = ?
                WHERE id = ? AND propietario_id = ?
                """,
                (
                    nombre,
                    tipo,
                    descripcion,
                    capacidad,
                    direccion,
                    telefono,
                    servicios,
                    alojamiento_id,
                    session["usuario_id"]
                )
            )

            db.commit()
            flash("El alojamiento fue actualizado correctamente.", "success")

        except sqlite3.Error:
            db.rollback()
            flash("No se pudo actualizar el alojamiento.", "error")

        return redirect(url_for("owner.dashboard"))

    return render_template(
        "owner/editar_alojamiento.html",
        alojamiento=alojamiento
    )
