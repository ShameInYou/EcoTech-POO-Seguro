import unittest
from datetime import date

from src.modelos.empleado import Empleado
from src.modelos.proyecto import Proyecto
from src.modelos.registro_tiempo import registro_tiempo
from src.modelos.rol import Rol
from src.modelos.usuario import Usuario


class TestRegistroTiempo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hash_password = Usuario.generar_hash("ClaveDePrueba123!")

    def setUp(self):
        rol = Rol("R01", "Empleado", ["registrar_horas"])

        self.empleado = Empleado(
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
            rol=rol
        )

        self.proyecto = Proyecto(
            "P01",
            "EcoTech",
            "Proyecto de prueba",
            date(2026, 10, 1)
        )

        self.registro = self.crear_registro()

    def crear_registro(self, **cambios):
        # Permite cambiar un dato para probar casos inválidos.
        datos = {
            "id_registro": "RT01",
            "fecha": date(2026, 10, 11),
            "horas_trabajadas": 3,
            "descripcion_tareas": "Implementación de validaciones",
            "empleado": self.empleado,
            "proyecto": self.proyecto,
            "aprobado": False
        }
        datos.update(cambios)
        return registro_tiempo(**datos)

    def test_creacion_valida_y_relaciones(self):
        self.assertTrue(self.registro.crear_registro())
        self.assertIs(self.registro.empleado, self.empleado)
        self.assertIs(self.registro.proyecto, self.proyecto)
        self.assertEqual(self.registro.horas_trabajadas, 3)
        self.assertFalse(self.registro.aprobado)

    def test_rechazar_horas_invalidas(self):
        for horas in (
            0, -2, float("nan"), float("inf"),
            float("-inf"), True, "dos", None
        ):
            with self.subTest(horas=horas):
                registro = self.crear_registro(
                    horas_trabajadas=horas
                )
                self.assertFalse(registro.crear_registro())

    def test_rechazar_descripciones_invalidas(self):
        for descripcion in ("", "   ", None, 123):
            with self.subTest(descripcion=descripcion):
                registro = self.crear_registro(
                    descripcion_tareas=descripcion
                )
                self.assertFalse(registro.crear_registro())

    def test_rechazar_fecha_e_identificador_invalidos(self):
        casos = [
            {"fecha": "11-10-2026"},
            {"fecha": None},
            {"id_registro": ""},
            {"id_registro": "   "}
        ]

        for cambios in casos:
            with self.subTest(cambios=cambios):
                registro = self.crear_registro(**cambios)
                self.assertFalse(registro.crear_registro())

    def test_rechazar_relaciones_invalidas(self):
        casos = [
            {"empleado": None},
            {"empleado": object()},
            {"proyecto": None},
            {"proyecto": object()}
        ]

        for cambios in casos:
            with self.subTest(cambios=cambios):
                registro = self.crear_registro(**cambios)
                self.assertFalse(registro.crear_registro())

    def test_rechazar_aprobacion_no_booleana(self):
        registro = self.crear_registro(aprobado="sí")
        self.assertFalse(registro.crear_registro())

    def test_modificacion_valida(self):
        resultado = self.registro.modificar_registro(
            fecha=date(2026, 10, 12),
            horas_trabajadas=4.5,
            descripcion_tareas="  Revisión de informes  "
        )

        self.assertTrue(resultado)
        self.assertEqual(self.registro.fecha, date(2026, 10, 12))
        self.assertEqual(self.registro.horas_trabajadas, 4.5)
        self.assertEqual(
            self.registro.descripcion_tareas,
            "Revisión de informes"
        )

    def test_cambiar_solo_horas_conserva_otros_datos(self):
        resultado = self.registro.modificar_registro(
            horas_trabajadas=5
        )

        self.assertTrue(resultado)
        self.assertEqual(self.registro.horas_trabajadas, 5)
        self.assertEqual(self.registro.fecha, date(2026, 10, 11))
        self.assertEqual(
            self.registro.descripcion_tareas,
            "Implementación de validaciones"
        )

    def test_modificacion_invalida_no_aplica_cambios(self):
        casos = [
            {
                "fecha": date(2026, 10, 12),
                "horas_trabajadas": -2
            },
            {
                "fecha": date(2026, 10, 12),
                "horas_trabajadas": 5,
                "descripcion_tareas": "   "
            },
            {"fecha": "incorrecta"},
            {"horas_trabajadas": float("nan")},
            {"horas_trabajadas": "dos"}
        ]

        for cambios in casos:
            with self.subTest(cambios=cambios):
                registro = self.crear_registro()

                self.assertFalse(
                    registro.modificar_registro(**cambios)
                )
                self.assertEqual(
                    registro.fecha, date(2026, 10, 11)
                )
                self.assertEqual(registro.horas_trabajadas, 3)
                self.assertEqual(
                    registro.descripcion_tareas,
                    "Implementación de validaciones"
                )

    def test_registro_aprobado_no_se_modifica(self):
        registro = self.crear_registro(aprobado=True)

        resultado = registro.modificar_registro(
            horas_trabajadas=6
        )

        self.assertFalse(resultado)
        self.assertEqual(registro.horas_trabajadas, 3)
        self.assertTrue(registro.aprobado)

    def test_propiedades_son_solo_lectura(self):
        with self.assertRaises(AttributeError):
            self.registro.horas_trabajadas = 10

        with self.assertRaises(AttributeError):
            self.registro.aprobado = True