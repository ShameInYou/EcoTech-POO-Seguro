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
        self.__id_asignacion = id_asignacion
        self.__fecha_asignacion = fecha_asignacion
        self.__rol_proyecto = rol_proyecto
        self.__activo = activo

        # Esta clase representa la relación muchos-a-muchos
        # entre Empleado y Proyecto.
        self.__empleado = empleado
        self.__proyecto = proyecto

    def finalizar_asignacion(self) -> bool:
        """Finaliza una asignación activa."""
        if not self.__activo:
            return False

        self.__activo = False
        return True