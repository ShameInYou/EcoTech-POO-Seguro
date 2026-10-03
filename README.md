# EcoTech — Programación Orientada a Objetos Segura

Proyecto grupal de tres integrantes. Esta versión contiene únicamente la estructura inicial: las clases, sus atributos, métodos, relaciones y herencia se implementarán después de validar el UML definitivo.

## Estructura

```text
src/
  modelos/
    usuario.py, rol.py, empleado.py, gerente.py
    departamento.py, proyecto.py, asignacion_proyecto.py, registro_tiempo.py
  servicios/
    gestor_cifrado.py, validador_entradas.py, gestor_informe.py
  informes/
    informe.py, informe_pdf.py, informe_excel.py
  database/
    conexion.py
tests/
main.py
requirements.txt
.gitignore
```

Cada carpeta Python incluye un archivo `__init__.py`.

## Preparar cada computador

Instalar Python 3, Git, VS Code y la extensión Python de Microsoft. Ejecutar en la terminal:

```powershell
git clone https://github.com/ShameInYou/EcoTech-POO-Seguro.git
cd EcoTech-POO-Seguro
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
code .
```

En VS Code, ejecutar **Python: Select Interpreter** y elegir el Python de `.venv`. No hace falta activar el entorno para usar los comandos de esta guía.

Ejecutar desde la raíz:

```powershell
.\.venv\Scripts\python.exe main.py
```

La salida indica que la implementación está pendiente. En macOS o Linux, usar `.venv/bin/python` en lugar de `.\.venv\Scripts\python.exe`.

## Trabajo con ramas y pull requests

1. Tomar una tarjeta del tablero, acordar su alcance y asignar un responsable.
2. Actualizar la rama principal y crear una rama por tarea:

```powershell
git switch main
git pull --ff-only
git switch -c feature/usuario-rol
```

3. Implementar el alcance de la tarjeta y revisar los cambios en VS Code.
4. Agregar únicamente los archivos correspondientes. Ejemplo:

```powershell
git add src/modelos/usuario.py src/modelos/rol.py
git commit -m "Implementa Usuario y Rol según UML"
git push -u origin feature/usuario-rol
```

5. En GitHub, abrir un pull request hacia `main`, enlazar la tarjeta y describir qué se cambió y cómo se comprobó.
6. Otro integrante revisa. Resolver observaciones y conflictos antes de fusionar.
7. Después de fusionar, volver a `main` y actualizarla antes de iniciar otra tarea.

Acuerdo del equipo: integrar mediante pull requests y una revisión de otro integrante. Este acuerdo no equivale a una protección técnica de la rama.

## Reparto inicial sugerido

| Responsable por acordar | Bloque |
| --- | --- |
| Integrante 1 | Usuario, Rol, Empleado y Gerente |
| Integrante 2 | Departamento, Proyecto, AsignacionProyecto y RegistroTiempo |
| Integrante 3 | Servicios e informes |
| Los tres | UML, base de datos, integración, pruebas y revisión |

Elegir un líder de la iteración y rotar el rol. Acordar interfaces antes de trabajar en paralelo y dividir servicios e informes si su carga resulta mayor.

## Criterio de terminado

- Cumple el UML y el alcance acordado.
- Incluye comprobaciones pertinentes del comportamiento implementado.
- Otro integrante revisó el pull request.
- Los cambios están integrados en `main` y la tarjeta está actualizada.

## Pruebas

La carpeta `tests/` todavía no contiene casos. Si se utiliza `unittest`, ejecutar desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Un resultado de cero pruebas no valida funcionalidades. Agregar dependencias si el equipo decide utilizar otro framework.

## Seguridad y decisiones pendientes

- No subir contraseñas, claves ni datos personales reales. `.env`, el entorno virtual y los ajustes locales de VS Code están ignorados.
- Acordar el motor de base de datos y las bibliotecas antes de modificar `requirements.txt`.
- Validar atributos, métodos, herencia y relaciones contra el UML definitivo.
- Definir el tratamiento de contraseñas y el cifrado antes de implementar `GestorCifrado`.
- Invitar a los otros dos integrantes desde la configuración del repositorio cuando se conozcan sus usuarios de GitHub.
