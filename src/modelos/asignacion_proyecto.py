"""Módulo reservado para AsignacionProyecto."""

# TODO: definir AsignacionProyecto según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

from datetime import date
from typing import Any


class AsignacionProyecto:
    def __init__(
        self,
        idAsignacion: str,
        fechaAsignacion: date,
        rolProyecto: str,
        empleado: Any,
        proyecto: Any,
        activo: bool = True
    ):
        self.__idAsignacion = idAsignacion
        self.__fechaAsignacion = fechaAsignacion
        self.__rolProyecto = rolProyecto
        self.__activo = activo

        # Esta clase representa la relación muchos-a-muchos
        # entre Empleado y Proyecto.
        self.__empleado = empleado
        self.__proyecto = proyecto

    def finalizarAsignacion(self) -> bool:
        """Finaliza una asignación activa."""
        if not self.__activo:
            return False

        self.__activo = False
        return True