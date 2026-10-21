"""Módulo reservado para Rol."""


class Rol:
    """Clase para representar un rol en el sistema."""  #Les juro que no usé mucha IA

    def __init__(self, id_rol: str, nombre_rol: str, permisos: list):
        self.__id_rol = id_rol
        self.__nombre_rol = nombre_rol
        self.__permisos = []

        for permiso in permisos:
            self.asignar_permiso(permiso)


    @property
    def id_rol(self):
        return self.__id_rol

    @id_rol.setter
    def id_rol(self, value):
        self.__id_rol = value

    @property
    def nombre_rol(self):
        return self.__nombre_rol

    @nombre_rol.setter
    def nombre_rol(self, value):
        self.__nombre_rol = value

    @property
    def permisos(self) -> tuple[str, ...]:
        return tuple(self.__permisos)
    

    def asignar_permiso(self, permiso: str) -> None:
        """Método para asignar un permiso al rol."""
        if not isinstance(permiso, str) or not permiso.strip():
            raise ValueError("El permiso no puede ser texto vacío")

        permiso = permiso.strip()

        if permiso not in self.__permisos:
            self.__permisos.append(permiso)


    def verificar_permiso(self, permiso: str) -> bool:
        """Método para verificar si el rol tiene un permiso específico."""
        return permiso in self.__permisos