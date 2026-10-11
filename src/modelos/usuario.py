"""Módulo reservado para Usuario."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.modelos.rol import Rol

#CLASE USUARIO
class Usuario:
    MAX_INTENTOS = 3
    __hasher = PasswordHasher()

    def __init__(self, id_usuario:str, username:str, password_hash:str, estado:bool, intentos_fallidos:int, rol: Rol):

        if not isinstance(rol, Rol):
            raise TypeError("El usuario debe tener un objeto Rol")

        self.__id_usuario = id_usuario
        self.__username = username
        self.__password_hash = password_hash
        self.__estado = estado
        self.__intentos_fallidos = intentos_fallidos
        self.__rol = rol

    @property
    def id_usuario(self):
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, value):
        self.__id_usuario = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password_hash(self):
        return self.__password_hash
        

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        self.__estado = value

    @property
    def intentos_fallidos(self):
        return self.__intentos_fallidos

    @intentos_fallidos.setter
    def intentos_fallidos(self, value):
        self.__intentos_fallidos = value

    @staticmethod
    def generar_hash(password: str) -> str:
        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña no puede ser un texto vacío")
        
        return Usuario.__hasher.hash(password)


    def autenticar(self, password:str) -> bool:
        if not self.__estado:
            return False

        if not isinstance(password, str):
            raise TypeError("La contraseña debe ser texto")

        try:
            self.__hasher.verify(self.__password_hash, password)
        except VerifyMismatchError:
            self.__intentos_fallidos += 1

            if self.__intentos_fallidos >= self.MAX_INTENTOS:
                self.bloquear_cuenta()

            return False

        self.__intentos_fallidos = 0
        return True

    def cambiar_pass(self, nueva_password: str) -> bool:
        nuevo_hash = self.generar_hash(nueva_password)
        self.__password_hash = nuevo_hash
        return True
        

    def bloquear_cuenta(self) -> None:
        """Método para bloquear la cuenta del usuario."""
        self.estado = False

    def desbloquear_cuenta(self) -> None:
        self.__estado = True
        self.__intentos_fallidos = 0

    def tiene_permiso(self, permiso: str) -> bool:
        return self.__estado and self.__rol.verificar_permiso(permiso)