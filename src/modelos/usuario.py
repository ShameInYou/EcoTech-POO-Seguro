"""Módulo reservado para Usuario."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

#CLASE USUARIO
class Usuario:
    MAX_INTENTOS = 3
    __hasher = PasswordHasher

    def __init__(self, id_usuario:str, username:str, password_hash:str, estado:bool, intentos_fallidos:int):
        self._id_usuario = id_usuario
        self._username = username
        self.__password_hash = password_hash
        self._estado = estado
        self._intentos_fallidos = intentos_fallidos

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, value):
        self._id_usuario = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password_hash(self):
        return self.__password_hash
        

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def intentos_fallidos(self):
        return self._intentos_fallidos

    @intentos_fallidos.setter
    def intentos_fallidos(self, value):
        self._intentos_fallidos = value

    @staticmethod
    def generar_hass(password: str) -> str:
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
                self.bloquearcuenta()

            return False

        self.__intentos_fallidos = 0
        return True

    def cambiar_pass(self, nueva_password: str) -> bool:
        nuevo_hash = self.__generar_hash(nueva_password)
        self.__password_hash = nuevo_hash
        return True
        

    def bloquearcuenta(self) -> None:
        """Método para bloquear la cuenta del usuario."""
        self.estado = False

    def desbloquearcuenta(self) -> None:
        self._estado = True
        self._intentos_fallidos = 0