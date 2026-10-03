# EcoTech 🌱

Proyecto grupal de Programación Orientada a Objetos Segura. Acá vamos a ir armando el código en Python y guardando los avances del equipo. Trabajaremos en VS Code, con GitHub para el código y Trello para organizar las tareas.

## Equipo

- [ShameInYou](https://github.com/ShameInYou)
- [johnny420jj](https://github.com/johnny420jj)
- [rojasigna1-rgb](https://github.com/rojasigna1-rgb)

## Modelo que vamos a usar

Vamos a trabajar con **el modelo UML de la versión del Informe de ShameInYou**. Esa será nuestra referencia común para las clases, sus atributos, métodos y relaciones. Si necesitamos cambiar algo, lo conversamos entre los tres y actualizamos el modelo y el código para que sigan coincidiendo.

Falta agregar aquí el nombre exacto de esa versión y el enlace al Informe. Por ahora, el repositorio tiene la estructura inicial: la lógica de las clases todavía no está implementada. Antes de programar, revisamos que los archivos coincidan con el modelo elegido.

## Qué hay en cada carpeta

```text
src/
  modelos/
    usuario.py
    rol.py
    empleado.py
    gerente.py
    departamento.py
    proyecto.py
    asignacion_proyecto.py
    registro_tiempo.py
  servicios/
    gestor_cifrado.py
    validador_entradas.py
    gestor_informe.py
  informes/
    informe.py
    informe_pdf.py
    informe_excel.py
  database/
    conexion.py
tests/
main.py
requirements.txt
.gitignore
```

- **modelos:** las clases principales del proyecto.
- **servicios:** validaciones, cifrado y gestión de informes.
- **informes:** la base de los informes y sus versiones PDF y Excel.
- **database:** la conexión a la base de datos.
- **tests:** las pruebas que vayamos agregando.
- **main.py:** el punto desde donde partimos el programa.

Cada carpeta Python tiene su `__init__.py`. Las bibliotecas que acordemos usar irán en `requirements.txt`.

## Para empezar en VS Code

Primero hay que tener Python 3, Git, VS Code y la extensión Python de Microsoft. Cada uno acepta su invitación de GitHub y descarga su propia copia con estos comandos en la terminal:

```powershell
git clone https://github.com/ShameInYou/EcoTech-POO-Seguro.git
cd EcoTech-POO-Seguro
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
code .
```

En VS Code, abrimos **Python: Select Interpreter** y elegimos el Python de `.venv`. Para ejecutar el proyecto desde su carpeta principal:

```powershell
.\.venv\Scripts\python.exe main.py
```

Por ahora solo aparecerá un mensaje avisando que la implementación está pendiente. Estos comandos son para Windows; en macOS o Linux usamos `.venv/bin/python` en lugar de `.\.venv\Scripts\python.exe`.

## Cómo nos vamos a organizar

1. Elegimos una tarjeta de Trello y dejamos claro quién la toma y qué hay que entregar.
2. Antes de empezar, actualizamos `main` y creamos una rama para esa tarea:

```powershell
git switch main
git pull --ff-only
git switch -c feature/usuario-rol
```

3. Hacemos los cambios en VS Code y comprobamos que funcionen.
4. Revisamos los archivos que vamos a subir. Por ejemplo:

```powershell
git add src/modelos/usuario.py src/modelos/rol.py
git commit -m "Agrega Usuario y Rol según el Informe"
git push -u origin feature/usuario-rol
```

5. Abrimos un **pull request hacia `main`** en GitHub: contamos qué hicimos, cómo lo probamos y pegamos el enlace de la tarjeta.
6. Otro compañero lo revisa. Cuando esté listo, integramos los cambios y actualizamos la tarjeta.
7. Volvemos a `main` y hacemos `git pull --ff-only` antes de empezar otra tarea.

La idea es que cada uno trabaje en su rama y revisemos los cambios entre nosotros antes de juntarlos. Esto es un acuerdo del equipo; todavía no hay una regla técnica que obligue a hacerlo.

## Reparto del trabajo

Todavía tenemos que asignar responsables. Podemos dividir las tareas en usuarios y roles; departamentos, proyectos y tiempos; y servicios e informes. La base de datos, la integración y las pruebas las coordinamos entre los tres.

En cada iteración elegimos un líder y vamos rotando. Si un bloque queda más pesado, lo repartimos de nuevo. Antes de programar por separado, acordamos cómo se van a conectar nuestras clases.

Una tarea queda terminada cuando cumple lo acordado y el modelo del Informe, la probamos, otro compañero la revisó y sus cambios ya están en `main`.

## Pruebas

Aún no hay casos de prueba. A medida que implementemos, los agregamos en `tests/`. Si usamos `unittest`, se ejecutan así:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Si aparecen cero pruebas, significa que todavía no hay nada comprobado por ese comando.

## Revisión del profesor

Queremos que el profesor pueda revisar tanto el código y los pull requests en GitHub como el avance de las tareas en Trello. **El acceso se gestiona por separado en cada plataforma**; compartir un enlace privado no basta para entrar.

Pendiente: confirmar su cuenta de GitHub y su correo o usuario de Trello, enviar las invitaciones y comprobar que pueda abrir ambos. También falta agregar el enlace del tablero aquí. Mantendremos el repositorio privado.

## Un par de acuerdos importantes

- No subimos contraseñas, claves ni datos personales reales. `.env`, `.venv`, las cachés de Python y los ajustes locales de VS Code están en `.gitignore`.
- Elegimos juntos el motor de base de datos y las bibliotecas antes de agregarlas.
- Acordamos cómo manejar las contraseñas y el cifrado antes de implementar esa parte.
- Si cambiamos algo del modelo, lo dejamos conversado y documentado para que nadie trabaje con una versión distinta.
