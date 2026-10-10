"""Módulo reservado para Empleado."""

from usuario import Usuario
from datetime import date as Date


class Empleado(Usuario):
    def __init__(self, id_usuario:str, username:str, password_hash:str, id_empleado:str, nombre:str, direccion:str, correo:str, fecha_contrato:Date, salario: float, estado, intentosfallidos):
        super().__init__(id_usuario, username, password_hash, estado, intentosfallidos)
        self.__id_empleado = id_empleado
        self.__nombre = nombre
        self.__direccion = direccion
        self.__correo = correo
        self.__fechaContrato = fecha_contrato
        self.__salario = salario

    @property
    def id_empleado(self):
        return self.__id_empleado

    @property
    def nombre(self):
        return self.__nombre

    @property
    def direccion(self):
        return self.__direccion

    @property
    def correo(self):
        return self.__correo

    @property
    def fechaContrato(self):
        return self.__fechaContrato

    @property
    def salario(self):
        return self.__salario

    @id_empleado.setter
    def id_empleado(self, value):
        self.__id_empleado = value

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value


    @direccion.setter
    def direccion(self, value):
        self.__direccion = value

    @correo.setter
    def correo(self, value):
        self.__correo = value

    @fechaContrato.setter
    def fechaContrato(self, value):
        self.__fechaContrato = value

    @salario.setter
    def salario(self, value):
        self.__salario = value

    #def registrarHoras AUN FALTAN PROYECTO Y REGISTROTIEMPO

    def consultarPerfil(self):     #Creo que fechacontrato y salario no deberian ser visibles...
        return {
            "id_empleado": self.__id_empleado,
            "nombre": self.__nombre,
            "direccion": self.__direccion,
            "correo": self.__correo,
            "fechaContrato": self.__fechaContrato,
            "salario": self.__salario}