"""Módulo reservado para AsignacionProyecto."""

from datetime import date
from typing import Any


class AsignacionProyecto:
    def __init__(
        self,
        id_asignacion: str,
        fecha_asignacion: date,
        rol_proyecto: str,
        empleado: Any,
        proyecto: Any,
        activo: bool = True
    ):
        # Imports locales para evitar ciclos al cargar los modelos.
        from src.modelos.empleado import Empleado
        from src.modelos.proyecto import Proyecto

        if not isinstance(empleado, Empleado):
            raise TypeError("Debes indicar un Empleado.")
        if not isinstance(proyecto, Proyecto):
            raise TypeError("Debes indicar un Proyecto.")

        self.__id_asignacion = id_asignacion
        self.__fecha_asignacion = fecha_asignacion
        self.__rol_proyecto = rol_proyecto
        self.__activo = activo

        # Esta clase representa la relación muchos-a-muchos
        # entre Empleado y Proyecto.
        self.__empleado = empleado
        self.__proyecto = proyecto

    @property
    def empleado(self):
        return self.__empleado

    @property
    def proyecto(self):
        return self.__proyecto

    @property
    def activo(self) -> bool:
        return self.__activo

    @property
    def rol_proyecto(self) -> str:
        return self.__rol_proyecto

    def finalizar_asignacion(self) -> bool:
        """Finaliza una asignación activa."""
        if not self.__activo:
            return False

        self.__activo = False
        return True