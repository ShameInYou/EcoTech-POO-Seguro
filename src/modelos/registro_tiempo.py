"""Módulo reservado para RegistroTiempo."""

# TODO: definir RegistroTiempo según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

from datetime import date
from typing import Any


class RegistroTiempo:
    def __init__(
        self,
        id_registro: str,
        fecha: date,
        horas_trabajadas: float,
        descripcion_tareas: str,
        empleado: Any,
        proyecto: Any,
        aprobado: bool = False
    ):
        if proyecto is not None and not proyecto.activo:
            raise ValueError("No se pueden registrar horas en un proyecto desactivado")
        self.__id_registro = id_registro
        self.__fecha = fecha
        self.__horas_trabajadas = horas_trabajadas
        self.__descripcion_tareas = descripcion_tareas
        self.__aprobado = aprobado

        # Relaciones necesarias para conservar la trazabilidad:
        # qué empleado registró horas y en qué proyecto.
        self.__empleado = empleado
        self.__proyecto = proyecto

    @property
    def empleado(self):
        return self.__empleado

    @property
    def proyecto(self):
        return self.__proyecto

    @property
    def horas_trabajadas(self):
        return self.__horas_trabajadas

    def crear_registro(self) -> bool:
        """Valida los datos mínimos necesarios para crear un registro."""
        if not self.__id_registro:
            return False

        if not isinstance(self.__fecha, date):
            return False

        if self.__horas_trabajadas <= 0:
            return False

        if not self.__descripcion_tareas:
            return False

        if self.__empleado is None or self.__proyecto is None:
            return False

        if not self.__proyecto.activo:
            return False

        return True

    def modificar_registro(
        self,
        fecha: date = None,
        horas_trabajadas: float = None,
        descripcion_tareas: str = None
    ) -> bool:
        """Permite modificar los datos del registro de tiempo."""
        if fecha is not None:
            if not isinstance(fecha, date):
                return False
            self.__fecha = fecha

        if horas_trabajadas is not None:
            if horas_trabajadas <= 0:
                return False
            self.__horas_trabajadas = horas_trabajadas

        if descripcion_tareas is not None:
            if not descripcion_tareas:
                return False
            self.__descripcion_tareas = descripcion_tareas

        return True
