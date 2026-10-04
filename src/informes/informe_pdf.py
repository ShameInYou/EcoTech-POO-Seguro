"""InformePDF: seguridad, validación e informes de EcoTech."""

# BytesIO funciona como un archivo en memoria, sin escribir todavía en disco.
from io import BytesIO
from xml.sax.saxutils import escape

# ReportLab construye PDF: Paragraph agrega texto y Spacer separa elementos.
# SimpleDocTemplate organiza el documento y distribuye el contenido en páginas.
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from src.informes.informe import Informe


class InformePDF(Informe):
    """Reutiliza los datos de Informe y resuelve la salida PDF."""

    def generar(self) -> None:
        memoria = BytesIO()
        # Los estilos predeterminados dan formato al título y al texto normal.
        estilos = getSampleStyleSheet()
        documento = SimpleDocTemplate(memoria, pagesize=A4)
        # Paragraph interpreta etiquetas: escape convierte signos como < y &
        # para mostrarlos como texto. Solo añadimos <br/> para los saltos de línea.
        elementos = [
            Paragraph(escape(self.getTitulo()), estilos["Title"]),
            Paragraph(f"Fecha: {self.getFechaCreacion().isoformat()}", estilos["Normal"]),
            Spacer(1, 12),
        ]
        for linea in self._getLineas():
            elementos.append(Paragraph(escape(linea).replace("\n", "<br/>"), estilos["Normal"]))
            elementos.append(Spacer(1, 6))
        # build genera el PDF completo; getvalue recupera sus bytes para exportarlos.
        documento.build(elementos)
        self._guardarContenido(memoria.getvalue())

    def exportar(self) -> None:
        self._exportarContenido(".pdf")
