# EcoTech 🌱 — Avance formativo Unidad 2

Proyecto grupal de Programación Orientada a Objetos Segura (TI3021).
Este avance presenta las clases y relaciones del modelo UML, su aplicación de POO
y una conexión a MySQL con PyMySQL. Incluye un menú de consola para registrar
usuarios y empleados y consultar sus datos.

## Equipo

- Gabriel Jara — [ShameInYou](https://github.com/ShameInYou)
- Juan Márquez — [johnny420jj](https://github.com/johnny420jj)
- Ignacio Rojas — [rojasigna1-rgb](https://github.com/rojasigna1-rgb)

Repositorio: https://github.com/ShameInYou/EcoTech-POO-Seguro

## Modelo y alcance

La referencia es el UML definitivo del Informe EcoTech de Gabriel Jara.
Los nombres de métodos pueden estar adaptados a snake_case en Python.
Se representan Usuario–Rol, la herencia Usuario → Empleado → Gerente,
Departamento–Empleado/Gerente y las relaciones de asignaciones y registros con
empleados y proyectos. InformePDF e InformeExcel especializan la clase abstracta Informe.

Este es un avance formativo, no el CRUD final de la evaluación sumativa.
Las relaciones se representan mediante objetos en memoria; el menú utiliza consultas
SQL para registrar y consultar datos. Todavía no reconstruye todos los modelos desde la BD.

## Estructura

```text
src/
  modelos/       # Entidades, relaciones y reglas del dominio
  servicios/     # Validación, cifrado y coordinación de informes
  informes/      # Informe abstracto y formatos PDF/Excel
  database/
    conexion.py  # ConexionDB con PyMySQL
    esquema_gestion_proyectos.sql  # Tablas y datos iniciales
    conexion_test.py  # Ejemplo adicional de inserción/consulta
tests/          # Pruebas automatizadas sin MySQL
menu_bd.py       # Menú que se debe ejecutar para la demostración
main.py          # Entrada inicial; todavía solo muestra un mensaje
requirements.txt
```

## Preparar el entorno

Requisitos: Python 3.10 o superior, MySQL Server 8.0.16 o superior y MySQL Workbench.
El desarrollo local utiliza Python 3.14. Workbench administra la base; MySQL Server
es el servicio al que se conecta Python.

Extraer el ZIP y abrir su carpeta EcoTech-POO-Seguro en VS Code.
Desde esa carpeta, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En VS Code seleccionar el intérprete de `.venv`.
Las dependencias incluyen PyMySQL, argon2-cffi, cryptography, ReportLab y openpyxl.

## Preparar la base de datos

1. Iniciar MySQL Server y abrir la conexión local en Workbench.
2. Abrir `src/database/esquema_gestion_proyectos.sql` y ejecutarlo completo.
3. Comprobar que existe `ecotech_db` y que las tablas fueron creadas.

**El SQL empieza con DROP DATABASE: borra y reconstruye ecotech_db.**
Se utiliza para preparar una demostración desde cero. No volver a ejecutarlo
si se quieren conservar los registros ingresados.

El script incluye el rol Empleado (`ROL-EMP`), sus permisos y el departamento
Desarrollo (`DEP-DEV`); no hay que agregarlos manualmente antes de abrir el menú.
Los identificadores de nuevos usuarios y empleados se generan como UUID desde Python.

## Comprobar la conexión

```powershell
.\.venv\Scripts\python.exe -m src.database.conexion
```

Introduce la contraseña local de MySQL cuando se solicite. La configuración
predeterminada es host `127.0.0.1`, puerto `3306`, usuario `root` y base `ecotech_db`.
Para otro usuario o servidor, ajustar los parámetros al construir ConexionDB.
La contraseña no se escribe en el código. La consulta `SELECT 1` no modifica datos.
Debe aparecer `Consulta de prueba: OK` y cerrarse la conexión.

## Ejecutar el menú

```powershell
.\.venv\Scripts\python.exe menu_bd.py
```

El menú pide el usuario de MySQL (root por defecto) y su contraseña.
La contraseña de MySQL es distinta de la contraseña del usuario que registramos en EcoTech.

1. Elegir **Ingresar usuario**: indicar username, escribir dos veces su contraseña
   y seleccionar el rol disponible por número. El ID del rol se asigna internamente.
2. Elegir **Ingresar empleado**: indicar el username creado, sus datos y el departamento.
3. Consultar usuarios, consultar empleados o buscar por username.
4. Salir y abrir de nuevo el menú para comprobar que los datos se conservaron.

La contraseña de EcoTech se guarda como hash Argon2; no se muestra en las consultas.
Las consultas usan parámetros y las operaciones del menú se confirman o revierten
con commit/rollback. Los listados muestran hasta 100 filas.

El menú es un prototipo administrativo local para datos ficticios: todavía no incorpora
inicio de sesión ni autorización por rol para administrar registros. La dirección
se omite en este menú hasta integrar el cifrado con la persistencia.

## Ejecutar las pruebas

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas cubren Rol, Usuario, Empleado, Proyecto, RegistroTiempo, relaciones
y desactivación. No requieren un servidor MySQL y no sustituyen la prueba de conexión.

`src/database/conexion_test.py` es un ejemplo manual adicional, no una prueba unittest.
No es la entrada recomendada para la entrega: conserva datos fijos de demostración
(incluido un valor de hash no válido para autenticar), requiere un rol específico
y puede producir duplicados al repetirse. Usar `conexion.py` y `menu_bd.py`.

## Pendientes para la sumativa

- Completar aprobación de horas y reasignación de proyectos en Gerente.
- Verificar asignación activa antes de registrar horas.
- Completar CRUD y reconstrucción de los objetos desde la base de datos.
- Integrar cifrado de datos sensibles y validaciones de contacto con persistencia.
- Incorporar autenticación/autorización al flujo del menú.
- Revisar manejo de errores, pruebas de integración y resultados de herramientas de seguridad.
- Actualizar el UML y documentar las decisiones y la validación del apoyo de IA.

## Trabajo en equipo

Trabajamos en ramas y revisamos los cambios mediante pull requests antes de integrarlos.
No compartir contraseñas, claves ni datos personales reales. El entorno virtual,
los archivos `.env` y los ajustes locales del editor no se incluyen en la entrega.
