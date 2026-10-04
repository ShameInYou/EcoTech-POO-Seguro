"""Módulo reservado para Proyecto."""

# TODO: definir Proyecto según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.


from datetime import date


class Proyecto:
    def __init__(
        self,
        idProyecto: str,
        nombre: str,
        descripcion: str,
        fechaInicio: date
    ):
        self.__idProyecto = idProyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fechaInicio = fechaInicio

    def crearProyecto(self) -> bool:
        """Valida que el proyecto tenga sus datos obligatorios."""
        if not self.__idProyecto or not self.__nombre:
            return False

        if not isinstance(self.__fechaInicio, date):
            return False

        return True

    def editarProyecto(
        self,
        nombre: str = None,
        descripcion: str = None,
        fechaInicio: date = None
    ) -> bool:
        """Permite modificar los datos principales del proyecto."""
        if nombre is not None:
            if not nombre:
                return False
            self.__nombre = nombre

        if descripcion is not None:
            self.__descripcion = descripcion

        if fechaInicio is not None:
            if not isinstance(fechaInicio, date):
                return False
            self.__fechaInicio = fechaInicio

        return True

    def eliminarProyecto(self) -> bool:
        """Representa la eliminación lógica del proyecto."""
        return True