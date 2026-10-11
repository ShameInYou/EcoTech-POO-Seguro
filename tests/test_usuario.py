import unittest

from src.modelos.rol import Rol
from src.modelos.usuario import Usuario

class TestUsuario(unittest.TestCase):
    PASSWORD = "ClaveTest123!"

    @classmethod
    def setUpClass(cls):
        cls.hash_incial = Usuario.generar_hash(cls.PASSWORD)

    def setUp(self):
        self.rol = Rol(
            "R-01", "Empleado", ["registrar_horas"]
        )

        self.usuario = Usuario(
            id_usuario="U-01",
            username="Rodrigo Cañas",
            password_hash=self.hash_incial,
            estado=True,
            intentos_fallidos=0,
            rol=self.rol
        )

    def test_instanciacion(self):
        self.assertEqual(self.usuario.id_usuario, "U-01")
        self.assertEqual(self.usuario.username, "Rodrigo Cañas")
        self.assertTrue(self.usuario.estado)

    def test_rechazar_rol_invalido(self):
        with self.assertRaises(TypeError):
            Usuario(
                "U-02,", "demo", self.hash_incial,
                True, 0, None
            )

    def test_autenticacion_correcta(self):
        self.assertTrue(
            self.usuario.autenticar(self.PASSWORD)
        )

    def test_intento_fallido(self):
        self.assertFalse(
            self.usuario.autenticar("incorrecta")
        )
        self.assertEqual(self.usuario.intentos_fallidos, 1)

    def test_acierto_reinicia_intentos(self):
        self.usuario.autenticar("incorrecta")
        self.usuario.autenticar(self.PASSWORD)

        self.assertEqual(self.usuario.intentos_fallidos, 0)

    def test_bloqueo_por_intentos(self):
        for _ in range(Usuario.MAX_INTENTOS):
            self.assertFalse(
                self.usuario.autenticar("incorrecta")
            )

        self.assertFalse(self.usuario.estado)
        self.assertFalse(
            self.usuario.autenticar(self.PASSWORD)
        )
        self.assertFalse(
            self.usuario.tiene_permiso("registrar_horas")
        )

    def test_desbloqueo(self):
        self.usuario.autenticar("incorrecta")
        self.usuario.bloquear_cuenta()
        self.usuario.desbloquear_cuenta()

        self.assertTrue(self.usuario.estado)
        self.assertEqual(self.usuario.intentos_fallidos, 0)
        self.assertTrue(
            self.usuario.autenticar(self.PASSWORD)
        )

    def test_comunicacion_con_rol(self):
        self.assertTrue(
            self.usuario.tiene_permiso("registrar_horas")
        )
        self.assertFalse(
            self.usuario.tiene_permiso("aprobar_horas")
        )

    def test_cambio_password(self):
        resultado = self.usuario.cambiar_pass(
            "2ClaveTest123!"
        )

        self.assertTrue(resultado)
        self.assertFalse(
            self.usuario.autenticar(self.PASSWORD)
        )
        self.assertTrue(
            self.usuario.autenticar("2ClaveTest123!")
        )