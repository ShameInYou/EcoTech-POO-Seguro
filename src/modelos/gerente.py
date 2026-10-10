"""Módulo reservado para Gerente."""

from src.modelos.empleado import Empleado
from src.modelos.rol import Rol
from datetime import date as Date


class Gerente(Empleado):
    def __init__(self, id_usuario:str, username:str, password_hash:str, id_empleado:str, nombre:str, direccion:str, correo:str, fecha_contrato:Date, salario: float, estado, intentosfallidos:int, departamento_asignado:str, presupuesto_asignado: float, rol: Rol):
        super().__init__(id_usuario, username, password_hash, id_empleado, nombre, direccion, correo, fecha_contrato, salario, estado, intentosfallidos, rol)
        self.__departamentoAsignado = departamento_asignado
        self.presupuestoAsignado = presupuesto_asignado

    @property
    def departamentoAsignado(self):
        return self.__departamentoAsignado

    @departamentoAsignado.setter
    def departamentoAsignado(self, value):
        self.__departamentoAsignado = value


    @property
    def presupuestoAsignado(self):
        return self.__presupuestoAsignado

    @presupuestoAsignado.setter
    def presupuestoAsignado(self, value):
        if value < 0:
            raise ValueError("El presupuesto no puede ser negativo")
        self.__presupuestoAsignado = value

    def aprobarHoras(self, registro) -> bool:
        if not self.tiene_permiso("aprobar_horas"):
            raise PermissionError("No tienes permiso para aprobar horas")


    def reasignarProyecto(self, empleado, proyecto) -> None:
       if not self.tiene_permiso("reasignar_proyecto"):
           raise PermissionError("No tienes permiso para reasignar proyectos")