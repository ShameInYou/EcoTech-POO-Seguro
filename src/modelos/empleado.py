"""Módulo reservado para Empleado."""

# TODO: definir Empleado según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.
from usuario import Usuario
from datetime import date as Date


class Empleado(Usuario):
    def __init__(self, id_usuario:str, username:str, passwordHash:str, id_empleado:str, nombre:str, direccion:str, correo:str, fechaContrato:Date, salario: float, estado, intentosfallidos):
        super().__init__(id_usuario, username, passwordHash, estado, intentosfallidos)
        self.__id_empleado = id_empleado
        self.__nombre = nombre
        self.__direccion = direccion
        self.__correo = correo
        self.__fechaContrato = fechaContrato
        self.__salario = salario