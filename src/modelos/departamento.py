"""Módulo reservado para Departamento."""

# TODO: definir Departamento según el UML definitivo del equipo.
# Atributos, métodos y relaciones pendientes de implementación.

class Departamento:
    def __init__(self, id_departamento: str, nombre: str):
        self.__id_departamento = id_departamento
        self.__nombre = nombre
        self.__activo = True
        self.__empleados = []
        self.__historial_empleados = []

    @property
    def activo(self) -> bool:
        return self.__activo

    @property
    def empleados(self) -> tuple:
        """Empleados actualmente asignados; no permite modificar la colección."""
        return tuple(self.__empleados)

    @property
    def historial_empleados(self) -> tuple:
        """Conserva las incorporaciones, incluso después de un traslado."""
        return tuple(self.__historial_empleados)

    def incorporar_empleado(self, empleado) -> bool:
        if not self.__activo or empleado is None or empleado in self.__empleados:
            return False
        if empleado.departamento is not None:
            return False
        self.__empleados.append(empleado)
        self.__historial_empleados.append(empleado)
        empleado._asignar_departamento(self)
        return True

    def trasladar_empleado(self, empleado, destino) -> bool:
        """Actualiza la pertenencia actual conservando las incorporaciones previas."""
        if empleado not in self.__empleados or destino is self:
            return False
        if not isinstance(destino, Departamento) or not destino.activo:
            return False
        self.__empleados.remove(empleado)
        empleado._asignar_departamento(None)
        destino.incorporar_empleado(empleado)
        return True

    def crear_departamento(self) -> bool:
        """Valida que el departamento tenga sus datos obligatorios."""
        if not self.__id_departamento or not self.__nombre:
            return False
        return True

    def editar_departamento(self, nuevo_nombre: str) -> bool:
        """Modifica el nombre del departamento."""
        if not nuevo_nombre:
            return False

        self.__nombre = nuevo_nombre
        return True

    def eliminar_departamento(self) -> bool:
        """Desactiva si no quedan empleados con estado activo asignados."""
        if not self.__activo or any(empleado.estado for empleado in self.__empleados):
            return False
        self.__activo = False
        return True
