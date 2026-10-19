"""Módulo reservado para Departamento."""


class Departamento:
    def __init__(self, id_departamento: str, nombre: str):
        self.__id_departamento = id_departamento
        self.__nombre = nombre
        self.__gerente = None

    @property
    def gerente(self):
        return self.__gerente

    def asignar_gerente(self, gerente) -> None:
        # Import local: Gerente hereda de Empleado, que utiliza Departamento.
        from src.modelos.gerente import Gerente

        if not isinstance(gerente, Gerente):
            raise TypeError("Debes indicar un Gerente.")
        if gerente.departamento is not self:
            raise ValueError("El gerente debe pertenecer a este departamento.")
        self.__gerente = gerente

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
        """Representa la eliminación lógica del departamento."""
        return True