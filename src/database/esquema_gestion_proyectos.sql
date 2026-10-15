-- Base de datos del sistema de gestión de proyectos
-- Motor: PostgreSQL
--
-- Orden de creación: primero las tablas que no dependen de nadie
-- (rol, permiso), después las que apuntan a ellas, y al final las
-- que dependen de varias.


-- ROLES Y PERMISOS
-- Cada rol tiene un nombre ("Administrador", "Empleado", etc.).
-- Los permisos van en su propia tabla, porque un rol puede tener
-- muchos permisos y un permiso puede estar en muchos roles.

CREATE TABLE rol (
    id_rol      VARCHAR(36) NOT NULL,
    nombre_rol  VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_rol),
    UNIQUE (nombre_rol)
);

CREATE TABLE permiso (
    id_permiso   VARCHAR(36)  NOT NULL,
    nombre       VARCHAR(100) NOT NULL,
    descripcion  VARCHAR(255),
    PRIMARY KEY (id_permiso),
    UNIQUE (nombre)
);

-- Tabla intermedia: qué permisos tiene cada rol.
-- Si se borra un rol o un permiso, se borra también la relación.
CREATE TABLE rol_permiso (
    id_rol      VARCHAR(36) NOT NULL,
    id_permiso  VARCHAR(36) NOT NULL,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol)     REFERENCES rol (id_rol)         ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permiso (id_permiso) ON DELETE CASCADE
);


-- USUARIOS
-- Todo el que entra al sistema es un usuario y tiene un solo rol.
-- Guardamos el hash de la contraseña, nunca la contraseña en texto plano.

CREATE TABLE usuario (
    id_usuario         VARCHAR(36)  NOT NULL,
    username           VARCHAR(50)  NOT NULL,
    password_hash      VARCHAR(255) NOT NULL,
    estado             BOOLEAN      NOT NULL DEFAULT TRUE,   -- TRUE = cuenta activa
    intentos_fallidos  INT          NOT NULL DEFAULT 0,
    id_rol             VARCHAR(36)  NOT NULL,
    PRIMARY KEY (id_usuario),
    UNIQUE (username),
    FOREIGN KEY (id_rol) REFERENCES rol (id_rol),
    CHECK (intentos_fallidos >= 0)
);


-- DEPARTAMENTOS
-- Ojo: el gerente de un departamento es un empleado, y los empleados
-- pertenecen a un departamento. Es un círculo, así que por ahora
-- id_gerente queda sin FK y la agregamos al final del script.

CREATE TABLE departamento (
    id_departamento  VARCHAR(36)  NOT NULL,
    nombre           VARCHAR(100) NOT NULL,
    id_gerente       VARCHAR(36),
    PRIMARY KEY (id_departamento),
    UNIQUE (nombre),
    UNIQUE (id_gerente)    -- un gerente solo puede dirigir un departamento
);


-- EMPLEADOS
-- Un empleado es un usuario con más datos, por eso su id es el mismo
-- id_usuario (la PK es también FK hacia usuario).

CREATE TABLE empleado (
    id_empleado      VARCHAR(36)   NOT NULL,
    nombre           VARCHAR(100)  NOT NULL,
    direccion        VARCHAR(200),
    telefono         VARCHAR(20),
    correo           VARCHAR(120)  NOT NULL,
    fecha_contrato   DATE          NOT NULL,
    salario          NUMERIC(12,2) NOT NULL,
    id_departamento  VARCHAR(36)   NOT NULL,
    PRIMARY KEY (id_empleado),
    UNIQUE (correo),
    FOREIGN KEY (id_empleado)     REFERENCES usuario (id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_departamento) REFERENCES departamento (id_departamento),
    CHECK (salario >= 0)
);


-- GERENTES
-- Un gerente es un empleado con un presupuesto asignado.
-- Mismo truco: su id es el id del empleado.

CREATE TABLE gerente (
    id_gerente            VARCHAR(36)   NOT NULL,
    presupuesto_asignado  NUMERIC(14,2) NOT NULL DEFAULT 0,
    PRIMARY KEY (id_gerente),
    FOREIGN KEY (id_gerente) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
    CHECK (presupuesto_asignado >= 0)
);

-- Ahora sí podemos cerrar el círculo: el departamento apunta a su gerente.
ALTER TABLE departamento
    ADD FOREIGN KEY (id_gerente) REFERENCES gerente (id_gerente);


-- PROYECTOS

CREATE TABLE proyecto (
    id_proyecto   VARCHAR(36)  NOT NULL,
    nombre        VARCHAR(100) NOT NULL,
    descripcion   VARCHAR(500),
    fecha_inicio  DATE         NOT NULL,
    PRIMARY KEY (id_proyecto),
    UNIQUE (nombre)
);


-- ASIGNACIONES
-- Un empleado puede trabajar en varios proyectos y un proyecto puede
-- tener varios empleados. Esta tabla une ambos y guarda además el rol
-- que cumple la persona dentro del proyecto.
-- El UNIQUE evita asignar al mismo empleado dos veces al mismo proyecto.

CREATE TABLE asignacion_proyecto (
    id_asignacion     VARCHAR(36) NOT NULL,
    id_empleado       VARCHAR(36) NOT NULL,
    id_proyecto       VARCHAR(36) NOT NULL,
    fecha_asignacion  DATE        NOT NULL DEFAULT CURRENT_DATE,
    rol_proyecto      VARCHAR(50) NOT NULL,
    activo            BOOLEAN     NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id_asignacion),
    UNIQUE (id_empleado, id_proyecto),
    FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto) ON DELETE CASCADE
);


-- REGISTROS DE TIEMPO
-- Las horas que un empleado trabaja en un proyecto cada día.
-- Si se elimina al empleado, se eliminan sus registros.
-- Las horas deben ser más de 0 y no pasar de 24 en un registro.

CREATE TABLE registro_tiempo (
    id_registro         VARCHAR(36)  NOT NULL,
    id_empleado         VARCHAR(36)  NOT NULL,
    id_proyecto         VARCHAR(36)  NOT NULL,
    fecha               DATE         NOT NULL,
    horas_trabajadas    NUMERIC(4,2) NOT NULL,
    descripcion_tareas  VARCHAR(500) NOT NULL,
    aprobado            BOOLEAN      NOT NULL DEFAULT FALSE,   -- lo aprueba el gerente
    PRIMARY KEY (id_registro),
    FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto),
    CHECK (horas_trabajadas > 0 AND horas_trabajadas <= 24)
);


-- ÍNDICES
-- Para que las búsquedas por clave foránea sean más rápidas.

CREATE INDEX idx_usuario_rol         ON usuario (id_rol);
CREATE INDEX idx_empleado_depto      ON empleado (id_departamento);
CREATE INDEX idx_asignacion_proyecto ON asignacion_proyecto (id_proyecto);
CREATE INDEX idx_registro_empleado   ON registro_tiempo (id_empleado, fecha);
CREATE INDEX idx_registro_proyecto   ON registro_tiempo (id_proyecto);
