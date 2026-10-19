"""Módulo reservado para Empleado."""
from src.modelos.registro_tiempo import registro_tiempo
from src.modelos.proyecto import Proyecto
from src.modelos.usuario import Usuario
from src.modelos.rol import Rol
from src.modelos.departamento import Departamento

from datetime import date as Date
from uuid import uuid4


class Empleado(Usuario):
    def __init__(self, id_usuario:str, username:str, password_hash:str, id_empleado:str, nombre:str, direccion:str, correo:str, fecha_contrato:Date, salario: float, estado, intentosfallidos, rol: Rol, departamento: Departamento):
        if not isinstance(departamento, Departamento):
            raise TypeError("El empleado debe tener un Departamento.")
        self.__departamento = departamento
        super().__init__(id_usuario, username, password_hash, estado, intentosfallidos, rol)
        self.__id_empleado = id_empleado
        self.__nombre = nombre
        self.__direccion = direccion
        self.__correo = correo
        self.__fecha_contrato = fecha_contrato
        self.__salario = salario

    @property
    def departamento(self) -> Departamento:
        return self.__departamento

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
    def fecha_contrato(self):
        return self.__fecha_contrato

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

    @fecha_contrato.setter
    def fecha_contrato(self, value):
        self.__fecha_contrato = value

    @salario.setter
    def salario(self, value):
        self.__salario = value

    def registrar_horas(self, proyecto: Proyecto, horas: float, tarea: str) -> registro_tiempo:
        if not self.tiene_permiso("registrar_horas"):
            raise PermissionError("No tienes permiso para registrar Horas")

        registro = registro_tiempo(
            id_registro=str(uuid4()),
            fecha=Date.today(),
            horas_trabajadas=horas,
            descripcion_tareas=tarea,
            empleado=self,
            proyecto=proyecto,
            aprobado=False
        )

        if not registro.crear_registro():
            raise ValueError("Los datos del registro no son válidos")
        
        return registro

    def consultar_perfil(self):     #Creo que fecha_contrato y salario no deberian ser visibles...
        return {
            "id_empleado": self.__id_empleado,
            "nombre": self.__nombre,
            "direccion": self.__direccion,
            "correo": self.__correo,
            "fecha_contrato": self.__fecha_contrato,
            "salario": self.__salario}