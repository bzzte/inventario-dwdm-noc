-- Esquema jerárquico propuesto (Fase 3). Implementados en el prototipo: plataforma_nms y nodo.
CREATE TABLE plataforma_nms (
    id          SERIAL PRIMARY KEY,
    fabricante  VARCHAR(50)  NOT NULL,
    nombre_nms  VARCHAR(100) NOT NULL
);

CREATE TABLE nodo (
    id             SERIAL PRIMARY KEY,
    plataforma_id  INTEGER NOT NULL REFERENCES plataforma_nms(id),
    ne_name        VARCHAR(100) NOT NULL,
    ne_type        VARCHAR(100),
    ip_gestion     INET,
    version_sw     VARCHAR(50),
    subred         VARCHAR(100)
);

CREATE TABLE chasis (
    id       SERIAL PRIMARY KEY,
    nodo_id  INTEGER NOT NULL REFERENCES nodo(id),
    subrack  VARCHAR(50),
    tipo     VARCHAR(100)
);

CREATE TABLE tarjeta (
    id          SERIAL PRIMARY KEY,
    chasis_id   INTEGER NOT NULL REFERENCES chasis(id),
    slot        VARCHAR(20),
    board_type  VARCHAR(50),
    serial      VARCHAR(100)
);

CREATE TABLE puerto (
    id          SERIAL PRIMARY KEY,
    tarjeta_id  INTEGER NOT NULL REFERENCES tarjeta(id),
    numero      VARCHAR(20),
    tipo        VARCHAR(50)
);

CREATE TABLE longitud_onda (
    id              SERIAL PRIMARY KEY,
    puerto_id       INTEGER NOT NULL REFERENCES puerto(id),
    canal_n         INTEGER,
    f_central_thz   NUMERIC(8,4)
);
