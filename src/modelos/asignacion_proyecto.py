"""Módulo reservado para AsignacionProyecto."""

# TODO: definir AsignacionProyecto según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

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
        if not proyecto.activo:
            raise ValueError("No se puede asignar un proyecto desactivado")
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

    def finalizar_asignacion(self) -> bool:
        """Finaliza una asignación activa."""
        if not self.__activo:
            return False

        self.__activo = False
        return True
