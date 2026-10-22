"""Punto de entrada del proyecto EcoTech."""

from getpass import getpass

from src.database.conexion import ConexionDB
from src.menu import MenuEcoTech


def main():
    # La contraseña se pide por consola: no se escribe en el código.
    db = ConexionDB(password=getpass("Contraseña de MySQL: "))
    try:
        if db.conectar() is None:
            return
        MenuEcoTech(db).ejecutar()
    finally:
        db.desconectar()


if __name__ == "__main__":
    main()
