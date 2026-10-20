"""Pruebas de desactivación y conservación de relaciones históricas."""

from datetime import date
import unittest

from src.modelos.asignacion_proyecto import AsignacionProyecto
from src.modelos.departamento import Departamento
from src.modelos.empleado import Empleado
from src.modelos.proyecto import Proyecto
from src.modelos.registro_tiempo import RegistroTiempo


class DesactivacionTest(unittest.TestCase):
    def setUp(self):
        self.fecha = date(2026, 10, 19)
        self.proyecto = Proyecto("P1", "EcoTech", "Descripción", self.fecha)
        self.departamento = Departamento("D1", "Desarrollo")
        self.empleado = Empleado(
            "U1", "usuario", "hash", "E1", "Nombre", "Dirección",
            "correo@example.com", self.fecha, 1000, True, 0,
        )

    def asignacion(self):
        return AsignacionProyecto(
            "A1", self.fecha, "Desarrollo", self.empleado, self.proyecto,
        )

    def registro(self):
        return RegistroTiempo(
            "R1", self.fecha, 8, "Implementación", self.empleado, self.proyecto,
        )

    def test_desactivar_proyecto_y_repetir(self):
        self.assertTrue(self.proyecto.activo)
        self.assertTrue(self.proyecto.eliminar_proyecto())
        self.assertFalse(self.proyecto.activo)
        self.assertFalse(self.proyecto.eliminar_proyecto())

    def test_estado_activo_es_solo_lectura(self):
        for objeto in (self.proyecto, self.departamento):
            with self.subTest(clase=type(objeto).__name__):
                with self.assertRaises(AttributeError):
                    objeto.activo = False

    def test_proyecto_desactivado_rechaza_asignaciones_y_horas(self):
        self.proyecto.eliminar_proyecto()
        with self.assertRaises(ValueError):
            self.asignacion()
        with self.assertRaises(ValueError):
            self.registro()

    def test_registro_pendiente_no_puede_crearse_tras_desactivar(self):
        registro = self.registro()
        self.proyecto.eliminar_proyecto()
        self.assertFalse(registro.crear_registro())

    def test_desactivacion_conserva_datos_asignaciones_y_registros(self):
        asignacion = self.asignacion()
        registro = self.registro()
        self.assertTrue(registro.crear_registro())
        datos_proyecto = vars(self.proyecto).copy()
        datos_asignacion = vars(asignacion).copy()
        datos_registro = vars(registro).copy()
        self.proyecto.eliminar_proyecto()
        datos_proyecto["_Proyecto__activo"] = False
        self.assertEqual(vars(self.proyecto), datos_proyecto)
        self.assertEqual(vars(asignacion), datos_asignacion)
        self.assertEqual(vars(registro), datos_registro)
        self.assertIs(asignacion.proyecto, self.proyecto)
        self.assertIs(asignacion.empleado, self.empleado)
        self.assertTrue(asignacion.activo)
        self.assertIs(registro.proyecto, self.proyecto)
        self.assertIs(registro.empleado, self.empleado)
        self.assertEqual(registro.horas_trabajadas, 8)

    def test_departamento_desactiva_repite_y_rechaza_incorporaciones(self):
        self.assertTrue(self.departamento.activo)
        self.assertTrue(self.departamento.eliminar_departamento())
        self.assertFalse(self.departamento.activo)
        self.assertFalse(self.departamento.eliminar_departamento())
        self.assertFalse(self.departamento.incorporar_empleado(self.empleado))
        self.assertIsNone(self.empleado.departamento)
        self.assertEqual(self.departamento.empleados, ())
        self.assertEqual(self.departamento.historial_empleados, ())

    def test_empleados_activos_deben_trasladarse_antes_de_desactivar(self):
        destino = Departamento("D2", "Operaciones")
        self.assertTrue(self.departamento.incorporar_empleado(self.empleado))
        self.assertFalse(self.departamento.eliminar_departamento())
        self.assertTrue(self.departamento.activo)
        self.assertTrue(self.departamento.trasladar_empleado(self.empleado, destino))
        self.assertTrue(self.departamento.eliminar_departamento())
        self.assertIs(self.empleado.departamento, destino)
        self.assertEqual(destino.empleados, (self.empleado,))
        self.assertEqual(self.departamento.empleados, ())
        self.assertEqual(self.departamento.historial_empleados, (self.empleado,))

    def test_desactivacion_conserva_empleados_inactivos_y_datos(self):
        self.departamento.incorporar_empleado(self.empleado)
        self.empleado.estado = False
        datos_empleado = vars(self.empleado).copy()
        self.assertTrue(self.departamento.eliminar_departamento())
        self.assertEqual(self.departamento.empleados, (self.empleado,))
        self.assertEqual(self.departamento.historial_empleados, (self.empleado,))
        self.assertIs(self.empleado.departamento, self.departamento)
        self.assertEqual(vars(self.empleado), datos_empleado)

    def test_traslado_a_departamento_inactivo_conserva_relaciones(self):
        destino = Departamento("D2", "Operaciones")
        self.departamento.incorporar_empleado(self.empleado)
        destino.eliminar_departamento()
        self.assertFalse(self.departamento.trasladar_empleado(self.empleado, destino))
        self.assertEqual(self.departamento.empleados, (self.empleado,))
        self.assertEqual(destino.empleados, ())
        self.assertEqual(destino.historial_empleados, ())
        self.assertIs(self.empleado.departamento, self.departamento)

    def test_no_admite_duplicados_ni_dos_departamentos_actuales(self):
        destino = Departamento("D2", "Operaciones")
        self.assertTrue(self.departamento.incorporar_empleado(self.empleado))
        self.assertFalse(self.departamento.incorporar_empleado(self.empleado))
        self.assertFalse(destino.incorporar_empleado(self.empleado))
        self.assertFalse(self.departamento.trasladar_empleado(self.empleado, self.departamento))
        self.assertEqual(self.departamento.empleados, (self.empleado,))

    def test_empleado_activo_bloquea_aunque_haya_otro_inactivo(self):
        otro = Empleado(
            "U2", "otro", "hash", "E2", "Otro", "Dirección",
            "otro@example.com", self.fecha, 1000, False, 0,
        )
        self.departamento.incorporar_empleado(otro)
        self.departamento.incorporar_empleado(self.empleado)
        self.assertFalse(self.departamento.eliminar_departamento())
        self.assertTrue(self.departamento.activo)
        self.assertEqual(self.departamento.empleados, (otro, self.empleado))


if __name__ == "__main__":
    unittest.main()
