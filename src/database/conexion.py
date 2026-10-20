"""Borrador de ConexionDB para EcoTech. Dependencia: PyMySQL."""

from getpass import getpass

import pymysql
from pymysql.err import MySQLError


class ConexionDB:
    def __init__(self, host="127.0.0.1", user="root", password="",
                 database="ecotech_db", port=3306):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = port
        self.__conexion = None

    def conectar(self):
        # Reutilizar una conexión abierta evita crear conexiones duplicadas.
        if self.__conexion is not None and self.__conexion.open:
            return self.__conexion

        try:
            self.__conexion = pymysql.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database,
                port=self.__port,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
                autocommit=True
            )
            print("Conexión a MySQL establecida correctamente.")
            return self.__conexion
        except MySQLError:
            self.__conexion = None
            print("ERROR: no se pudo conectar. Revisa servidor, base y credenciales.")
            return None

    def desconectar(self):
        if self.__conexion is not None:
            try:
                if self.__conexion.open:
                    self.__conexion.close()
                    print("Conexión cerrada correctamente.")
            finally:
                self.__conexion = None


if __name__ == "__main__":
    # Pedimos la contraseña sin mostrarla ni escribirla en el archivo.
    db = ConexionDB(password=getpass("Contraseña de MySQL: "))

    try:
        conexion = db.conectar()
        if conexion is not None:
            # DictCursor devuelve un diccionario; el alias define su clave.
            with conexion.cursor() as cursor:
                cursor.execute("SELECT 1 AS resultado")
                fila = cursor.fetchone()

            if fila is not None and fila["resultado"] == 1:
                print("Consulta de prueba: OK.")
            else:
                print("La consulta no devolvió el resultado esperado.")
    except MySQLError:
        print("ERROR: no se pudo completar la consulta de prueba.")
    finally:
        # También se cierra si la consulta falla.
        db.desconectar()
