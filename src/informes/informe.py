"""Informe: seguridad, validación e informes de EcoTech."""

# ABC y abstractmethod definen una clase base que exige métodos a sus hijas.
from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path

from src.servicios.validador_entradas import ValidadorEntradas


class Informe(ABC):
    """Contrato común: las hijas cambian el formato, no la forma de usarlas."""

    # __init__ prepara cada objeto. Las anotaciones como str o -> None ayudan
    # a leer los tipos esperados; por sí solas no validan los datos al ejecutar.
    def __init__(self, titulo: str, lineas: list[str], ruta_salida: Path) -> None:
        self.__titulo = ValidadorEntradas.sanitizar_entrada(titulo)
        if not self.__titulo:
            raise ValueError("El título no puede estar vacío.")
        if not isinstance(lineas, list):
            raise TypeError("Las líneas deben venir en una lista de textos.")
        # Copia: cambiar la lista original después no cambia este informe.
        # tuple mantiene los textos en una colección que no se puede modificar.
        # La expresión interior limpia cada línea antes de almacenarla.
        self.__lineas = tuple(ValidadorEntradas.sanitizar_entrada(linea) for linea in lineas)
        self.__fechaCreacion = date.today()
        self.__rutaSalida = Path(ruta_salida)
        # None significa que todavía no se generó el documento; después serán bytes.
        self.__contenido: bytes | None = None

    def getTitulo(self) -> str:
        return self.__titulo

    def getFechaCreacion(self) -> date:
        return self.__fechaCreacion

    # Un solo _ indica, por convención, un método de apoyo para la clase y sus hijas.
    def _getLineas(self) -> tuple[str, ...]:
        """Apoyo protegido agregado para reutilizar datos en ambas hijas."""
        return self.__lineas

    def _guardarContenido(self, contenido: bytes) -> None:
        self.__contenido = contenido

    def _exportarContenido(self, extension: str) -> None:
        if self.__contenido is None:
            raise RuntimeError("Primero hay que generar el informe.")
        if self.__rutaSalida.suffix.lower() != extension:
            raise ValueError(f"La ruta debe terminar en {extension}.")
        # Creamos también carpetas intermedias; si ya existen, no es un error.
        self.__rutaSalida.parent.mkdir(parents=True, exist_ok=True)
        # 'x' crea sin sobrescribir y 'b' escribe bytes. El with cierra el archivo
        # al salir del bloque, incluso si ocurre un error.
        with self.__rutaSalida.open("xb") as archivo:
            archivo.write(self.__contenido)

    # @abstractmethod obliga a las hijas a implementar estos métodos.
    # Informe no se puede instanciar directamente: usamos InformePDF o InformeExcel.
    @abstractmethod
    def generar(self) -> None:
        """Preparar el documento en memoria; todavía no guardarlo en disco."""

    @abstractmethod
    def exportar(self) -> None:
        """Guardar el documento generado en el formato de la hija."""
