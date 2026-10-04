"""InformeExcel: seguridad, validación e informes de EcoTech."""

from io import BytesIO

# openpyxl crea archivos Excel .xlsx; Workbook representa el libro completo.
from openpyxl import Workbook

from src.informes.informe import Informe


class InformeExcel(Informe):
    """Reutiliza los datos de Informe y resuelve la salida XLSX."""

    def generar(self) -> None:
        libro = Workbook()
        # Trabajamos en la hoja que viene creada por defecto dentro del libro.
        hoja = libro.active
        hoja.title = "Informe"
        # El * incorpora cada línea a la lista, después del título y la fecha.
        valores = [self.getTitulo(), f"Fecha: {self.getFechaCreacion().isoformat()}", *self._getLineas()]
        # enumerate entrega número de fila y texto; Excel comienza sus filas en 1.
        for fila, valor in enumerate(valores, start=1):
            celda = hoja.cell(row=fila, column=1, value=valor)
            # Forzamos texto: '=...' recibido como dato no se ejecuta como fórmula.
            celda.data_type = "s"
        hoja.column_dimensions["A"].width = 70
        # Guardamos primero en memoria; exportar() se encarga del archivo en disco.
        memoria = BytesIO()
        libro.save(memoria)
        libro.close()
        self._guardarContenido(memoria.getvalue())

    def exportar(self) -> None:
        self._exportarContenido(".xlsx")
