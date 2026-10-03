"""Módulo reservado para Usuario."""

# TODO: definir Usuario según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.


#CLASE USUARIO
class Usuario:
    def __init__(self, id_usuario:str, username:str, passwordHash:str, estado:bool, intentosfallidos:int):
        self.id_usuario = id_usuario
        self.username = username
        self.passwordHash = passwordHash
        self.estado = estado
        self.intentosfallidos = intentosfallidos

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
    def passwordHash(self):
        return self._passwordHash

    @passwordHash.setter
    def passwordHash(self, value):
        self._passwordHash = value
        

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def intentosfallidos(self):
        return self._intentosfallidos

    @intentosfallidos.setter
    def intentosfallidos(self, value):
        self._intentosfallidos = value


    def autenticar(self, password:str) -> bool:
        """Método para autenticar al usuario.

        Args:
            password (str): Contraseña proporcionada por el usuario.

        Returns:
            bool: True si la autenticación es exitosa, False en caso contrario.
        """
        # Aquí se implementaría la lógica de autenticación, comparando el hash de la contraseña proporcionada con el almacenado.
        # Por simplicidad, se devuelve True si las contraseñas coinciden, False en caso contrario.
        return self.passwordHash == password

    def cambiarPass(self, nueva_password:str) -> None:
        """Método para cambiar la contraseña del usuario.

        Args:
            nueva_password (str): Nueva contraseña proporcionada por el usuario.
        """
        # Aquí se implementaría la lógica para cambiar la contraseña, actualizando el hash de la nueva contraseña.
        self.passwordHash = nueva_password

    def bloquearcuenta(self) -> None:
        """Método para bloquear la cuenta del usuario."""
        self.estado = False

    def desbloquearcuenta(self) -> None:
        """Método para desbloquear la cuenta del usuario."""
        self.estado = True