"""Módulo reservado para Departamento."""

# TODO: definir Departamento según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

class Departamento:
    def __init__(self, idDepartamento: str, nombre: str):
        self.__idDepartamento = idDepartamento
        self.__nombre = nombre

    def crearDepartamento(self) -> bool:
        """Valida que el departamento tenga sus datos obligatorios."""
        if not self.__idDepartamento or not self.__nombre:
            return False
        return True

    def editarDepartamento(self, nuevoNombre: str) -> bool:
        """Modifica el nombre del departamento."""
        if not nuevoNombre:
            return False

        self.__nombre = nuevoNombre
        return True

    def eliminarDepartamento(self) -> bool:
        """Representa la eliminación lógica del departamento."""
        return True