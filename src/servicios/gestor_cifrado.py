"""GestorCifrado: seguridad, validación e informes de EcoTech."""

# Fernet cifra y comprueba que el contenido no haya sido alterado.
# InvalidToken indica un dato inválido o una clave que no corresponde.
from cryptography.fernet import Fernet, InvalidToken


class GestorCifrado:
    """Servicio independiente para cifrar y recuperar datos sensibles."""

    def __init__(self, clave: bytes) -> None:
        # La clave se recibe: otra instancia puede recuperar los mismos datos.
        # Los atributos con __ se encapsulan para usarlos desde esta clase.
        self.__algoritmo = "Fernet"
        self.__cifrador = Fernet(clave)

    def cifrarDato(self, dato: str) -> str:
        if not isinstance(dato, str):
            raise TypeError("El dato a cifrar debe ser texto.")
        # Fernet trabaja con bytes: UTF-8 convierte el texto de entrada y
        # ASCII convierte el token resultante a texto para poder guardarlo.
        return self.__cifrador.encrypt(dato.encode("utf-8")).decode("ascii")

    def descifrarDato(self, dato: str) -> str:
        if not isinstance(dato, str):
            raise TypeError("El dato cifrado debe ser texto.")
        # Invertimos las conversiones para recuperar el texto original.
        try:
            return self.__cifrador.decrypt(dato.encode("ascii")).decode("utf-8")
        except (InvalidToken, UnicodeError) as error:
            raise ValueError("No se pudo descifrar: clave incorrecta o dato inválido.") from error

