"""Módulo reservado para RegistroTiempo."""
from math import isfinite
from src.modelos.proyecto import Proyecto

from datetime import date
from typing import Any


class registro_tiempo:
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
        if isinstance(proyecto, Proyecto) and not proyecto.activo:
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
    def fecha(self):
        return self.__fecha

    @property
    def horas_trabajadas(self):
        return self.__horas_trabajadas

    @property
    def descripcion_tareas(self):
        return self.__descripcion_tareas

    @property
    def empleado(self):
        return self.__empleado

    @property
    def proyecto(self):
        return self.__proyecto

    @property
    def aprobado(self):
        return self.__aprobado



    @staticmethod
    def _horas_validas(horas) -> bool:
        return(
            not isinstance(horas, bool)
            and isinstance(horas, (int, float))
            and isfinite(horas)
            and horas > 0
        )

    @staticmethod
    def _texto_valido(texto) -> bool:
        return isinstance(texto, str) and bool (texto.strip())


    def crear_registro(self) -> bool:
        """Valida los datos mínimos necesarios para crear un registro."""
        if not self._texto_valido(self.__id_registro):
            return False

        if not isinstance(self.__fecha, date):
            return False

        if not self._horas_validas(self.__horas_trabajadas):
            return False

        if not self._texto_valido(self.__descripcion_tareas):
            return False

        from src.modelos.empleado import Empleado

        if not isinstance(self.__empleado, Empleado):
            return False

        if not isinstance(self.__proyecto, Proyecto):
            return False

        if not isinstance(self.__aprobado, bool):
            return False

        if not self.__proyecto.activo:
            return False

        return True

    def modificar_registro(
        self,
        fecha: date | None = None,
        horas_trabajadas: float | None = None,
        descripcion_tareas: str | None = None
    ) -> bool:
        if self.__aprobado:
             return False

        # Primero se validan los cambios solicitados
        if fecha is not None and not isinstance(fecha, date):
                return False

        if horas_trabajadas is not None and not self._horas_validas(horas_trabajadas):
                return False

        if descripcion_tareas is not None and not self._texto_valido(descripcion_tareas):
                return False

        # Después de la validación se aplican cambios
        if fecha is not None:
             self.__fecha = fecha

        if horas_trabajadas is not None:
             self.__horas_trabajadas = horas_trabajadas

        if descripcion_tareas is not None:
            self.__descripcion_tareas = descripcion_tareas.strip()

        return True
