"""Módulo reservado para Gerente."""

# TODO: definir Gerente según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.
from empleado import Empleado
from datetime import date as Date


class Gerente(Empleado):
    def __init__(self, id_usuario:str, username:str, passwordHash:str, id_empleado:str, nombre:str, direccion:str, correo:str, fechaContrato:Date, salario: float, estado, intentosfallidos:int, departamentoAsignado:str, presupuestoAsignado: float):
        super().__init__(id_usuario, username, passwordHash, id_empleado, nombre, direccion, correo, fechaContrato, salario, estado, intentosfallidos)
        self.__departamentoAsignado = departamentoAsignado
        self.presupuestoAsignado = presupuestoAsignado

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
        return True