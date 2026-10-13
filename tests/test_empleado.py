import unittest
from datetime import date

from src.modelos.empleado import Empleado
from src.modelos.proyecto import Proyecto
from src.modelos.registro_tiempo import registro_tiempo
from src.modelos.rol import Rol
from src.modelos.usuario import Usuario


class TestEmpleado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hash_password = Usuario.generar_hash("ClaveDePrueba123!")

    def setUp(self):
        self.empleado = self.crear_empleado(["registrar_horas"])
        self.proyecto = Proyecto(
            "P01",
            "EcoTech",
            "Proyecto de prueba",
            date(2026, 10, 1)
        )

    def crear_empleado(self, permisos):
        return Empleado(
            id_usuario="U01",
            username="empleado_prueba",
            password_hash=self.hash_password,
            id_empleado="E01",
            nombre="Persona de prueba",
            direccion="Dirección ficticia",
            correo="persona@example.com",
            fecha_contrato=date(2026, 1, 1),
            salario=1000,
            estado=True,
            intentosfallidos=0,
            rol=Rol("R01", "Empleado", permisos)
        )

    def test_registrar_horas_con_permiso(self):
        registro = self.empleado.registrar_horas(
            self.proyecto, 3.5, "Revisión de validaciones"
        )

        self.assertIsInstance(registro, registro_tiempo)
        self.assertTrue(registro.crear_registro())
        self.assertIs(registro.empleado, self.empleado)
        self.assertIs(registro.proyecto, self.proyecto)
        self.assertEqual(registro.horas_trabajadas, 3.5)
        self.assertEqual(
            registro.descripcion_tareas,
            "Revisión de validaciones"
        )
        self.assertEqual(registro.fecha, date.today())
        self.assertFalse(registro.aprobado)

    def test_rechazar_registro_sin_permiso(self):
        empleado = self.crear_empleado(["consultar_perfil"])

        with self.assertRaises(PermissionError):
            empleado.registrar_horas(
                self.proyecto, 2, "Tarea de prueba"
            )

    def test_rechazar_registro_con_cuenta_bloqueada(self):
        self.empleado.bloquear_cuenta()

        with self.assertRaises(PermissionError):
            self.empleado.registrar_horas(
                self.proyecto, 2, "Tarea de prueba"
            )

    def test_rechazar_horas_invalidas(self):
        for horas in (
            0, -1, float("nan"), float("inf"),
            True, "dos", None
        ):
            with self.subTest(horas=horas):
                with self.assertRaises(ValueError):
                    self.empleado.registrar_horas(
                        self.proyecto, horas, "Tarea de prueba"
                    )

    def test_rechazar_descripcion_invalida(self):
        for tarea in ("", "   ", None, 123):
            with self.subTest(tarea=tarea):
                with self.assertRaises(ValueError):
                    self.empleado.registrar_horas(
                        self.proyecto, 2, tarea
                    )