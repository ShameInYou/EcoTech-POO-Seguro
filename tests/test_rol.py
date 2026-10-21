import unittest

from src.modelos.rol import Rol

class test_rol(unittest.TestCase):

    def setUp(self):
        self.rol = Rol(
            id_rol="R-01",
            nombre_rol="Empleado",
            permisos=["registrar_horas"]
        )

    def test_instanciacion(self):
        self.assertEqual(self.rol.id_rol, "R-01")
        self.assertEqual(self.rol.nombre_rol,"Empleado")
        self.assertEqual(self.rol.permisos, ("registrar_horas",))

    def test_asignar_permiso_sin_duplicados(self):
        self.rol.asignar_permiso("consultar_perfil")
        self.rol.asignar_permiso("consultar_perfil")

        self.assertTrue(self.rol.verificar_permiso("consultar_perfil"))
        self.assertEqual(
            self.rol.permisos.count("consultar_perfil"), 1
        )

    def test_permiso_no_asignado(self):
        self.assertFalse(self.rol.verificar_permiso("aprobar_horas"))

    def test_rechazar_permiso_vacio(self):
        with self.assertRaises(ValueError):
            self.rol.asignar_permiso("  ")

    def test_no_compartir_lista_original(self):
        permisos = ["registrar_horas"]
        rol = Rol("R-02", "Empleado", permisos)

        permisos.append("aprobar_horas")

        self.assertFalse(rol.verificar_permiso("aprobar_horas"))