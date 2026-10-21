import unittest
from datetime import date

from src.modelos.proyecto import Proyecto


class TestProyecto(unittest.TestCase):
    def setUp(self):
        self.proyecto = Proyecto(
            "P01",
            "EcoTech",
            "Proyecto inicial",
            date(2026, 10, 1)
        )

    def test_edicion_valida(self):
        resultado = self.proyecto.editar_proyecto(
            nombre="EcoTech actualizado",
            fecha_inicio=date(2026, 10, 11)
        )

        self.assertTrue(resultado)
        self.assertEqual(self.proyecto.nombre, "EcoTech actualizado")
        self.assertEqual(self.proyecto.fecha_inicio, date(2026, 10, 11))
        self.assertEqual(self.proyecto.descripcion, "Proyecto inicial")

    def test_edicion_invalida_no_aplica_cambios(self):
        resultado = self.proyecto.editar_proyecto(
            nombre="Este cambio no debe aplicarse",
            descripcion="Tampoco debe cambiar",
            fecha_inicio="incorrecta"
        )

        self.assertFalse(resultado)
        self.assertEqual(self.proyecto.nombre, "EcoTech")
        self.assertEqual(self.proyecto.descripcion, "Proyecto inicial")
        self.assertEqual(self.proyecto.fecha_inicio, date(2026, 10, 1))

    def test_rechazar_nombre_con_espacios(self):
        resultado = self.proyecto.editar_proyecto(nombre="   ")

        self.assertFalse(resultado)
        self.assertEqual(self.proyecto.nombre, "EcoTech")