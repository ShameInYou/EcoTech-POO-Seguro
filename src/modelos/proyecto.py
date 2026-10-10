"""Módulo reservado para Proyecto."""


from datetime import date


class Proyecto:
    def __init__(
        self,
        id_proyecto: str,
        nombre: str,
        descripcion: str,
        fecha_inicio: date
    ):
        self.__id_proyecto = id_proyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio

    def crear_proyecto(self) -> bool:
        """Valida que el proyecto tenga sus datos obligatorios."""
        if not self.__id_proyecto or not self.__nombre:
            return False

        if not isinstance(self.__fecha_inicio, date):
            return False

        return True

    def editar_proyecto(
        self,
        nombre: str = None,
        descripcion: str = None,
        fecha_inicio: date = None
    ) -> bool:
        """Permite modificar los datos principales del proyecto."""
        if nombre is not None:
            if not nombre:
                return False
            self.__nombre = nombre

        if descripcion is not None:
            self.__descripcion = descripcion

        if fecha_inicio is not None:
            if not isinstance(fecha_inicio, date):
                return False
            self.__fecha_inicio = fecha_inicio

        return True

    def eliminar_proyecto(self) -> bool:
        """Representa la eliminación lógica del proyecto."""
        return True