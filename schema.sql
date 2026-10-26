PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS alojamientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    direccion TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    capacidad INTEGER NOT NULL DEFAULT 1 CHECK (capacidad > 0),
    telefono TEXT NOT NULL DEFAULT '',
    servicios TEXT NOT NULL DEFAULT '',
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS anuncios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alojamientos_activo
ON alojamientos(activo);

CREATE INDEX IF NOT EXISTS idx_anuncios_activo
ON anuncios(activo);
