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
        self.__activo = True

    @property
    def activo(self) -> bool:
        return self.__activo


    @property
    def nombre(self):
        return self.__nombre

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    def crear_proyecto(self) -> bool:
        """Valida que el proyecto tenga sus datos obligatorios."""
        if not self.__id_proyecto or not self.__nombre:
            return False

        if not isinstance(self.__fecha_inicio, date):
            return False

        return True

    def editar_proyecto(
        self,
        nombre: str | None = None,
        descripcion: str | None = None,
        fecha_inicio: date | None = None
    ) -> bool:
        # Primero se comprueban cambios solicitados
        if nombre is not None:
            if not isinstance(nombre, str) or not nombre.strip():
                return False

        if descripcion is not None:
            if not isinstance(descripcion, str):
                return False

        if fecha_inicio is not None:
            if not isinstance(fecha_inicio, date):
                return False



        if nombre is not None:
            self.__nombre = nombre.strip()

        if descripcion is not None:
            self.__descripcion = descripcion.strip()

        if fecha_inicio is not None:
            self.__fecha_inicio = fecha_inicio

        return True

    def eliminar_proyecto(self) -> bool:
        """Desactiva sin borrar los datos ni las relaciones del proyecto."""
        if not self.__activo:
            return False
        self.__activo = False
        return True
