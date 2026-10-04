"""Módulo reservado para Rol."""

# TODO: definir Rol según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

class Rol:
    """Clase para representar un rol en el sistema."""  #Les juro que no usé mucha IA

    def __init__(self, id_rol:str, nombreRol:str, permisos:list):
        self.__id_rol = id_rol
        self.__nombreRol = nombreRol
        self.__permisos = permisos


    @property
    def id_rol(self):
        return self._id_rol

    @id_rol.setter
    def id_rol(self, value):
        self._id_rol = value

    @property
    def nombreRol(self):
        return self._nombreRol

    @nombreRol.setter
    def nombreRol(self, value):
        self._nombreRol = value

    @property
    def permisos(self):
        return self._permisos

    @permisos.setter
    def permisos(self, value):
        self._permisos = value



    def asignarPermiso(self, permiso:str) -> None:
        """Método para asignar un permiso al rol."""
        if permiso not in self.permisos:
            self.permisos.append(permiso)


    def verificarPermiso(self, permiso:str) -> bool:
        """Método para verificar si el rol tiene un permiso específico."""
        return permiso in self.permisos