PRAGMA foreign_keys = ON;

-- 1. Cuentas de las personas que utilizan el sistema.
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,

    rol TEXT NOT NULL DEFAULT 'usuario'
        CHECK (rol IN ('usuario', 'propietario', 'admin')),

    activo INTEGER NOT NULL DEFAULT 1
        CHECK (activo IN (0, 1)),

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Alojamientos registrados en la plataforma.
CREATE TABLE alojamientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    propietario_id INTEGER NOT NULL,

    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',

    capacidad INTEGER NOT NULL DEFAULT 1
        CHECK (capacidad > 0),

    direccion_referencia TEXT NOT NULL DEFAULT '',
    telefono TEXT NOT NULL DEFAULT '',
    servicios TEXT NOT NULL DEFAULT '',

    latitud REAL,
    longitud REAL,
    google_maps_url TEXT NOT NULL DEFAULT '',

    estado TEXT NOT NULL DEFAULT 'pendiente'
        CHECK (
            estado IN (
                'borrador',
                'pendiente',
                'publicado',
                'suspendido'
            )
        ),

    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (propietario_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT,

    CHECK (
        (latitud IS NULL AND longitud IS NULL)
        OR
        (
            latitud BETWEEN -90 AND 90
            AND longitud BETWEEN -180 AND 180
        )
    )
);

-- Índices para consultas frecuentes.
CREATE INDEX idx_alojamientos_propietario
ON alojamientos(propietario_id);

CREATE INDEX idx_alojamientos_estado
ON alojamientos(estado);

-- 3. Imagenes de alojamientos
CREATE TABLE imagenes_alojamiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alojamiento_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    texto_alternativo TEXT NOT NULL DEFAULT '',
    orden INTEGER NOT NULL DEFAULT 0 CHECK (orden >= 0),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (alojamiento_id)
        REFERENCES alojamientos(id)
        ON DELETE CASCADE,

    CHECK (length(trim(url)) > 0)
);

CREATE INDEX idx_imagenes_alojamiento
    ON imagenes_alojamiento(alojamiento_id);

-- 4. Reservas Usuarios, Alojamientos
CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    alojamiento_id INTEGER NOT NULL,
    fecha_entrada TEXT NOT NULL,
    fecha_salida TEXT NOT NULL,
    cantidad_huespedes INTEGER NOT NULL DEFAULT 1
        CHECK (cantidad_huespedes > 0),
    mensaje TEXT NOT NULL DEFAULT '',
    estado TEXT NOT NULL DEFAULT 'pendiente'
        CHECK (
            estado IN (
                'pendiente',
                'confirmada',
                'rechazada',
                'cancelada'
            )
        ),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT,

    FOREIGN KEY (alojamiento_id)
        REFERENCES alojamientos(id)
        ON DELETE RESTRICT,

    CHECK (fecha_salida > fecha_entrada)
);

CREATE INDEX idx_reservas_usuario
    ON reservas(usuario_id);

CREATE INDEX idx_reservas_alojamiento
    ON reservas(alojamiento_id);

CREATE INDEX idx_reservas_estado
    ON reservas(estado);

-- 5. Anuncios
CREATE TABLE anuncios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    imagen_url TEXT NOT NULL DEFAULT '',
    destino_url TEXT NOT NULL DEFAULT '',
    activo INTEGER NOT NULL DEFAULT 1
        CHECK (activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_anuncios_activo
    ON anuncios(activo);
