"""ValidadorEntradas: seguridad, validación e informes de EcoTech."""

# re permite comprobar formatos de texto mediante expresiones regulares.
import re


class ValidadorEntradas:
    """Utilidad sin estado, tal como aparece en el UML."""

    # @staticmethod no necesita self ni datos de una instancia. Podemos llamar
    # ValidadorEntradas.validarEmail(...) sin crear un objeto primero.
    @staticmethod
    def validar_email(email: str) -> bool:
        # Validamos sin corregir silenciosamente lo que escribió la persona.
        if not isinstance(email, str) or len(email) > 254:
            return False
        # La r conserva las barras del patrón; fullmatch revisa el email completo.
        patron = r"[A-Za-z0-9_%+.-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+"
        if not re.fullmatch(patron, email):
            return False
        # Separamos lo que va antes y después de @ para revisar sus límites.
        local, dominio = email.rsplit("@", 1)
        return (
            len(local) <= 64
            and not local.startswith(".")
            and not local.endswith(".")
            and ".." not in local
            and all(len(etiqueta) <= 63 for etiqueta in dominio.split("."))
        )

    @staticmethod
    def validar_telefono(tel: str) -> bool:
        # Formato internacional: signo + seguido de entre 8 y 15 dígitos.
        return isinstance(tel, str) and bool(re.fullmatch(r"\+[1-9][0-9]{7,14}", tel))

    @staticmethod
    def sanitizar_entrada(txt: str) -> str:
        if not isinstance(txt, str):
            raise TypeError("La entrada debe ser texto.")
        # Limpiar espacios no sustituye consultas SQL parametrizadas.
        # Conservamos signos legítimos como la comilla en O'Connor.
        # ord obtiene el número de cada carácter; rechazamos controles invisibles,
        # pero permitimos saltos de línea y tabulaciones en textos normales.
        if any(ord(c) < 32 and c not in "\n\r\t" for c in txt):
            raise ValueError("El texto contiene caracteres de control.")
        return txt.strip()
