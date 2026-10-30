
from flask import Blueprint, render_template, request, abort

from database import get_db


bp = Blueprint("public", __name__)


@bp.route("/")
def index():
    """Página principal del directorio."""

    db = get_db()

    anuncios = db.execute("""
        SELECT
            id,
            titulo,
            descripcion AS contenido
        FROM anuncios
        WHERE activo = 1
        ORDER BY creado_en DESC
    """).fetchall()

    alojamientos = db.execute("""
        SELECT
            a.id,
            a.nombre,
            a.tipo,
            a.direccion_referencia AS direccion,
            a.capacidad,
            a.descripcion,
            imagen.url AS imagen_url,
            imagen.texto_alternativo AS imagen_alt
        FROM alojamientos AS a
        LEFT JOIN imagenes_alojamiento AS imagen
            ON imagen.id = (
                SELECT img.id
                FROM imagenes_alojamiento AS img
                WHERE img.alojamiento_id = a.id
                ORDER BY img.orden ASC, img.id ASC
                LIMIT 1
            )
        WHERE a.estado = 'publicado'
        ORDER BY a.creado_en DESC
        LIMIT 6
    """).fetchall()

    return render_template(
        "index.html",
        anuncios=anuncios,
        alojamientos=alojamientos
    )


@bp.route("/alojamientos")
def alojamientos():
    """Listado público con búsqueda."""

    db = get_db()
    termino = request.args.get("q", "").strip()

    consulta = """
        SELECT
            a.id,
            a.nombre,
            a.tipo,
            a.direccion_referencia AS direccion,
            a.capacidad,
            a.descripcion,
            imagen.url AS imagen_url,
            imagen.texto_alternativo AS imagen_alt
        FROM alojamientos AS a
        LEFT JOIN imagenes_alojamiento AS imagen
            ON imagen.id = (
                SELECT img.id
                FROM imagenes_alojamiento AS img
                WHERE img.alojamiento_id = a.id
                ORDER BY img.orden ASC, img.id ASC
                LIMIT 1
            )
        WHERE a.estado = 'publicado'
    """

    parametros = []

    if termino:
        consulta += """
            AND (
                a.nombre LIKE ?
                OR a.tipo LIKE ?
                OR a.direccion_referencia LIKE ?
                OR a.servicios LIKE ?
                OR a.descripcion LIKE ?
            )
        """

        busqueda = f"%{termino}%"
        parametros.extend([busqueda] * 5)

    consulta += " ORDER BY a.creado_en DESC"

    alojamientos = db.execute(
        consulta,
        parametros
    ).fetchall()

    return render_template(
        "alojamientos.html",
        alojamientos=alojamientos,
        termino=termino
    )


@bp.route("/alojamientos/<int:alojamiento_id>")
def alojamiento_detalle(alojamiento_id):
    """Muestra la ficha pública de un alojamiento."""

    db = get_db()

    alojamiento = db.execute("""
        SELECT
            id,
            nombre,
            tipo,
            direccion_referencia AS direccion,
            capacidad,
            telefono,
            servicios,
            descripcion,
            latitud,
            longitud,
            google_maps_url
        FROM alojamientos
        WHERE id = ? AND estado = 'publicado'
    """, (alojamiento_id,)).fetchone()

    if alojamiento is None:
        abort(404)

    imagenes = db.execute("""
        SELECT id, url, texto_alternativo, orden
        FROM imagenes_alojamiento
        WHERE alojamiento_id = ?
        ORDER BY orden ASC, id ASC
    """, (alojamiento_id,)).fetchall()

    return render_template(
        "alojamiento_detalle.html",
        alojamiento=alojamiento,
        imagenes=imagenes
    )
