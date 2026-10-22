"""Borrador de menú administrativo local para EcoTech (datos ficticios).

Copiar como menu_bd.py en la raíz del proyecto para ejecutarlo:
    python menu_bd.py
Requiere PyMySQL, las dependencias del proyecto, ConexionDB y el DDL local.
Roles y departamentos deben existir previamente. No implementa inicio de sesión.
La dirección se omite: requiere integrar el cifrado y adecuar la columna SQL.
"""

from datetime import date
from decimal import Decimal, InvalidOperation
from getpass import getpass
from uuid import uuid4

from pymysql.err import MySQLError

from src.database.conexion import ConexionDB
from src.modelos.usuario import Usuario
from src.servicios.validador_entradas import ValidadorEntradas


def pedir_texto(mensaje, maximo):
    texto = ValidadorEntradas.sanitizar_entrada(input(mensaje))
    if not texto or len(texto) > maximo:
        raise ValueError(f"El texto debe tener entre 1 y {maximo} caracteres.")
    return texto


def mostrar_filas(filas):
    print()
    if not filas:
        print("No hay registros para mostrar.")
    for fila in filas:
        print(" | ".join(f"{campo}: {valor}" for campo, valor in fila.items()))


def elegir_opcion(filas, campo_nombre, titulo):
    """Muestra nombres y devuelve la fila elegida, conservando su ID interno."""
    print(f"\n{titulo}")
    for numero, fila in enumerate(filas, start=1):
        print(f"{numero}. {fila[campo_nombre]}")
    while True:
        opcion = input("Elige el número de la opción: ").strip()
        if opcion.isascii() and opcion.isdecimal():
            numero = int(opcion)
            if 1 <= numero <= len(filas):
                elegida = filas[numero - 1]
                print(f"Seleccionado: {elegida[campo_nombre]}.")
                return elegida
        print(f"Introduce un número entre 1 y {len(filas)}.")


def pedir_password():
    print("La contraseña no se muestra mientras escribes; es normal.")
    while True:
        password = getpass("Contraseña del nuevo usuario: ")
        if not password:
            print("La contraseña no puede estar vacía.")
            continue
        confirmacion = getpass("Repite la contraseña: ")
        if password == confirmacion:
            print("Contraseña ingresada y confirmada correctamente.")
            return password
        print("Las contraseñas no coinciden. Inténtalo nuevamente.")


def ingresar_usuario(conexion):
    username = pedir_texto("Nombre de usuario: ", 50)
    password = pedir_password()
    password_hash = Usuario.generar_hash(password)

    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_rol, nombre_rol FROM rol ORDER BY nombre_rol")
        roles = cursor.fetchall()
        if not roles:
            raise ValueError("Primero deben crear los roles en la base de datos.")
        rol = elegir_opcion(roles, "nombre_rol", "Roles disponibles:")
        id_rol = rol["id_rol"]

        # Los valores van separados del SQL; nunca concatenamos entradas.
        cursor.execute(
            """INSERT INTO usuario
               (id_usuario, username, password_hash, estado, intentos_fallidos, id_rol)
               VALUES (%s, %s, %s, TRUE, 0, %s)""",
            (str(uuid4()), username, password_hash, id_rol)
        )


def ingresar_empleado(conexion):
    # El usuario debe haberse creado antes con la opción 1.
    username = pedir_texto("Usuario existente al que vincular el empleado: ", 50)
    nombre = pedir_texto("Nombre del empleado: ", 100)
    correo = pedir_texto("Correo: ", 120)
    if not ValidadorEntradas.validar_email(correo):
        raise ValueError("El correo no tiene un formato válido.")

    telefono = input("Teléfono internacional (Enter para omitir): ").strip()
    if telefono and not ValidadorEntradas.validar_telefono(telefono):
        raise ValueError("Usa un teléfono internacional, por ejemplo +56912345678.")

    try:
        fecha = date.fromisoformat(input("Fecha de contrato AAAA-MM-DD: ").strip())
    except ValueError:
        raise ValueError("La fecha no es válida; utiliza AAAA-MM-DD.") from None

    try:
        salario = Decimal(input("Salario, sin separador de miles: ").strip())
        if not salario.is_finite() or salario < 0 or salario > Decimal("9999999999.99"):
            raise ValueError("Salario fuera de rango.")
        if salario != salario.quantize(Decimal("0.01")):
            raise ValueError("El salario admite como máximo dos decimales.")
    except InvalidOperation:
        raise ValueError("El salario debe ser un número válido.") from None

    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_departamento, nombre FROM departamento WHERE activo = TRUE ORDER BY nombre"
        )
        departamentos = cursor.fetchall()
        if not departamentos:
            raise ValueError("Primero deben crear un departamento activo.")
        mostrar_filas(departamentos)
        id_departamento = pedir_texto("ID del departamento: ", 36)
        departamento = elegir_opcion(departamentos, "nombre", "Departamentos disponibles:")
        id_departamento = departamento["id_departamento"]

        # Bloqueamos las filas seleccionadas hasta confirmar el alta.
        cursor.execute(
            "SELECT id_usuario, estado FROM usuario WHERE username = %s FOR UPDATE",
            (username,)
        )
        usuario = cursor.fetchone()
        if usuario is None or not usuario["estado"]:
            raise ValueError("El usuario no existe o está bloqueado.")
        cursor.execute(
            "SELECT id_departamento FROM departamento WHERE id_departamento = %s AND activo = TRUE FOR UPDATE",
            (id_departamento,)
        )
        if cursor.fetchone() is None:
            raise ValueError("El departamento no existe o está desactivado.")

        # id_usuario UNIQUE en SQL evita vincularlo a dos empleados.
        # direccion queda NULL en el esquema local, hasta integrar el cifrado.
        cursor.execute(
            """INSERT INTO empleado
               (id_empleado, id_usuario, nombre, telefono, correo,
                fecha_contrato, salario, id_departamento)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (str(uuid4()), usuario["id_usuario"], nombre, telefono or None,
             correo, fecha, salario, id_departamento)
        )


def consultar_usuarios(conexion):
    with conexion.cursor() as cursor:
        # No consultamos ni mostramos hashes de contraseñas.
        cursor.execute(
            """SELECT u.id_usuario, u.username, r.nombre_rol, u.estado
               FROM usuario u JOIN rol r ON r.id_rol = u.id_rol
               ORDER BY u.username LIMIT 100"""
        )
        mostrar_filas(cursor.fetchall())


def consultar_empleados(conexion):
    with conexion.cursor() as cursor:
        cursor.execute(
            """SELECT e.id_empleado, e.nombre, u.username, e.correo,
                      d.nombre AS departamento, u.estado
               FROM empleado e
               JOIN usuario u ON u.id_usuario = e.id_usuario
               JOIN departamento d ON d.id_departamento = e.id_departamento
               ORDER BY e.nombre LIMIT 100"""
        )
        mostrar_filas(cursor.fetchall())


def buscar_empleado(conexion):
    username = pedir_texto("Nombre de usuario a buscar: ", 50)
    with conexion.cursor() as cursor:
        cursor.execute(
            """SELECT e.id_empleado, e.nombre, u.username, e.correo,
                      e.fecha_contrato, d.nombre AS departamento
               FROM empleado e
               JOIN usuario u ON u.id_usuario = e.id_usuario
               JOIN departamento d ON d.id_departamento = e.id_departamento
               WHERE u.username = %s""",
            (username,)
        )
        mostrar_filas(cursor.fetchall())


def main():
    print("Borrador administrativo local: usar datos ficticios.")
    usuario_db = input("Usuario de MySQL [root]: ").strip() or "root"
    db = ConexionDB(user=usuario_db, password=getpass("Contraseña de MySQL: "))
    conexion = None
    acciones = {
        "1": ingresar_usuario,
        "2": ingresar_empleado,
        "3": consultar_usuarios,
        "4": consultar_empleados,
        "5": buscar_empleado
    }
    nombres_opciones = {
        "1": "Ingresar usuario",
        "2": "Ingresar empleado de usuario existente",
        "3": "Consultar usuarios",
        "4": "Consultar empleados",
        "5": "Buscar empleado por usuario"
    }
    try:
        conexion = db.conectar()
        if conexion is None:
            return
        # El ejemplo de clases usa autocommit=True; aquí confirmamos cada opción.
        conexion.autocommit(False)
        while True:
            print("\n=== ECOTECH — USUARIOS Y EMPLEADOS ===")
            print("Primero crea el usuario de acceso (opción 1).")
            print("Después registra su empleado usando ese nombre de usuario (opción 2).")
            print("Los roles y departamentos se eligen de las opciones disponibles.")
            print("\n1. Ingresar usuario\n2. Ingresar empleado de usuario existente")
            print("3. Consultar usuarios (máximo 100)\n4. Consultar empleados (máximo 100)")
            print("5. Buscar empleado por usuario\n0. Salir")
            opcion = input("Opción: ").strip()
            if opcion == "0":
                print("\nOpción elegida: Salir.\n")
                break
            accion = acciones.get(opcion)
            if accion is None:
                print("Opción no válida.")
                continue
            print(f"\nOpción elegida: {nombres_opciones[opcion]}.\n")
            try:
                conexion.begin()
                accion(conexion)
                conexion.commit()
                if opcion == "1":
                    print("\nUsuario ingresado correctamente.\n")
                elif opcion == "2":
                    print("\nEmpleado ingresado correctamente.\n")
                else:
                    print("\nOperación completada.\n")
            except ValueError as error:
                conexion.rollback()
                print(f"Datos inválidos: {error}")
            except MySQLError as error:
                conexion.rollback()
                if error.args and error.args[0] == 1062:
                    print("Ya existe el usuario, correo o vínculo usuario-empleado.")
                else:
                    print("No se pudo completar la operación en MySQL.")
    except (EOFError, KeyboardInterrupt):
        print("\nOperación cancelada.")
        if conexion is not None and conexion.open:
            conexion.rollback()
    except MySQLError:
        print("La conexión falló. Revisa el servidor antes de continuar.")
    finally:
        db.desconectar()


if __name__ == "__main__":
    main()
