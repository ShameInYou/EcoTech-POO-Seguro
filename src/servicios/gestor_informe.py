"""GestorInforme: seguridad, validación e informes de EcoTech."""

# Path representa rutas y permite unir carpetas y archivos con el operador /.
from pathlib import Path

from src.informes.informe import Informe
from src.informes.informe_pdf import InformePDF
from src.informes.informe_excel import InformeExcel


class GestorInforme:
    """Crea la hija elegida y delega en sus métodos polimórficos."""

    def __init__(self, titulo: str, lineas: list[str], carpetaSalida: Path) -> None:
        self.__formatoSalida = ""
        self.__titulo = titulo
        # Copiamos la lista para que cambios externos no afecten al gestor.
        self.__lineas = list(lineas)
        self.__carpetaSalida = Path(carpetaSalida)

    def generarInforme(self, tipo: str) -> Informe:
        if not isinstance(tipo, str):
            raise TypeError("El formato debe ser texto.")
        # Aceptamos también entradas como " PDF " o "Excel".
        formato = tipo.strip().lower()
        # Dos formatos: un if/elif es suficiente y fácil de seguir.
        if formato == "pdf":
            informe = InformePDF(self.__titulo, self.__lineas, self.__carpetaSalida / "informe.pdf")
        elif formato == "excel":
            informe = InformeExcel(self.__titulo, self.__lineas, self.__carpetaSalida / "informe.xlsx")
        else:
            raise ValueError("Elige PDF o Excel.")
        # Cada hija sabe preparar su formato; el gestor solo coordina la llamada.
        informe.generar()
        self.__formatoSalida = formato
        return informe

    def exportarInforme(self, inf: Informe) -> bool:
        if not isinstance(inf, Informe):
            raise TypeError("Se esperaba un objeto Informe.")
        try:
            inf.exportar()  # Misma llamada: comportamiento distinto según la hija.
            return True
        except OSError:
            # Contrato Boolean del UML: errores de disco/permisos devuelven False.
            # Errores de uso (no generar antes o extensión incorrecta) se propagan.
            return False
