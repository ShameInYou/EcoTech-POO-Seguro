"""Módulo reservado para RegistroTiempo."""

# TODO: definir RegistroTiempo según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

from datetime import date
from typing import Any


class RegistroTiempo:
    def __init__(
        self,
        idRegistro: str,
        fecha: date,
        horasTrabajadas: float,
        descripcionTareas: str,
        empleado: Any,
        proyecto: Any,
        aprobado: bool = False
    ):
        self.__idRegistro = idRegistro
        self.__fecha = fecha
        self.__horasTrabajadas = horasTrabajadas
        self.__descripcionTareas = descripcionTareas
        self.__aprobado = aprobado

        # Relaciones necesarias para conservar la trazabilidad:
        # qué empleado registró horas y en qué proyecto.
        self.__empleado = empleado
        self.__proyecto = proyecto

    def crearRegistro(self) -> bool:
        """Valida los datos mínimos necesarios para crear un registro."""
        if not self.__idRegistro:
            return False

        if not isinstance(self.__fecha, date):
            return False

        if self.__horasTrabajadas <= 0:
            return False

        if not self.__descripcionTareas:
            return False

        if self.__empleado is None or self.__proyecto is None:
            return False

        return True

    def modificarRegistro(
        self,
        fecha: date = None,
        horasTrabajadas: float = None,
        descripcionTareas: str = None
    ) -> bool:
        """Permite modificar los datos del registro de tiempo."""
        if fecha is not None:
            if not isinstance(fecha, date):
                return False
            self.__fecha = fecha

        if horasTrabajadas is not None:
            if horasTrabajadas <= 0:
                return False
            self.__horasTrabajadas = horasTrabajadas

        if descripcionTareas is not None:
            if not descripcionTareas:
                return False
            self.__descripcionTareas = descripcionTareas

        return True