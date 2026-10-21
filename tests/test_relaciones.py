import unittest
from datetime import date

from src.modelos.asignacion_proyecto import AsignacionProyecto
from src.modelos.departamento import Departamento
from src.modelos.empleado import Empleado
from src.modelos.gerente import Gerente
from src.modelos.proyecto import Proyecto
from src.modelos.rol import Rol


class TestRelaciones(unittest.TestCase):
    def setUp(self):
        self.departamento = Departamento("D01", "Desarrollo")
        self.otro_departamento = Departamento("D02", "Administración")
        # Estas pruebas no autentican: no necesitan calcular hashes.
        self.datos = dict(
            id_usuario="U01", username="persona", password_hash="no-utilizado",
            id_empleado="E01", nombre="Persona", direccion="Ficticia",
            correo="persona@example.com", fecha_contrato=date(2026, 1, 1),
            salario=1000, estado=True, intentosfallidos=0,
            rol=Rol("R01", "Empleado", ["registrar_horas"]),
            departamento=self.departamento
        )
        self.empleado = Empleado(**self.datos)
        self.gerente = Gerente(**self.datos, presupuesto_asignado=2000)
        self.proyecto = Proyecto("P01", "EcoTech", "Prueba", date.today())

    def asignar(self, empleado=None, proyecto=None):
        return AsignacionProyecto(
            "A01", date.today(), "Desarrollo",
            self.empleado if empleado is None else empleado,
            self.proyecto if proyecto is None else proyecto
        )

    def test_empleado_pertenece_a_departamento(self):
        self.assertIs(self.empleado.departamento, self.departamento)
        with self.assertRaises(AttributeError):
            self.empleado.departamento = self.otro_departamento

    def test_rechazar_departamento_invalido(self):
        for departamento in (None, "Desarrollo"):
            with self.subTest(departamento=departamento):
                with self.assertRaises(TypeError):
                    Empleado(**{**self.datos, "departamento": departamento})

    def test_asignar_gerente_del_mismo_departamento(self):
        self.assertIsNone(self.departamento.gerente)
        self.departamento.asignar_gerente(self.gerente)
        self.assertIs(self.departamento.gerente, self.gerente)
        self.assertIs(self.gerente.departamento, self.departamento)
        self.assertTrue(self.gerente.tiene_permiso("registrar_horas"))

    def test_rechazar_gerente_de_otro_departamento(self):
        with self.assertRaises(ValueError):
            self.otro_departamento.asignar_gerente(self.gerente)
        self.assertIsNone(self.otro_departamento.gerente)

    def test_rechazar_empleado_como_gerente(self):
        with self.assertRaises(TypeError):
            self.departamento.asignar_gerente(self.empleado)
        self.assertIsNone(self.departamento.gerente)

    def test_asignacion_y_finalizacion(self):
        asignacion = self.asignar()
        self.assertIs(asignacion.empleado, self.empleado)
        self.assertIs(asignacion.proyecto, self.proyecto)
        self.assertEqual(asignacion.rol_proyecto, "Desarrollo")
        self.assertTrue(asignacion.activo)
        self.assertTrue(asignacion.finalizar_asignacion())
        self.assertFalse(asignacion.activo)
        self.assertFalse(asignacion.finalizar_asignacion())

    def test_rechazar_referencias_invalidas_en_asignacion(self):
        for empleado, proyecto in [(None, self.proyecto), (self.empleado, None),
                                   ("persona", self.proyecto), (self.empleado, "proyecto")]:
            with self.subTest(empleado=empleado, proyecto=proyecto):
                with self.assertRaises(TypeError):
                    AsignacionProyecto("A01", date.today(), "Desarrollo", empleado, proyecto)

    def test_relacion_muchos_a_muchos(self):
        otro_proyecto = Proyecto("P02", "Otro", "Prueba", date.today())
        otro_empleado = Empleado(**{**self.datos, "id_usuario": "U02", "id_empleado": "E02"})
        asignaciones = [
            self.asignar(),
            self.asignar(proyecto=otro_proyecto),
            self.asignar(empleado=otro_empleado)
        ]
        self.assertEqual(sum(a.empleado is self.empleado for a in asignaciones), 2)
        self.assertEqual(sum(a.proyecto is self.proyecto for a in asignaciones), 2)

    def test_registro_conserva_relaciones(self):
        registro = self.empleado.registrar_horas(self.proyecto, 2, "Tarea")
        self.assertIs(registro.empleado, self.empleado)
        self.assertIs(registro.proyecto, self.proyecto)
        self.assertIs(registro.empleado.departamento, self.departamento)
