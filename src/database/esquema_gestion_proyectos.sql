DROP DATABASE IF EXISTS ecotech_db;
CREATE DATABASE ecotech_db
	CHARACTER SET utf8mb4 
    COLLATE utf8mb4_spanish_ci;
USE ecotech_db;


CREATE TABLE rol (
    id_rol      VARCHAR(36) NOT NULL PRIMARY KEY,
    nombre_rol  VARCHAR(50) NOT NULL UNIQUE,

    CONSTRAINT chk_rol_nombre CHECK (CHAR_LENGTH(TRIM(nombre_rol)) > 0)
) ENGINE = InnoDB;

CREATE TABLE permiso (
    id_permiso   VARCHAR(36)  NOT NULL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL UNIQUE,
    descripcion  VARCHAR(255),
  
    CONSTRAINT chk_permiso_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) > 0)
) ENGINE = InnoDB;

-- Tabla intermedia: qué permisos tiene cada rol.
-- Si se borra un rol o un permiso, se borra también la relación.
CREATE TABLE rol_permiso (
    id_rol      VARCHAR(36) NOT NULL,
    id_permiso  VARCHAR(36) NOT NULL,

    PRIMARY KEY (id_rol, id_permiso),

    FOREIGN KEY (id_rol) 
        REFERENCES rol (id_rol)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_permiso) 
        REFERENCES permiso (id_permiso)
        ON DELETE RESTRICT
) ENGINE = InnoDB;


-- USUARIOS
-- Todo el que entra al sistema es un usuario y tiene un solo rol.
-- Guardamos el hash de la contraseña, nunca la contraseña en texto plano.

CREATE TABLE usuario (
    id_usuario         VARCHAR(36)  NOT NULL PRIMARY KEY,
    username           VARCHAR(50)  NOT NULL UNIQUE,
    password_hash      VARCHAR(255) NOT NULL,
    estado             BOOLEAN      NOT NULL DEFAULT TRUE,   -- TRUE = cuenta activa
    intentos_fallidos  INT          NOT NULL DEFAULT 0,
    id_rol             VARCHAR(36)  NOT NULL,

    CONSTRAINT chk_usuario_nombre CHECK (CHAR_LENGTH(TRIM(username)) > 0),
    CONSTRAINT chk_usuario_hash CHECK (CHAR_LENGTH(TRIM(password_hash)) > 0),
    CONSTRAINT chk_usuario_estado CHECK (estado IN (0, 1)),
    CONSTRAINT chk_usuario_intentos CHECK (intentos_fallidos >= 0),

    FOREIGN KEY (id_rol)
        REFERENCES rol(id_rol)
        ON DELETE RESTRICT
) ENGINE = InnoDB;


-- DEPARTAMENTOS
-- Ojo: el gerente de un departamento es un empleado, y los empleados
-- pertenecen a un departamento. Es un círculo, así que por ahora
-- id_gerente queda sin FK y la agregamos al final del script.

CREATE TABLE departamento (
    id_departamento  VARCHAR(36)  NOT NULL PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL UNIQUE,
    id_gerente       VARCHAR(36)  NULL UNIQUE,
    activo           BOOLEAN      NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_departamento_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),
    CONSTRAINT chk_departamento_activo CHECK (activo IN (0, 1))
) ENGINE = InnoDB;

-- EMPLEADOS
-- Un empleado es un usuario con más datos, por eso su id es el mismo
-- id_usuario (la PK es también FK hacia usuario).

CREATE TABLE empleado (
    id_empleado      VARCHAR(36)   NOT NULL PRIMARY KEY,
    id_usuario       VARCHAR(36)   NOT NULL UNIQUE,
    nombre           VARCHAR(100)  NOT NULL,
    direccion        VARCHAR(200)  NULL,
    telefono         VARCHAR(20)   NULL,
    correo           VARCHAR(120)  NOT NULL UNIQUE,
    fecha_contrato   DATE          NOT NULL,
    salario          NUMERIC(12,2) NOT NULL,
    id_departamento  VARCHAR(36)   NOT NULL,


    CONSTRAINT chk_empleado_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),
    CONSTRAINT chk_empleado_correo CHECK (CHAR_LENGTH(TRIM(correo)) > 0),
    CONSTRAINT chk_empleado_salario CHECK (salario >= 0),

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_departamento)
        REFERENCES departamento(id_departamento)
        ON DELETE RESTRICT
) ENGINE = InnoDB;


-- GERENTES
-- Un gerente es un empleado con un presupuesto asignado.
-- Mismo truco: su id es el id del empleado.

CREATE TABLE gerente (
    id_gerente            VARCHAR(36)   NOT NULL PRIMARY KEY,
    presupuesto_asignado  NUMERIC(14,2) NOT NULL DEFAULT 0,

    CONSTRAINT chk_gerente_presupuesto CHECK (presupuesto_asignado >= 0),
    FOREIGN KEY (id_gerente)
        REFERENCES empleado(id_empleado)
        ON DELETE RESTRICT
) ENGINE = InnoDB;

-- Ahora sí podemos cerrar el círculo: el departamento apunta a su gerente.
ALTER TABLE departamento
    ADD CONSTRAINT fk_departamento_gerente
    FOREIGN KEY (id_gerente) REFERENCES gerente (id_gerente) ON DELETE RESTRICT;


-- PROYECTOS

CREATE TABLE proyecto (
    id_proyecto   VARCHAR(36)  NOT NULL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL UNIQUE,
    descripcion   VARCHAR(500) NULL,
    fecha_inicio  DATE         NOT NULL,
    activo        BOOLEAN      NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_proyecto_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) > 0),
    CONSTRAINT chk_proyecto_activo CHECK (activo IN (0, 1))
) ENGINE = InnoDB;


-- ASIGNACIONES
-- Un empleado puede trabajar en varios proyectos y un proyecto puede
-- tener varios empleados. Esta tabla une ambos y guarda además el rol
-- que cumple la persona dentro del proyecto.
-- El UNIQUE evita asignar al mismo empleado dos veces al mismo proyecto.

CREATE TABLE asignacion_proyecto (
    id_asignacion     VARCHAR(36) NOT NULL PRIMARY KEY,
    id_empleado       VARCHAR(36) NOT NULL,
    id_proyecto       VARCHAR(36) NOT NULL,
    fecha_asignacion  DATE        NOT NULL DEFAULT (CURRENT_DATE),
    rol_proyecto      VARCHAR(50) NOT NULL,
    activo            BOOLEAN     NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_asignacion_empleado_proyecto UNIQUE (id_empleado, id_proyecto),
    CONSTRAINT chk_asignacion_rol CHECK (CHAR_LENGTH(TRIM(rol_proyecto)) > 0),
    CONSTRAINT chk_asignacion_activo CHECK (activo IN (0, 1)),

    FOREIGN KEY (id_empleado)
        REFERENCES empleado(id_empleado)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_proyecto)
        REFERENCES proyecto(id_proyecto)
        ON DELETE RESTRICT
) ENGINE = InnoDB;


-- REGISTROS DE TIEMPO
-- Las horas que un empleado trabaja en un proyecto cada día.
-- Si se elimina al empleado, se eliminan sus registros.
-- Las horas deben ser más de 0 y no pasar de 24 en un registro.

CREATE TABLE registro_tiempo (
    id_registro         VARCHAR(36)  NOT NULL PRIMARY KEY,
    id_empleado         VARCHAR(36)  NOT NULL,
    id_proyecto         VARCHAR(36)  NOT NULL,
    fecha               DATE         NOT NULL,
    horas_trabajadas    NUMERIC(4,2) NOT NULL,
    descripcion_tareas  VARCHAR(500) NOT NULL,
    aprobado            BOOLEAN      NOT NULL DEFAULT FALSE,   -- lo aprueba el gerente
    CONSTRAINT chk_registro_horas CHECK (horas_trabajadas > 0),
    CONSTRAINT chk_registro_descripcion
        CHECK (CHAR_LENGTH(TRIM(descripcion_tareas)) > 0),
    CONSTRAINT chk_registro_aprobado CHECK (aprobado IN (0, 1)),

    FOREIGN KEY (id_empleado)
        REFERENCES empleado(id_empleado)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_proyecto)
        REFERENCES proyecto(id_proyecto)
        ON DELETE RESTRICT,

    CONSTRAINT fk_registro_asignacion
        FOREIGN KEY (id_empleado, id_proyecto)
        REFERENCES asignacion_proyecto(id_empleado, id_proyecto) ON DELETE RESTRICT

) ENGINE = InnoDB;


-- ÍNDICES
-- Para que las búsquedas por clave foránea sean más rápidas.

CREATE INDEX idx_usuario_rol         ON usuario (id_rol);
CREATE INDEX idx_empleado_depto      ON empleado (id_departamento);
CREATE INDEX idx_asignacion_proyecto ON asignacion_proyecto (id_proyecto);
CREATE INDEX idx_registro_empleado   ON registro_tiempo (id_empleado, fecha);
CREATE INDEX idx_registro_proyecto   ON registro_tiempo (id_proyecto);
